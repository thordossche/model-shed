from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from random import random
import pandas as pd

import pickle

def generate_data():
    X = [random()*10 - 5 for _ in range(400)]
    y = [2*x for x in X] 
    df = pd.DataFrame({'x': X, 'target': y})

    train_df, test_df = train_test_split(df, test_size=0.02, random_state=42)
    return train_df, test_df

def train_and_save_gluon(train_data, model_dir):
    TabularPredictor(label='target', path=model_dir).fit(train_data)

def train_and_save_sklearn(train_data, temp_file):
    regressor = MLPRegressor(random_state=0, max_iter=5000)
    regressor.fit(train_data.drop(columns=['target']), train_data['target'])

    pickle.dump(regressor, temp_file)


