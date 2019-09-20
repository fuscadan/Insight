'''
    Created on Wed September  18 2019

    @author danie

    Definition of features that a string (typically a paragraph in a game 
    recap) may have. Used to construct feature vectors.
'''

import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')

from Git.nba_smart_database.games import Game
import Git.scripts.dataframe_builder as dataframe_builder

raw_data_path = dataframe_builder.raw_data_path


def n_numbers(paragraph):
    # Count the number of numbers (word or digits) appearing in paragraph
    number_words = ['one','two','three','four','five','six','seven','eight','nine']
    n_num = len([s for s in paragraph.split() if s.isdigit() or s in number_words])

    # count the number of strings of the form "125-536" (game scores)
    possible_scores = [s for s in paragraph.split() if '-' in s]
    n_scores = len([s for s in possible_scores if 2 == len([i for i in s.split('-') if i.isdigit()])])
    
    return n_num + n_scores


def n_names(paragraph):
    names_path = '/mnt/c/Users/danie/OneDrive/Documents/Insight/Git/data/raw/nba_player_names.txt'

    with open(names_path,'r') as names_file:
        names = names_file.read().split('\n')
    
    return len([s for s in paragraph.split() if s in names])


def n_teams(paragraph):
    teams_path = '/mnt/c/Users/danie/OneDrive/Documents/Insight/Git/data/raw/nba_team_names.txt'

    with open(teams_path,'r') as teams_file:
        teams = teams_file.read().split('\n')
    
    return len([s for s in paragraph.split() if s in teams])


def n_sentences(paragraph):
    return len(paragraph.split('.')) - 1


if __name__ == "__main__":
    game_id = 400899380

    game = Game(game_id,df_path=raw_data_path)

    paragraph_number = 4
    paragraph = game.article[paragraph_number]

    n_numbers(paragraph)

    print('For game with id {0}, paragraph {1} has {2} numbers, {3} player names, and {4} team names'.format(str(game_id), 
            str(paragraph_number),
            str(n_numbers(paragraph)),
            str(n_names(paragraph)),
            str(n_teams(paragraph)),))
