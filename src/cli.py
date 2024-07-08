import typer

from src import app as module_app


cli = typer.Typer()


@cli.command()
def hello(name: str):
    module_app.app.grid_model.grid[0][0] = 1
    print(f"Hello {name}")


@cli.command()
def _(command: str):
    print(f"Command: {command}")
