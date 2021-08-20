from _scenario_conftest import *

from contextlib import suppress
from os import remove

with suppress(FileNotFoundError):
    remove("log")

