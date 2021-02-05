from typing import Tuple

import click

from src.util.data import import_track


@click.group()
def cli():
    """
    An experimental project for extracting component audio tracks from songs.
    """


@cli.group()
def data():
    """
    Manage raw data files.
    """


@data.command()
@click.argument("file_location", nargs=-1)
def add_track(file_location_parts: Tuple[str]):
    """
    Add in a new track to the project.
    """
    file_location = " ".join(file_location_parts)
    import_track(file_location)


if __name__ == "__main__":
    cli()
