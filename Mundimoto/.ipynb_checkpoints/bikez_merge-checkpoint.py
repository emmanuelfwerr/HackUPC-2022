import pandas as pd
import numpy as np
import json
import glob
import os

'''
This script concatenates all individual yearly files extracted by `bikez_scrape.py` and produces a unified .csv file with all the extracted motorcycle information and exports it to the persistent landing zone.
Args:
    (none)
Returns:
    (.csv) all_bikez_data.csv - .csv file containing all extracted data from bikez.com
'''

path = r'landing/temporal/bikez_scrape/' # use your path
all_files = glob.glob(path + "/*.csv")

li = []

for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    li.append(df)

df = pd.concat(li, axis=0, ignore_index=True)

df.to_csv('landing/persistent/bikez_scrape/all_bikez_data.csv', index=False)