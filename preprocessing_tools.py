# -*- coding: utf-8 -*-
import re
import string


def dashrepl(matchobj):
    if matchobj.group(0) == '-': return ' '
    else: return '-'

# class Text  contains methods for text file preprocessing 
class Text():

    def __init__(self, input_file):
        self.text = input_file.read()
        
    def process_dots(self):
        self.text = self.text.replace('...', '.').replace('.', ' . ')
        return self
        
    def remove_inside_quatation(self):
        for opening_sign, closing_sign in [('\'', '\''),  ('<', '>')]:
            self.text = re.sub('{0}[^{1}]+{1}'.format(\
                        opening_sign, closing_sign), '', self.text)
        return self
       
    def remove_not_printable(self):
        self.text = filter(lambda x: x in string.printable, self.text)
        return self  

    def replace_repeated_hyphens(self):
        self.text = re.sub('-{2,}', dashrepl, self.text)
        return self
    
    def split(self):
        return self.text.split()

    # Create list of word triples
    def collect_triples(self, stopwords):
        punct = string.punctuation.replace('.', '') + string.whitespace + string.digits        
        
        words = [word.strip(punct).lower() for word in self.text.split() if word.strip(punct) != '']             
        words = filter(lambda x : x not in stopwords, words)
        
        return zip(iter(words), iter(words[1:]), iter(words[2:]))