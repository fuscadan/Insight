'''
    Created on Thur September  18 2019

    @author danie

        train a svm model to predict whether a given paragraph from a game
        recap article will be promoted to the game summary page.
'''

from sklearn.svm import LinearSVC
from sklearn import preprocessing
from sklearn import pipeline
import joblib
import pandas as pd
import numpy as np
import ast

model_path = 'Git/nba_smart_database/svc_model_balanced.joblib'
Xy_data_path = 'Git/data/processed/Xy_data_balanced_regular_season_2017-2018.csv'

Xy_df = pd.read_csv(Xy_data_path, index_col=0)

X_temp = Xy_df['0'].tolist()

X = []

for x in X_temp:
    X.append(ast.literal_eval(x))

y = Xy_df['1'].tolist()

X = np.array(X)

standardizer = preprocessing.StandardScaler()
clf = LinearSVC()

model = pipeline.Pipeline([('standardizer' , standardizer) , ('clf', clf)])

model.set_params(clf__max_iter=10000).fit(X,y) 

joblib.dump(model,model_path)


