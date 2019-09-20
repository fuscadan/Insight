'''
    Created on Wed September  18 2019

    @author danie

        script to take a given game recap and label each paragraph (which I 
        think on ESPN are usually 1 sentence long) and label it as either 
        similar or dissimilar to the one-sentence descriptor appearing on the
        game summary page.
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import pandas as pd
import numpy as np

from Git.nba_smart_database import features as ft
from Git.nba_smart_database.games import Game
import Git.scripts.dataframe_builder as dataframe_builder
import Git.scripts.labelling as labelling
import Git.scripts.id_finder as id_finder

raw_data_path = dataframe_builder.raw_data_path
labelled_data_path = labelling.labelled_data_path
relative_path = id_finder.relative_path
season_type_names = id_finder.season_type_names
season_type = id_finder.season_type
start_year = id_finder.start_year
end_year = id_finder.end_year

# path to the outputted data file; feature vectors X and labels y
Xy_data_path = relative_path + 'processed/' + \
    'Xy_data_{0}_{1}-{2}.csv'.format(season_type_names[season_type],str(start_year),str(end_year))

raw_data = pd.read_csv(raw_data_path, index_col = 0)
labels = pd.read_csv(labelled_data_path, index_col= 0)

id_list = labels.index

if __name__ == "__main__":
        
    X = []
    y = []

    for game_id in id_list:

        game = Game(game_id, df_path=raw_data_path)

        paragr_lbls = labels.loc[game_id].dropna()

        for i in range(len(paragr_lbls)):

            if paragr_lbls[i] == 1:
                paragraph = game.article[i]

                feature_list = [ft.n_names(paragraph),ft.n_teams(paragraph),ft.n_numbers(paragraph)]

                X.append(feature_list)
                y.append(paragr_lbls[i])
            else:
                
    
    Xy_df = pd.DataFrame([X,y]).transpose()

    Xy_df.to_csv(Xy_data_path)

# need to refactor the function that assigns a feature vector to a given 
# paragraph




