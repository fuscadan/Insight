'''
    Created on Tue September  24 2019

    @author danie

    construct feature vectors for historic NBA games. Vectors will be used in 
    the final search algorithm.
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

from Git.nba_smart_database.games import Game
from  Git.scripts.LSA_model import LemmaTokenizer
import Git.nba_smart_database.features as ft
import Git.scripts.dataframe_builder as dataframe_builder
import Git.scripts.LSA_model as LSA_model
import Git.scripts.id_finder as id_finder

# set all paths to relevant files
RAW_DATA_PATH = dataframe_builder.RAW_DATA_PATH
LSA_MODEL_PATH = LSA_model.LSA_MODEL_PATH
RELATIVE_PATH = id_finder.RELATIVE_PATH
SEASON_TYPE_NAMES = id_finder.SEASON_TYPE_NAMES
SEASON_TYPE = id_finder.SEASON_TYPE
START_YEAR = id_finder.START_YEAR
END_YEAR = id_finder.END_YEAR
FEATURES_PATH = (RELATIVE_PATH 
    + 'processed/'
    + 'game_features_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
ART_NAMES_PATH = (RELATIVE_PATH 
    + 'processed/'
    + 'article_names_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
TEAMS_PATH = (RELATIVE_PATH 
    + 'processed/'
    + 'teams_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )
LEADERS_PATH = (RELATIVE_PATH 
    + 'processed/'
    + 'leaders_{0}_{1}-{2}.pickle'.format(
        SEASON_TYPE_NAMES[SEASON_TYPE],
        str(START_YEAR),
        str(END_YEAR)
        )
    )

# objects related to cleaning punctuation from text
PUNCTUATION = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~'
translator = str.maketrans('', '', PUNCTUATION)


if __name__ == "__main__":
    # create and save the following dataframes (pickle).  Below is a
    # description of the information stored in each row of the corresponding
    # dataframe.
    # df_features - LSA vector of game article + basic game info
    # df_teams - BOW vector of team names involved in a game
    # df_leaders - BOW vector of player names in the 'game leaders' box
    # df_article_names - BOW vector of player names in a game article

    # load raw data and the LSA model
    raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
    ID_LIST = raw_data.index
    LSA = joblib.load(LSA_MODEL_PATH)

    # build the basic game info dataframe
    df_features = pd.DataFrame()
    for game_id in ID_LIST:
        game = Game(game_id, df=raw_data)

        # concatenate article paragraphs into a single string and clean it
        full_article = ''
        for paragraph in game.article:
            full_article = full_article + paragraph + '\n'
        full_article = full_article.translate(translator)

        # build a dictionary of features
        feature_dict = {}
        feature_dict['LSA'] = [LSA.transform([full_article])]
        feature_dict['scores'] = [[game.scores['away'][0], 
                                    game.scores['home'][0]]]
        feature_dict['pts'] = [[game.pts['away']['pts'], 
                                    game.pts['home']['pts']]]

        new_row = pd.DataFrame(feature_dict, index = [game_id])
        df_features = df_features.append(new_row)

    df_features.to_pickle(FEATURES_PATH)

    teams = []
    for game_id in ID_LIST:
        game = Game(game_id, df=raw_data)

        teams_str = (game.names['away']['team'] + ' '
                    + game.names['away']['city'] + ' '
                    + game.names['away']['abbr'] + ' '
                    + game.names['home']['team'] + ' '
                    + game.names['home']['city'] + ' '
                    + game.names['home']['abbr'])

        teams.append(ft.get_teams(teams_str)[1])

    teams_array = sparse.vstack(teams)

    df_teams = pd.DataFrame.sparse.from_spmatrix(teams_array, 
        index=ID_LIST)

    df_teams.to_pickle(TEAMS_PATH)


    leaders = []

    for game_id in ID_LIST:
        game = Game(game_id, df=raw_data)

        players_str = (game.pts['away']['leader'] + ' '
                    + game.pts['home']['leader'] + ' '
                    + game.ast['away']['leader'] + ' '
                    + game.ast['home']['leader'] + ' '
                    + game.reb['away']['leader'] + ' '
                    + game.reb['home']['leader'])

        leaders.append(ft.get_names(players_str)[1])

    leaders_array = sparse.vstack(leaders)

    df_leaders = pd.DataFrame.sparse.from_spmatrix(leaders_array, 
        index=ID_LIST)

    df_leaders.to_pickle(LEADERS_PATH)


    article_names = []

    for game_id in ID_LIST:
        game = Game(game_id, df=raw_data)
        full_article = ''
        for paragraph in game.article:
            full_article = full_article + paragraph + '\n'
        full_article = full_article.translate(translator)

        article_names.append(ft.get_names(full_article)[1])

    art_names_array = sparse.vstack(article_names)

    df_article_names = pd.DataFrame.sparse.from_spmatrix(art_names_array, 
        index=ID_LIST)

    df_article_names.to_pickle(ART_NAMES_PATH)


