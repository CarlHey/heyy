from typing import Iterable

from .types import _T


def _lower_str_iterable_wrap(iterable: Iterable[_T]) -> Iterable[_T]:
    for i in iterable:
        if isinstance(i, str):
            i = i.lower()
        yield i


def _lowered_if_str(o: _T) -> _T:
    if isinstance(o, str):
        o = o.lower()
    return o