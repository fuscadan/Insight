'''
    simple script to scrape basic NBA game data from ESPN using the 'games' 
    module and store the data in a pandas dataframe. Exports a .csv file at
    location specified by raw_data_path.
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import pandas as pd
from Git.nba_smart_database.games import Game
import Git.scripts.id_finder as id_finder

#set the location of the raw data file to be built, using naming conventions
#from id_finder

relative_path = id_finder.relative_path
season_type_names = id_finder.season_type_names
season_type = id_finder.season_type
start_year = id_finder.start_year
end_year = id_finder.end_year

raw_data_path = relative_path + 'raw_data_{0}_{1}-{2}.csv'.format(
    season_type_names[season_type],str(start_year),str(end_year))

if __name__ == '__main__':

    #give the file path of the text file containing the list of espn game ids.
    id_file_path = id_finder.id_file_path
    
    #read the game ids from the text file, and add raw game data row by row
    #into the dataframe df

    df = pd.DataFrame()

    with open(id_file_path , 'r') as id_file:
        id_list = id_file.readlines()

    for game_id in id_list:
        #a few game pages have variations in the standard html structure that 
        #will not be parsed correctly by the BeautifulSoup code in the Game class.
        #A simple try catch handles these exceptions.
        try:
            game = Game(game_id)
            
            new_row = pd.DataFrame(game.to_dict() , index=[game_id])
            
            df = df.append(new_row)
        except:
            print('missing data at game id ' + game_id)
    
    #export the dataframe containing raw game data to a csv file
    df.to_csv(raw_data_path)