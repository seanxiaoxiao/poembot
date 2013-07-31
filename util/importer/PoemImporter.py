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

def import_poems(poems):
    db = Connection().poembot
    poems_collection = db.poems
    poems_collection.insert(poems)

def import_templates(templates):
    db = Connection().poembot
    template_collection = db.templates
    template_collection.insert(templates)

def remove_poems():
    db = Connection().poembot
    db.drop_collection("poems")

def remove_templates():
    db = Connection().poembot
    db.drop_collection("templates")

remove_poems()
poems = read_poems(CI_RESOURCE_FIEL)
import_poems(poems)

remove_templates()
templates = read_template(CI_TEMPLATE_RESOURCE_FILE)
import_templates(templates)
