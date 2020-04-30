import time
from collections import OrderedDict

CACHE_SIZE =5
cache = OrderedDict()
'''
def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        print('Function', method.__name__, 'time:', round((te -ts)*1000,1), 'ms')
        print()
        return result
    return timed

@timeit
def math_harder():
    [x**(x%17)^x%17 for x in range(1,5555)]
math_harder()

@timeit
def sleeper_agent():
    time.sleep(1)
sleeper_agent()

def lru_cache(method):
    def inner(key, value):
        print(f"Checking LRU cache with capacity :{CACHE_SIZE}")
        if method.__name__ == "get":
            print("GET in LRU Cache")
            if key in cache:
                cache.move_to_end(key)
                return key
            else:
                return method(key,value)
        return inner


@lru_cache
def get(key,val):
    print("GET inside GET")
    return key*val

get(5,10)
'''
def lru_cache(func):
   def inner(*args, **kw):
      key = args[0]
      print("Checking LRU cache")
      if func.__name__ == "get":
         if key in cache:
            print("In LRU Cache GET")
            cache.move_to_end(key)
            return cache[key]

      elif func.__name__ == "put":
         val = args[1] #val only in the case of PUT
         print("In LRU Cache PUT")
         cache[key] = val
         cache.move_to_end(key)
         if len(cache) > CACHE_SIZE:
             cache.popitem(last=False)

      elif func.__name__ == "delete":
         print("In LRU Cache DELETE")

      return func(*args, **kw)
   return inner

@lru_cache
def get(key):
    print(f"GET in Get: {key}")
    return key

@lru_cache
def put(key, val):
    print(f"PUT in Put: {key,val}")
    return key

@lru_cache
def delete(key):
    print(f"GET in Delete: {key}")
    return key

get(5)
put(5,5)
delete(5)