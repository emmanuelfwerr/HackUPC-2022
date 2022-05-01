from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import collections
from CustomTools import get_urls, get_strain_data


def main():
    '''
    Orchestrator
    '''
    # Input page link
    #page = 'https://bikez.com/years/index.php'
    page = 'https://bikez.com/year/2022-motorcycle-models.php'

    #
    df_allbikes = pd.DataFrame()

    #
    bike_links = get_urls(page)
    df_bikes_perpage = get_bikes_data(bike_links)
    df_allbikes = df_allbikes.append(df_bikes_perpage, ignore_index=True)

    #
    df_allbikes.to_csv('y2022_bike_data.csv', index=False)

if __name__ == "__main__":
    main()