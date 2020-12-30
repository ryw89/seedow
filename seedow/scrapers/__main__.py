import argparse

from .templates import Scraper


def templates():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v',
                        '--values',
                        action='store_true',
                        help='Print values only.')

    args = parser.parse_args()

    template_links = Scraper(values_only=args.values)
    template_links.get_all_links()
    template_links.print_links()
