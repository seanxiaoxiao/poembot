# -*- coding: utf-8 -*-
import pymongo
from pymongo import Connection

def show_templates():
    db = Connection().poembot
    poems_collection = db.poems
    poems = poems_collection.find({})
    templates = []
    for poem in poems:
        if not poem.get("template") in templates:
            templates.append(unicode(poem.get("template")))
    return templates

def show_poem_info():
    db = Connection().poembot
    poems_collection = db.poems
    return [poem for poem in poems_collection.find({})]

def template_info():
    db = Connection().poembot
    template_collection = db.templates
    return [template for template in template_collection.find({})]

def character_info():
    db = Connection().poembot
    character_collection = db.characters
    characters = character_collection.find({})
    character_map = {}
    for character in characters:
        character_map[character["char"]] = character["pronunciation"]
    return character_map

# character_map = character_info()


