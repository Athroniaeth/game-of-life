import typer
from typer.testing import CliRunner

cli = typer.Typer(
    name="",
    add_completion=False,
    no_args_is_help=False,
    help="This is a simple CLI app.",
    add_help_option=True,
    context_settings={"help_option_names": ["--help"]},
)


@cli.command()
def hello(name: str):
    typer.echo(f"hello {name}")


@cli.command(name="help", help="Display help message, list of commands.")
def _help():
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    typer.echo(result.stdout)
    print(result.stdout)


if __name__ == "__main__":
    cli()
