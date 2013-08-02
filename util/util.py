# -*- coding: utf-8 -*-
def is_ping_sound(pronunciation):
	tune = pronunciation[len(pronunciation) - 1]
	return tune == 1 or tune == 2 or tune == 0

def is_ze_sound(pronunciation):
	tune = pronunciation[len(pronunciation) - 1]
	return tune == 3 or tune == 4 or tune == 0
