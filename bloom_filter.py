#import mmh3
import math
from bitarray import bitarray
from pickle_hash import hash_code_hex


class BloomFilter():
    def __init__(self, num_key, false_positive_prob):
        self.size = self.get_size(num_key, false_positive_prob) # Size of array
        self.hash_count = self.get_hash_count(self.size, num_key) # number of hash functions
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0) # set all elements to 0

    #Add key to bloom filter
    def add(self, key):
        for i in range(self.hash_count):
            #index = mmh3.hash(key, i) % self.size
            index = int(hash_code_hex(key.encode() + bytes(i)), base=16) % self.size
            #print(f"INDEX: {index}")
            self.bit_array[index] = True

    #Check if key is a member of bloom filter
    def is_member(self, key):
        for i in range(self.hash_count):
            #index = mmh3.hash(key, i) % self.size
            index = int(hash_code_hex(key.encode() + bytes(i)), base=16) % self.size
            if self.bit_array[index] == False:
                return False
        return True

    # get m bit size
    def get_size(self, n, p):
        m = -(n * math.log(p)) / (math.log(2) ** 2)
        return int(m)

    #get number of hash
    def get_hash_count(self, m, n):
        k = (m / n) * math.log(2)
        return int(k)