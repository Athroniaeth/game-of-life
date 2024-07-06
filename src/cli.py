import typer

from src import app as module_app


cli = typer.Typer()


@cli.command()
def hello(name: str):
    print(module_app.app.grid_model.grid[0][0])
    print(f"Hello {name}")


@cli.command()
def _(command: str):
    print(f"Command: {command}")
