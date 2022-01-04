"""This module manages the scripts we use to interact with the application."""
import os
import pytest
import click
from dotenv import load_dotenv
from src.app import create_app

load_dotenv()
app = create_app()


@app.cli.command("tests")
@click.argument("option", required=False)
def run_test_with_option(option: str = None):
    """Run tests with option."""
    from subprocess import run
    from shlex import split

    if option is None:
        raise SystemExit(
            pytest.main(
                [
                    "--disable-pytest-warnings",
                    "--cov=.",
                    "--cov-report=term:skip-covered",
                    "--cov-report=xml",
                    "--cov-report=html",
                    "--cov-config=.coveragerc",
                    "--cov-append",
                    "--no-cov-on-fail",
                ]
            )
        )
    elif option == "watch":
        run(
            split(
                'ptw --runner "python3 -m pytest tests --durations=5 '
                '--disable-pytest-warnings"'
            )
        )
    elif option == "debug":
        run(
            split(
                'ptw --pdb --runner "python3 -m pytest tests --durations=5 '
                '--disable-pytest-warnings"'
            )
        )


@app.cli.command("seed")
def seed():
    """Seed the Backing Redis with some data."""
    from tests.seed import seed_db

    seed_db()


@app.cli.command("clean")
def clean_seed():
    """Clean the seed data."""
    from tests.seed import clean_db

    clean_db()


if __name__ == "__main__":
    HOST = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    PORT = int(os.getenv("FLASK_RUN_PORT", 5000))
    DEBUG = os.getenv("FLASK_DEBUG", False)

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG,
    )
