from typing import Callable
from implementations.averaged_cardinality_estimator import AveragedCardinalityEstimator
from math import log



class HyperLogLog(AveragedCardinalityEstimator):
    def __init__(self, hash_f: Callable[[str], int], hash_size: int, m: int):
        super().__init__(hash_f, hash_size, m)

        self.substream = [self.mask for _ in range(m)]
        
        if self.m == 16:
            self.alpha = 0.673
        elif self.m == 32:
            self.alpha = 0.697
        elif self.m == 64:
            self.alpha = 0.709
        elif self.m >= 128:
            self.alpha = 0.7213 / (1 + 1.079 / m)
        else:
            assert False, "m too small (cannot assign alpha)"


    def add_to_subset(self, idx: int, hash: int):
        self.substream[idx] = min(self.substream[idx], hash)


    def count(self) -> float:
        R = [self.hash_leading_zeros(h) + 1 for h in self.substream]
        Z = sum(2**(-r) for r in R)**(-1)
        E = self.alpha * self.m**2 * Z

        if E <= 5 * self.m / 2:
            V = R.count(0)
            # apply small range correction
            if V != 0:
                return self.m * log(self.m / V)

        return E
