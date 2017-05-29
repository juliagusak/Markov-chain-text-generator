# -*- coding: utf-8 -*-
from collections import defaultdict
import os
from preprocessing_tools import *
import cPickle as pkl
from path import *
import numpy as np

# class WordDict is created to count the occurence of word combinations.
# WordDict.word_dict - {current word combination: {next word : occurence of next word}}, where 
# current word combination - (word1, ) or (word1, word2),
# next word - word that follows the current word combination,
# occurence of next word - occurence of sequence (current word combination, next word).
class WordDict():
    def __init__(self):
        self.word_dict = defaultdict(lambda : defaultdict(int))
        self.word_count = 0
    
    def update(self, word_triples):                     
        for first_word, second_word, third_word in word_triples:
            self.word_dict[(first_word,)][second_word] += 1
            self.word_dict[(first_word, second_word)][third_word] += 1
            
        self.word_count += (len(word_triples) + 2)
        return self



# Collect word statistics from one folder from the corpus
def collect_dict_from_author(author_path, stopwords, word_dict):
       
    for file_name in os.listdir(author_path):
        if '~' not in file_name:
            print 'FILE NAME : {}'.format(file_name)
            
            with open(author_path + '/{}'.format(file_name), 'r') as input_file:
            
                text = Text(input_file)
                text = text.process_dots().remove_inside_quatation(\
                        ).remove_not_printable().replace_repeated_hyphens()
                         
                word_dict.update(text.collect_triples(stopwords))

            
            
# Collect word statistics from the whole corpus 
def collect_dict_from_corpus(corpus_path, stopwords):
    word_dict = WordDict()

    for directory_name in os.listdir(corpus_path):
        author_path = os.path.join(corpus_path, directory_name)

        if author_path == corpus_path + '/asimov':
        # if os.path.isdir(author_path):        
            collect_dict_from_author(author_path, stopwords, word_dict)
    print "COLLECTED"
    return word_dict
    


def sort_pairs_by_frequency(tuple):
    return tuple[1]

# Convert (current word combination, {next word : occurence of next word}}) to 
# (current word combination, occurence of current word combination, {next word : frequency of next word})
def convert_dict_element(elem, words_count):
    try:
        yield elem[0][0], elem[0][1]
    except:
        yield elem[0][0],
        
    summ = float(sum(elem[1].values()))+0.00000001
    l = []
    for k in elem[1].keys():
        l.append((k, elem[1][k]/summ))
    l = np.array(l)
    yield np.append([summ/words_count], sorted(l, key = sort_pairs_by_frequency, 
        reverse = True))



def convert_dict(word_dict_items):
    words_count = sum([sum(elem[1].values()) for elem in word_dict_items if len(elem[0]) == 1]) 
    return dict([convert_dict_element(elem, words_count) for elem in word_dict_items])



def save_dict_items(file_name, dictt):
    with open(file_name, 'wb') as f:
        pkl.dump(dictt.items(), f, protocol = 2)

def save_dict(file_name, dictt):
    with open(file_name, 'wb') as f:
        pkl.dump(dictt, f, protocol = 2)

def load(file_name):
    with open(file_name, 'rb') as f:
        return pkl.load(f)


if __name__=='__main__':
    with open(stopwords_path, 'r') as f:
        stopwords = f.read().split()

    print "Collecting word dict"
    word_dict = collect_dict_from_corpus(corpus_path, stopwords)

    # print "Saving word dict"
    # save_dict_items(word_dict_path, word_dict.word_dict)
    
    print "Converting word dict to word_frequency dict" 
    word_frequency_dict = convert_dict(word_dict.word_dict.items())

    del word_dict

    print "Saving word_frequency dict"
    save_dict(word_frequency_dict_path, word_frequency_dict)