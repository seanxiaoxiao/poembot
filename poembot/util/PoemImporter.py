# -*- coding: utf-8 -*-
CI_RESOURCE_FIEL = "../../resource/ci-set-first"
CI_TEMPLATE_RESOURCE_FILE = "../../resource/ci-template"

import pymongo
from pymongo import Connection

def read_poems(path):
    with open(path, "r") as poem_file:
        results = []
        contents = poem_file.readlines()
        poem = {}
        for line in contents:
            line = line.strip()
            if len(line) == 0:
                if poem.get("template") and poem.get("author"):
                    results.append(poem)
                    poem = {}
            elif not poem.get("template"):
                components = line.split('-')
                poem["template"] = components[0]
                poem["author"] = components[1]
                if len(components) >= 3:
                    poem["title"] = components[2]
                if len(components) >= 4:
                    poem["summary"] = components[3]
                poem["contents"] = []
            else:
                poem["contents"].append(line)
        return results

def read_template(path):
    with open(path, "r") as template_file:
        results = []
        contents = template_file.readlines()
        template = {}
        for line in contents:
            line = line.strip()
            if len(line) == 0:
                if template.get("title"):
                    results.append(template)
                    template = {}
            elif not template.get("title"):
                template["title"] = line
                template["contents"] = []
            else:
                template["contents"].append(line)
        return results

def read_character(path):
    _vowel_map = vowel_map()
    _vowel_list = vowel_list()
    _vowel_tune_number = vowel_tune_number()

    with open(path, "r") as character_file:
        results = []
        contents = character_file.readlines()
        character = {}
        for line in contents:
            line = line.strip()
            components = line.split("\t")
            character["char"] = components[0]
            character["pronunciation"] = []
            for i in range(1, len(components)):
                pronunciations = components[i].split(',')
                for j in range(0, len(pronunciations)):
                    pronunciation = pronunciations[j]
                    character["pronunciation"].append(_format_pronunciation(pronunciation, _vowel_map, _vowel_list, _vowel_tune_number))
            results.append(character)
            character = {}
    return results

def _format_pronunciation(pronunciation, _vowel_map, _vowel_list, _vowel_tune_number):
    formatted = ""
    tune = 0
    for c in pronunciation.decode('utf8'):
        if c in _vowel_list:
            formatted += _vowel_map[c]
            tune = _vowel_tune_number[c]
        else:
            formatted += c
    formatted += str(tune)
    return formatted

def vowel_map():
    result = {}
    result[u'a'] = 'a'
    result[u'ā'] = 'a'
    result[u'á'] = 'a'
    result[u'ǎ'] = 'a'
    result[u'à'] = 'a'
    result[u'e'] = 'e'
    result[u'ē'] = 'e'
    result[u'é'] = 'e'
    result[u'ě'] = 'e'
    result[u'è'] = 'e'
    result[u'i'] = 'i'
    result[u'ī'] = 'i'
    result[u'í'] = 'i'
    result[u'ǐ'] = 'i'
    result[u'ì'] = 'i'
    result[u'o'] = 'o'
    result[u'ō'] = 'o'
    result[u'ó'] = 'o'
    result[u'ǒ'] = 'o'
    result[u'ò'] = 'o'
    result[u'u'] = 'u'
    result[u'ū'] = 'u'
    result[u'ú'] = 'u'
    result[u'ǔ'] = 'u'
    result[u'ù'] = 'u'
    result[u'v'] = 'v'
    result[u'ǘ'] = 'v'
    result[u'ǚ'] = 'v'
    result[u'ǜ'] = 'v'
    return result

def vowel_list():
    return [u'ā', u'á', u'ǎ', u'à', u'ē', u'é', u'ě', u'è', u'ī', u'í', u'ǐ', u'ì', u'ō', u'ó', u'ǒ', u'ò', u'ū', u'ú', u'ǔ', u'ù', u'ǘ', u'ǚ', u'ǜ']

def vowel_tune_number():
    result = {}
    result[u'ā'] = 1
    result[u'á'] = 2
    result[u'ǎ'] = 3
    result[u'à'] = 4
    result[u'ē'] = 1
    result[u'é'] = 2
    result[u'ě'] = 3
    result[u'è'] = 4
    result[u'ī'] = 1
    result[u'í'] = 2
    result[u'ǐ'] = 3
    result[u'ì'] = 4
    result[u'ō'] = 1
    result[u'ó'] = 2
    result[u'ǒ'] = 3
    result[u'ò'] = 4
    result[u'ū'] = 1
    result[u'ú'] = 2
    result[u'ǔ'] = 3
    result[u'ù'] = 4
    result[u'ǘ'] = 2
    result[u'ǚ'] = 3
    result[u'ǜ'] = 4
    return result

def import_poems(poems):
    db = Connection().poembot
    poems_collection = db.poems
    poems_collection.insert(poems)

def import_templates(templates):
    db = Connection().poembot
    template_collection = db.templates
    template_collection.insert(templates)

def import_characters(characters):
    db = Connection().poembot
    character_collection = db.characters
    character_collection.insert(characters)

def remove_poems():
    db = Connection().poembot
    db.drop_collection("poems")

def remove_templates():
    db = Connection().poembot
    db.drop_collection("templates")

def remove_characters():
    db = Connection().poembot
    db.drop_collection("characters")

def import_tokens(tokens):
    db = Connection().poembot
    token_collection = db.tokens
    token_collection.insert(tokens)

def remove_tokens():
    db = Connection.poembot
    db.drop_collection("tokens")



