from wikitablescrape.parse import *


def _parse_header(self):
    """Monkey-patched version of
    :code:`wikitablescrape.parse.HtmlTable.parse_headers`. Doesn't
    combine headers and sub-headers into one string; returns a
    dictionary instead.
    """
    headers = {}
    caption = self.tag.find('caption')
    if caption:
        headers['header'] = clean_cell(caption)
        return headers

    h2 = self.tag.findPrevious('h2')
    if h2:
        headers['header'] = clean_cell(h2)
        # Try to find a subheader as well
        h3 = self.tag.findPrevious('h3')
        if h3:
            headers['subheader'] = clean_cell(h3)
        return headers

    return None


class Parser(Parser):
    """Simple wrapper around :code:`wikitablescrape.parse.Parser` that
    adds some more helpful methods.
    """
    def __init__(self, text):
        super().__init__(text)

    @property
    def parsed_tables(self):
        """Tables as parsed by :code:`wikitablescrape`, including their
        headers and row content.
        """
        parsed = []
        for table in self.tables:
            header = table.parse_header()
            rows = []
            for row in table.parse_rows():
                rows.append(row)

            parsed.append({'header': header, 'rows': rows})

        return parsed

    @property
    def headers(self):
        """Parsed headers of all tables in a Wikpiedia page. Can be a string
        or None.
        """
        return [x['header'] for x in self.parsed_tables]


# Apply monkey patch
HtmlTable.parse_header = _parse_header
