import random
import string
import math



class ZipfianDataGenerator:
    @staticmethod
    def random_list_of_words(n: int, length: int | None = None) -> list[str]:
        alphabet = string.ascii_lowercase
        alphabet_length = len(alphabet)
        if length is None:
            length = 5 + math.ceil(math.log(n) / math.log(alphabet_length))
        else:
            assert length >= math.ceil(math.log(n) / math.log(alphabet_length)), "length too short"
        words = set()
        while len(words) < n:
            random_word = ''.join(random.choices(alphabet, k=length))
            words.add(random_word)
        return list(words)


    def __init__(self, alpha: float, n: int):
        self.alpha = alpha
        assert alpha >= 0, "alpha must be >= 0"

        self.n = n
        assert n >= 1, "n must be >= 1"

        self.words = self.random_list_of_words(n)

        c_n = sum(i**(-alpha) for i in range(1, n+1))
        self.probabilities = [c_n / i**alpha for i in range(1, n+1)]


    def random_stream(self, length: int = 1) -> list[str]:
        assert length >= 0, "length must be >= 0"
        return random.choices(self.words, weights=self.probabilities, k=length)

