import click
from pprint import pprint
from model_types import ModelType
from database_layer import DatabaseLayer
from autogluon.tabular import TabularPredictor
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from tempfile import TemporaryDirectory, TemporaryFile
from zip_utils import *
from random import random
import pandas as pd
import pickle
import requests

BASE_URL = 'http://localhost:5000'

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


########################################################################################################################
# Testing CLI
########################################################################################################################

@click.group()
def cli():
    pass

@cli.command()
@click.argument('model_name')
def insert_gluon(model_name):
    with TemporaryDirectory() as tmpdir:
        train_df, _ = generate_data()
        train_and_save_gluon(train_df, tmpdir)
        model = zip_directory(tmpdir)
        DatabaseLayer().add_model(model_name, ModelType.TABULAR_PREDICTOR, model)


@cli.command()
@click.argument('model_name')
def insert_sklearn(model_name):
    with TemporaryFile() as tmpfile:
        train_df, _ = generate_data()
        train_and_save_sklearn(train_df, tmpfile)
        tmpfile.seek(0)
        DatabaseLayer().add_model(model_name, ModelType.MLP_REGRESSOR, tmpfile.read())


@cli.command()
@click.argument('model_name')
def test_api(model_name):
    _, test_data = generate_data()
    test_data = test_data.drop(columns=['target']).to_dict('records')

    data = {'features': test_data}
    pprint(data)

    response = requests.post(f'{BASE_URL}/{model_name}/predict', json=data)
    if response.status_code == 200:
        pprint(response.json())
    else:
        click.echo(response.content)


@cli.command()
@click.argument('model_name')
def test_revenue(model_name):
    with open('revenue.pkl', 'br') as f:
        test_data = pickle.load(f)

    test_data = test_data.to_dict('records')[0]
    test_data["Stores 1km"] = 0
    del test_data["start_date"]
    del test_data["end_date"]
    del test_data["period"]

    test_data = [test_data]

    data = {'features': test_data}
    pprint(data)

    response = requests.post(f'{BASE_URL}/{model_name}/predict', json=data)
    if response.status_code == 200:
        pprint(response.json())
    else:
        click.echo(response.content)

if __name__ == '__main__':
    cli()
