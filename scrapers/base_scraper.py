import json
import logging
import os
import time
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all scrapers, providing common functionality."""
    
    def __init__(self, source_id, source_name, base_url):
        self.source_id = source_id
        self.source_name = source_name
        self.base_url = base_url
        self.data_dir = Path("data/raw") / self.source_id
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        })
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def fetch_url(self, url, retry_count=3, retry_delay=5):
        """Fetch content from URL with retry logic."""
        for attempt in range(retry_count):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt+1}/{retry_count} failed for {url}: {str(e)}")
                if attempt < retry_count - 1:
                    time.sleep(retry_delay)
                else:
                    logger.error(f"Failed to fetch {url} after {retry_count} attempts")
                    raise
    
    def parse_html(self, html_content):
        """Parse HTML content using BeautifulSoup."""
        return BeautifulSoup(html_content, 'html.parser')
    
    def save_data(self, data, filename):
        """Save scraped data to JSON file."""
        filepath = self.data_dir / filename
        
        # Add metadata
        if isinstance(data, dict):
            data.update({
                "source_id": self.source_id,
                "source_name": self.source_name,
                "source_url": self.base_url,
                "scrape_timestamp": datetime.now().isoformat()
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved data to {filepath}")
        return filepath
    
    def save_raw_html(self, html_content, url):
        """Save raw HTML content for archival purposes."""
        filename = f"{self.source_id}_{url.replace('://', '_').replace('/', '_').replace('?', '_')}.html"
        filepath = self.data_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.debug(f"Saved raw HTML to {filepath}")
        return filepath
    
    @abstractmethod
    def scrape(self):
        """Main scraping logic implemented by each specific scraper."""
        pass
    
    def run_scraper(self):
        """Run the scraper and handle exceptions."""
        logger.info(f"Starting scraper for {self.source_name}")
        try:
            result = self.scrape()
            logger.info(f"Successfully completed scraping {self.source_name}")
            return result
        except Exception as e:
            logger.error(f"Error scraping {self.source_name}: {str(e)}", exc_info=True)
            raise 