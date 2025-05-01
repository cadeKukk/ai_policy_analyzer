import logging
import re
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class NAIIAScraper(BaseScraper):
    """Scraper for the National Artificial Intelligence Initiative Act."""
    
    def __init__(self):
        super().__init__(
            source_id="naiia",
            source_name="National Artificial Intelligence Initiative Act",
            base_url="https://www.ai.gov/naiia/"
        )
        self.text_url = "https://www.congress.gov/116/plaws/publ283/PLAW-116publ283.pdf"
        self.summary_url = "https://www.ai.gov/wp-content/uploads/2021/05/National-AI-Initiative-Act-of-2020-Explainer.pdf"
        
    def scrape(self):
        """Scrape NAIIA information from multiple sources."""
        results = {
            "overview": self.scrape_overview(),
            "sections": self.scrape_sections(),
            "key_provisions": self.scrape_key_provisions(),
            "related_resources": self.scrape_related_resources()
        }
        
        # Save the combined results
        self.save_data(results, "naiia_combined.json")
        return results
    
    def scrape_overview(self):
        """Scrape the overview information from the main page."""
        logger.info("Scraping NAIIA overview")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        # Save raw HTML
        self.save_raw_html(response.text, self.base_url)
        
        # Extract main content
        main_content = soup.select_one("main.site-main")
        if not main_content:
            main_content = soup.select_one(".entry-content")
        
        overview = {}
        
        # Extract title
        title_elem = main_content.select_one("h1") or main_content.select_one("h2")
        if title_elem:
            overview["title"] = title_elem.get_text(strip=True)
        
        # Extract description
        description_paras = main_content.select("p")[:3]  # First few paragraphs usually contain overview
        overview["description"] = "\n\n".join([p.get_text(strip=True) for p in description_paras if p.get_text(strip=True)])
        
        # Extract enactment date if available
        date_match = re.search(r'enacted\s+on\s+(\w+\s+\d+,\s+\d{4})', overview["description"], re.IGNORECASE)
        if date_match:
            overview["enactment_date"] = date_match.group(1)
            
        return overview
    
    def scrape_sections(self):
        """Scrape the sections of the NAIIA."""
        logger.info("Scraping NAIIA sections")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        sections = []
        
        # Look for section headings
        section_headings = soup.select("h2, h3")
        for heading in section_headings:
            section_text = heading.get_text(strip=True)
            if re.search(r'section|title|subtitle', section_text, re.IGNORECASE):
                section_content = []
                next_elem = heading.next_sibling
                while next_elem and next_elem.name not in ['h2', 'h3']:
                    if next_elem.name == 'p':
                        section_content.append(next_elem.get_text(strip=True))
                    next_elem = next_elem.next_sibling
                
                sections.append({
                    "title": section_text,
                    "content": "\n".join(section_content)
                })
        
        return sections
    
    def scrape_key_provisions(self):
        """Scrape key provisions of the NAIIA."""
        logger.info("Scraping NAIIA key provisions")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        provisions = []
        
        # Look for lists which often contain key provisions
        lists = soup.select("ul, ol")
        for list_elem in lists:
            list_items = list_elem.select("li")
            
            # Check if this list might contain provisions
            for item in list_items:
                item_text = item.get_text(strip=True)
                if re.search(r'establish|create|develop|implement|require', item_text, re.IGNORECASE):
                    provisions.append(item_text)
        
        return provisions
    
    def scrape_related_resources(self):
        """Scrape related resources linked from the NAIIA page."""
        logger.info("Scraping NAIIA related resources")
        
        response = self.fetch_url(self.base_url)
        soup = self.parse_html(response.text)
        
        resources = []
        
        # Find all links that might be resources
        links = soup.select("a")
        for link in links:
            href = link.get('href', '')
            text = link.get_text(strip=True)
            
            # Skip empty or navigation links
            if not href or not text or re.search(r'(#|javascript:|mailto:|tel:)', href) or len(text) < 5:
                continue
                
            # Make sure URL is absolute
            if not href.startswith(('http://', 'https://')):
                href = urljoin(self.base_url, href)
                
            resources.append({
                "title": text,
                "url": href
            })
            
        return resources

def run_scraper():
    """Run the NAIIA scraper."""
    scraper = NAIIAScraper()
    return scraper.run_scraper() 