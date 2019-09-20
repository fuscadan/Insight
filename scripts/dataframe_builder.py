'''
    simple script to scrape basic NBA game data from ESPN using the 'games' 
    module and store the data in a pandas dataframe. Exports a .csv file at
    location specified by RAW_DATA_PATH.
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import pandas as pd
from Git.nba_smart_database.games import Game
import Git.scripts.id_finder as id_finder

# set the location of the raw data file to be built, using naming conventions
# from id_finder
RELATIVE_PATH = id_finder.RELATIVE_PATH
ID_FILE_PATH = id_finder.ID_FILE_PATH
SEASON_TYPE_NAMES = id_finder.SEASON_TYPE_NAMES
SEASON_TYPE = id_finder.SEASON_TYPE
START_YEAR = id_finder.START_YEAR
END_YEAR = id_finder.END_YEAR

RAW_DATA_PATH = (RELATIVE_PATH 
    + 'raw/' 
    + 'raw_data_{0}_{1}-{2}.csv'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

if __name__ == '__main__':
    # read the game ids from the text file, and add raw game data row by row
    # into the dataframe df.  Write the dataframe containing raw game data to a 
    # csv file.
    df = pd.DataFrame()

    with open(ID_FILE_PATH , 'r') as id_file:
        id_list = id_file.readlines()

    for game_id in id_list:
        # a few game pages have variations in the standard html structure that 
        # will not be parsed correctly by the BeautifulSoup code in the Game 
        # class.  A simple try catch handles these exceptions.
        try:
            game = Game(game_id)
            new_row = pd.DataFrame(game.to_dict() , index=[game_id])
            df = df.append(new_row)
        except:
            print('missing data at game id ' + game_id)
    
    df.to_csv(RAW_DATA_PATH)