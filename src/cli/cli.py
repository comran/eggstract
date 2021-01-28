import click

from src.library.library import Library

@click.group()
def cli():
    """
    An experimental project for extracting component audio tracks from songs.
    """
    pass

@cli.group()
def library():
    """
    Maintains track data used for training and testing.
    """
    pass

@library.command()
def load():
    track_library = Library()
    track_library.load_from_folder()

if __name__ == '__main__':
    cli()
