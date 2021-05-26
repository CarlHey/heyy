from functools import wraps as _wraps, partial
from typing import Iterable

from .types import _T

wraps_doc = partial(_wraps, assigned=('__doc__',))

_singleton_null = None


class Null:

    def __new__(cls, *args, **kwargs):
        global _singleton_null
        if _singleton_null is None:
            _singleton_null = super().__new__(cls, *args, **kwargs)
        return _singleton_null

    def __repr__(self):
        return 'Null'


def _lower_str_iterable_wrap(iterable: Iterable[_T]) -> Iterable[_T]:
    for i in iterable:
        if isinstance(i, str):
            i = i.lower()
        yield i


def _lowered_if_str(o: _T) -> _T:
    if isinstance(o, str):
        o = o.lower()
    return o
