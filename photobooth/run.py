#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from argparse import ArgumentParser

if __name__ == "__main__":
    # Create script arguments parser
    args_parse = ArgumentParser("Run photobooth.")
    args_parse.add_argument("--output", "-o", metavar="folder", help="directory to store pictures")

    params = args_parse.parse_args()

