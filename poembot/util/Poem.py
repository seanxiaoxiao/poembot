# -*- coding: utf-8 -*-

from Query import show_poem_info, character_info, template_info
from Query import find_poems_by_template, find_templates_by_title
from util import preprocess_template, is_ping_sound, is_ze_sound
import re
import string

templates = template_info()
characters = character_info()

templates_map = {}
for template in templates:
    if not templates_map.get(template.get('title')):
        templates_map[template.get('title')] = []
    templates_map[template.get('title')].append(template)

poems_info = find_poems_by_template(u'满江红')

missing_template = {}

p = re.compile(u"，|。|、", re.UNICODE)


class Poem:

    def __init__(self, poem):
        self.poem = poem
        self.templates = []
        self._preprocess_poem()
        self.incorrect_chars = []
        self.is_valid = True

    def _preprocess_poem(self):
        self.poem["refined_contents"] = []
        for content in self.poem.get("contents"):
            refined_contents = p.split(content)
            for refined_content in refined_contents:
                if len(refined_content) != 0:
                    self.poem["refined_contents"].append(refined_content)

    def add_template(self, templates):
        for template in templates:
            preprocess_template(template)
            self.templates.append(template)

    def validate(self):
        for template in self.templates:
            if self.match_length(template):
                self.is_valid = True
                self.match_rhythm(template)
            else:
                self.is_valid = False

    def match_length(self, template):
        if len(self.poem.get("refined_contents")) != len(template.get("refined_contents")):
            return False
        contents_length = len(self.poem.get("refined_contents"))
        for i in range(0, contents_length):
            poem_content = self.poem.get("refined_contents")[i]
            template_content = template.get("refined_contents")[i]
            if len(poem_content) != len(template_content):
                return False
        return True

    def match_rhythm(self, template):
        contents_length = len(self.poem.get("refined_contents"))
        for i in range(0, contents_length):
            poem_content = self.poem.get("refined_contents")[i]
            template_content = template.get("refined_contents")[i]
            content_length = len(poem_content)
            for j in range(0, content_length):
                poem_char = poem_content[j]
                template_char = template_content[j]
                rule_code = int(template_char, 16)
                character = characters.get(poem_char)
                if not character:
                    continue
                if rule_code % 5 == 0 or rule_code % 5 == 3:
                    if not is_ping_sound(character):
                        self.incorrect_chars.append(poem_char)
                elif rule_code % 5 == 1 or rule_code % 5 == 4:
                    if not is_ze_sound(character):
                        self.incorrect_chars.append(poem_char)
                if rule_code >= 10 and i > 0 and template.get("refined_contents")[i - 1][j] >= 10:
                    if poem_char != self.poem.get("refined_contents")[i - 1][j]:
                        self.incorrect_chars.append(poem_char)

    def print_poem(self):
        print u"ID is %s" % self.poem.get("_id")
        print u"词牌: %s" % self.poem.get("template")
        for content in self.poem.get("contents"):
            print content
        print u"Incorrect words: " + string.join(self.incorrect_chars, ",")

    def is_perfect_poem(self):
        return self.is_valid and len(self.incorrect_chars) == 0

poems = []

for poem_info in poems_info:
    poem_instance = Poem(poem_info)
    matched_templates = templates_map.get(poem_info.get("template"))
    if matched_templates:
        poem_instance.add_template(matched_templates)
    if len(poem_instance.templates) >= 0:
        poem_instance.validate()
        if len(poem_instance.incorrect_chars) > 0:
            poem_instance.print_poem()
    poems.append(poem_instance)

