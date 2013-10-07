# coding=utf8

import urllib2
from BeautifulSoup import BeautifulSoup
from PoemImporter import remove_templates
from PoemImporter import import_templates
from PoemImporter import remove_poems
from PoemImporter import import_poems


TEMPLATE_ROOT_URL = "http://longyusheng.org/cipai/mulu.html"
POEM_ROOT_URL = "http://www.guoxue.com/qsc/qscml%d.htm"


def parse_poem_root():
    for i in range(1, 26):
        url = POEM_ROOT_URL % i
        print url
        content_stream = urllib2.urlopen(url)
        content = content_stream.read()
        soup = BeautifulSoup(content.decode('gb2312','ignore'))
        blockquotes = soup.body.findAll('blockquote')
        for blockquote in blockquotes:
            links = blockquote.findAll('a')
            for link in links:
                author = link.text
                try:
                    poem_url = "http://www.guoxue.com/qsc/" + link.get('href')
                    poems = parse_poem(poem_url)
                    import_poems(poems)
                except:
                    pass

def parse_poem(url):
    print url
    content_stream = urllib2.urlopen(url)
    content = content_stream.read()
    soup = BeautifulSoup(content.decode('gb2312','ignore'))
    paragraphs = soup.body.findAll('p', {'align': 'center'})
    poems = []
    for paragraph in paragraphs:
        poem = {}
        template_with_title = paragraph.text
        index = template_with_title.find(u'（')
        if index >= 0:
            poem['template'] = template_with_title[0: index]
            end_index = template_with_title.find(u'）')
            poem['title'] = template_with_title[index + 1: end_index]
        else:
            poem['template'] = template_with_title
        poem['contents'] = paragraph.findNextSibling().text.split('&nbsp;&nbsp;&nbsp;&nbsp;')[1:]
        poems.append(poem)
    return poems

def parse_template_root():
    templates = []
    content_stream = urllib2.urlopen(TEMPLATE_ROOT_URL)
    content = content_stream.read()
    soup = BeautifulSoup(content.decode('gb2312','ignore'))
    spans = soup.body.findAll('span', {'class': 'item'})

    for span in spans:
        titles = []
        link = span.find('a')
        href = link.get('href')
        titles.append(link.text)
        alias_span = span.find('span')
        if alias_span:
            titles.extend(alias_span.text[1:-1].split(u'、'))
        for title in titles:
            print title
        template_url = "http://longyusheng.org/" + href[3:]
        template_infos = parse_template(template_url)
        for contents in template_infos:
            count = 0
            for content in contents:
                for char in content:
                    if char == u'中' or char == u'仄' or char == u'平':
                        count += 1

            for title in titles:
                template = {}
                template['title'] = title
                template['contents'] = contents
                template['count'] = count
                templates.append(template)

    return templates

def parse_template(url):
    content_stream = urllib2.urlopen(url)
    content = content_stream.read()
    soup = BeautifulSoup(content.decode('gb2312','ignore'))
    blockquotes = soup.body.findAll('blockquote')
    template_infos = []
    for blockquote in blockquotes:
        contents = []
        templates_divs = blockquote.findAll('div')
        for div in templates_divs:
            if not div.get('class'):
                contents.append(div.text)
        template_infos.append(contents)
    return template_infos

remove_poems()
parse_poem_root()

# remove_templates()
# templates = parse_template_root()
# import_templates(templates)
