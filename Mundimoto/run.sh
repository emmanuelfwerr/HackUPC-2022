#! /bin/bash

BASEDIR=./

# running bikez specs web-scraper script
echo "Scraping bikez specifications..."
python bikez_scrape.py 1970 2022

# running bikez brands web-scraper script
echo "Scraping bikez brands..."
python bikez_brand_scrape.py

# merging all yearly bike specs
echo "Merging all bikez specifications CSVs..."
python bikez_merge.py

# data preprocessing and export to formatted zone
echo "Preprocessing and exporting to formatted zone"
python bikez_wrangle.py

# exploring and modelling in the exploitation zone
echo "Exploring and modelling in the exploitation zone"
