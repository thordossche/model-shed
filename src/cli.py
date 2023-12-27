import click
import os
import requests
from model_types import ModelType
from zip_utils import zip_directory
from pprint import pprint

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


if __name__ == '__main__':
    cli()

