import numpy as np

from base.iwv import IncrementalWordVector
from river.utils import VectorDict

from iwcm.wcm_vocab import Vocabulary, Context, WordRep


class WordContextMatrix(IncrementalWordVector):

    def __init__(
        self, 
        v_size, 
        c_size, 
        w_size, 
        normalize=True,
        on=None,
        strip_accents=True,
        lowercase=True,
        preprocessor=None,
        tokenizer=None,
        ngram_range=(1, 1),
        is_ppmi=True
    ):
        super().__init__(
            v_size,
            c_size,
            w_size,
            on=on,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            ngram_range=ngram_range,
        )
        self.vocabulary = Vocabulary(self.vocab_size)
        self.contexts = Context(self.vector_size)
        self.d = 0

        self.is_ppmi = is_ppmi

        self.vocabulary.add(WordRep('unk', self.vector_size))

        self.f = 0
    
    def transform_one(self, x):
        x = x if x in self.vocabulary else 'unk'
        word_rep = self.vocabulary[x]
        contexts = word_rep.contexts.items()
        if self.is_ppmi:
            embedding = {
                context: max(np.log2(
                        (coocurence * self.d) / (word_rep.counter * self.vocabulary[context].counter) 
                    ), 0) for context, coocurence in contexts
            }
        else:
            embedding = dict(word_rep.contexts)
        return VectorDict(embedding)


    def learn_one(self, x, **kwargs):
        tokens = self.process_text(x)
        for w in tokens:
            #print(w)
            i = tokens.index(w)
            self.d += 1
            if w not in self.vocabulary:
                self.vocabulary.add(WordRep(w, self.vector_size))
            contexts = _get_contexts(i, self.window_size, tokens)
            focus_word = self.vocabulary[w]
            # if x in self.vocabulary:
            #     self.vocabulary[x].counter += 1
            for c in contexts:
                if c not in self.contexts:
                    self.contexts.add(c)
                if c not in self.contexts and len(self.contexts) == self.vector_size and focus_word.word == 'unk':
                    focus_word.add_context('unk')
                elif c not in self.contexts:
                    focus_word.add_context('unk')
                elif c in self.contexts:
                    focus_word.add_context(c)
            # print(f"{focus_word.word} {self.transform_one(focus_word.word)}")
        return self
    
    def learn_many(X, y=None, **kwargs):
        ...
    
    def get_embedding(self, x):
        if x in self.vocabulary:
            word_rep = self.vocabulary[x]
            embedding = np.zeros(self.vector_size, dtype=float)
            contexts = word_rep.contexts.items()
            if self.is_ppmi:
                for context, coocurence in contexts:
                    ind_c = self.contexts[context]
                    pmi = np.log2(
                        (coocurence * self.d) / (word_rep.counter * self.vocabulary[context].counter) 
                    )
                    embedding[ind_c] = max(0, pmi)
            else:
                for context, coocurence in contexts:
                    ind_c = self.contexts[context]
                    embedding[ind_c] = coocurence 
            return embedding
        False

    
    def most_similar(self, word, n=5):
        ...



def _get_contexts(ind_word, w_size, tokens):
    # to do: agregar try para check que es posible obtener los elementos de los tokens
    slice_start = ind_word - w_size if (ind_word - w_size >= 0) else 0
    slice_end = len(tokens) if (ind_word + w_size + 1 >= len(tokens)) else ind_word + w_size + 1
    first_part = tokens[slice_start: ind_word]
    last_part = tokens[ind_word + 1: slice_end]
    contexts = tuple(first_part + last_part)
    return contexts