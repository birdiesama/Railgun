################################################################################
__Script__		= 'global_RG.general.module.compose_name'
__Author__		= 'Weerapot Chaoman'
__Version__		= 2.0
__Date__		= 20191212
################################################################################
import os, sys
__self_name__   = os.path.basename(__file__)
__self_path__   = ((os.path.realpath(__file__)).replace(__self_name__, '')).replace('\\', '/')
__project__     = 'Railgun'
################################################################################

import re
from collections import OrderedDict

class ComposeName(object):

    def __init__(self, *args, **kwargs):
        super(ComposeName, self).__init__(*args, **kwargs)

    def list_remove_blank(self, list):
        item_list = list
        for item in item_list:
            if item == '':
                item_list.remove('')
        return item_list

    def list_remove_duplicate(self, list):
        item_list = list
        item_dict = OrderedDict.fromkeys(list)
        item_list = item_dict.keys()
        return item_list

    def disect_word(self, word, splitter):
        # return disect_dict
        if splitter in word :
            disect_list = []
            word = word.replace(splitter, '_' + splitter + '_')
            split_list = word.split('_')
            split_list = self.list_remove_blank(split_list)
            disect_list.extend(split_list)
        else :
            return [word]
        return disect_list

    def disect_list(self, list, splitter):
        item_list = list
        new_item_list = []
        for item in item_list:
            disect_list = self.disect_word(item, splitter)
            new_item_list.extend(disect_list)
        return new_item_list

    def regex_list(self, list, regex, exception_regex='/[$-/:-?{-~!"^_`\[\]]/'):
        item_list = list
        regex = re.compile(regex)
        exception_regex = re.compile(exception_regex)
        new_item_list = []

        for item in item_list:
            # if match exception_regex
            if exception_regex.findall(item):
                new_item_list.append(item)
            else:
                match_object_list = regex.findall(item)
                match_object_list = self.list_remove_duplicate(match_object_list)
                match_object_list = self.list_remove_blank(match_object_list)
                if match_object_list:
                    split_list = [item]
                    for match_object in match_object_list:
                        split_list = self.disect_list(split_list, match_object)
                    split_list = self.list_remove_blank(split_list)
                    new_item_list.extend(split_list)
                else :
                    new_item_list.append(item)
        return new_item_list

    def _split(self, text):
        # remove special characters
        regex = re.compile('[a-zA-Z0-9]*')
        split_list = regex.findall(text)
        split_list = self.list_remove_blank(split_list)
        # begin disecting
        split_list = self.regex_list(split_list, '[v|V]$[0-9]+')
        split_list = self.regex_list(split_list, '[0-9]*', '[v|V]$[0-9]*')
        split_list = self.regex_list(split_list, '[A-Z]{2,}[^a-z]')
        split_list = self.regex_list(split_list, '[A-Z][a-z]+', '[A-Z]{2,}[^a-z]')
        return split_list

    def compose_snake_case(self, text, suffix=None):
        text_split = self._split(text)
        name = ''
        name += text_split[0].lower()
        if len(text_split) > 1:
            for text in text_split[1:]:
                name += '_' + text.lower()
        if suffix:
            name += '_' + suffix
        return name

    def compose_camel_case(self, text, suffix=None):
        text_split = self._split(text)
        name = ''
        name += text_split[0].lower()
        if len(text_split)>1:
            for text in text_split[1:]:
                name += text.capitalize()
        if suffix:
            name += '_' + suffix
        return name

    def compose_nice_name(self, text):
        text_split = self._split(text)
        name = ''
        name += text_split[0][0].upper() # first split
        if len(text_split[0]) > 1:
            name += text_split[0][1:]
        if len(text_split) > 1: # anything else
            for text in text_split[1:]:
                name += ' '
                name += text[0].upper()
                if len(name) > 1:
                    name += text[1:]
        return name
