import json
import logging
import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def load_processed_data():
    """Load processed data for comparative analysis."""
    processed_dir = Path("data/processed")
    
    try:
        text_analysis_path = processed_dir / "text_analysis_results.json"
        if text_analysis_path.exists():
            with open(text_analysis_path, 'r', encoding='utf-8') as f:
                text_analysis = json.load(f)
        else:
            logger.warning("Text analysis results not found")
            text_analysis = None
            
        return {
            "text_analysis": text_analysis
        }
    except Exception as e:
        logger.error(f"Error loading processed data: {str(e)}")
        return {}

def load_raw_data():
    """Load raw data from all sources."""
    data_dir = Path("data/raw")
    all_data = {}
    
    for source_dir in data_dir.iterdir():
        if source_dir.is_dir():
            source_id = source_dir.name
            all_data[source_id] = []
            
            for json_file in source_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        all_data[source_id].append({
                            "filename": json_file.name,
                            "data": data
                        })
                except Exception as e:
                    logger.error(f"Error loading {json_file}: {str(e)}")
    
    return all_data

def extract_source_documents(raw_data):
    """Extract text documents from each source for comparison."""
    source_docs = {}
    
    for source_id, source_files in raw_data.items():
        source_docs[source_id] = []
        
        for file_data in source_files:
            try:
                data = file_data["data"]
                
                # Extract text from different data structures
                if isinstance(data, dict):
                    # Try to find description or overview
                    if "overview" in data and isinstance(data["overview"], dict):
                        if "description" in data["overview"]:
                            source_docs[source_id].append(data["overview"]["description"])
                    
                    # Try to find sections content
                    if "sections" in data and isinstance(data["sections"], list):
                        for section in data["sections"]:
                            if isinstance(section, dict) and "content" in section:
                                source_docs[source_id].append(section["content"])
                                
                    # General recursive extraction
                    for key, value in data.items():
                        if isinstance(value, str) and len(value) > 100:
                            source_docs[source_id].append(value)
            except Exception as e:
                logger.warning(f"Error extracting text from {source_id}/{file_data['filename']}: {str(e)}")
    
    # Combine documents per source
    source_combined = {}
    for source_id, docs in source_docs.items():
        if docs:
            source_combined[source_id] = " ".join(docs)
    
    return source_combined

def calculate_similarity_matrix(source_docs):
    """Calculate similarity matrix between different sources."""
    if not source_docs:
        logger.warning("No source documents available for similarity calculation")
        return None
    
    # Get source IDs and texts
    sources = list(source_docs.keys())
    texts = [source_docs[source] for source in sources]
    
    # Calculate TF-IDF vectors
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    
    # Create DataFrame for easier processing
    sim_df = pd.DataFrame(similarity_matrix, index=sources, columns=sources)
    
    return sim_df

def find_key_policy_themes(text_analysis):
    """Identify key policy themes across sources."""
    if not text_analysis or "topics" not in text_analysis:
        logger.warning("No topic data available for theme analysis")
        return {}
    
    # Extract overall topics
    overall_topics = text_analysis["topics"].get("overall_topics", {})
    
    # Extract source topics
    source_topics = text_analysis["topics"].get("source_topics", {})
    
    # Identify shared themes across sources
    theme_sources = defaultdict(list)
    
    for source, topics in source_topics.items():
        for topic_id, words in topics.items():
            theme_key = "-".join(words[:3])  # Use first three words as theme identifier
            theme_sources[theme_key].append(source)
    
    # Filter for themes shared by multiple sources
    shared_themes = {
        "-".join(words[:3]): sources
        for theme, sources in theme_sources.items()
        if len(sources) > 1  # Theme must be present in more than one source
    }
    
    return {
        "overall_topics": overall_topics,
        "shared_themes": shared_themes
    }

def compare_policy_focus(text_analysis):
    """Compare the focus of different AI policies based on key terms."""
    if not text_analysis or "key_terms" not in text_analysis:
        logger.warning("No key terms data available for focus analysis")
        return {}
    
    source_terms = text_analysis["key_terms"].get("source_top_terms", {})
    
    # Calculate term frequency per source
    focus_data = {}
    
    for source, terms in source_terms.items():
        # Extract terms and counts, ignore scores
        term_dict = {term: count for term, count in terms}
        focus_data[source] = term_dict
    
    # Find distinctive terms for each source
    distinctive_terms = {}
    all_terms = set()
    
    for source, terms in focus_data.items():
        all_terms.update(terms.keys())
    
    for source, terms in focus_data.items():
        # Find terms that are more frequent in this source than others
        source_distinctive = {}
        
        for term in terms:
            current_count = terms.get(term, 0)
            is_distinctive = True
            
            for other_source, other_terms in focus_data.items():
                if other_source == source:
                    continue
                
                other_count = other_terms.get(term, 0)
                if other_count >= current_count:
                    is_distinctive = False
                    break
            
            if is_distinctive and current_count > 2:  # Term must appear at least 3 times
                source_distinctive[term] = current_count
        
        distinctive_terms[source] = sorted(source_distinctive.items(), key=lambda x: x[1], reverse=True)
    
    return {
        "focus_data": focus_data,
        "distinctive_terms": distinctive_terms
    }

def run_comparative_analysis():
    """Run full comparative analysis across sources."""
    logger.info("Starting comparative analysis")
    
    # Load processed data
    processed_data = load_processed_data()
    text_analysis = processed_data.get("text_analysis")
    
    # Load raw data
    raw_data = load_raw_data()
    logger.info(f"Loaded raw data from {len(raw_data)} sources")
    
    # Extract documents for similarity analysis
    source_docs = extract_source_documents(raw_data)
    logger.info(f"Extracted documents from {len(source_docs)} sources")
    
    # Calculate similarity matrix
    similarity_matrix = calculate_similarity_matrix(source_docs)
    logger.info("Calculated similarity matrix between sources")
    
    # Find key policy themes
    policy_themes = find_key_policy_themes(text_analysis)
    logger.info("Identified key policy themes across sources")
    
    # Compare policy focus
    policy_focus = compare_policy_focus(text_analysis)
    logger.info("Compared policy focus areas")
    
    # Combine results
    results = {
        "similarity_matrix": similarity_matrix.to_dict() if isinstance(similarity_matrix, pd.DataFrame) else None,
        "policy_themes": policy_themes,
        "policy_focus": policy_focus
    }
    
    # Save results
    output_path = Path("data/processed/comparative_analysis_results.json")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Convert DataFrame to dict for JSON serialization
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Comparative analysis results saved to {output_path}")
    return results 