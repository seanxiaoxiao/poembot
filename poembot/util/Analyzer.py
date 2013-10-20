# -*- coding: utf-8 -*-

from Query import show_poem_info
from Query import character_info
from Query import template_info

from util import is_ping_sound
from util import is_ze_sound
from util import preprocess_template

class PoemError:
    NO_TEMPLATE = 1
    CONTENT_MISMATCH = 2
    SENTENCE_MISMATCH = 3
    PRONUNCIATION_ERROR = 4

class PoemAnalyzer:

    def __init__(self):
        self.templates = template_info()
        for template in self.templates:
            preprocess_template(template)
        self.char_info = character_info()

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

    def _sentence_match(self, poem, template):
        setence_errors = []
        for i in range(len(template.get("contents"))):
            for j in range(len(template.get("contents")[i])):
                if template.get("contents")[i][j] == '1' or template.get("contents")[i][j] == '4':
                    if not is_ping_sound(self.char_info.get(poem.get("contents")[i][j])):
                        setence_errors.append({"code": PoemError.PRONUNCIATION_ERROR, "poem_id": poem.get("_id"),
                                "wrong_chars": poem.get("contents")[i][j], "actual": poem.get("contents")[i][j]})
                if template.get("contents")[i][j] == '2' or template.get("contents")[i][j] == '5':
                    if not is_ze_sound(self.char_info.get(poem.get("contents")[i][j])):
                        setence_errors.append({"code": PoemError.PRONUNCIATION_ERROR, "poem_id": poem.get("_id"),
                                "wrong_chars": poem.get("contents")[i][j], "actual": poem.get("contents")[i][j]})
        return setence_errors
            

    def _general_match(self, poem, template):
        errors = []
        if not template:
            errors.append({"code": PoemError.NO_TEMPLATE, "template": poem.get("template"), "poem_id": poem.get("_id")})
        elif len(template.get("contents")) != len(poem.get("contents")):
            errors.append({"code": PoemError.CONTENT_MISMATCH, "poem_id": poem.get("_id"),
                    "content_len": len(poem.get("contents")), "template_len": len(poem.get("template"))})
        if template:
            for i in range(len(template.get("contents"))):
                if len(template.get("contents")[i]) != len(poem.get("contents")[i]):
                    errors.append({"code": PoemError.SENTENCE_MISMATCH, "sentence": poem.get("contents")[i],
                        "template": poem.get("template"), "sentence_seq": i, "poem_id": poem.get("_id"),
                        "expect": len(template.get("contents")[i]), "acctual": len(poem.get("contents")[i])})
        return errors

    def match_poem(self, poem):
        template = self._find_template(poem.get("template"))
        return self._general_match(poem, template) or self._sentence_match(poem, template)

poem_analyzer = PoemAnalyzer()
poems = show_poem_info()
for poem in poems:
    errors = poem_analyzer.match_poem(poem)
    if errors:
        for error in errors:
            print error.get("poem_id")
            print error.get("code")
        


