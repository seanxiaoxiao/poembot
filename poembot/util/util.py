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
                

def is_ping_sound(character):
    for pronunciation in character.get("pronunciation"):
        tune = pronunciation[len(pronunciation) - 1]
        tune = int(tune[len(tune) - 1])
        if tune == 1 or tune == 2 or tune == 0:
            return True
    return False

def is_ze_sound(character):
    for pronunciation in character.get("pronunciation"):
        tune = pronunciation[len(pronunciation) - 1]
        tune = int(tune[len(tune) - 1])
        if tune == 3 or tune == 4 or tune == 0:
            return True
    return False

def _analyse_content(contents):
    contents_after_split = p.split(contents)
    for content in contents_after_split:
        if len(content) == 0:
            continue

        current_char = content[0]
        if current_char in characters:
            if not character_posibility.get(current_char):
                character_posibility[current_char] = {"count": 0, "suffixes": [], "leading_count": 0}
            character_posibility[current_char]["count"] += 1

        for i in range(0, len(content) - 1):
            current_char = content[i]
            next_char = content[i + 1]
            if current_char in characters and next_char in characters:
                if not character_posibility.get(current_char):
                    character_posibility[current_char] = {"count": 0, "suffixes": [], "leading_count": 0}
                if i == 0:
                    character_posibility[current_char]["leading_count"] += 1
                character_posibility[current_char]["count"] += 1
                new_suffix = True
                for suffix in character_posibility[current_char]["suffixes"]:
                    if suffix.get("char") == next_char:
                        suffix["count"] += 1
                        new_suffix = False
                        break
                if new_suffix:
                    character_posibility[current_char]["suffixes"].append({"char": next_char, "count": 1})
            else:
                pass

def possibility():
    poems = show_poem_info()
    for poem in poems:
        contents = poem.get("contents")
        for content in contents:
            _analyse_content(content)
    sorted_character_posibility = sorted(character_posibility.iteritems(), key=lambda x: x[1].get("count"))
    for item in sorted_character_posibility:
        sorted(item[1].get("suffixes"), key=lambda x: x.get("count"))
    return sorted_character_posibility

def possibility_to_tokens():
    poems = show_poem_info()
    for poem in poems:
        contents = poem.get("contents")
        for content in contents:
            _analyse_content(content)
    tokens = []
    for key in character_posibility:
        char_info = character_posibility.get(key)
        single_word_token = {}
        single_word_token["content"] = key
        single_word_token["count"] = char_info.get("count")
        single_word_token["leading_count"] = char_info.get("leading_count")
        tokens.append(single_word_token)
        for suffix in char_info.get("suffixes"):
            token = {}
            token["content"] = key + suffix.get("char")
            token["count"] = suffix.get("count")
            tokens.append(token)
    import_tokens(tokens)

