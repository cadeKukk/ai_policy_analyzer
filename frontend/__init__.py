import json
import logging
import os
from pathlib import Path

from flask import Flask, render_template, request, jsonify

from .visualization import generate_visualizations

logger = logging.getLogger(__name__)

# Create the Flask application
app = Flask(__name__)

# Load data for the application
def load_analysis_results():
    """Load analysis results from processed data files."""
    processed_dir = Path("data/processed")
    results = {}
    
    # Load text analysis results
    text_analysis_path = processed_dir / "text_analysis_results.json"
    if text_analysis_path.exists():
        try:
            with open(text_analysis_path, 'r', encoding='utf-8') as f:
                results["text_analysis"] = json.load(f)
        except Exception as e:
            logger.error(f"Error loading text analysis results: {str(e)}")
    
    # Load comparative analysis results
    comp_analysis_path = processed_dir / "comparative_analysis_results.json"
    if comp_analysis_path.exists():
        try:
            with open(comp_analysis_path, 'r', encoding='utf-8') as f:
                results["comparative_analysis"] = json.load(f)
        except Exception as e:
            logger.error(f"Error loading comparative analysis results: {str(e)}")
    
    return results

# Define routes
@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html')

@app.route('/overview')
def overview():
    """Render the overview page with key findings."""
    results = load_analysis_results()
    return render_template('overview.html', results=results)

@app.route('/sources')
def sources():
    """Render the page showing information about data sources."""
    from scrapers import DATA_SOURCES
    return render_template('sources.html', sources=DATA_SOURCES)

@app.route('/analysis')
def analysis():
    """Render the analysis page with detailed findings."""
    results = load_analysis_results()
    return render_template('analysis.html', results=results)

@app.route('/compare')
def compare():
    """Render the comparison page for comparing different sources."""
    results = load_analysis_results()
    sources = request.args.getlist('sources')
    return render_template('compare.html', results=results, selected_sources=sources)

@app.route('/api/results')
def api_results():
    """API endpoint to get analysis results as JSON."""
    results = load_analysis_results()
    return jsonify(results)

@app.route('/api/visualizations')
def api_visualizations():
    """API endpoint to get visualization data."""
    viz_type = request.args.get('type', 'wordcloud')
    results = load_analysis_results()
    
    # Generate visualizations based on results
    visualizations = generate_visualizations(results, viz_type)
    return jsonify(visualizations)

# Create required templates directory
os.makedirs(os.path.join(os.path.dirname(__file__), 'templates'), exist_ok=True)
os.makedirs(os.path.join(os.path.dirname(__file__), 'static'), exist_ok=True) 