from wikitablescrape.parse import *


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
