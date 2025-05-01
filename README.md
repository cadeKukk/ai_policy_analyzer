# AI Policy Analyzer

A web scraping and analysis application focused on evaluating the National Artificial Intelligence Initiative Act (NAIIA) and related AI governance frameworks worldwide.

## Project Overview

This application collects, analyzes, and presents information from various authoritative sources on AI policy, with a special focus on the National Artificial Intelligence Initiative Act and its implementation. The tool helps researchers, policymakers, and interested individuals understand the global AI governance landscape.

## Data Sources

The application scrapes and analyzes information from numerous sources, including:

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

## Features

- **Comprehensive Data Collection**: Scrape and archive AI policy information from 50+ authoritative sources
- **Text Analysis**: Extract key terms, topics, and themes from policy documents using NLP techniques
- **Policy Comparison**: Compare different AI policies to identify similarities, differences, and unique approaches
- **Network Analysis**: Visualize relationships and influences between various AI governance frameworks
- **Interactive Web Interface**: Explore findings through an intuitive and informative web application

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

### Scraping Data

To scrape data from all configured sources:

```bash
python main.py --scrape
```

The scraped data will be stored in the `/data/raw` directory, organized by source.

### Running Analysis

To analyze the collected data:

```bash
python main.py --analyze
```

This will process the raw data and generate analysis results in the `/data/processed` directory.

### Starting the Web Interface

To launch the web interface for exploring the results:

```bash
python main.py --serve
```

This will start a Flask web server on http://localhost:5000.

### All-in-One Command

To scrape data, run analysis, and start the web interface in sequence:

```bash
python main.py --all
```

## Extending the Application

### Adding New Data Sources

1. Define the source in `/scrapers/__init__.py` by adding to the `DATA_SOURCES` list
2. Create a new scraper module in `/scrapers/` following the pattern of existing scrapers
3. Implement the required `run_scraper()` function

### Adding New Analysis Methods

1. Create a new analysis module in `/analysis/`
2. Implement the analysis logic
3. Update the `analyze_all_data()` function in `/analysis/__init__.py` to include your new analysis

## License

MIT

## Contributors

- Your Name
