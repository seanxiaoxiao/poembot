# -*- coding: utf-8 -*-
from Query import show_poem_info, character_info, template_info
from PoemImporter import import_tokens
import re
import operator

characters = character_info()
character_posibility = {}

p = re.compile(u"，|。|、", re.UNICODE)
template_rule_pattern = re.compile("[0-9|A-E]+", re.UNICODE)


def preprocess_template(template):
    if template.get("refined_contents"):
        return
    template["refined_contents"] = []
    for content in template.get("contents"):
        refined_contents = p.split(content)
        for refined_content in refined_contents:
            if len(refined_content) > 0:
                refined_content = refined_content.replace(u'仄（增韵）', '4')
                refined_content = refined_content.replace(u'平（增韵）', '3')
                refined_content = refined_content.replace(u'仄（韵）', '4')
                refined_content = refined_content.replace(u'平（韵）', '3')
                refined_content = refined_content.replace(u'中', '2')
                refined_content = refined_content.replace(u'平', '0')
                refined_content = refined_content.replace(u'仄', '1')
                refined_content = refined_content.replace(u'去', '1')
                if refined_content.find(u'『') >= 0 or refined_content.find(u'』') >= 0:
                    new_refined_content = ""
                    for char in refined_content:
                        try:
                            if int(char) in range(0, 5):
                                new_refined_content += str((int(char) + 5))
                        except:
                            pass
                    template["refined_contents"].append(new_refined_content)
                elif refined_content.find(u'〖') >= 0 and refined_content.find(u'〗') >= 0:
                    new_refined_content = ""
                    for char in refined_content:
                        try:
                            if int(char) in range(0, 5):
                                new_refined_content += "%x" % (int(char) + 10)
                        except:
                            pass
                    last_rule = template["refined_contents"][len(template["refined_contents"]) - 1]
                    new_last_rule = ""
                    for char in last_rule:
                        try:
                            if int(char) in range(0, 5):
                                new_last_rule += "%x" % (int(char) + 10)
                        except:
                            pass
                    if len(new_last_rule) == len(last_rule):
                        template["refined_contents"][len(template["refined_contents"]) - 1] = new_last_rule
                    template["refined_contents"].append(new_refined_content)
                elif refined_content.find(u'〖') >= 0 or refined_content.find(u'〗') >= 0:
                    new_refined_content = ""
                    for char in refined_content:
                        try:
                            if int(char) in range(0, 5):
                                new_refined_content += "%x" % (int(char) + 10)
                        except:
                            pass
                    template["refined_contents"].append(new_refined_content)
                else:                    
                    template["refined_contents"].append(refined_content)
                

def is_ping_sound(pronunciation):
    tune = pronunciation[len(pronunciation) - 1]
    tune = int(tune[len(tune) - 1])
    return tune == 1 or tune == 2 or tune == 0

def is_ze_sound(pronunciation):
    tune = pronunciation[len(pronunciation) - 1]
    tune = int(tune[len(tune) - 1])
    return tune == 3 or tune == 4 or tune == 0

def _analyse_content(poem, contents):
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
    return sorted_character_posibility

def possibility_to_tokens():
    poems = show_poem_info()
    for poem in poems:
        contents = poem.get("contents")
        for content in contents:
            _analyse_content(poem, content)
    tokens = []
    for key in character_posibility:
        char_info = character_posibility.get(key)
        for prefix in char_info.get("prefixs"):
            token = {}
            token["content"] = prefix.get("char") + key
            token["count"] = prefix.get("count")
            tokens.append(token)
    import_tokens(tokens)

possibility_to_tokens()
