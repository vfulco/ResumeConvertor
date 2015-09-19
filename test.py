from copy import deepcopy

__author__ = 'siredvin'
import json
from functools import reduce
import os
import jinja2 as jnj
import util

a = "java"
local_file = open(os.path.join("locale", "en.py"))
print(eval(util.read_full_file(local_file)))
print()
local_file.close()


