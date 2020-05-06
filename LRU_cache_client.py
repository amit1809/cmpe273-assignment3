import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, deserialize, serialize_DELETE
from node_ring import NodeRing
from cache_client import UDPClient
from lru_cache_deco import lru_cache
from bloom_filter import BloomFilter

BUFFER_SIZE = 1024
LRU_CACHE_SIZE = 3
hash_codes = set()
BLOOM_FILTER_ARRAY_SIZE = 500
BLOOM_FILTER_NO_OF_HASHES = 3

bloom_f = BloomFilter(BLOOM_FILTER_ARRAY_SIZE, BLOOM_FILTER_NO_OF_HASHES)

@lru_cache(LRU_CACHE_SIZE)
def get(key):
    if(bloom_f.is_member(key)):
        data_bytes, key_ser = serialize_GET(key.encode())
        print(f"*** GET from SERVER: ***")
        ring = NodeRing(nodes=NODES)
        fix_me_server_id = NODES.index(ring.get_node(key_ser))
        response = clients[fix_me_server_id].send(data_bytes)
        # print(deserialize(response))
        #print(response)
        return response
    else:
        print("### KEY FOR GET NOT FOUND IN BLOOM FILTER ###")
        return None

@lru_cache(LRU_CACHE_SIZE)
def put(key, val):
    print("ADD KEY to BLOOM FILTER")
    bloom_f.add(key)
    print("PUT to SERVER:")
    ring = NodeRing(nodes=NODES)
    fix_me_server_id = NODES.index(ring.get_node(key))
    print(f"Server id: {fix_me_server_id}")
    response = clients[fix_me_server_id].send(val)
    hash_codes.add(response)
    #print(response)
    return response

@lru_cache(LRU_CACHE_SIZE)
def delete(key):
    if (bloom_f.is_member(key)):
        print(f"DELETE on SERVER:")
        data_bytes, key_ser = serialize_DELETE(key.encode())
        ring = NodeRing(nodes=NODES)
        fix_me_server_id = NODES.index(ring.get_node(key_ser))
        response = clients[fix_me_server_id].send(data_bytes)
        print(response)
        return response
    else:
        print("### KEY FOR DELETE NOT FOUND IN BLOOM FILTER ###")
        return None

def get_key_value(ALL_USERS):
    data_byte_list_put = []
    keys_list_put = []
    for u in ALL_USERS:
        data_bytes, key = serialize_PUT(u)
        data_byte_list_put.append(data_bytes)
        keys_list_put.append(key)
    return keys_list_put, data_byte_list_put

def test_lru():
    '''
    This is to test LRU cache and Bloom Filter implementations by running calling put, get and delete in sequence
    '''

    # get all keys and values from sample data in a list
    keys_list_put, data_byte_list_put = get_key_value(USERS)

    # Test LRU cache
    put(keys_list_put[0], data_byte_list_put[0])
    get(keys_list_put[0])

    put(keys_list_put[1], data_byte_list_put[1])
    get(keys_list_put[1])

    put(keys_list_put[2], data_byte_list_put[2])
    get(keys_list_put[2])
    get(keys_list_put[1])
    get(keys_list_put[0])

    put(keys_list_put[3], data_byte_list_put[3])  # this PUT will delete key 2 from LRU cache
    get(keys_list_put[0])
    get(keys_list_put[3])
    get(keys_list_put[2])  # will not find this key value in cache, will get it from server
    get(keys_list_put[1])

    get(keys_list_put[0]) # will not find this key value in cache, will get it from server
    get(keys_list_put[3])
    get(keys_list_put[1])

    delete(keys_list_put[1])

    get(keys_list_put[4]) # Key not available on bloom filter
    delete(keys_list_put[4]) # Key not available on bloom filter


if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    print(f"clients :{clients}")
    test_lru()

