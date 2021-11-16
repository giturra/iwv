import abc


class BaseVocab:

    def __init__(self, max_size):
        self.max_size = max_size
        self.current_size = 0
        self.table = dict()

    def is_full(self):
        return self.current_size == self.max_size

    @abc.abstractmethod
    def add(self, word):
        ...
    
    def __len__(self):
        return len(self.table.values())
    
    @abc.abstractmethod
    def __getitem__(self, word):
        ...

    def __repr__(self):
        return self.table.keys().__repr__()
    
    def __contains__(self, word):
        return word in self.table
        