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

print len(show_templates())
for template in show_templates():
    print template
    