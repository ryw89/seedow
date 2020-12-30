import argparse

from .words import Words


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u',
                        '--url',
                        type=str,
                        help='Path to list of URLs to scrape.')
    parser.add_argument('-d',
                        '--data',
                        type=str,
                        help='Path to summaries data in JSON format.')

    args = parser.parse_args()

    words = Words(summaries_data=args.data, urls_data_path=args.url)

    try:
        words.summaries
    except AttributeError:
        words.fetch_summaries()

    words.write_counts()
