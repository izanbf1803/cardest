from typing import Callable
import heapq



class MinSet:
    def __init__(self):
        self.set = set()
        self.heap = []


    def __len__(self) -> int:
        return len(self.set)
    

    def __contains__(self, elem) -> bool:
        return elem in self.set


    def add(self, elem):
        if elem not in self.set:
            self.set.add(elem)
            heapq.heappush(self.heap, elem)

    
    def min(self):
        if len(self) == 0:
            return None
        else:
            return self.heap[0]
        
    
    def pop_min(self):
        min_elem = self.heap[0]
        heapq.heappop(self.heap)
        self.set.remove(min_elem)
        return min_elem



class Recordinality:
    def __init__(self, salt: str, hash_f: Callable[[str], int], k: int):
        self.salt = salt

        self.hash_f = hash_f

        self.k = k
        assert k >= 1, "k should be >= 1"

        self.R = 0
        self.S = MinSet()


    def add(self, elem: str):
        h = self.hash_f(self.salt + elem)
        if len(self.S) < self.k:
            self.S.add(h)
            self.R = len(self.S)
        else:
            S_min = self.S.min()
            if h > S_min and (h not in self.S):
                self.R += 1
                self.S.pop_min()
                self.S.add(h)


    def count(self) -> float:
        if self.R >= self.k:
            Z = self.k * (1 + 1/self.k)**(self.R - self.k + 1) - 1
            return Z
        else:
            return len(self.S)

