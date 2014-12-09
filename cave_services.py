import abc
import re
import urllib2

from cave import Cave

from lxml import html


class CaveService(object):

    _user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
                  '(KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36'
    _regex_number = re.compile("[0-9]+")
    _regex_namespace = {'re': 'http://exslt.org/regular-expressions'}

    def __init__(self, search_url='', search_description=''):
        self.search_url = search_url
        self.search_description = search_description

        headers = {
            'User-Agent': self._user_agent
        }
        self._opener = urllib2.build_opener()
        self._opener.addheaders = headers.items()

    @abc.abstractmethod
    def search_caves(self, old_caves=[]):
        return


class IdealistaService(CaveService):

    def search_caves(self, old_caves=[]):
        new_caves = []

        data_html = self._opener.open(self.search_url).read()
        dom = html.fromstring(data_html)

        caves = dom.xpath('.//li[re:test(@id, "[0-9]+")]',
                          namespaces=self._regex_namespace)
        caves = {cave.attrib['id']: cave for cave in caves}

        # A solution with a comprehension will use another for ;)
        for cave_id in caves:
            if cave_id not in old_caves:
                new_cave = caves[cave_id]

                price = new_cave.xpath('.//li[@class="col-0"]')[0].text
                price = self._regex_number.findall(price)[0]

                meters = new_cave.xpath('.//li[@class="col-1"]')[0].text
                meters = self._regex_number.findall(meters)[0]

                description = new_cave.xpath(
                    './/a[@href="/inmueble/{0}/"]'.format(
                        new_cave.attrib['id']))[1].text.strip()

                url = 'http://idealista.com/inmueble/{0}/'.format(
                    new_cave.attrib['id'])

                new_cave_obj = Cave(price, meters, description, url,
                                    self.search_url)
                new_caves.append(new_cave_obj)

        return new_caves


class SegundaManoService(CaveService):

    def search_caves(self, old_caves=[]):
        new_caves = []

        data_html = self._opener.open(self.search_url).read()
        dom = html.fromstring(data_html)

        caves = dom.xpath('.//ul[re:test(@id, "[0-9]+")]',
                          namespaces=self._regex_namespace)
        caves = {cave.attrib['id']: cave for cave in caves}

        # A solution with a comprehension will use another for ;)
        for cave_id in caves:
            if cave_id not in old_caves:
                new_cave = caves[cave_id]

                price = new_cave.xpath('.//a[@class="subjectPrice"]')[0].text
                price = self._regex_number.findall(price)[0]

                try:
                    meters = new_cave.xpath(
                        './/div[@class="infoBottom"]/text()')[3]
                    meters = self._regex_number.findall(meters)[0]
                except:
                    meters = 'not available'

                description = new_cave.xpath(
                    './/a[@class="subjectTitle"]')[0].text.strip()

                url = new_cave.xpath(
                    './/a[@class="subjectTitle"]')[0].attrib['href']

                new_cave_obj = Cave(price, meters, description, url,
                                    self.search_url)
                new_caves.append(new_cave_obj)

        return new_caves
