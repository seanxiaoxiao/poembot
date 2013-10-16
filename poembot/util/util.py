# -*- coding: utf-8 -*-
from Query import show_poem_info, character_info
import re
import operator

characters = character_info()
character_posibility = {}


def is_ping_sound(pronunciation):
    tune = pronunciation[len(pronunciation) - 1]
    tune = int(tune[len(tune) - 1])
    return tune == 1 or tune == 2 or tune == 0

def is_ze_sound(pronunciation):
    tune = pronunciation[len(pronunciation) - 1]
    tune = int(tune[len(tune) - 1])
    return tune == 3 or tune == 4 or tune == 0

def _analyse_content(poem, contents):
    p = re.compile(u"，|。|、", re.UNICODE)
    contents_after_split = p.split(contents)
    for content in contents_after_split:
        if len(content) == 0:
            continue

        current_char = content[0]
        if current_char in characters:
            if not character_posibility.get(current_char):
                character_posibility[current_char] = {"count": 0, "prefixs": []}
            character_posibility[current_char]["count"] += 1

        for i in range(1, len(content)):
            current_char = content[i]
            last_char = content[i - 1]
            if current_char in characters and last_char in characters:
                if not character_posibility.get(current_char):
                    character_posibility[current_char] = {"count": 0, "prefixs": []}
                character_posibility[current_char]["count"] += 1
                new_prefix = True
                for prefix in character_posibility[current_char]["prefixs"]:
                    if prefix.get("char") == last_char:
                        prefix["count"] += 1
                        new_prefix = False
                        break
                if new_prefix:
                    character_posibility[current_char]["prefixs"].append({"char": last_char, "count": 1})
            else:
                pass

def possibility():
    poems = show_poem_info()
    for poem in poems:
        contents = poem.get("contents")
        for content in contents:
            _analyse_content(poem, content)
    sorted_character_posibility = sorted(character_posibility.iteritems(), key=lambda x: x[1].get("count"))
    for item in sorted_character_posibility:
        sorted(item[1].get("prefixs"), key=lambda x: x.get("count"))
    print sorted_character_posibility

possibility()