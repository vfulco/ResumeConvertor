from copy import deepcopy

__author__ = 'siredvin'

import util

def latex_parse_link(link_node):
    return "\\href{"+link_node['link']+'}{'+link_node['text']+'}'

def generate_localized_latex(resume, locale):
    resume = deepcopy(resume)
    localizations = resume['localizations']
    resume.pop('localizations', None)
    return generate_latex_part(resume, locale, localizations)

def generate_latex_part(resume, locale, localizations):
    for key in resume.keys():
        resume[key] = parse_latex_part(resume[key], locale, localizations)
    return resume

def parse_latex_part(node, locale, localizations):
    if isinstance(node, dict):
        node = generate_latex_part(node, locale, localizations)
    if isinstance(node, list):
        node = list(map(lambda x: parse_latex_part(x, locale, localizations), node))
    if util.link_check(node):
        node = latex_parse_link(node)
    if util.localized_check(node, localizations):
        node = node[locale]
    elif util.text_flow_check(node):
        generated_text = ''
        for text_element in node["text_flow"]:
            if util.link_check(text_element):
                generated_text += latex_parse_link(text_element)
            else:
                generated_text += text_element
        node = generated_text
    return node
