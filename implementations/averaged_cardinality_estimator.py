from typing import Callable



class AveragedCardinalityEstimator:
    @staticmethod
    def is_power_of_2(x: int) -> bool:
        # returns True if x = 2^k for some natural k, False otherwise
        return (x & (x-1)) == 0
    

    @staticmethod
    def ilog2(x: int) -> int:
        lg = 0
        while x > 1:
            lg += 1
            x >>= 1
        return lg
    

    @staticmethod
    def binary_length(x: int) -> int:
        return 1 + AveragedCardinalityEstimator.ilog2(x)


    def __init__(self, salt: str, hash_f: Callable[[str], int], hash_size: int, m: int):
        self.salt = salt
        
        # m is the number of substreams used to average the estimation
        self.m = m
        self.log2m = self.ilog2(m)
        assert self.is_power_of_2(m), "m must be a power of 2"
        assert self.log2m >= 4, "m must be >= 4"

        # chosen hash for the estimations, should support call with elements and return hash (ex: hash('hello') -> (int)0b0101001...)
        self.hash_f = hash_f
        self.hash_size = hash_size
        assert hash_size >= self.log2m + 32, "hash_size too small"

        self.mask_len = hash_size - self.log2m
        self.mask = 2**self.mask_len - 1


    def hash_leading_zeros(self, h: int) -> int:
        return self.mask_len - self.binary_length(h)


    def add(self, elem: str):
        hash = self.hash_f(self.salt + elem)

        # (hash & self.mask) == hash % self.m
        leftmost_log2m_bits = hash >> self.mask_len

        hash &= self.mask
        
        self.add_to_subset(leftmost_log2m_bits, hash)

    
    def add_to_subset(self, idx: int, hash: int):
        # To implement in subclasses
        pass
        

    def count(self) -> float:
        # To implement in subclasses
        pass