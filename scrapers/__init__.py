import importlib
import logging
import os
import pkgutil
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

def discover_scrapers():
    """Dynamically discover all scraper modules in the package."""
    scrapers = []
    package_path = os.path.dirname(__file__)
    
    for _, name, is_pkg in pkgutil.iter_modules([package_path]):
        if not is_pkg and name != "__init__" and name.endswith("_scraper"):
            try:
                module = importlib.import_module(f"scrapers.{name}")
                if hasattr(module, "run_scraper"):
                    scrapers.append(module)
                    logger.info(f"Discovered scraper module: {name}")
                else:
                    logger.warning(f"Module {name} does not have a run_scraper function")
            except Exception as e:
                logger.error(f"Error importing scraper module {name}: {str(e)}")
    
    return scrapers

def run_all_scrapers(max_workers=5):
    """Run all discovered scrapers in parallel."""
    scrapers = discover_scrapers()
    logger.info(f"Found {len(scrapers)} scraper modules to run")
    
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_scraper = {
            executor.submit(scraper.run_scraper): scraper.__name__ 
            for scraper in scrapers
        }
        
        for future in future_to_scraper:
            scraper_name = future_to_scraper[future]
            try:
                results[scraper_name] = future.result()
                logger.info(f"Successfully completed scraper: {scraper_name}")
            except Exception as e:
                logger.error(f"Error running scraper {scraper_name}: {str(e)}")
                results[scraper_name] = None
    
    return results

# Define the list of data sources
DATA_SOURCES = [
    {"id": "naiia", "name": "National Artificial Intelligence Initiative Act", "url": "https://www.ai.gov/naiia/"},
    {"id": "naiio", "name": "National Artificial Intelligence Initiative Office", "url": "https://www.ai.gov/"},
    {"id": "nairrtf", "name": "National AI Research Resource Task Force", "url": "https://www.ai.gov/nairrtf/"},
    {"id": "nitrd", "name": "Networking & Information Technology Research & Development", "url": "https://www.nitrd.gov/"},
    {"id": "nist", "name": "NIST AI Risk Management Framework", "url": "https://www.nist.gov/itl/ai-risk-management-framework"},
    {"id": "nsf_ai", "name": "NSF AI Research Institutes", "url": "https://beta.nsf.gov/funding/opportunities/national-artificial-intelligence-research-institutes"},
    {"id": "doe_aito", "name": "DOE Artificial Intelligence & Technology Office", "url": "https://www.energy.gov/ai/artificial-intelligence-technology-office"},
    {"id": "ostp", "name": "Office of Science and Technology Policy", "url": "https://www.whitehouse.gov/ostp/"},
    {"id": "oecd_aipo", "name": "OECD AI Policy Observatory", "url": "https://oecd.ai/"},
    {"id": "gpai", "name": "Global Partnership on Artificial Intelligence", "url": "https://gpai.ai/"},
    {"id": "unesco_aiethics", "name": "UNESCO Recommendation on AI Ethics", "url": "https://en.unesco.org/artificial-intelligence/ethics"},
    {"id": "eu_ai_act", "name": "European Union Artificial Intelligence Act", "url": "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"},
    {"id": "wef_ai", "name": "World Economic Forum AI Governance Alliance", "url": "https://www.weforum.org/communities/gfc-on-artificial-intelligence-for-humanity/"},
    {"id": "stanford_hai", "name": "Stanford Human-Centered Artificial Intelligence", "url": "https://hai.stanford.edu/"}
    # Add the remaining sources here
] 