from river.base.transformer import Transformer
from river.feature_extraction.vectorize import VectorizerMixin


class IncrementalWordVector(Transformer, VectorizerMixin):

    def __init__(
        self,
        vocab_size,
        vector_size,
        window_size,
        normalize=True,
        on=None,
        strip_accents=True,
        lowercase=True,
        preprocessor=None,
        tokenizer=None,
        ngram_range=(1, 1),
    ):

        super().__init__(
            on=on,
            strip_accents=strip_accents,
            lowercase=lowercase,
            preprocessor=preprocessor,
            tokenizer=tokenizer,
            ngram_range=ngram_range,
        )
        
        self.vocab_size = vocab_size
        self.vocab_size = vector_size
        self.window_size = window_size