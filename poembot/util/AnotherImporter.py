# -*- coding: utf-8 -*-
from Query import show_templates

FULL_RESOURCE_PATH = "../../resource/ci.txt"

existing_templates = show_templates()

def find_ci_template():
    results = {}
    with open(FULL_RESOURCE_PATH, 'r') as poem_file:
        contents = poem_file.readlines()
        for content in contents:
            line = content.strip()

            if line and len(line) < 10 and (line.decode('utf-8') not in existing_templates):
                if not results.get(line):
                    results[line] = 1
                results[line] = results[line] + 1
    return results


templates = find_ci_template()
templates = sorted(templates.iteritems(), key=lambda d:d[1], reverse = True)
for i in range(10):
    print "%s : %s" % (templates[i][0], templates[i][1])


