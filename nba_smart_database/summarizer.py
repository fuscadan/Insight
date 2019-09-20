'''
    Created on Thur September  18 2019

    @author danie

    Predict the most important sentence from a given game recap article.
'''
import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import joblib
import argparse
from Git.nba_smart_database import features as ft
from Git.nba_smart_database.games import Game
from Git.nba_smart_database import tree_model
# from Git.nba_smart_database import svm_model
# import dataframe_builder
# import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-id', '--game_id', type=int,
                        help='input a valid ESPN game ID for a game you wish to generate a headline for. If no ID specified, the program runs with a hard-coded ID.')
args = parser.parse_args()

if args.game_id == None:
    game_id = 400827911
else:
    game_id = args.game_id

# game_id = 400827911
# game_id = 400899380

new_game = Game(game_id)

model_path = '/mnt/c/Users/danie/OneDrive/Documents/Insight/Git/nba_smart_database/tree_model_balanced.joblib'
# model_path = tree_model.model_path
# model_path = svm_model.model_path

model = joblib.load(model_path)

candidates = []

print('\n Most descriptive paragraph for game with ID {0}: \n'.format(str(game_id)))

for paragraph in new_game.article:
    X = [[ft.n_names(paragraph),
            ft.n_teams(paragraph),
            ft.n_numbers(paragraph),
            ft.n_sentences(paragraph)]]

    if model.predict(X) == 1:
        candidates.append(paragraph)

print(candidates[0] + '\n')



