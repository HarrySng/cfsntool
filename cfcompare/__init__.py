from .cfcompare import version, standardnames, descriptions, uom, aliases

# if somebody does "from somepackage import *", this is what they will
# be able to access:
__all__ = [
    'version',
    'standardnames',
    'descriptions',
    'uom',
    'aliases',
]