from base.iwv import IncrementalWordVector

from isgns_vocab import Vocabulary
from unigram_table import UnigramTable


class ISGNS(IncrementalWordVector):

    def __init__(self, 
    vocab_size, 
    vector_size, window_size, 
    normalize=True, on=None, 
    strip_accents=True, 
    lowercase=True, 
    preprocessor=None, 
    tokenizer=None, 
    ngram_range=False):
        
        super().__init__(
            vocab_size, 
            vector_size, 
            window_size, 
            normalize=normalize, 
            on=on, 
            strip_accents=strip_accents, 
            lowercase=lowercase, 
            preprocessor=preprocessor, 
            tokenizer=tokenizer, 
            ngram_range=ngram_range
        )

        self.vector_size = int(vector_size)

        self.max_vocab_size = int(2 * max_vocab_size)
        self.vocab = Vocabulary(int(self.max_vocab_size * 2))

        self.unigram_table_size = unigram_table_size
        self.unigram_table = UnigramTable(self.unigram_table_size, device=device)

        self.device = device

        self.counts = torch.zeros(int(2 * self.max_vocab_size))
        self.counts.to(self.device)

        self.total_count = 0

        self.neg_sample_num = neg_sample_num
        
        self.tokenizer = tokenizer

        self.alpha = alpha
        self.window_size = window_size
        self.subsampling_threshold = subsampling_threshold
        
        self.randomizer = RandomNum(1234)

        # net in pytorch
        self.model = SkipGram(self.max_vocab_size, self.vector_size)
        if self.device == 'cuda':
            self.model.cuda()
        #self.optimizer = torch.optim.SGD(self.model.parameters(), lr=0.5, momentum=0.9)
        self.optimizer = torch.optim.Adagrad(self.model.parameters())
        self.criterion = torch.nn.BCEWithLogitsLoss()