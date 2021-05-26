from functools import wraps
from os import chdir, getcwd
from pathlib import Path
from typing import Any, Optional, Iterable, MutableMapping, Mapping

from .types import _T, _S, _KT, _VT, AttrNames
from .utils import Null,  wraps_doc, _lowered_if_str, _lower_str_iterable_wrap


_null = Null()


def with_folder(folder, create_if_not_exists=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            path = Path(folder).resolve()
            if not path.exists():
                if create_if_not_exists:
                    path.mkdir(parents=True)
                else:
                    raise ValueError(f'Folder <{path}> do not exists')
            cwd = getcwd()
            chdir(path)
            try:
                res = func(*args, **kw)
            finally:
                chdir(cwd)
            return res
        return wrapper
    return decorator


def reflect(obj, *, skip_callable=False, exclude: Optional[AttrNames] = None):
    exclude_attrs = set(exclude) if exclude is not None else set()
    for attr in dir(obj):
        if attr in exclude_attrs:
            continue
        if attr.startswith('__'):
            continue
        try:
            value = getattr(obj, attr)
        except Exception as e:
            value = f'[Error: <{repr(e)}>]'
        if skip_callable and callable(value):
            continue
        print(attr, value)


class DictObjHelper:

    def __getattr__(self, item):
        def wrapper(obj, *args, **kw):
            return getattr(obj.__class__, item)(obj, *args, **kw)
        return wrapper


class DictObj(dict, MutableMapping[_KT, _VT]):

    def __init__(self, *args, **kw) -> None:
        super().__init__(*args, **kw)
        self.__dict__ = self

    @classmethod
    @wraps_doc(dict.fromkeys)
    def fromkeys(cls, iterable: Iterable[_T], value: _S = _null) -> 'DictObj[_T, _S]':
        if value is _null:
            result = super().fromkeys(iterable)
        else:
            result = super().fromkeys(iterable, value)
        return cls(result)

    @wraps_doc(dict.copy)
    def copy(self) -> 'DictObj[_KT, _VT]':
        return self.__class__(super().copy())

    def select(self, attrs: Iterable[str], *, ignore_error=True):
        o = self.__class__()
        for attr in attrs:
            try:
                o[attr] = self[attr]
            except KeyError:
                if ignore_error:
                    continue
                raise
        return o

    def omit(self, attrs: Iterable[str]):
        o = self.copy()
        for attr in attrs:
            if attr in self:
                del o[attr]
        return o


class CaseInsensitiveDictObj(DictObj[_KT, _VT]):

    def __init__(self, *args, **kw) -> None:
        super().__init__()
        self.update(*args, **kw)

    @wraps_doc(dict.update)
    def update(self, *args, **kwargs) -> None:
        if len(args) > 1:
            raise TypeError('update expected at most 1 arguments, got %d' % len(args))
        if args:
            other = args[0]
            if isinstance(other, Mapping):
                for key in other:
                    self[_lowered_if_str(key)] = other[key]
            elif hasattr(other, "keys"):
                for key in other.keys():
                    self[_lowered_if_str(key)] = other[key]
            else:
                for key, value in other:
                    self[_lowered_if_str(key)] = value
        for key, value in kwargs.items():
            self[key.lower()] = value

    @classmethod
    @wraps_doc(dict.fromkeys)
    def fromkeys(cls, iterable: Iterable[_T], value: _S = _null) -> 'CaseInsensitiveDictObj[_T, _S]':
        if value is _null:
            result = super().fromkeys(_lower_str_iterable_wrap(iterable))
        else:
            result = super().fromkeys(_lower_str_iterable_wrap(iterable), value)
        return cls(result)

    @wraps_doc(dict.setdefault)
    def setdefault(self, key, default=None) -> _VT:
        key = _lowered_if_str(key)
        return super().setdefault(key, default)

    @wraps_doc(dict.pop)
    def pop(self, key, default=_null):
        key = _lowered_if_str(key)
        if default is _null:
            return super().pop(key)
        else:
            return super().pop(key, default)

    @wraps_doc(dict.get)
    def get(self, key, default=_null):
        key = _lowered_if_str(key)
        if default is _null:
            return super().get(key)
        else:
            return super().get(key, default)

    def __getitem__(self, k: _KT) -> _VT:
        k = _lowered_if_str(k)
        return super().__getitem__(k)

    def __setitem__(self, k: _KT, v: _VT) -> None:
        k = _lowered_if_str(k)
        super().__setitem__(k, v)

    def __delitem__(self, k: _KT) -> None:
        k = _lowered_if_str(k)
        super().__delitem__(k)

    def __contains__(self, o: object) -> bool:
        o = _lowered_if_str(o)
        return super().__contains__(o)

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name.lower())

    def __setattr__(self, name: str, value):
        super().__setattr__(name.lower(), value)

    def __delattr__(self, name: str):
        super().__delattr__(name.lower())


def json2obj(data: Any = _null, *, ignore_case=False):
    dict_obj_class = DictObj if not ignore_case else CaseInsensitiveDictObj
    if isinstance(data, dict):
        data = data.copy()
        for k, v in data.items():
            data[k] = json2obj(v, ignore_case=ignore_case)
        return dict_obj_class(data)
    elif isinstance(data, list):
        data = data.copy()
        for i, v in enumerate(data):
            data[i] = json2obj(v, ignore_case=ignore_case)
        return data
    elif isinstance(data, tuple):
        return json2obj(list(data), ignore_case=ignore_case)
    elif data is _null:
        return dict_obj_class()
    else:
        return data
