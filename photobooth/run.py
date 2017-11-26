#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import logging
import os


def set_logging(lvl=logging.INFO):
    """
    Set logging output.
    :param lvl: Log level.
    :type lvl: Int
    """
    logging.basicConfig(level=lvl)


if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--output", "-o", metavar="folder", help="directory to store pictures")

    params = args_parse.parse_args()

    # Check output directory
    try:
        if os.path.isdir(params.output):
            with open("{}/{}".format(params.output, "photobooth.txt", 'w')) as f:
                f.write("")

            # delete test file
            os.remove("{}/{}".format(params.output, "photobooth.txt"))

        else:
            os.makedirs(params.output)
    except os.error as e:
        logging.error("Failed to write in {}: {}".format(params.output, e))
