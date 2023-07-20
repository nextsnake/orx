"""
orx
~~~
A simple wrapper for the Discord API.

:license: MIT
:copyright: 2023 tag-epic
"""

from typing import Literal


__version__: Literal['0.1.0'] = '0.1.0'


from .bot import *
from .events import *
from .flags import *
from .models import *
from .state import *
