import mmh3
from pickle_hash import hash_code_hex
import math


class BloomFilter():
    def __init__(self, num_key, false_positive_prob):
        self.size = self.get_size(num_key, false_positive_prob) # Size of array
        self.hash_count = self.get_hash_count(self.size, num_key) # number of hash functions
        self.bit_array = [0] * self.size # set all elements to 0

    def add(self, key):
        for i in range(self.hash_count):
            #index = mmh3.hash(key, i) % self.size
            index = int(hash_code_hex(key.encode() + bytes(i)), base=16) % self.size
            print(f"INDEX: {index}")
            self.bit_array[index] = 1 # set index elements to 1

    def is_member(self, key):
        for i in range(self.hash_count):
            #index = mmh3.hash(key, i) % self.size
            index = int(hash_code_hex(key.encode() + bytes(i)), base=16) % self.size
            if self.bit_array[index] == 0:
                return False
        return True

    def get_size(self, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)
    def get_hash_count(self, m, n):
        k = (m / n) * math.log(2)
        return int(k)