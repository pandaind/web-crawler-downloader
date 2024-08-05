#!/bin/bash


# Prompt for the keywords
read -p "Enter keywords (space-separated): " keywords

# Prompt for the folder to save
read -p "Enter the folder location to save (default is '$keywords'): " download_tag
download_tag=${download_tag:$keywords}

# Prompt for the maximum depth
read -p "Enter the maximum depth (default is 2): " max_depth

# Set default value for max_depth if not provided
max_depth=${max_depth:-2}


# Prompt for the HTML tag and attribute used to find video sources
read -p "Enter the HTML tag and attribute used to find video sources (format: tag:attribute, default is 'source:src'): " download_tag
download_tag=${download_tag:-source:src}

# Prompt for the HTML tag and attribute used to find links to explore
read -p "Enter the HTML tag and attribute used to find links to explore (format: tag:attribute, default is 'a:href'): " explore_tag
explore_tag=${explore_tag:-a:href}


# Run the Python script with the provided inputs
python crawler.py "https://deephot.link/?s=$keywords" "$keywords" $keywords --max_depth "$max_depth"  --download_tag "$download_tag" --explore_tag "$explore_tag"

