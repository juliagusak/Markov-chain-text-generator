# -*- coding: utf-8 -*-


from worddict_tools import *
from path import *
from random import choice
import numpy as np


# class GeneratedText contains methods for text generation
# word_count - number of words to generate
# rang: for a fixed current word we choose a next word from the most frequent n = rang words 
# that can follow the current word (we choose according to the probability distribution)
class GeneratedText():
    def __init__(self, word_count, rang):
        self.sequence = []
        self.rang = rang
        self.word_count = word_count


    def choose_curr(self, data):
        curr =  choice(filter(lambda key : len(key) == 1 and key != ('.',), data.keys()))
        return curr

    def choose_nextt(self, curr, data):
        try:
            # nextt = data[curr][choice(range(1, self.rang)[ :len(data[curr]) - 1])]
            nextt_p = [float(el) for el in np.array(data[curr][1:])[:, 1]][:self.rang]
            nextt = data[curr][1:][np.random.choice(range(len(nextt_p)), p = nextt_p)]
        
        except:
            nextt = self.choose_curr(data)
        return (nextt[0],)
    
    def choose_after_nextt(self, pair, data):
        try:
            return self.choose_nextt(pair, data)
        except:
            return self.choose_nextt((pair[1],), data)

    def add(self, tuple):
        self.sequence.append(tuple[0])
        return self

    def generate(self, data):        
        
        curr = self.choose_curr(data)
        nextt = self.choose_nextt(curr, data)        
        self.add(curr).add(nextt)

        sentence = 2
        dot_counter = 0
        for i in xrange(self.word_count):
            
                pair = (curr[0], nextt[0])
                after_nextt = self.choose_after_nextt(pair, data)
                
                if after_nextt[0] == '.':
                    if sentence > 20:
                        curr = self.choose_curr(data)
                        nextt = self.choose_nextt(curr, data)                    
                       
                        self.add(('.',))
                        dot_counter += 1
                        sentence = 2
                        
                        if dot_counter == 5:
                            self.add(('\n',))
                            dot_counter = 0
                        self.add(curr).add(nextt)

                    else:
                        after_nextt = self.choose_after_nextt(pair, data)                    
                        self.add(after_nextt)

                        curr = nextt
                        nextt = after_nextt

                        sentence += 1
                else:
                    self.add(after_nextt)

                    curr = nextt
                    nextt = after_nextt

                    sentence += 1
        return self

    
def capitalize(sequence):
    sequence[0] = sequence[0].capitalize()
    for index in filter(lambda ind : sequence[ind] in ['.', '\n'] and ind < len(sequence) - 2, range(len(sequence))):
        sequence[index + 1] = sequence[index + 1].capitalize()
    sequence.append('.')
    return sequence

if __name__=='__main__':


    print "Loading word_frequency dict"
    word_frequency_dict = load(word_frequency_dict_path)

    print "Generating text"
    generated_sequence = GeneratedText(1000, 30).generate(word_frequency_dict).sequence
    generated_text = ' '.join(capitalize(generated_sequence)).replace(' . ', '. ')

    print "Saving generated text"
    with open(generated_text_path, 'w') as f:
        f.write(generated_text)