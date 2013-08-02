import pymongo
from pymongo import Connection

def show_templates():
    db = Connection().poembot
    poems_collection = db.poems
    poems = poems_collection.find({})
    tempates = []
    for poem in poems:
        if not poem.get("template") in tempates:
            tempates.append(poem.get("template"))
    return tempates

def character_info():
	db = Connection().poembot
	character_collection = db.characters
	characters = character_collection.find({})
	character_map = {}
	for character in characters:
		character_map[character["char"]] = character["pronunciation"]
	return character_map["pronunciation"]

character_map = character_info()


