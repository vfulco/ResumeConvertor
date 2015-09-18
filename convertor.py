import util

__author__ = 'siredvin'

import argparse
import json
from functools import reduce
import markdowncovert as md
from jinja2 import Environment, FileSystemLoader
import os

parser = argparse.ArgumentParser(description='Tool to convert json resume to markdown and latex format')
parser.add_argument("file", type=str, help="path to json resume file")
parser.add_argument("--template", type=str, default="markdown.template", help="custom template based on jinja2")
parser.add_argument("--localization-directory", type=str, default="locale",
                    help="directory with localization python files")
parser.add_argument("--output", type=str, default="resume_%", help="Output file template % will be replaced by locale")
parser.add_argument("--markdown", "-m", action='store_true', default=False, help="Enable markdown output")
parser.add_argument("--latex", '-l', action='store_true', default=False, help="Enable latex output")

args = parser.parse_args()
resumeFile = open(args.file)
resume = json.loads(reduce(lambda x, y: x + y, resumeFile.readlines(), ""))
resumeFile.close()
locales = resume['localizations']
en_json_markdown = md.generate_localized_markdown(resume, 'en')
local_file = open(os.path.join(args.localization_directory, "en.py"))
exec(util.read_full_file(local_file))
local_file.close()
print(localization_map) #inject from en.py
en_json_markdown.update(localization_map)
# print(json.dumps(en_json_markdown, sort_keys=True, indent=4, separators=(',', ': ')))

THIS_DIR = os.path.dirname(os.path.abspath(__file__))

markdown_en = open(args.output.replace('%', 'en')+".md", 'w')
j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
markdown_en.write(j2_env.get_template('markdown.template').render(en_json_markdown))
markdown_en.close()





