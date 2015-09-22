from copy import deepcopy

__author__ = 'siredvin'

import util

def markdown_parse_link(link_node):
    return "["+link_node['text']+']('+link_node['link']+')'

def generate_localized_markdown(resume, locale):
    resume = deepcopy(resume)
    localizations = resume['localizations']
    resume.pop('localizations', None)
    result = generate_markdown_part(resume, locale, localizations)
    result.update({'locale': locale})
    return result

def generate_markdown_part(resume, locale, localizations):
    for key in resume.keys():
        resume[key] = parse_markdown_part(resume[key], locale, localizations)
    return resume

def parse_markdown_part(node, locale, localizations):
    if isinstance(node, dict):
        node = generate_markdown_part(node, locale, localizations)
    if isinstance(node, list):
        node = list(map(lambda x: parse_markdown_part(x, locale, localizations), node))
    if util.link_check(node):
        node = markdown_parse_link(node)
    if util.localized_check(node, localizations):
        node = node[locale]
    elif util.text_flow_check(node):
        generated_text = ''
        for text_element in node["text_flow"]:
            if util.link_check(text_element):
                generated_text += markdown_parse_link(text_element)
            else:
                generated_text += text_element
        node = generated_text
    return node
