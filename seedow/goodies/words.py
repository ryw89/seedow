"""Get the most common words from election article summaries."""

import html
import json
import sys
import time

import nltk
import pandas as pd
import pkg_resources
import tqdm
import wikipedia

from ..lib.py.pkg import get_base_pkg


class Words():
    """Fetch the most common words from election article summaries."""
    def __init__(self, summaries_data=None):
        self.urls_data_path = pkg_resources.resource_filename(
            get_base_pkg(), 'data/urls.txt')

        with open(self.urls_data_path) as f:
            self.urls = [
                html.unescape(x.strip()) for x in f.readlines()
                if x.startswith('http')
            ]

        if summaries_data is not None:
            with open(summaries_data, 'r') as f:
                self.summaries = json.load(f)

    def fetch_summaries(self, wait=0.1):
        """Fetch Wikpiedia article summaries using wikipedia module."""
        self.summaries = {}
        sys.stderr.write('Fetching Wikipedia article summaries...\n')
        for url in tqdm.tqdm(self.urls):
            url_ending = url.split('/')[-1]
            try:
                page = wikipedia.page(url_ending)
            except wikipedia.exceptions.PageError:
                pass
            else:
                summary = page.summary
                self.summaries[url] = summary
                time.sleep(wait)

    @property
    def words(self):
        return list(self.summaries.values())

    @property
    def joined_words(self):
        return ' '.join(self.words)

    @property
    def tokenized(self):
        """Tokenized :code:`self.joined_words` without punctuation, removing
        English stopwords.
        """
        return [
            x.lower() for x in nltk.tokenize.word_tokenize(self.joined_words)
            if x.isalpha() and x not in nltk.corpus.stopwords.words('english')
        ]

    @property
    def stemmed(self):
        """Stemmed :code:`self.tokenized`."""
        ps = nltk.stem.PorterStemmer()
        return [ps.stem(x) for x in self.tokenized]

    @property
    def stemmed_counts(self):
        series = pd.Series(self.stemmed)
        return series.value_counts()

    def write_counts(self):
        print(self.stemmed_counts.to_csv(), end='')
