__author__ = 'siredvin'

import argparse
import util
import json
from functools import reduce
import markdowncovert as md
import latexconvert as tex
from jinja2 import Environment, FileSystemLoader
import os
import subprocess

def markdown_generation(_resume, _localizations, _output, _output_directory, _j2_env):
    for _locale in _localizations:
        generated_json = md.generate_localized_markdown(_resume, _locale)

        local_file = open(os.path.join(args.localization_directory, _locale + ".py"))
        localization_map = eval(util.read_full_file(local_file))
        local_file.close()
        generated_json.update(localization_map)

        markdown_file = open(os.path.join(_output_directory, _output.replace("%", _locale)+'.md'), 'w')
        markdown_file.write(_j2_env.get_template('markdown.template').render(generated_json))
        markdown_file.close()

def latex_generation(_resume, _localization, _output, _output_directory, _j2_env, _template_directory):
    for _locale in _localization:
        generated_json = tex.generate_localized_latex(_resume, _locale)

        local_file = open(os.path.join(args.localization_directory, _locale + ".py"))
        localization_map = eval(util.read_full_file(local_file))
        local_file.close()
        generated_json.update(localization_map)

        latex_file = open(os.path.join(_template_directory, "LatexInclude", "main.tex"), 'w')
        latex_file.write(_j2_env.get_template('latex.template').render(generated_json))
        latex_file.close()
        latex_include = os.path.join(_template_directory, "LatexInclude")
        subprocess.call(["xelatex", "main.tex"], cwd=latex_include)
        for file in ['main.aux', 'main.out', 'main.log', 'main.tex']:
            os.remove(os.path.join(latex_include, file))
        os.rename(os.path.join(latex_include, 'main.pdf'), os.path.join(_output_directory,
                                                                        _output.replace('%', _locale)+'.pdf'))


scriptDirectory = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(description='Tool to convert json resume to markdown and latex format')
parser.add_argument("file", type=str, help="path to json resume file")
parser.add_argument("--template-directory", type=str, default=os.path.join(scriptDirectory, "templates"),
                    help="template directory with markdown and latex templates")
parser.add_argument("--localization-directory", type=str, default=os.path.join(scriptDirectory, "locale"),
                    help="directory with localization python files")
parser.add_argument("--output", type=str, default="resume_%", help="Output file template % will be replaced by locale")
parser.add_argument("--output-directory", "-d", default="output", help="Output directory for results")
parser.add_argument("--markdown", "-m", action='store_true', default=False, help="Enable markdown output")
parser.add_argument("--pdf", '-p', action='store_true', default=False, help="Enable pdf output via latex")

args = parser.parse_args()
if not os.path.exists(args.output_directory):
    os.mkdir(args.output_directory)
print("Заванатження файлу резюме")
resumeFile = open(args.file)
resume = json.loads(reduce(lambda x, y: x + y, resumeFile.readlines(), ""))
resumeFile.close()
locales = resume['localizations']

j2_env = Environment(loader=FileSystemLoader(args.template_directory), trim_blocks=True)
if args.markdown:
    markdown_generation(resume, locales, args.output, args.output_directory, j2_env)
if args.pdf:
    latex_generation(resume, locales, args.output, args.output_directory, j2_env, args.template_directory)
