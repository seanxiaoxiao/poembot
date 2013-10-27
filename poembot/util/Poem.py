# -*- coding: utf-8 -*-

from Query import show_poem_info, character_info, template_info
from util import preprocess_template

templates = template_info()

templates_map = {}
for template in templates:
    if not templates_map.get(template.get('title')):
        templates_map[template.get('title')] = []
    templates_map[template.get('title')].append(template)

poems_info = show_poem_info()

print len(poems_info)

missing_template = {}

class Poem:

    def __init__(self, poem):
        self.poem = poem;
        self.templates = []

    def addTemplate(self, templates):
        for template in templates:
            preprocess_template(template)
            self.templates.append(template)

    def validate(self):
        for template in self.templates:
            if self.match_length(template):
                print template.get("title")
                break

    def match_length(self, template):
        poem_character_count = 0
        for content in self.poem.get("contents"):
            poem_character_count += len(content)
        self.print_poem()
        print "Poem has count %d vs template count %d" % (poem_character_count, template.get("count"))
        return template.get("count") == poem_character_count

    def _validate_length(self, template):
        pass

    def print_poem(self):
        pass
        # if not missing_template.get(self.poem.get("template")):
        #     missing_template[self.poem.get("template")] = self.poem.get("template")
        print u"ID is %s" % self.poem.get("_id")
        print u"词牌: %s" % self.poem.get("template")
        for content in self.poem.get("contents"):
          print content

poems = []

for poem_info in poems_info:
    poem_instance = Poem(poem_info)
    matched_templates = templates_map.get(poem_info.get("template"))
    if matched_templates:
        poem_instance.addTemplate(matched_templates)
    if len(poem_instance.templates) == 1:
        # poem_instance.print_poem()
        poem_instance.validate()
    poems.append(poem_instance)

