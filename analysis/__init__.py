import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

def analyze_all_data():
    """Run all analysis modules on the collected data."""
    from .text_analysis import analyze_text_data
    from .network_analysis import analyze_network
    from .comparative_analysis import run_comparative_analysis
    from frontend.visualization import generate_visualizations
    
    logger.info("Starting comprehensive data analysis")
    
    # Create processed data directory if it doesn't exist
    processed_dir = Path("data/processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    # Run text analysis on scraped content
    text_results = analyze_text_data()
    logger.info("Completed text analysis")
    
    # Run comparative analysis across sources
    comparative_results = run_comparative_analysis()
    logger.info("Completed comparative analysis")
    
    # Analyze relationships between organizations and policies
    # (reads the similarity scores the comparative analysis just saved)
    network_results = analyze_network()
    logger.info("Completed network analysis")
    
    # Generate visualizations
    visualization_results = generate_visualizations({
        "text_analysis": text_results,
        "comparative_analysis": comparative_results
    })
    logger.info("Completed visualization generation")
    
    # Return summary of all analysis results
    return {
        "text_analysis": text_results,
        "network_analysis": network_results,
        "comparative_analysis": comparative_results,
        "visualizations": visualization_results
    } 