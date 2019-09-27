'''
    Created on Wed September  18 2019

    @author danie

    Definition of features that a string (typically a paragraph in a game 
    recap) may have. Used to construct feature vectors.
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

from sklearn.feature_extraction.text import CountVectorizer

from Git.nba_smart_database.games import Game
import Git.scripts.dataframe_builder as dataframe_builder

RAW_DATA_PATH = dataframe_builder.RAW_DATA_PATH
NAMES_PATH = ('/mnt/c/Users/danie/OneDrive/Documents/Insight/Git/data/raw/'
    + 'nba_player_names.txt')
TEAMS_PATH = ('/mnt/c/Users/danie/OneDrive/Documents/Insight/Git/data/raw/'
    + 'nba_team_names.txt')

with open(NAMES_PATH,'r') as names_file:
    names = names_file.read().split('\n')
with open(TEAMS_PATH,'r') as teams_file:
    teams = teams_file.read().split('\n')

names_vectorizer = CountVectorizer()
names_bow = names_vectorizer.fit(names) 
teams_vectorizer = CountVectorizer()
teams_bow = teams_vectorizer.fit(teams)

def n_numbers(paragraph):
    # Count the number of numbers (word or digits) appearing in paragraph
    number_words = ['one','two','three','four',
        'five','six','seven','eight','nine']
    n_num = len([s for s in paragraph.split() 
                    if s.isdigit() or s in number_words])

    # count the number of strings of the form "125-536" (game scores)
    possible_scores = [s for s in paragraph.split() if '-' in s]
    n_scores = len([s for s in possible_scores 
                    if 2 == len([i for i in s.split('-') if i.isdigit()])])
    
    return n_num + n_scores

def n_names(paragraph):   
    return len([s for s in paragraph.split() if s in names])

def n_teams(paragraph):   
    return len([s for s in paragraph.split() if s in teams])

def n_sentences(paragraph):
    return len(paragraph.split('.')) - 1

def get_names(paragraph):
    names_list = [s for s in paragraph.split() if s in names]
    names_tokens = names_bow.transform([paragraph])
    return names_list, names_tokens

def get_teams(paragraph):
    teams_list = [s for s in paragraph.split() if s in teams]
    teams_tokens = teams_bow.transform([paragraph])
    return teams_list, teams_tokens

def has_pts(paragraph):
    for s in ['point', 'points', 'pt', 'pts']: 
        if s in paragraph.lower().split():
            return True
    return False

def has_reb(paragraph):
    for s in ['rebound', 'rebounds', 'reb']: 
        if s in paragraph.lower().split():
            return True
    return False

def has_ast(paragraph):
    for s in ['assist', 'assists', 'ast']: 
        if s in paragraph.lower().split():
            return True
    return False

def get_numbers(paragraph):
    numbers = [int(s) for s in paragraph.split() if s.isdigit()]
    return numbers
    

if __name__ == "__main__":
    game_id = 400899380

    game = Game(game_id,df_path=RAW_DATA_PATH)

    paragraph_number = 4
    paragraph = game.article[paragraph_number]

    n_numbers(paragraph)

    print('For game with id {0}, paragraph {1} has {2} numbers, \
            {3} player names, and {4} team names'.format(str(game_id), 
            str(paragraph_number),
            str(n_numbers(paragraph)),
            str(n_names(paragraph)),
            str(n_teams(paragraph)),))
