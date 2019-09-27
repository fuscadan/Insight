'''
    Created on Thur September  18 2019

    @author danie

    Predict the most important sentence from a given game recap article.
'''
import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

import joblib
from Git.nba_smart_database import features as ft
from Git.nba_smart_database.games import Game
from Git.nba_smart_database import tree_model


model_path = ('/mnt/c/Users/danie/OneDrive/Documents/Insight/Git'
    + '/nba_smart_database/tree_model_balanced.joblib')
model = joblib.load(model_path)

def summarize(game_id, raw_data):
    game = Game(game_id, df=raw_data)
    candidates = []
    
    for paragraph in game.article:
        X = [[ft.n_names(paragraph),
                ft.n_teams(paragraph),
                ft.n_numbers(paragraph),
                ft.n_sentences(paragraph)]]

        if model.predict(X) == 1:
            candidates.append(paragraph)

    return candidates[0] + '\n'



