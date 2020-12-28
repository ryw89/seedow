import argparse

from .words import *


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d',
                        '--data',
                        type=str,
                        help='Path to summaries data in JSON format.')

    args = parser.parse_args()

    words = Words(args.data)
    words.write_counts()
