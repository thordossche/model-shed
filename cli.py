import click
import os
import requests
import pickle
from database_layer import DatabaseLayer, ModelType
from zip_utils import zip_directory
from test_utils import generate_data, train_and_save_gluon, train_and_save_sklearn
from pprint import pprint
from tempfile import TemporaryDirectory, TemporaryFile


########################################################################################################################
# CLI
########################################################################################################################

BASE_URL = 'http://localhost:5000'

@click.group()
def cli():
    pass


@cli.command()
def list():
    response = requests.get(f'{BASE_URL}/models')
    if response.status_code == 200:
        pprint(response.json())
    else:
        click.echo(response.content)


@cli.command()
@click.argument('model_name')
def info(model_name):
    response = requests.get(f'{BASE_URL}/{model_name}')
    if response.status_code == 200:
        pprint(response.json())
    else:
        click.echo(response.content)


@cli.command()
@click.argument('model_name')
@click.argument('file_path', type=click.Path(exists=True))
@click.argument('model_type', type=click.Choice([e.model_name for e in ModelType], case_sensitive=False))
def upload(model_name, file_path, model_type):
    if os.path.isdir(file_path):
        file = zip_directory(file_path)
    else:
        file = open(file_path, 'rb')

    response = requests.put(
        f'{BASE_URL}/{model_name}', 
        files={'file': file},
        data={'model_type': model_type}
    )
    click.echo(response.text)


@cli.command()
@click.argument('model_name')
def delete(model_name):
    response = requests.delete(f'{BASE_URL}/{model_name}')
    click.echo(response.text)


########################################################################################################################
# Testing
########################################################################################################################

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
    with open('./revenue.pkl', 'br') as f:
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

