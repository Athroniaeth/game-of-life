import logging
import sys
from pathlib import Path

path = Path(__file__).parents[1].absolute()
sys.path.append(f'{path}')

from src.app import app  # noqa: E402


def main():
    return_code = 0
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    try:
        app.run()
    except KeyboardInterrupt as exception:
        logging.info(f"Exiting the program: '{exception}'")

    except SystemExit as exception:
        logging.info(f"Exiting the program: '{exception}'")
        return_code = exception.code

    except Exception as exception:
        logging.error(f"An error occurred: '{exception}'")
        return_code = 1

    finally:
        sys.exit(return_code)


if __name__ == '__main__':
    main()
