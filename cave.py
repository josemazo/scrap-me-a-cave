# -*- coding: utf-8 -*-

import re


class Cave(object):

    _regex_spaces = r'[ ]{21}'

    def __init__(self, price=0, meters=0, description='', url='',
                 service_url=''):
        self.price = price
        self.meters = meters
        # 'description' is the only possible attribute with 'special' chars
        self.description = description.encode('unicode_escape')
        self.url = url
        self.service_url = service_url

    def __str__(self):
        message = '''Founded a new cave!
                     Price: {0} euros
                     Meters: {1} m2
                     Description: {2}
                     <a href="{3}">Link</a>
                     <a href="{4}">Search link</a>

                     Good luck!'''

        message = message.format(self.price, self.meters, self.description,
                                 self.url, self.service_url)
        message = re.sub(self._regex_spaces, '', message)
        return message

    def __unicode__(self):
        return self.__str__().decode('unicode-escape')

    def __repr__(self):
        return self.__str__()
