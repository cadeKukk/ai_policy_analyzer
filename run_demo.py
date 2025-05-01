#!/usr/bin/env python3
"""
Demo script for AI Policy Analyzer.
This script sets up sample data and starts the web interface.
"""

import os
import json
import logging
import sys
from pathlib import Path

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("ai_policy_analyzer_demo")

def setup_sample_data():
    """Create sample data files for demonstration purposes."""
    logger.info("Setting up sample data...")
    
    # Create required directories
    for dir_path in ["data/raw/naiia", "data/raw/nist_ai", "data/processed"]:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create sample NAIIA data
    naiia_data = {
        "source_id": "naiia",
        "source_name": "National Artificial Intelligence Initiative Act",
        "source_url": "https://www.ai.gov/naiia/",
        "scrape_timestamp": "2023-05-01T12:00:00",
        "overview": {
            "title": "National Artificial Intelligence Initiative Act of 2020",
            "description": "The National Artificial Intelligence Initiative Act of 2020 (NAIIA) establishes a coordinated program across the federal government to accelerate AI research and application for the nation's economic prosperity and national security. Enacted as part of the National Defense Authorization Act for Fiscal Year 2021, the NAIIA creates a framework for expanding AI innovation while addressing critical challenges like AI ethics, bias, and workforce impacts."
        },
        "sections": [
            {
                "title": "Title I: National Artificial Intelligence Initiative",
                "content": "Establishes the National AI Initiative to support and coordinate federal activities in AI research and development, education, and workforce training. Creates the National AI Initiative Office within the White House Office of Science and Technology Policy to coordinate implementation."
            },
            {
                "title": "Title II: National AI Research Institutes",
                "content": "Directs the National Science Foundation to establish a program of AI research institutes focused on economic development, health care, education, manufacturing, agriculture, sustainability, and national security. These institutes will conduct research, develop infrastructure, and support education and workforce development."
            },
            {
                "title": "Title III: National Institute of Standards and Technology AI Activities",
                "content": "Directs NIST to support development of technical standards for reliable, robust, trustworthy, secure, portable, and interoperable AI systems, and to develop metrics to measure AI systems' accuracy, privacy protection, and security."
            }
        ],
        "key_provisions": [
            "Establishes the National AI Initiative to coordinate federal AI R&D activities",
            "Creates the National AI Initiative Office within the White House OSTP",
            "Establishes an advisory committee with representatives from industry, academia, and civil society",
            "Directs the NSF to establish a network of AI research institutes",
            "Requires NIST to develop AI standards and metrics",
            "Creates an AI education and workforce development program"
        ]
    }
    
    # Create sample NIST AI data
    nist_data = {
        "source_id": "nist_ai",
        "source_name": "NIST AI Risk Management Framework",
        "source_url": "https://www.nist.gov/itl/ai-risk-management-framework",
        "scrape_timestamp": "2023-05-01T12:00:00",
        "overview": {
            "title": "Artificial Intelligence Risk Management Framework",
            "description": "The AI Risk Management Framework (AI RMF) is intended to improve the ability to incorporate trustworthiness considerations into the design, development, use, and evaluation of AI products, services, and systems. The AI RMF provides a structure that enables a better understanding of the risks of AI systems while enabling AI innovation."
        },
        "core_framework": {
            "functions": [
                {
                    "name": "Govern",
                    "description": "Cultivate a culture of risk management across the organization and develop processes to support and sustain trustworthy AI systems."
                },
                {
                    "name": "Map",
                    "description": "Contextualize risks related to specific AI systems in wider sociotechnical contexts, identifying system features and risks."
                },
                {
                    "name": "Measure",
                    "description": "Analyze and quantify risk, including factors such as likelihood, magnitude, nature of harm, and expected impacts."
                },
                {
                    "name": "Manage",
                    "description": "Allocate resources to address risks, prioritizing actions based on the organization's risk tolerance."
                }
            ]
        },
        "resources": [
            {
                "title": "AI RMF 1.0",
                "url": "https://www.nist.gov/itl/ai-risk-management-framework/ai-rmf-10",
                "type": "Document"
            },
            {
                "title": "AI RMF Playbook",
                "url": "https://www.nist.gov/itl/ai-risk-management-framework/ai-rmf-playbook",
                "type": "Guide"
            }
        ]
    }
    
    # Write sample data to files
    with open("data/raw/naiia/naiia_combined.json", "w", encoding="utf-8") as f:
        json.dump(naiia_data, f, indent=2)
    
    with open("data/raw/nist_ai/nist_ai_combined.json", "w", encoding="utf-8") as f:
        json.dump(nist_data, f, indent=2)
    
    # Create sample text analysis results
    text_analysis = {
        "key_terms": {
            "overall_top_terms": [
                ["artificial", 156],
                ["intelligence", 142],
                ["risk", 78],
                ["framework", 65],
                ["system", 58],
                ["development", 52],
                ["research", 48],
                ["national", 45],
                ["initiative", 42],
                ["trustworthy", 38]
            ],
            "source_top_terms": {
                "naiia": [
                    ["initiative", 32],
                    ["national", 30],
                    ["research", 28],
                    ["artificial", 26],
                    ["intelligence", 26]
                ],
                "nist_ai": [
                    ["risk", 42],
                    ["framework", 38],
                    ["artificial", 25],
                    ["intelligence", 25],
                    ["management", 22]
                ]
            }
        },
        "topics": {
            "overall_topics": {
                "topic_1": ["initiative", "national", "artificial", "intelligence", "research"],
                "topic_2": ["risk", "framework", "management", "trustworthy", "evaluation"],
                "topic_3": ["development", "education", "workforce", "training", "skills"]
            },
            "source_topics": {
                "naiia": {
                    "topic_1": ["initiative", "national", "artificial", "intelligence", "research"],
                    "topic_2": ["education", "workforce", "development", "training", "skills"]
                },
                "nist_ai": {
                    "topic_1": ["risk", "framework", "management", "ai", "systems"],
                    "topic_2": ["trustworthy", "evaluation", "measure", "governance", "map"]
                }
            }
        }
    }
    
    # Create sample comparative analysis results
    comparative_analysis = {
        "similarity_matrix": {
            "naiia": {
                "naiia": 1.0,
                "nist_ai": 0.45
            },
            "nist_ai": {
                "naiia": 0.45,
                "nist_ai": 1.0
            }
        },
        "policy_themes": {
            "overall_topics": {
                "topic_1": ["initiative", "national", "artificial", "intelligence", "research"],
                "topic_2": ["risk", "framework", "management", "trustworthy", "evaluation"]
            },
            "shared_themes": {
                "artificial-intelligence-systems": ["naiia", "nist_ai"]
            }
        },
        "policy_focus": {
            "focus_data": {
                "naiia": {
                    "initiative": 32,
                    "national": 30,
                    "research": 28,
                    "artificial": 26,
                    "intelligence": 26
                },
                "nist_ai": {
                    "risk": 42,
                    "framework": 38,
                    "artificial": 25,
                    "intelligence": 25,
                    "management": 22
                }
            },
            "distinctive_terms": {
                "naiia": [
                    ["initiative", 32],
                    ["national", 30],
                    ["research", 28]
                ],
                "nist_ai": [
                    ["risk", 42],
                    ["framework", 38],
                    ["management", 22]
                ]
            }
        }
    }
    
    # Create sample network analysis results
    network_analysis = {
        "citations": [
            {"source": "nist_ai", "target": "naiia"}
        ],
        "similarities": [
            {"source1": "naiia", "source2": "nist_ai", "similarity": 0.45}
        ],
        "clusters": [
            {
                "id": 0,
                "name": "US Government AI Policies",
                "sources": ["naiia", "nist_ai"],
                "avg_similarity": 0.45
            }
        ]
    }
    
    # Write sample analysis results to files
    with open("data/processed/text_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(text_analysis, f, indent=2)
    
    with open("data/processed/comparative_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(comparative_analysis, f, indent=2)
    
    with open("data/processed/network_analysis_results.json", "w", encoding="utf-8") as f:
        json.dump(network_analysis, f, indent=2)
    
    logger.info("Sample data setup complete!")

def start_web_interface():
    """Start the Flask web interface."""
    logger.info("Starting web interface...")
    
    # Import the Flask app from the frontend module
    try:
        from frontend import app
        app.run(debug=True, host='0.0.0.0', port=5000)
    except ImportError as e:
        logger.error(f"Error importing Flask app: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error starting web interface: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Setup sample data
    setup_sample_data()
    
    # Start the web interface
    start_web_interface() 