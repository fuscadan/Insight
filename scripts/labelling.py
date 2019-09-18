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


#set file paths for the raw input and labelled output files
raw_data_path = dataframe_builder.raw_data_path
labelled_data_path = raw_data_path.replace('raw','labelled')


raw_data = pd.read_csv(raw_data_path, index_col = 0)
id_list = raw_data.index

game_id = 400899380

game = Game(game_id, df_path=raw_data_path)

sentences = [game.summary] + game.article

vectorizer = CountVectorizer()
vectorized_list = vectorizer.fit_transform(sentences)

paragraph_tags = []
for i in range(len(game.article)):
    if cosine_similarity(vectorized_list[i+1],vectorized_list[0])[0][0] > 0.75:
        paragraph_tags.append(1)
    else:
        paragraph_tags.append(0)


