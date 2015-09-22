from copy import deepcopy

__author__ = 'siredvin'
import json
from functools import reduce
import os
import jinja2 as jnj
import util
import languagetool
import requests

r = requests.post("http://localhost:8081", {"language": 'en', 'text': 'my texd'})
print(r.text)

