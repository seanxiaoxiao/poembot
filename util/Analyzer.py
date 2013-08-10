# -*- coding: utf-8 -*-

from Query import show_poem_info
from Query import character_info
from Query import template_info

from util import is_ping_sound
from util import is_ze_sound

class PoemError:
    NO_TEMPLATE = 1
    CONTENT_MISMATCH = 2
    PRONUNCIATION_ERROR = 3

class PoemAnalyzer:

    def __init__(self):
        self.templates = template_info()

    def analyze_poems(self):
        poems = show_poem_info()
        for poem in poems:
            for content in poem["contents"]:
                for char in content:
                    if char not in characters and \
                        not (char == u'，' or char == u'、' or char == u'。' or char == u'！' or char == u'？' or char == u'；'):
                        print char 

    def _find_template(self, title):
        for template in self.templates:
            if template.get("title") == title:
                return template

    def match_poem(self, poem):
        template = self._find_template(poem.get("template"))
        error = {}
        error["wrong_chars"] = []
        if not template:
            error["code"] = PoemError.NO_TEMPLATE
            error["template"] = poem.get("template")
            return error
        if len(template.get("contents")) != len(poem.get("contents")):
            error["code"] = PoemError.CONTENT_MISMATCH
            error["expect"] = len(template.get("contents"))
            error["acctual"] = len(poem.get("contents"))
            return error
        for i in range(len(template.get("contents"))):
            if len(template.get("contents")[i]) != len(poem.get("contents")[i]):
                error["code"] = PoemError.CONTENT_MISMATCH
                error["expect"] = len(template.get("contents")[i])
                error["acctual"] = len(poem.get("contents")[i])
                return error
        for i in range(len(template.get("contents"))):
            for j in range(len(template.get("contents")[i])):
                if template.get("contents")[i][j] == 1 or template.get("contents")[i][j] == 4:
                    if not is_ping_sound(poem.get("contents")[i][j]):
                        error["code"] = PoemError.PRONOCIATION_ERROR
                        error["wrong_chars"].append(poem.get("contents")[i][j])
                if template.get("contents")[i][j] == 2 or template.get("contents")[i][j] == 5:
                    if not is_ze_sound(poem.get("contents")[i][j]):
                        error["code"] = PoemError.PRONOCIATION_ERROR
                        error["wrong_chars"].append(poem.get("contents")[i][j])
        return error

poem_analyzer = PoemAnalyzer()
poems = show_poem_info()
for poem in poems:
    error = poem_analyzer.match_poem(poem)
    if error:
        print poem["template"]
        print poem["author"]
        print error
        print


