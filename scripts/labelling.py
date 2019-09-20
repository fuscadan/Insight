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

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Git.nba_smart_database.games import Game
import Git.scripts.dataframe_builder as dataframe_builder
import Git.scripts.id_finder as id_finder


# set file paths for the raw input and labelled output files
RAW_DATA_PATH = dataframe_builder.RAW_DATA_PATH
RELATIVE_PATH = id_finder.RELATIVE_PATH
SEASON_TYPE_NAMES = id_finder.SEASON_TYPE_NAMES
SEASON_TYPE = id_finder.SEASON_TYPE
START_YEAR = id_finder.START_YEAR
END_YEAR = id_finder.END_YEAR
LABELLED_DATA_PATH = (RELATIVE_PATH 
    + 'processed/' 
    + 'labels_{0}_{1}-{2}.csv'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

# load raw game data and list of game IDs
raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
id_list = raw_data.index



if __name__ == '__main__':
    # if a given paragraph in the article is sufficiently similar to the 
    # summary, label it with 1. Otherwise, label with 0. Do this for all game 
    # articles. Store all the labels in a Dataframe. Each row is a game 
    # (indexed by game ID), and the i^th column of a row is the label (0 or 1) 
    # of the i^th paragraph of the corresponding game's recap article.
    labels = pd.DataFrame()

    for game_id in id_list:
        try:
            game = Game(game_id, df_path=RAW_DATA_PATH)
            sentences = [game.summary] + game.article

            vectorizer = CountVectorizer()
            vectorized_list = vectorizer.fit_transform(sentences)

            paragraph_tags = []
            for i in range(len(game.article)):
                if (cosine_similarity(
                        vectorized_list[i+1],
                        vectorized_list[0])[0][0] 
                        > 0.75):
                    paragraph_tags.append(1)
                else:
                    paragraph_tags.append(0)
            
            new_row = pd.DataFrame([paragraph_tags], index=[game_id])  
            labels = labels.append(new_row)
        
        except:
            print('problem at game id ' + str(game_id))

    labels.to_csv(LABELLED_DATA_PATH)

# problem at game id 400975360
# problem at game id 400975116
# problem at game id 400975127
# problem at game id 400975127
# problem at game id 400975116
# problem at game id 400975360