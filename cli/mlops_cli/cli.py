import click
from mlops_cli.commands import auth, dataset

@click.group()
def cli():
    pass

cli.add_command(auth.login)
cli.add_command(dataset.pull)
