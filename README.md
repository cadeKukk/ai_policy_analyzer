# AI Policy Analyzer

A web scraping and analysis application focused on evaluating the National Artificial Intelligence Initiative Act (NAIIA) and related AI governance frameworks worldwide.

## Project Overview

This application collects, analyzes, and presents information from various authoritative sources on AI policy, with a special focus on the National Artificial Intelligence Initiative Act and its implementation. The tool helps researchers, policymakers, and interested individuals understand the global AI governance landscape.

## Data Sources

The application scrapes and analyzes information from numerous sources mainly:

- National Artificial Intelligence Initiative Act (NAIIA)
- National AI Initiative Office (NAIIO)
- National AI Research Resource Task Force (NAIRRTF)
- NIST AI Risk Management Framework
- NSF AI Research Institutes
- And 50+ other international AI governance organizations and frameworks

## Project Structure

- `/scrapers`: Web scraping modules for each data source
- `/analysis`: Text analysis and evaluation tools
- `/data`: Storage for scraped data and analysis results
- `/frontend`: Web interface for exploring results
- `/utils`: Helper functions and utilities

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai_policy_analyzer.git
cd ai_policy_analyzer

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

1. **Scrape data from sources:**
   ```bash
   python main.py --scrape
   ```

2. **Analyze collected data:**
   ```bash
   python main.py --analyze
   ```

3. **Run the web interface:**
   ```bash
   python main.py --serve
   ```
