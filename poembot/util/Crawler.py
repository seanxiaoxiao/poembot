# coding=utf8

import urllib2
from BeautifulSoup import BeautifulSoup
from PoemImporter import remove_templates
from PoemImporter import import_templates

ROOT_URL = "http://longyusheng.org/cipai/mulu.html"


def parse_root():
    templates = []
    content_stream = urllib2.urlopen(ROOT_URL)
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

remove_templates()
templates = parse_root()
import_templates(templates)
