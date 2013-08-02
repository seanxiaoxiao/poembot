# -*- coding: utf-8 -*-
from Query import show_poem_info
from Query import character_info

def analyze_poems():
	poems = show_poem_info()
	characters = character_info()
	for poem in poems:
		for content in poem["contents"]:
			for char in content:
				if char not in characters and \
					not (char == u'，' or char == u'、' or char == u'。' or char == u'！' or char == u'？' or char == u'；'):
					print char 

analyze_poems()

