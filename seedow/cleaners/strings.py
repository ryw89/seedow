"""Various string-cleaning methods."""

import importlib


def _get_base_pkg():
    return __name__.split('.')[0]


clean_number = getattr(importlib.import_module(_get_base_pkg() + '.lib'),
                       'clean_number')
