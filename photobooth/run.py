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
    args_parse.add_argument("--output", "-o", metavar="folder", help="directory to store pictures", required=True)

    params = args_parse.parse_args()

    # Check if output directory is writable.
    try:
        if os.path.isdir(params.output):
            open(os.path.join(params.output, "photobooth.txt"), 'a').close()

            # delete test file
            os.remove("{}/{}".format(params.output, "photobooth.txt"))

        else:
            raise os.error("Folder does not exists.")
    except os.error as e:
        logging.error("Failed to write in {}: {}".format(params.output, e))
        exit(2)
