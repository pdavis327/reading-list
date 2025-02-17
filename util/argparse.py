"""
Utilities for use with argparse
"""

from datetime import datetime
import argparse
import logging
import os


def valid_date(s):
    """
    Use with argparse to validate a date parameter

    Example Usage:
    parser.add_argument('--start_date', type=valid_date,
                    help='Start date for the pipeline. '
                         'Format: YYYY-MM-DD (default: %(default)s)',
                    default='2019-01-01')
    """

    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def pretty_print_args(args):
    arg_str = "\n".join(f"  {k}={v}" for k, v in vars(args).items())
    return f"Executing with parameters:\n{arg_str}"


def setup_logging(verbosity):
    """
    Configures logging with verbosity levels and file output.
    """
    # Determine base log level
    base_loglevel = getattr(
        logging, os.getenv("LOGLEVEL", "INFO").upper(), logging.INFO
    )

    # Adjust log level based on verbosity
    if verbosity == 0:
        loglevel = logging.WARNING
    elif verbosity == 1:
        loglevel = logging.INFO
    elif verbosity == 2:
        loglevel = logging.DEBUG
    else:
        loglevel = base_loglevel  # Default to environment LOGLEVEL

    # Log format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Set the log file path to the root directory of your scripts
    log_file_path = os.path.join(
        os.getcwd(), "pipeline.log"
    )  # Log file in current working directory

    # Configure logging with file output
    logging.basicConfig(
        level=loglevel,
        format=log_format,
        handlers=[
            logging.FileHandler(log_file_path, encoding="utf-8"),  # Log to file
        ],
    )
