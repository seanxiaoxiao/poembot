# -*- coding: utf-8 -*-
CI_RESOURCE_FIEL = "../resource/ci.txt"


def import_ci():
    ci_file = open(CI_RESOURCE_FIEL, "r")

    author = None
    read_state = None
    content = []
    with ci_file as file:
        for i, line in enumerate(file):
            line = line.strip()
            if line == "":
                author = None
            if author == None and line != "":
                author = line
            elif author:
                if line.find("（") > 0 or len(line) < 20:
                    if len(content) != 2:
                        for line_in_content in content:
                            print line_in_content
                        print "\n"
                    content = []
                else:
                    content.append(line)

import_ci()