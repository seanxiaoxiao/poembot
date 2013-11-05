from optparse import OptionParser
from optparse import OptionGroup
import sys

from PoemImporter import remove_templates, import_templates, import_characters
from PoemImporter import remove_poems, remove_characters, read_character
from Crawler import parse_template_root, parse_poem_root

CI_CHARACTER_FILE = "../../resource/pinyin.txt"

def import_character():
    print "Begin Importing Characters"
    remove_characters()
    characters = read_character(CI_CHARACTER_FILE)
    import_characters(characters)
    print "End Importing Characters"

def import_template():
    print "Begin Importing Templates"
    remove_templates()
    templates = parse_template_root()
    import_templates(templates)
    print "End Importing Templates"

def import_poem():
    print "Begin Importing Poems"
    remove_poems()
    parse_poem_root()
    print "End Importing Poems"

def import_all():
    import_character()
    import_template()
    import_poem()


if __name__ == '__main__':
    usage = "usage: %prog -[c|t|p|a]"
    parser = OptionParser(usage=usage)

    group = OptionGroup(parser, "Import Options", "Import the raw data for Poembot")
    group.add_option("-c", action="store_true", help="Import all the character information")
    group.add_option("-t", action="store_true", help="Import all the template information")
    group.add_option("-p", action="store_true", help="Import all the poem information")
    group.add_option("-a", action="store_true", help="Import all the information")
    parser.add_option_group(group)

    (options, args) = parser.parse_args()
    if options.a:
        import_all()
    elif options.c:
        import_character()
    elif options.t:
        import_template()
    elif options.p:
        import_poem()
    else:
        parser.print_usage()
