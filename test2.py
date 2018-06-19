#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser

parser = ArgumentParser()

# Add more options if you like
parser.add_argument("-f", "--file", dest="myFilenameVariable",
                    help="write report to FILE", metavar="FILE")
parser.add_argument("-q", "--quiet",
                    action="store_false", dest="verbose", default=True,
                    help="don't print status messages to stdout")

args = parser.parse_args()

print(args.myFilenameVariable)