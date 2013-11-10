from optparse import OptionParser
from optparse import OptionGroup
import sys

from PoemImporter import remove_templates, import_templates, import_characters
from PoemImporter import remove_poems, remove_characters, read_character, remove_tokens
from Crawler import parse_template_root, parse_poem_root
from util import possibility_to_tokens

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

def preprocess_data():
    print "Preprocess the poem data"
    remove_tokens()
    possibility_to_tokens()
    print "Finish processing data"

def import_all():
    import_character()
    import_template()
    import_poem()


if __name__ == '__main__':
    usage = "usage: %prog -[c|t|p|a]"
    parser = OptionParser(usage=usage)

    group_import = OptionGroup(parser, "Import Options", "Import the raw data for Poembot")
    group_import.add_option("-c", action="store_true", help="Import all the character information")
    group_import.add_option("-t", action="store_true", help="Import all the template information")
    group_import.add_option("-p", action="store_true", help="Import all the poem information")
    group_import.add_option("-a", action="store_true", help="Import all the information")

    group_preprocess = OptionGroup(parser, "Preprocess Data", "Preprocess with existing data")
    group_preprocess.add_option("-d", action="store_true", help="Preprocess with existing data")
    parser.add_option_group(group_import)
    parser.add_option_group(group_preprocess)

    (options, args) = parser.parse_args()
    if options.a:
        import_all()
    elif options.c:
        import_character()
    elif options.t:
        import_template()
    elif options.p:
        import_poem()
    elif options.d:
        preprocess_data()
    else:
        parser.print_usage()
