import logging
import re
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class NISTAIScraper(BaseScraper):
    """Scraper for the NIST AI Risk Management Framework."""
    
    def __init__(self):
        super().__init__(
            source_id="nist_ai",
            source_name="NIST AI Risk Management Framework",
            base_url="https://www.nist.gov/itl/ai-risk-management-framework"
        )
        self.rm_url = "https://www.nist.gov/itl/ai-risk-management-framework/ai-rmf-core"
        self.playbook_url = "https://www.nist.gov/itl/ai-risk-management-framework/resources"
        
    def scrape(self):
        """Scrape NIST AI Risk Management Framework information."""
        results = {
            "overview": self.scrape_overview(),
            "core_framework": self.scrape_core_framework(),
            "resources": self.scrape_resources(),
            "news": self.scrape_news()
        }
        
        # Save the combined results
        self.save_data(results, "nist_ai_combined.json")
        return results
    
    def scrape_overview(self):
        """Scrape the overview information from the main page."""
        logger.info("Scraping NIST AI RMF overview")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        # Save raw HTML
        self.save_raw_html(response.text, self.base_url)
        
        # Extract main content
        main_content = soup.select_one("#main-content")
        
        overview = {}
        
        # Extract title
        title_elem = main_content.select_one("h1")
        if title_elem:
            overview["title"] = title_elem.get_text(strip=True)
        
        # Extract description
        description_area = main_content.select_one(".grid-container")
        if description_area:
            description_paras = description_area.select("p")
            overview["description"] = "\n\n".join([p.get_text(strip=True) for p in description_paras if p.get_text(strip=True)])
        
        # Extract publication date if available
        date_area = main_content.select_one(".display-date, .published-date")
        if date_area:
            overview["publication_date"] = date_area.get_text(strip=True)
            
        return overview
    
    def scrape_core_framework(self):
        """Scrape the AI Risk Management Framework core information."""
        logger.info("Scraping NIST AI RMF core framework")
        
        response = self.fetch_url(self.rm_url)
        soup = self.parse_html(response.text)
        
        # Save raw HTML
        self.save_raw_html(response.text, self.rm_url)
        
        framework = {
            "functions": [],
            "categories": [],
            "subcategories": []
        }
        
        # Extract main content
        main_content = soup.select_one("#main-content")
        
        # Look for framework functions (main pillars)
        function_sections = main_content.select(".usa-accordion__heading, h2, h3")
        current_function = None
        current_category = None
        
        for section in function_sections:
            text = section.get_text(strip=True)
            
            # Check if this is a function heading (main pillar)
            if re.search(r'(govern|map|measure|manage)', text, re.IGNORECASE):
                current_function = {
                    "name": text,
                    "description": ""
                }
                
                # Look for description paragraph
                next_elem = section.find_next("p")
                if next_elem:
                    current_function["description"] = next_elem.get_text(strip=True)
                
                framework["functions"].append(current_function)
                current_category = None
                
            # Check if this is a category heading
            elif current_function and re.search(r'(context|risk|monitor|governance)', text, re.IGNORECASE):
                current_category = {
                    "function": current_function["name"],
                    "name": text,
                    "description": ""
                }
                
                # Look for description paragraph
                next_elem = section.find_next("p")
                if next_elem:
                    current_category["description"] = next_elem.get_text(strip=True)
                
                framework["categories"].append(current_category)
                
            # Check if this is a subcategory heading
            elif current_category and section.name == "h3":
                subcategory = {
                    "function": current_function["name"],
                    "category": current_category["name"],
                    "name": text,
                    "description": ""
                }
                
                # Look for description paragraph
                next_elem = section.find_next("p")
                if next_elem:
                    subcategory["description"] = next_elem.get_text(strip=True)
                
                framework["subcategories"].append(subcategory)
        
        return framework
    
    def scrape_resources(self):
        """Scrape resources from the Resources page."""
        logger.info("Scraping NIST AI RMF resources")
        
        response = self.fetch_url(self.playbook_url)
        soup = self.parse_html(response.text)
        
        # Save raw HTML
        self.save_raw_html(response.text, self.playbook_url)
        
        resources = []
        
        # Extract main content
        main_content = soup.select_one("#main-content")
        
        # Find all links in the content area
        links = main_content.select("a")
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip empty or navigation links
            if not href or not text or re.search(r'(#|javascript:|mailto:|tel:)', href) or len(text) < 5:
                continue
                
            # Make sure URL is absolute
            if not href.startswith(('http://', 'https://')):
                href = urljoin(self.playbook_url, href)
                
            # Try to determine resource type
            resource_type = "Other"
            if re.search(r'\.(pdf|doc|docx)$', href, re.IGNORECASE):
                resource_type = "Document"
            elif re.search(r'playbook|guidance|guide', text, re.IGNORECASE):
                resource_type = "Guide"
            elif re.search(r'tool|software|assessment', text, re.IGNORECASE):
                resource_type = "Tool"
                
            resources.append({
                "title": text,
                "url": href,
                "type": resource_type
            })
            
        return resources
    
    def scrape_news(self):
        """Scrape news and updates related to the AI RMF."""
        logger.info("Scraping NIST AI RMF news")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        news_items = []
        
        # Look for news items
        news_sections = soup.select(".news-item, .usa-card, article")
        
        for item in news_sections:
            news_item = {}
            
            # Extract title
            title_elem = item.select_one("h2, h3, .title")
            if title_elem:
                news_item["title"] = title_elem.get_text(strip=True)
            else:
                continue  # Skip items without title
            
            # Extract date
            date_elem = item.select_one(".date, .published-date, time")
            if date_elem:
                news_item["date"] = date_elem.get_text(strip=True)
            
            # Extract description
            desc_elem = item.select_one("p, .description, .summary")
            if desc_elem:
                news_item["description"] = desc_elem.get_text(strip=True)
            
            # Extract link
            link_elem = item.select_one("a")
            if link_elem and link_elem.get('href'):
                href = link_elem.get('href')
                if not href.startswith(('http://', 'https://')):
                    href = urljoin(self.base_url, href)
                news_item["url"] = href
            
            news_items.append(news_item)
            
        return news_items

def run_scraper():
    """Run the NIST AI RMF scraper."""
    scraper = NISTAIScraper()
    return scraper.run_scraper() 