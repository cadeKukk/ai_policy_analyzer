import json
import logging
import os
from collections import Counter, defaultdict
from pathlib import Path

logger = logging.getLogger(__name__)

def prepare_wordcloud_data(results):
    """Prepare data for word cloud visualizations."""
    wordcloud_data = {}
    
    if not results or "text_analysis" not in results:
        logger.warning("No text analysis results available for word cloud")
        return {}
    
    # Extract key terms data
    key_terms = results["text_analysis"].get("key_terms", {})
    
    # Overall word cloud
    if "overall_top_terms" in key_terms:
        overall_terms = key_terms["overall_top_terms"]
        wordcloud_data["overall"] = {term: count for term, count in overall_terms}
    
    # Per-source word clouds
    if "source_top_terms" in key_terms:
        source_terms = key_terms["source_top_terms"]
        wordcloud_data["sources"] = {
            source: {term: count for term, count in terms}
            for source, terms in source_terms.items()
        }
    
    return wordcloud_data

def prepare_topic_data(results):
    """Prepare data for topic visualizations."""
    topic_data = {}
    
    if not results or "text_analysis" not in results:
        logger.warning("No text analysis results available for topic visualization")
        return {}
    
    # Extract topics data
    topics = results["text_analysis"].get("topics", {})
    
    # Overall topics
    if "overall_topics" in topics:
        topic_data["overall"] = topics["overall_topics"]
    
    # Per-source topics
    if "source_topics" in topics:
        topic_data["sources"] = topics["source_topics"]
    
    return topic_data

def prepare_similarity_data(results):
    """Prepare data for similarity matrix visualization."""
    similarity_data = {}
    
    if not results or "comparative_analysis" not in results:
        logger.warning("No comparative analysis results available for similarity visualization")
        return {}
    
    # Extract similarity matrix
    similarity_matrix = results["comparative_analysis"].get("similarity_matrix")
    if similarity_matrix:
        similarity_data["matrix"] = similarity_matrix
    
    return similarity_data

def prepare_focus_data(results):
    """Prepare data for policy focus visualizations."""
    focus_data = {}
    
    if not results or "comparative_analysis" not in results:
        logger.warning("No comparative analysis results available for focus visualization")
        return {}
    
    # Extract policy focus data
    policy_focus = results["comparative_analysis"].get("policy_focus", {})
    
    if "focus_data" in policy_focus:
        # Aggregate terms across sources for comparison
        aggregated_focus = defaultdict(dict)
        
        for source, terms in policy_focus["focus_data"].items():
            for term, count in terms.items():
                aggregated_focus[term][source] = count
        
        # Filter for terms that appear in multiple sources
        multi_source_terms = {
            term: source_counts
            for term, source_counts in aggregated_focus.items()
            if len(source_counts) > 1
        }
        
        # Sort by total frequency across sources
        sorted_terms = sorted(
            multi_source_terms.items(),
            key=lambda x: sum(x[1].values()),
            reverse=True
        )
        
        # Take top terms for visualization
        top_comparison_terms = dict(sorted_terms[:20])
        focus_data["comparison"] = top_comparison_terms
    
    if "distinctive_terms" in policy_focus:
        focus_data["distinctive"] = policy_focus["distinctive_terms"]
    
    return focus_data

def generate_visualizations(results, viz_type="all"):
    """Generate visualization data based on analysis results."""
    visualizations = {}
    
    if viz_type in ["wordcloud", "all"]:
        visualizations["wordcloud"] = prepare_wordcloud_data(results)
    
    if viz_type in ["topics", "all"]:
        visualizations["topics"] = prepare_topic_data(results)
    
    if viz_type in ["similarity", "all"]:
        visualizations["similarity"] = prepare_similarity_data(results)
    
    if viz_type in ["focus", "all"]:
        visualizations["focus"] = prepare_focus_data(results)
    
    # Save visualization data to file for caching
    output_path = Path("data/processed/visualization_data.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(visualizations, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Generated visualization data: {', '.join(visualizations.keys())}")
    return visualizations 