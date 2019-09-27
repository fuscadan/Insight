'''
    Created on Tue September  24 2019

    @author danie

    Train the LSA model.  Will be called by the game article preprocessor and
    the search query preprocessor to generate a dimension-reduced feature 
    vector for the text.
'''
import sys
sys.path.insert(1, '/mnt/c/Users/danie/OneDrive/Documents/Insight/')


from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import joblib
import string
import pandas as pd
import numpy as np
import random
from datetime import datetime
from Git.nba_smart_database.games import Game
import Git.scripts.dataframe_builder as dataframe_builder


startTime = datetime.now()

# set file paths for the raw data and for the trained LSA model
RAW_DATA_PATH = dataframe_builder.RAW_DATA_PATH
LSA_MODEL_PATH = 'Git/nba_smart_database/lsa_model.joblib'

# load raw data and full list of game IDs
raw_data = pd.read_csv(RAW_DATA_PATH, index_col = 0)
FULL_ID_LIST = raw_data.index

# randomly select a fraction of IDs to train the LSA model on
TRAINING_FRACTION = 1
ID_LIST = [game_id for game_id in FULL_ID_LIST 
            if random.randint(1,TRAINING_FRACTION) == 1]

# objects used in text pre-processing; removing punctuation, stopwords, and
# lemmatizing
PUNCTUATION = '!"#$%&\'()*+,./;<=>?@[\\]^_`{|}~'
translator = str.maketrans('', '', PUNCTUATION)

stopWords = set(stopwords.words('english'))

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


if __name__ == "__main__":

    # make a list X of all game articles
    X = []
    for game_id in ID_LIST:
        game = Game(game_id, df_path=RAW_DATA_PATH)

        full_article = ''
        for paragraph in game.article:
            full_article = full_article + paragraph + '\n'
        full_article = full_article.translate(translator)
        X.append(full_article)

    # set up the LSA model and fit it to the list of articles X. Save the model
    # as a joblib file.
    vectorizer = TfidfVectorizer(tokenizer=LemmaTokenizer(), 
                                    analyzer='word', 
                                    stop_words=stopWords)
    LSA = TruncatedSVD(n_components=100)

    lsa_model = Pipeline([('vectorizer',vectorizer),
                            ('LSA',LSA)])
    lsa_model.fit(X)

    joblib.dump(lsa_model, LSA_MODEL_PATH)

    # print how long that took
    print(datetime.now() - startTime)