import time
import re
import os
from typing import List, Dict, Tuple, Union, Optional
from colorama import Fore, Style, init
import logging
import sys
from io import StringIO
from web_scraper import get_web_content, can_fetch
from llm_config import get_llm_config
from llm_response_parser import UltimateLLMResponseParser
from llm_wrapper import LLMWrapper
from urllib.parse import urlparse, quote_plus
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import threading
from queue import Queue
import concurrent.futures

# Initialize colorama
init()

# Set up logging
log_directory = 'logs'
if not os.path.exists(log_directory):
  os.makedirs(log_directory)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = os.path.join(log_directory, 'search.log')
file_handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class SearchResult:
  def __init__(self, title: str, url: str, snippet: str, score: float = 0.0):
      self.title = title
      self.url = url
      self.snippet = snippet
      self.score = score
      self.content: Optional[str] = None
      self.processed = False
      self.error = None

  def to_dict(self) -> Dict:
      return {
          'title': self.title,
          'url': self.url,
          'snippet': self.snippet,
          'score': self.score,
          'has_content': bool(self.content),
          'processed': self.processed,
          'error': str(self.error) if self.error else None
      }

class EnhancedSelfImprovingSearch:
  def __init__(self, llm: LLMWrapper, parser: UltimateLLMResponseParser, max_attempts: int = 5):
      self.llm = llm
      self.parser = parser
      self.max_attempts = max_attempts
      self.llm_config = get_llm_config()
      self.last_query = ""
      self.last_time_range = ""
      self.search_cache = {}
      self.content_cache = {}
      self.max_cache_size = 100
      self.max_concurrent_requests = 5
      self.request_timeout = 15
      self.headers = {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }

  def search_and_improve(self, query: str, time_range: str = "auto") -> str:
      """Main search method that includes self-improvement"""
      try:
          logger.info(f"Starting search for query: {query}")
          self.last_query = query
          self.last_time_range = time_range

          # Check cache first
          cache_key = f"{query}_{time_range}"
          if cache_key in self.search_cache:
              logger.info("Returning cached results")
              return self.search_cache[cache_key]

          # Perform initial search
          results = self.perform_search(query, time_range)
          if not results:
              return "No results found."

          # Enhance results with content fetching
          enhanced_results = self.enhance_search_results(results)
          
          # Generate improved summary
          summary = self.generate_enhanced_summary(enhanced_results, query)
          
          # Cache the results
          self.cache_results(cache_key, summary)
          
          return summary

      except Exception as e:
          logger.error(f"Search and improve error: {str(e)}", exc_info=True)
          return f"Error during search: {str(e)}"

  def perform_search(self, query: str, time_range: str) -> List[SearchResult]:
      """Performs web search with improved error handling and retry logic"""
      if not query:
          return []

      results = []
      retries = 3
      delay = 2

      for attempt in range(retries):
          try:
              encoded_query = quote_plus(query)
              search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
              
              response = requests.get(search_url, headers=self.headers, timeout=self.request_timeout)
              response.raise_for_status()
              
              soup = BeautifulSoup(response.text, 'html.parser')
              
              for i, result in enumerate(soup.select('.result'), 1):
                  if i > 15:  # Increased limit for better coverage
                      break
                      
                  title_elem = result.select_one('.result__title')
                  snippet_elem = result.select_one('.result__snippet')
                  link_elem = result.select_one('.result__url')
                  
                  if title_elem and link_elem:
                      title = title_elem.get_text(strip=True)
                      snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
                      url = link_elem.get('href', '')
                      
                      # Basic result scoring
                      score = self.calculate_result_score(title, snippet, query)
                      
                      results.append(SearchResult(title, url, snippet, score))

              if results:
                  # Sort results by score
                  results.sort(key=lambda x: x.score, reverse=True)
                  return results
              
              if attempt < retries - 1:
                  logger.warning(f"No results found, retrying ({attempt + 1}/{retries})...")
                  time.sleep(delay)
                  
          except Exception as e:
              logger.error(f"Search attempt {attempt + 1} failed: {str(e)}")
              if attempt < retries - 1:
                  time.sleep(delay)
              else:
                  raise

      return results

  def calculate_result_score(self, title: str, snippet: str, query: str) -> float:
      """Calculate relevance score for search result"""
      score = 0.0
      query_terms = query.lower().split()
      
      # Title matching
      title_lower = title.lower()
      for term in query_terms:
          if term in title_lower:
              score += 2.0
              
      # Snippet matching
      snippet_lower = snippet.lower()
      for term in query_terms:
          if term in snippet_lower:
              score += 1.0
              
      # Exact phrase matching
      if query.lower() in title_lower:
          score += 3.0
      if query.lower() in snippet_lower:
          score += 1.5
          
      return score

  def enhance_search_results(self, results: List[SearchResult]) -> List[SearchResult]:
      """Enhance search results with parallel content fetching"""
      enhanced_results = []
      
      with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent_requests) as executor:
          future_to_result = {
              executor.submit(self.fetch_and_process_content, result): result 
              for result in results[:10]  # Limit to top 10 results
          }
          
          for future in concurrent.futures.as_completed(future_to_result):
              result = future_to_result[future]
              try:
                  content = future.result()
                  if content:
                      result.content = content
                      result.processed = True
                      enhanced_results.append(result)
              except Exception as e:
                  logger.error(f"Error processing {result.url}: {str(e)}")
                  result.error = e
                  
      return enhanced_results

  def fetch_and_process_content(self, result: SearchResult) -> Optional[str]:
      """Fetch and process content for a search result"""
      try:
          # Check cache first
          if result.url in self.content_cache:
              return self.content_cache[result.url]

          # Check if we can fetch the content
          if not can_fetch(result.url):
              logger.warning(f"Cannot fetch content from {result.url}")
              return None

          content = get_web_content(result.url)
          if content:
              # Process and clean content
              cleaned_content = self.clean_content(content)
              
              # Cache the content
              self.cache_content(result.url, cleaned_content)
              
              return cleaned_content
              
      except Exception as e:
          logger.error(f"Error fetching content from {result.url}: {str(e)}")
          return None

  def clean_content(self, content: str) -> str:
      """Clean and normalize web content"""
      # Remove HTML tags if any remained
      content = re.sub(r'<[^>]+>', '', content)
      
      # Remove extra whitespace
      content = re.sub(r'\s+', ' ', content)
      
      # Remove special characters
      content = re.sub(r'[^\w\s.,!?-]', '', content)
      
      # Truncate if too long
      max_length = 5000
      if len(content) > max_length:
          content = content[:max_length] + "..."
          
      return content.strip()

  def generate_enhanced_summary(self, results: List[SearchResult], query: str) -> str:
      """Generate an enhanced summary using LLM with improved context"""
      try:
          # Prepare context from enhanced results
          context = self.prepare_summary_context(results, query)
          
          prompt = f"""
          Based on the following comprehensive search results for "{query}",
          provide a detailed analysis that:
          1. Synthesizes key information from multiple sources
          2. Highlights important findings and patterns
          3. Maintains factual accuracy and cites sources
          4. Presents a balanced view of different perspectives
          5. Identifies any gaps or limitations in the available information

          Context:
          {context}

          Please provide a well-structured analysis:
          """

          summary = self.llm.generate(prompt, max_tokens=1500)
          return self.format_summary(summary)

      except Exception as e:
          logger.error(f"Summary generation error: {str(e)}")
          return f"Error generating summary: {str(e)}"

  def prepare_summary_context(self, results: List[SearchResult], query: str) -> str:
      """Prepare context for summary generation"""
      context = f"Query: {query}\n\n"
      
      for i, result in enumerate(results, 1):
          context += f"Source {i}:\n"
          context += f"Title: {result.title}\n"
          context += f"URL: {result.url}\n"
          
          if result.content:
              # Include relevant excerpts from content
              excerpts = self.extract_relevant_excerpts(result.content, query)
              context += f"Key Excerpts:\n{excerpts}\n"
          else:
              context += f"Summary: {result.snippet}\n"
              
          context += "\n"
          
      return context

  def extract_relevant_excerpts(self, content: str, query: str, max_excerpts: int = 3) -> str:
      """Extract relevant excerpts from content"""
      sentences = re.split(r'[.!?]+', content)
      scored_sentences = []
      
      query_terms = set(query.lower().split())
      
      for sentence in sentences:
          sentence = sentence.strip()
          if not sentence:
              continue
              
          score = sum(1 for term in query_terms if term in sentence.lower())
          if score > 0:
              scored_sentences.append((sentence, score))
              
      # Sort by relevance score and take top excerpts
      scored_sentences.sort(key=lambda x: x[1], reverse=True)
      excerpts = [sentence for sentence, _ in scored_sentences[:max_excerpts]]
      
      return "\n".join(f"- {excerpt}" for excerpt in excerpts)

  def format_summary(self, summary: str) -> str:
      """Format the final summary for better readability"""
      # Add section headers if not present
      if not re.search(r'^Key Findings:', summary, re.MULTILINE):
          summary = "Key Findings:\n" + summary
          
      # Add source attribution if not present
      if not re.search(r'^Sources:', summary, re.MULTILINE):
          summary += "\n\nSources: Based on analysis of search results"
          
      # Add formatting
      summary = summary.replace('Key Findings:', f"{Fore.CYAN}Key Findings:{Style.RESET_ALL}")
      summary = summary.replace('Sources:', f"\n{Fore.CYAN}Sources:{Style.RESET_ALL}")
      
      return summary

  def cache_results(self, key: str, value: str) -> None:
      """Cache search results with size limit"""
      if len(self.search_cache) >= self.max_cache_size:
          # Remove oldest entry
          oldest_key = next(iter(self.search_cache))
          del self.search_cache[oldest_key]
      
      self.search_cache[key] = value

  def cache_content(self, url: str, content: str) -> None:
      """Cache web content with size limit"""
      if len(self.content_cache) >= self.max_cache_size:
          # Remove oldest entry
          oldest_key = next(iter(self.content_cache))
          del self.content_cache[oldest_key]
      
      self.content_cache[url] = content

  def clear_cache(self) -> None:
      """Clear all caches"""
      self.search_cache.clear()
      self.content_cache.clear()

  def get_last_query(self) -> str:
      """Returns the last executed query"""
      return self.last_query

  def get_last_time_range(self) -> str:
      """Returns the last used time range"""
      return self.last_time_range

if __name__ == "__main__":
  pass
