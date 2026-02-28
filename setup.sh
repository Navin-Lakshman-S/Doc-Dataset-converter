#!/bin/bash

# Setup and run script

echo "================================================"
echo "  Document to Dataset Converter - Setup"
echo "================================================"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "${GREEN}Found: $python_version${NC}"
echo ""

# Check if requirements.txt exists
if [ ! -f "requirements.txt" ]; then
    echo "${RED}Error: requirements.txt not found${NC}"
    exit 1
fi

# Ask user if they want to create a virtual environment
echo "Setup Options:"
echo "1. Install in virtual environment (Recommended)"
echo "2. Install globally"
read -p "Choose option (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo ""
    echo "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
    
    echo "${YELLOW}Activating virtual environment...${NC}"
    source venv/bin/activate
    
    echo "${GREEN}Virtual environment activated${NC}"
    echo ""
fi

# Install dependencies
echo "${YELLOW}Installing dependencies...${NC}"
echo "This may take a few minutes..."
echo ""

pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "${GREEN}All dependencies installed.${NC}"
else
    echo ""
    echo "${RED}Error installing dependencies.${NC}"
    exit 1
fi

# Create output directory
echo ""
echo "${YELLOW}Creating output directory...${NC}"
mkdir -p output
echo "${GREEN}Done.${NC}"

echo ""
echo "================================================"
echo "  Setup Complete"
echo "================================================"
echo ""
echo "To run the application:"
echo ""
if [ "$choice" = "1" ]; then
    echo "  ${GREEN}source venv/bin/activate${NC}  (if not already activated)"
fi
echo "  ${GREEN}python app.py${NC}"
echo ""
echo "Then open your browser to: ${YELLOW}http://localhost:7860${NC}"
echo ""
echo "================================================"
