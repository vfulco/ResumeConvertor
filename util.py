__author__ = 'siredvin'
from functools import reduce

link_keys = ['link', 'text']

def link_check(node):
    return isinstance(node, dict) and len(list(filter(lambda x: x not in link_keys, node.keys()))) == 0

def localized_check(node, localizations):
    return isinstance(node, dict) and len(list(filter(lambda x: x not in localizations, node.keys()))) == 0

def text_flow_check(node):
    return isinstance(node, dict) and len(list(filter(lambda x: x != 'text_flow', node.keys()))) == 0

def read_full_file(file):
    return reduce(lambda x, y: x+y, file.readlines())
