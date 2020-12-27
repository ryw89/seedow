"""Package-wide extension modules and helper functions, implemented in
either C, Rust, or Python.
"""

# Note that we intentionally import .py first so as to replace
# same-named functions with their faster Rust or C implementations.
from .py import *
from .rust import *
from .c import *
