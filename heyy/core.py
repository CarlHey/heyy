from functools import wraps
from os import chdir, getcwd
from pathlib import Path
from typing import Any


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


def reflect(obj, skip_callable=False):
    for attr in dir(obj):
        if attr.startswith('__'):
            continue
        value = getattr(obj, attr)
        if skip_callable and callable(value):
            continue
        print(attr, value)


class DictObj:

    def __init__(self, data: dict):
        self.__dict__.update(data)

    def __str__(self):
        return self.__dict__.__str__()

    def __repr__(self):
        return self.__dict__.__repr__()

    def __len__(self):
        return self.__dict__.__len__()

    def __getitem__(self, item):
        return self.__dict__.__getitem__(item)

    def __contains__(self, item):
        return self.__dict__.__contains__(item)

    def __iter__(self):
        return iter(self.__dict__)

    def items(self):
        return self.__dict__.items()


def json2obj(data: Any):
    if isinstance(data, dict):
        data = data.copy()
        for k, v in data.items():
            data[k] = json2obj(v)
        return DictObj(data)
    elif isinstance(data, list):
        data = data.copy()
        for i, v in enumerate(data):
            data[i] = json2obj(v)
        return data
    elif isinstance(data, tuple):
        return json2obj(list(data))
    else:
        return data
