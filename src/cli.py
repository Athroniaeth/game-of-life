import numpy
import typer
from typer.testing import CliRunner

# Todo: WARNING
# Instantiation, outside a function, allows Typer to capture the application so that it can interact with it.
# I haven't found any other way of doing this, while still allowing the CLI to be detached to create the Console.
cli = typer.Typer(
    name="APPLICATION",
    add_completion=False,
    no_args_is_help=False,
    add_help_option=True,
    context_settings={"help_option_names": ["--help"]},
)


def get_app():
    """ Shorter way to get the application. """
    from src.app import app
    return app


@cli.command(help="Reshape the grid to the specified dimensions. (delete all cells)")
def reshape(
        width: int = typer.Argument(65, help="Width of the grid"),
        height: int = typer.Argument(37, help="Height of the grid")
):
    """
    Reshape the grid to the specified dimensions (delete all cells).
    Args:
        width (int): New width of the grid.
        height (int): New height of the grid.
    """
    app = get_app()
    app.grid_model.grid = numpy.zeros((width, height), dtype=int)
    typer.echo(f"Grid reshaped, new dimensions: {width}x{height}")


@cli.command(help="Change the speed of the game.")
def limit_fps(fps: int = typer.Argument(60, help="Frames per second")):
    """
    Change the speed of the game (frames per second).

    Args:
        fps (int): New frames per second to set.
    """
    app = get_app()
    app.limit_fps = fps
    typer.echo(f"Speed changed, new speed: {fps}")


@cli.command(help="Clear the grid of all live cells.")
def clear():
    """ Clear the grid of all live cells. """
    app = get_app()
    number_cells_live = app.grid_model.grid.sum()

    app.grid_model.clear_grid()
    typer.echo(f"Grid cleared, deleted cells: {number_cells_live}")


@cli.command(name="help", help="Display help message, list of commands.")
def _help():
    """ Makes the 'help' command more consistent in a console. """
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    typer.echo(result.stdout)


if __name__ == "__main__":
    cli()
