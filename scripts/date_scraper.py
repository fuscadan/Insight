'''
    Created on Thur September  25 2019

    @author danie

    Script to scrape dates of NBA games and store them in a dataframe
'''
import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import pandas as pd
import urllib3
import certifi
from bs4 import BeautifulSoup
import Git.scripts.id_finder as id_finder

# decide if the script should run in 'retry' mode

RETRYING = False

# set file paths
ID_FILE_PATH = id_finder.ID_FILE_PATH
RELATIVE_PATH = id_finder.RELATIVE_PATH
ERROR_FILE_PATH = RELATIVE_PATH + 'raw/date_error_ids'
SEASON_TYPE_NAMES = id_finder.SEASON_TYPE_NAMES
SEASON_TYPE = id_finder.SEASON_TYPE
START_YEAR = id_finder.START_YEAR
END_YEAR = id_finder.END_YEAR
DATE_DATA_PATH = (RELATIVE_PATH 
    + 'raw/' 
    + 'dates_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

GAME_ARTICLE_ROOT = 'https://www.espn.com/nba/game?gameId='

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())

def date_scrape(id_list):
    for game_id in id_list:
        url = GAME_ARTICLE_ROOT + str(game_id)
        r = http.request('GET' , url)
        soup = BeautifulSoup(r.data, 'html.parser')

        soup.find_all("a", attrs={"class": "sister"})


    return df, errors


if __name__ == "__main__":

    # connect to espn

    if RETRYING == True:
        file_path = ERROR_FILE_PATH
    else:
        file_path = ID_FILE_PATH

    with open(file_path, 'r') as id_file:
        id_list = id_file.readlines()

    df, errors = date_scrape(id_list)
    



