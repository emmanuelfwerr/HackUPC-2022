from bs4 import BeautifulSoup, Comment
import requests
import pandas as pd
import numpy as np
import collections
import sys


def get_urls(link):
    '''
    Requests html from parent website and extracts all useable urls. 
    Args:
        (str) link - parent link.
    Returns:
        (obj) bike_links - list of links for motorcycles and their specifications.
    '''
    html_text = requests.get(link).text
    soup = BeautifulSoup(html_text, features="html.parser")
    page_bikes = soup.find('table', {'class': 'zebra'})

    # Extract urls from Soup and append to url_extensions[]
    url_extensions = []
    counter = 0
    for i in page_bikes.findAll('a', href=True):
        url_extensions.append(i['href'])


    # Create list of
    parent_link = 'https://bikez.com'
    bike_links = []
    for i in url_extensions:
        bike_links.append(parent_link + '{}'.format(i[2:]))

    return bike_links


def verify_urls(links_list):
    '''
    Iterates through list of scraped links and removes duplicates and other unwanted links. 
    Args:
        (obj) links_list - list of extracted links.
    Returns:
        (obj) verified_links - verified list of links.
    '''
    verified_links = set()
    for i in links_list:
        if 'models.php' not in i:
            verified_links.add(i)
            
    return verified_links


def get_bike_data(bike_links):
    '''
    Accesses each bike link and collects individual bike specifications data.
    Args:
        (obj) bike_links - list of verified links for motorcycles and their specifications.
    Returns:
        (obj) bikez_info_df - DataFrame containing extracted data for all available motorcycles of the same year
    '''
    bikez_info = []
    loop_counter = 1
    for link in bike_links:
        # Progress tracker (debugging)
        print(loop_counter, link)
        loop_counter += 1

        # Request HTML for each link
        html_text = requests.get(link).text
        soup = BeautifulSoup(html_text, features="html.parser")
        # Parse link HTML
        bike_specs = soup.findAll('td', {'style': ['vertical-align:top;width:25%;', 'vertical-align:top;']})
        
        # fill dictionary with bike_specifications_data
        bike_spec_dict = {}
        iter = 0
        for i in bike_specs:
            if (iter % 2) == 0:
                bike_spec_dict['{}'.format(i.text)] = '{}'.format(bike_specs[iter+1].text)
            iter += 1

        # Fill bikez_info[]
        bikez_info.append(bike_spec_dict)

    # Create and fill DataFrame
    bikez_info_df = pd.DataFrame(bikez_info)

    return bikez_info_df

def main():
    '''
    Orchestrator. Calls functions defined above in order. Exports dataframe containing yearly motorcycle data to temporal landing zone (path specified below).
    Args:
        (none)
    Returns:
        (.csv) y{}_bike_data.csv - .csv file containing extracted data for all available motorcycles of the same year
    '''
    # Input page link
    #page = 'https://bikez.com/years/index.php'
    print(29*'-'+'\n'+'*** Commencing Extraction ***\n'+29*'-')
    
    def createList(r1, r2):
        return list(range(r1, r2+1))
      
    # User specified list in command line
    r1, r2 = int(sys.argv[1]), int(sys.argv[2])
    
    for year in createList(r1, r2):
        # initializing extraction page
        page = 'https://bikez.com/year/{}-motorcycle-models.php'.format(year)

        # get all bike links
        bike_links = get_urls(page)
        bike_links_verified = verify_urls(bike_links)

        # length of bike_links_verified
        print('There are {} total bikes listed in the year {}:\n'.format(len(bike_links_verified), year))

        # get specifications
        df_bikez = get_bike_data(bike_links_verified)

        # export to csv
        df_bikez.to_csv('y{}_test.csv'.format(year), index=False)
        print('year {} extraction completed!\n'.format(year))
    
if __name__ == "__main__":
    main()