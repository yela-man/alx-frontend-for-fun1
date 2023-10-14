#!/usr/bin/python3
"""
markdown2html.py
Module that converts Markdown to HTML
"""

import os
import sys
import hashlib
import re


def markdown2html(md_filename, html_filename):
    """
    A function that converts Markdown to HTML
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html", file=sys.stderr)
        exit(1)
    if not os.path.isfile(md_filename):
        print("Missing {}".format(md_filename), file=sys.stderr)
        exit(1)

    with open(md_filename, 'r') as md_file, open(html_filename, 'w') as html_file:
        lines = md_file.readlines()
        while len(lines) > 0:
            line = lines.pop(0)
            hash_tag, content = line.split(' ', 1)
            # handle headings
            if line.startswith('#'):
                level = len(hash_tag)
                content = content.strip()
                html_file.write('<h{}>{}</h{}>\n'.format(level, content, level))
            # handle unordered lists
            elif line.startswith('- '):
                html_file.write('<ul>\n')
                while line.startswith('- '):
                    content = line[2:].strip()
                    html_file.write('<li>{}</li>\n'.format(content))
                    if len(lines) > 0:
                        line = lines.pop(0)
                    else:
                        break
                html_file.write('</ul>\n')
            # handle ordered lists
            elif line.startswith('* '):
                html_file.write('<ol>\n')
                while line.startswith('* '):
                    content = line[2:].strip()
                    html_file.write('<li>{}</li>\n'.format(content))
                    if len(lines) > 0:
                        line = lines.pop(0)
                    else:
                        break
                html_file.write('</ol>\n')
            # handle simple text
            else:
                html_file.write('<p>\n')
                while not line.startswith(('#', '-', '*')):
                    content = line.strip().replace('\n', '<br/>\n')
                    html_file.write('{}\n'.format(content))
                    if len(lines) > 0:
                        line = lines.pop(0)
                    else:
                        break
                html_file.write('</p>\n')
            # handle bold and emphasis text
            line = line.replace('**', '<b>', 1).replace('**', '</b>', 1)
            line = line.replace('__', '<em>', 1).replace('__', '</em>', 1)
            # handle special syntax
            line = re.sub(r'\[\[(.+?)\]\]', lambda m: hashlib.md5(m.group(1).encode()).hexdigest(), line)
            line = re.sub(r'\(\((.+?)\)\)', lambda m: m.group(1).replace('c', '').replace('C', ''), line)


if __name__ == "__main__":
    markdown2html(sys.argv[1], sys.argv[2])
