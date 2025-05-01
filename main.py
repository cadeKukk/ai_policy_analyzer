#!/usr/bin/env python3
import argparse
import logging
import os
import sys
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("ai_policy_analyzer")

def setup_directories():
    """Ensure all required directories exist."""
    dirs = ["data/raw", "data/processed", "data/reports"]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"Ensured directory exists: {dir_path}")

def run_scrapers():
    """Run all scraper modules to collect data."""
    from scrapers import run_all_scrapers
    logger.info("Starting data scraping process...")
    run_all_scrapers()
    logger.info("Data scraping completed.")

def run_analysis():
    """Perform analysis on collected data."""
    from analysis import analyze_all_data
    logger.info("Starting data analysis...")
    analyze_all_data()
    logger.info("Data analysis completed.")

def serve_frontend():
    """Start the web interface for exploring results."""
    from frontend import app
    logger.info("Starting web interface...")
    app.run(debug=True, host='0.0.0.0', port=5000)

def main():
    """Main entry point with command-line argument parsing."""
    parser = argparse.ArgumentParser(
        description="AI Policy Analyzer - Tool for scraping and analyzing AI policy information"
    )
    parser.add_argument("--scrape", action="store_true", help="Run scrapers to collect data")
    parser.add_argument("--analyze", action="store_true", help="Run analysis on collected data")
    parser.add_argument("--serve", action="store_true", help="Start the web interface")
    parser.add_argument("--all", action="store_true", help="Run all steps (scrape, analyze, serve)")
    
    args = parser.parse_args()
    
    # Create required directories
    setup_directories()
    
    if args.all or (not any([args.scrape, args.analyze, args.serve])):
        run_scrapers()
        run_analysis()
        serve_frontend()
    else:
        if args.scrape:
            run_scrapers()
        if args.analyze:
            run_analysis()
        if args.serve:
            serve_frontend()

if __name__ == "__main__":
    main() 