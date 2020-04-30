import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, deserialize, serialize_DELETE
from node_ring import NodeRing
from collections import OrderedDict
from cache_client import UDPClient

BUFFER_SIZE = 1024
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

@lru_cache(LRU_CACHE_SIZE)
def get(key):
    data_bytes, key_ser = serialize_GET(key.encode())
    print(f"GET from SERVER:")
    ring = NodeRing(nodes=NODES)
    fix_me_server_id = NODES.index(ring.get_node(key_ser))
    response = clients[fix_me_server_id].send(data_bytes)
    # print(deserialize(response))
    print(response)
    return response

@lru_cache(LRU_CACHE_SIZE)
def put(key, val):
    print(f"PUT to SERVER:")
    ring = NodeRing(nodes=NODES)
    fix_me_server_id = NODES.index(ring.get_node(key))
    print(f"Server id: {fix_me_server_id}")
    response = clients[fix_me_server_id].send(val)
    hash_codes.add(response)
    #print(response)
    return response

@lru_cache(LRU_CACHE_SIZE)
def delete(key):
    print(f"DELETE on SERVER:")
    data_bytes, key_ser = serialize_DELETE(key.encode())
    ring = NodeRing(nodes=NODES)
    fix_me_server_id = NODES.index(ring.get_node(key_ser))
    response = clients[fix_me_server_id].send(data_bytes)
    print(response)
    return response

def get_key_value_put(ALL_USERS):
    data_byte_list_put = []
    keys_list_put = []
    for u in ALL_USERS:
        data_bytes, key = serialize_PUT(u)
        data_byte_list_put.append(data_bytes)
        keys_list_put.append(key)
    return keys_list_put, data_byte_list_put

def get_key_value_get(ALL_USERS):
    data_byte_list_get = []
    keys_list_get = []
    for u in ALL_USERS:
        data_bytes, key = serialize_GET(u)
        data_byte_list_get.append(data_bytes)
        keys_list_get.append(key)
    return keys_list_get, data_byte_list_get

def get_key_value_delete(ALL_USERS):
    data_byte_list_delete = []
    keys_list_delete = []
    for u in ALL_USERS:
        data_bytes, key = serialize_GET(u)
        data_byte_list_delete.append(data_bytes)
        keys_list_delete.append(key)
    return keys_list_delete, data_byte_list_delete


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    print(f"clients :{clients}")
    keys_list_put, data_byte_list_put = get_key_value_put(USERS)
    keys_list_get, data_byte_list_get = get_key_value_get(USERS)
    keys_list_delete, data_byte_list_delete = get_key_value_delete(USERS)

    #Test LRU cache
    put(keys_list_put[0], data_byte_list_put[0])
    get(keys_list_put[0])

    put(keys_list_put[1], data_byte_list_put[1])
    get(keys_list_put[1])

    put(keys_list_put[2], data_byte_list_put[2]) # this PUT will delete key 0 from LRU cache
    get(keys_list_put[2])
    get(keys_list_put[1])
    get(keys_list_put[0]) # will not find this key value in cache, will get from server

    put(keys_list_put[3], data_byte_list_put[3]) # this PUT will delete key 2 from LRU cache
    get(keys_list_put[3])
    get(keys_list_put[2]) # will not find this key value in cache, will get from server
    get(keys_list_put[1])
    delete(keys_list_put[1])
    print(cache.keys()) # Only one key remains in cache after above delete