# -*- coding: utf-8 -*-
CI_RESOURCE_FIEL = "../../resource/ci-set-first"

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
            elif not poem.get("content-first"):
                poem["content-first"] = line
            else:
                poem["content-second"] = line
        return results

def import_poems(poems):
    db = Connection().poembot
    poems_collection = db.poems
    poems_collection.insert(poems)

def remove_poems():
    db = Connection().poembot
    db.drop_collection("poems")

remove_poems()
poems = read_poems(CI_RESOURCE_FIEL)
import_poems(poems)