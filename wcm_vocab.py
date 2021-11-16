from collections import defaultdict
from _vocab import BaseVocab

class Vocabulary(BaseVocab):

    def __init__(self, max_size):
        super().__init__(max_size)

    def add(self, word):
        if not self.is_full():
            self.table[word.word] = word
            self.table[word.word].counter += 1
            self.current_size += 1
    
    def __getitem__(self, word):
        if word in self.table:
            return self.table[word]
        return self.table['unk']



class Context(BaseVocab):

    def __init__(self, c_size):
        super().__init__(c_size)
        self.counter = 1

    def add(self, word):
        if len(self) == 0:
                self.table['unk'] = 0 
        if word not in self.table and not self.is_full(): 
            self.table[word] = self.counter
            self.counter += 1


class WordRep:

    def __init__(self, word, c_size):
        self.word = word
        self.c_size = c_size
        self.c_counter = 0
        # save counter between target and its contexts
        self.contexts = defaultdict(int)
        # for tracking number of tweets that appears
        #self.num_tweets = 0
        self.counter = 0
        
    def is_empty(self):
        return self.c_counter == 0

    def is_full(self):
        return self.c_counter == self.c_size

    def add_context(self, context):
        if context in self.contexts or self.is_full():
            if context in self.contexts:
                self.contexts[context] += 1
            else:
                self.contexts['unk'] += 1
        elif self.c_counter + 1 == self.c_size:
            self.contexts['unk'] += 1
            self.c_counter += 1
        else:
            self.contexts[context] += 1
            self.c_counter += 1

    def __len__(self):
        return len(self.contexts.keys())

    def __repr__(self):
        return self.word

    def __getitem__(self, context):
        return self.contexts[context]