import json
import logging
import os
import re
from collections import Counter
from pathlib import Path

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

logger = logging.getLogger(__name__)

# Download required NLTK data
def download_nltk_data():
    """Download required NLTK data packages."""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except Exception as e:
        logger.warning(f"Failed to download some NLTK data: {str(e)}")

def load_raw_data():
    """Load all the scraped data from JSON files in the raw data directory."""
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

def extract_text_content(data_dict):
    """Extract all text content from the data dictionary for analysis."""
    text_content = []
    
    def extract_text_from_item(item, source_id):
        """Recursively extract text from a data item."""
        if isinstance(item, str):
            text_content.append({"source": source_id, "text": item})
        elif isinstance(item, dict):
            for key, value in item.items():
                if key not in ["source_id", "source_name", "source_url", "scrape_timestamp", "url", "href"]:
                    extract_text_from_item(value, source_id)
        elif isinstance(item, list):
            for subitem in item:
                extract_text_from_item(subitem, source_id)
    
    for source_id, source_data in data_dict.items():
        for data_file in source_data:
            extract_text_from_item(data_file["data"], source_id)
    
    return text_content

def preprocess_text(text_list):
    """Preprocess text for analysis (tokenize, remove stopwords, lemmatize)."""
    download_nltk_data()
    
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    preprocessed_texts = []
    
    for text_item in text_list:
        source = text_item["source"]
        text = text_item["text"]
        
        # Skip if text is too short
        if len(text) < 10:
            continue
            
        # Tokenize and lowercase
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords, numbers, and short tokens
        filtered_tokens = [
            token for token in tokens 
            if token not in stop_words and 
            not token.isdigit() and
            len(token) > 2 and
            re.match(r'^[a-zA-Z]+$', token)
        ]
        
        # Lemmatize
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
        
        preprocessed_texts.append({
            "source": source,
            "raw_text": text,
            "tokens": lemmatized_tokens,
            "preprocessed_text": " ".join(lemmatized_tokens)
        })
    
    return preprocessed_texts

def extract_key_terms(preprocessed_texts, top_n=30):
    """Extract key terms using term frequency."""
    all_tokens = []
    source_tokens = {}
    
    for item in preprocessed_texts:
        source = item["source"]
        tokens = item["tokens"]
        all_tokens.extend(tokens)
        
        if source not in source_tokens:
            source_tokens[source] = []
        source_tokens[source].extend(tokens)
    
    # Calculate overall term frequency
    term_freq = Counter(all_tokens)
    overall_top_terms = term_freq.most_common(top_n)
    
    # Calculate per-source term frequency
    source_top_terms = {}
    for source, tokens in source_tokens.items():
        source_term_freq = Counter(tokens)
        source_top_terms[source] = source_term_freq.most_common(top_n)
    
    return {
        "overall_top_terms": overall_top_terms,
        "source_top_terms": source_top_terms
    }

def topic_modeling(preprocessed_texts, num_topics=5, num_words=10):
    """Perform topic modeling using Latent Dirichlet Allocation."""
    # Combine texts by source
    source_texts = {}
    for item in preprocessed_texts:
        source = item["source"]
        if source not in source_texts:
            source_texts[source] = []
        source_texts[source].append(item["preprocessed_text"])
    
    # Combine all texts
    all_texts = [item["preprocessed_text"] for item in preprocessed_texts]
    
    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, stop_words='english')
    
    # Perform topic modeling for all texts combined
    overall_topics = {}
    if all_texts:
        tfidf = vectorizer.fit_transform(all_texts)
        feature_names = vectorizer.get_feature_names_out()
        
        lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
        lda.fit(tfidf)
        
        for topic_idx, topic in enumerate(lda.components_):
            top_words_idx = topic.argsort()[:-num_words-1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            overall_topics[f"topic_{topic_idx+1}"] = top_words
    
    # Perform topic modeling per source
    source_topics = {}
    for source, texts in source_texts.items():
        if len(texts) < 2:  # Skip sources with too few documents
            continue
            
        try:
            source_tfidf = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            source_lda = LatentDirichletAllocation(
                n_components=min(num_topics, len(texts)), 
                random_state=42
            )
            source_lda.fit(source_tfidf)
            
            source_topic_list = {}
            for topic_idx, topic in enumerate(source_lda.components_):
                top_words_idx = topic.argsort()[:-num_words-1:-1]
                top_words = [feature_names[i] for i in top_words_idx]
                source_topic_list[f"topic_{topic_idx+1}"] = top_words
                
            source_topics[source] = source_topic_list
        except Exception as e:
            logger.warning(f"Error in topic modeling for source {source}: {str(e)}")
    
    return {
        "overall_topics": overall_topics,
        "source_topics": source_topics
    }

def analyze_text_data():
    """Main function to analyze all text data."""
    logger.info("Starting text analysis")
    
    # Load all scraped data
    all_data = load_raw_data()
    logger.info(f"Loaded data from {len(all_data)} sources")
    
    # Extract text content for analysis
    text_content = extract_text_content(all_data)
    logger.info(f"Extracted {len(text_content)} text items for analysis")
    
    # Preprocess text
    preprocessed_texts = preprocess_text(text_content)
    logger.info(f"Preprocessed {len(preprocessed_texts)} text items")
    
    # Extract key terms
    key_terms = extract_key_terms(preprocessed_texts)
    logger.info(f"Extracted key terms for {len(key_terms['source_top_terms'])} sources")
    
    # Perform topic modeling
    topics = topic_modeling(preprocessed_texts)
    logger.info(f"Generated topics for {len(topics['source_topics'])} sources")
    
    # Save results
    analysis_results = {
        "key_terms": key_terms,
        "topics": topics
    }
    
    output_path = Path("data/processed/text_analysis_results.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(analysis_results, f, ensure_ascii=False, indent=2)
    
    logger.info(f"Text analysis results saved to {output_path}")
    return analysis_results 