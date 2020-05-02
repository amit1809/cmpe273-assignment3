from pickle_hash import hash_code_hex, serialize
import mmh3

class BloomFilter(object):
    def __init__(self, m, h):
        self.size = m # Size of array
        self.hash_count = h # number of hash functions
        self.bit_array = [0] * self.size # set all elements to 0

    def add(self, key):
        for i in range(self.hash_count):
            index = mmh3.hash(key, i) % self.size
            #index = (int(hash_code_hex(serialize(key)), base=16)+i) % self.size
            print(f"INDEX: {index}")
            self.bit_array[index] = 1 # set index elements to 1

    def is_member(self, key):
        for i in range(self.hash_count):
            index = mmh3.hash(key, i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True