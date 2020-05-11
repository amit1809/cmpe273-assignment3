# -cmpe273-assignment3

## Bloom Filter size

What are the best k hashes and m bits values to store one million n keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from pickle_hash.py and explain why?

As per the wikipedia https://en.wikipedia.org/wiki/Bloom_filter

m bits size is calculated based on false positve probabilty rate (p) and n as per formula:

```
m = -(n * math.log(p)) / (math.log(2) ** 2)
```

k hashes count is calculated from m and n as per below:

```
k = (m / n) * math.log(2)
```

So with above formulas considering false positive rate (p) of 0.05, below m bits and k hashes for one million n keys:

```
m = 6235224
k = 4
```
