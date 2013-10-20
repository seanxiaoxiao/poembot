# -*- coding: utf-8 -*-

from Query import show_poem_info, character_info, template_info
from util import preprocess_template

templates = template_info()
poems_info = show_poem_info()

missing_template = {}

class Poem:

    def __init__(self, poem):
        self.poem = poem;
        self.templates = []

    def addTemplate(self, template):
        preprocess_template(template)
        self.templates.append(template)

    def validate(self):
        pass

    def _validate(self, template):
        pass

    def print_poem(self):
        # if not missing_template.get(self.poem.get("template")):
        #     missing_template[self.poem.get("template")] = self.poem.get("template")
        # # print u"词牌: %s" % self.poem.get("template")
        # for content in self.poem.get("contents"):
        #   print content

poems = []

for poem_info in poems_info:
    poem_instance = Poem(poem_info)
    for template in templates:
        if template.get("title") == poem_info.get("template"):
            poem_instance.addTemplate(template)
    if len(poem_instance.templates) == 0:
        poem_instance.print_poem()
    poems.append(poem_instance)

for template in missing_template.values():
    print template

print len(missing_template)