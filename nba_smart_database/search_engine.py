'''
    Created on Wed September  25 2019

    @author danie

    Takes a query and searches the database of NBA games
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import joblib
import pandas as pd
import numpy as np
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
from scipy import sparse
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from Git.nba_smart_database.summarizer_backend import summarize
from Git.nba_smart_database.games import Game
from  Git.scripts.LSA_model import LemmaTokenizer
import Git.nba_smart_database.features as ft
import Git.scripts.dataframe_builder as dataframe_builder
import Git.scripts.LSA_model as LSA_model
import Git.scripts.id_finder as id_finder
import Git.scripts.search_preprocessing as preprocessing

# set paths to relevant models and pickled dataframes
RAW_DATA_PATH = dataframe_builder.RAW_DATA_PATH
LSA_MODEL_PATH = LSA_model.LSA_MODEL_PATH
FEATURES_PATH = preprocessing.FEATURES_PATH
ART_NAMES_PATH = preprocessing.ART_NAMES_PATH
TEAMS_PATH = preprocessing.TEAMS_PATH
LEADERS_PATH = preprocessing.LEADERS_PATH

# load the LSA model and dataframes

PUNCTUATION = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~'
translator = str.maketrans('', '', PUNCTUATION)
LSA = joblib.load(LSA_MODEL_PATH)

df_features = pd.read_pickle(FEATURES_PATH)
df_teams = pd.read_pickle(TEAMS_PATH)
df_players = pd.read_pickle(LEADERS_PATH)

raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
ID_LIST = raw_data.index

def search(query):
    global df_players
    # parse the query string
    q_teams = ft.get_teams(query)[1]
    q_players = ft.get_names(query)[1]
    q_LSA = LSA.transform([query])
    q_numbers = ft.get_numbers(query)

    # begin with a list of IDs to search that contains every game
    id_search_list = ID_LIST

    # reduce the search, if possible, to games with teams mentioned in the query
    db_teams = sparse.csr_matrix(df_teams.values)
    similarities = cosine_similarity(q_teams, db_teams)

    # TODO take the IDs that give the maximum similarity

    reduced_list = [id_search_list[i] for i in similarities.nonzero()[1]]

    # if the list can be reduced, reduce it and take the appropriate sub-dataframe
    # of df_players
    if len(reduced_list) != 0:
        id_search_list = reduced_list
        df_players = df_players.loc[id_search_list].fillna(0).astype(int)

    # reduce the search, if possible, to games with players mentioned in the query
    db_players = sparse.csr_matrix(df_players.values) 
    similarities = cosine_similarity(q_players, db_players)

    # TODO take the IDs that give the max similarity

    reduced_list = [id_search_list[i] for i in similarities.nonzero()[1]]

    if len(reduced_list) != 0:
        id_search_list = reduced_list


    # reduce the search, if possible, to games with numbers mentioned in the query
    reduced_list = []
    for game_id in id_search_list:
        if len([n for n in q_numbers if n in df_features.loc[game_id]['pts']]) > 0:
            reduced_list.append(game_id)

    if len(reduced_list) != 0:
        id_search_list = reduced_list

    # finally apply LSA context-matching between the query and the games in the
    # reduced list

    LSA_similarities = np.array([cosine_similarity(q_LSA, 
        df_features.loc[game_id]['LSA'])[0][0]
        for game_id in id_search_list])

    top_game_ids = [id_search_list[i] for i in np.argsort(LSA_similarities)[-3:]]
    top_game_ids.reverse()

    results = [(Game(game_id, df=raw_data).headline,summarize(game_id,raw_data)) 
                    for game_id in top_game_ids]

    return results

if __name__ == "__main__":
    
    query = 'jalen career best'
    results = search(query)

    print('\n')
    for result in results:
        print(result[0] + '\n\n' + result[1] + '\n')