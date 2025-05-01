#!/bin/bash
# Startup script for AI Policy Analyzer

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== AI Policy Analyzer Startup ===${NC}"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed. Please install Python 3 to run this application.${NC}"
    exit 1
fi

# Check if virtual environment exists, if not create it
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}Error: Failed to create virtual environment.${NC}"
        exit 1
    fi
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to activate virtual environment.${NC}"
    exit 1
fi

# Install requirements if needed
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Failed to install dependencies.${NC}"
    exit 1
fi

# Run the demo
echo -e "${GREEN}Starting AI Policy Analyzer...${NC}"
echo -e "${GREEN}Once the server starts, open your web browser and go to: http://localhost:5000${NC}"
python run_demo.py

# Deactivate virtual environment on exit
deactivate 