"""Scrape election template pages from Wikipedia for their links."""

import csv
import json
import re
import sys
import time
import urllib

import pkg_resources
import tqdm
from bs4 import BeautifulSoup

from ..config.config import get_wikipedia_sleep
from ..lib.py.pkg import get_base_pkg


class Scraper():
    """Scrape election template pages from Wikipedia for their links."""
    def __init__(self, values_only=False):
        self.wait = get_wikipedia_sleep()
        self.base_url = 'https://en.wikipedia.org/wiki/Template:'
        self.values_only = values_only

    @property
    def country_names(self):
        names = pkg_resources.resource_filename(get_base_pkg(),
                                                'data/country_altnames.csv')
        with open(names) as f:
            rows = csv.reader(f)
            res = list(rows)

        # Remove empty strings & replace space w/ underscore (spaces
        # are illegal in URLs)
        cleaned = []
        for r in res:
            cleaned.append([x.replace(' ', '_') for x in r if x])

        return cleaned

    def get_country_list(self, country):
        for c in self.country_names:
            if country in c:
                return c

        return None

    @staticmethod
    def clean_wiki_link(link):
        """Helper method for cleaning links so they can be fed into
        :code:`wikipedia.page`.
        """
        return urllib.parse.unquote(str(link).split('/wiki/')[1])

    def get_links(self, country):
        """Get all links on a country's Wikipedia template page."""
        country_list = self.get_country_list(country)
        if country_list is None:
            raise ValueError(
                f'{country} was not found from get_country_list().')

        for c in country_list:
            link = f'{self.base_url}{c}_elections'
            try:
                html_content = urllib.request.urlopen(link)
            except (urllib.error.HTTPError, UnicodeEncodeError):
                continue

            soup = BeautifulSoup(html_content, 'html.parser')

            link_list = []
            for link in soup.find('div', {
                    'id': 'bodyContent'
            }).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
                if 'href' in link.attrs:
                    link_list.append(self.clean_wiki_link(link.attrs['href']))

            return list(set(link_list))

        return None

    def get_all_links(self):
        self.links = {}
        sys.stderr.write('Fetching links for all countries...\n')
        for country in tqdm.tqdm(self.country_names):
            # finished_ctry here is used to avoid having duplicate
            # dictionary keys for a country -- Wikipedia has multiple
            # duplicates pages (or more precisely, redirections) for
            # certain pages (e.g., Zimbabwe = Zimbabwean)
            finished_ctry = False
            for c in country:
                if finished_ctry:
                    continue
                time.sleep(self.wait)
                res = self.get_links(c)
                if res:
                    self.links[c] = res
                    finished_ctry = True

    def print_links(self):
        """Print :code:`self.links`, either the full dictionary as JSON or
        just the links themselves.
        """
        if self.values_only:
            for _, links in self.links.items():
                for link in links:
                    print(link)
        else:
            json.dumps(self.links, indent=4)
