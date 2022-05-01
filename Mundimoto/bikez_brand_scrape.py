from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import numpy as np
import collections


# Input page link
link = 'https://bikez.com/brands/index.php'

# Request HTML for the link
html_text = requests.get(link).text
soup = BeautifulSoup(html_text)
# Parse link HTML
brands_table = soup.find('table', {'class': 'zebra', 'style': 'width:100%'})
bike_brands = brands_table.findAll('a', href=True)

# extracting brands from html
bikez_brands = []
for i in bike_brands:
    bikez_brands.append(i.text.replace(" motorcycles", " "))

# output to csv as dataframe
bikez_brands_df = pd.DataFrame(bikez_brands, columns=['Brand'])
bikez_brands_df.to_csv('landing/persistent/bikez_scrape/bikez_brands.csv', index=False)


    
