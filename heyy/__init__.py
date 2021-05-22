from .__version__ import __version__
from .core import *
from .pathtool import PathTool

pt = PathTool()
do = DictObjHelper()

__all__ = [
    'with_folder',
    'reflect',
    'json2obj',
    'DictObj',
    'CaseInsensitiveDictObj',
    'pt',
    'do',
]
