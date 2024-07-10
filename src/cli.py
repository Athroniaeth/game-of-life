import numpy
import typer
from typer.testing import CliRunner

cli = typer.Typer(
    name="APPLICATION",
    add_completion=False,
    no_args_is_help=False,
    add_help_option=True,
    context_settings={"help_option_names": ["--help"]},
)


def get_app():
    from src.app import app
    return app


@cli.command(help="Reshape the grid to the specified dimensions. (delete all cells)")
def reshape(
        width: int = typer.Argument(65, help="Width of the grid"),
        height: int = typer.Argument(37, help="Height of the grid")
):
    app = get_app()
    app.grid_model.grid = numpy.zeros((width, height), dtype=int)
    typer.echo(f"Grid reshaped, new dimensions: {width}x{height}")


@cli.command(help="Change the speed of the game.")
def limit_fps(fps: int = typer.Argument(60, help="Frames per second")):
    app = get_app()
    app.fps = fps
    typer.echo(f"Speed changed, new speed: {fps}")


@cli.command(name="help", help="Display help message, list of commands.")
def _help():
    """ Permet d'avoir la commande 'help' plus cohérente dans une console. """
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    typer.echo(result.stdout)


if __name__ == "__main__":
    cli()
