import json
import logging
import os
from collections import defaultdict
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

def load_data():
    """Load processed and raw data for network analysis."""
    processed_dir = Path("data/processed")
    raw_dir = Path("data/raw")
    
    # Load comparative analysis results if available
    comp_path = processed_dir / "comparative_analysis_results.json"
    if comp_path.exists():
        with open(comp_path, 'r', encoding='utf-8') as f:
            comparative_data = json.load(f)
    else:
        comparative_data = None
    
    # Load raw source data
    sources_data = {}
    for source_dir in raw_dir.iterdir():
        if source_dir.is_dir():
            source_id = source_dir.name
            sources_data[source_id] = []
            for json_file in source_dir.glob("*.json"):
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        sources_data[source_id].append(data)
                except Exception as e:
                    logger.error(f"Error loading {json_file}: {str(e)}")
    
    return {
        "comparative_data": comparative_data,
        "sources_data": sources_data
    }

def extract_citations(sources_data):
    """Extract citations between different sources."""
    citations = defaultdict(list)
    
    # Define common citation patterns for each source
    source_patterns = {
        "naiia": ["national artificial intelligence initiative", "naii act", "naiia"],
        "naiio": ["national ai initiative office", "naiio"],
        "nist_ai": ["nist", "ai risk management framework", "ai rmf"],
        "nsf_ai": ["nsf", "national science foundation", "ai research institutes"],
        "oecd_aipo": ["oecd", "ai policy observatory"],
        "eu_ai_act": ["eu ai act", "european union artificial intelligence act"],
        "unesco_aiethics": ["unesco", "recommendation on ai ethics"],
        "gpai": ["global partnership on artificial intelligence", "gpai"]
        # Add more patterns for other sources as needed
    }
    
    # Scan each source for references to other sources
    for source_id, source_files in sources_data.items():
        for file_data in source_files:
            if isinstance(file_data, dict):
                # Extract text content from file data
                text_content = json.dumps(file_data).lower()
                
                # Check for references to other sources
                for target_id, patterns in source_patterns.items():
                    if source_id != target_id:  # Don't count self-references
                        for pattern in patterns:
                            if pattern.lower() in text_content:
                                citations[source_id].append(target_id)
                                break  # Only count one citation per target source
    
    # Convert to a more structured format
    citation_records = []
    for source, targets in citations.items():
        for target in targets:
            citation_records.append({
                "source": source,
                "target": target
            })
    
    return pd.DataFrame(citation_records)

def extract_similarity_data(comparative_data):
    """Extract source similarity data from comparative analysis."""
    if not comparative_data or "similarity_matrix" not in comparative_data:
        logger.warning("No similarity matrix available in comparative data")
        return None
    
    similarity_matrix = comparative_data["similarity_matrix"]
    if not similarity_matrix:
        return None
    
    # Convert the similarity matrix to a list of pairwise similarities
    similarity_data = []
    
    for source1 in similarity_matrix:
        for source2, sim_value in similarity_matrix[source1].items():
            if source1 != source2:  # Skip self-similarities
                similarity_data.append({
                    "source1": source1,
                    "source2": source2,
                    "similarity": sim_value
                })
    
    # Convert to DataFrame and sort by similarity
    sim_df = pd.DataFrame(similarity_data)
    if not sim_df.empty:
        sim_df = sim_df.sort_values(by="similarity", ascending=False)
    
    return sim_df

def identify_clusters(similarity_data, threshold=0.6):
    """Identify clusters of similar sources."""
    if similarity_data is None or similarity_data.empty:
        logger.warning("No similarity data available for clustering")
        return []
    
    # Create a list of all unique sources
    all_sources = set(similarity_data["source1"].tolist() + similarity_data["source2"].tolist())
    
    # Dictionary to track which cluster each source belongs to
    source_clusters = {source: None for source in all_sources}
    clusters = []
    
    # Group by similarity above threshold
    high_similarity = similarity_data[similarity_data["similarity"] > threshold]
    
    # Process each high-similarity pair
    cluster_id = 0
    for _, row in high_similarity.iterrows():
        source1 = row["source1"]
        source2 = row["source2"]
        
        # Check if either source is already in a cluster
        cluster1 = source_clusters[source1]
        cluster2 = source_clusters[source2]
        
        if cluster1 is None and cluster2 is None:
            # Create new cluster
            new_cluster = {
                "id": cluster_id,
                "name": f"Cluster {cluster_id + 1}",
                "sources": [source1, source2],
                "avg_similarity": row["similarity"]
            }
            clusters.append(new_cluster)
            
            # Assign sources to this cluster
            source_clusters[source1] = cluster_id
            source_clusters[source2] = cluster_id
            
            cluster_id += 1
            
        elif cluster1 is not None and cluster2 is None:
            # Add source2 to source1's cluster
            clusters[cluster1]["sources"].append(source2)
            source_clusters[source2] = cluster1
            
        elif cluster1 is None and cluster2 is not None:
            # Add source1 to source2's cluster
            clusters[cluster2]["sources"].append(source1)
            source_clusters[source1] = cluster2
            
        elif cluster1 != cluster2:
            # Merge clusters
            # Keep cluster1, remove cluster2
            clusters[cluster1]["sources"].extend(clusters[cluster2]["sources"])
            
            # Update cluster assignments
            for source in clusters[cluster2]["sources"]:
                source_clusters[source] = cluster1
            
            # Remove the merged cluster
            clusters.pop(cluster2)
            
            # Update remaining cluster IDs
            for i in range(cluster2, len(clusters)):
                for source in clusters[i]["sources"]:
                    source_clusters[source] = i
    
    # Update average similarities
    for cluster in clusters:
        cluster_sources = cluster["sources"]
        if len(cluster_sources) > 1:
            # Get all pairwise similarities within this cluster
            cluster_similarities = []
            for i, source1 in enumerate(cluster_sources):
                for source2 in cluster_sources[i+1:]:
                    # Find this pair in similarity_data
                    pair_data = similarity_data[
                        ((similarity_data["source1"] == source1) & (similarity_data["source2"] == source2)) |
                        ((similarity_data["source1"] == source2) & (similarity_data["source2"] == source1))
                    ]
                    if not pair_data.empty:
                        cluster_similarities.append(pair_data["similarity"].values[0])
            
            if cluster_similarities:
                cluster["avg_similarity"] = sum(cluster_similarities) / len(cluster_similarities)
    
    return clusters

def analyze_network():
    """Main function to analyze the network of AI policy sources."""
    logger.info("Starting network analysis")
    
    # Load data
    data = load_data()
    comparative_data = data["comparative_data"]
    sources_data = data["sources_data"]
    
    # Extract citations between sources
    citation_df = extract_citations(sources_data)
    logger.info(f"Extracted {len(citation_df) if citation_df is not None else 0} citations between sources")
    
    # Extract similarity data
    similarity_df = extract_similarity_data(comparative_data)
    logger.info(f"Extracted {len(similarity_df) if similarity_df is not None else 0} similarity pairs")
    
    # Identify clusters
    clusters = identify_clusters(similarity_df)
    logger.info(f"Identified {len(clusters)} clusters of similar sources")
    
    # Create network analysis results
    results = {
        "citations": citation_df.to_dict("records") if citation_df is not None else [],
        "similarities": similarity_df.to_dict("records") if similarity_df is not None else [],
        "clusters": clusters
    }
    
    # Save results
    output_path = Path("data/processed/network_analysis_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Network analysis results saved to {output_path}")
    return results 