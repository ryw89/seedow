"""Various string-cleaning methods."""

import importlib

from ..lib.py.pkg import get_base_pkg

clean_number = getattr(importlib.import_module(get_base_pkg() + '.lib'),
                       'clean_number')
