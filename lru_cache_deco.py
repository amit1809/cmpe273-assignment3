from collections import OrderedDict

LRU_CACHE_SIZE = 2
cache = OrderedDict()
hash_codes = set()

# LRU cache decorator using OrderedDict. Most recent used in the end(right) and lease recent in the beginning(left)
def lru_cache(cache_size):
    def real_decorator(func):
        def inner(*args, **kw):
            key = args[0]
            print("Checking LRU cache")
            if func.__name__ == "get":
                if key in cache:
                    print("In LRU Cache GET")
                    cache.move_to_end(key) #move key to the end to make it most recent
                    print(cache[key])
                    return cache[key]

            elif func.__name__ == "put":
                val = args[1] #val only in the case of PUT
                print("In LRU Cache PUT")
                cache[key] = val
                cache.move_to_end(key) #move key to the end to make it most recent
                if len(cache) > cache_size:
                    cache.popitem(last=False) #Delete the least recent used from left

            elif func.__name__ == "delete":
                if key in cache:
                    print("In LRU Cache DELETE")
                    del cache[key]

            return func(*args, **kw)
        return inner
    return real_decorator
