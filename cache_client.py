import socket
from sample_data import USERS
from server_config import NODES
from pickle_hash import serialize_GET, serialize_PUT, deserialize, serialize_DELETE
from node_ring import NodeRing


BUFFER_SIZE = 1024

class UDPClient():
    def __init__(self, host, port):
        self.host = host
        self.port = int(port)       

    def send(self, request):
        print('Connecting to server at {}:{}'.format(self.host, self.port))
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(request, (self.host, self.port))
            response, ip = s.recvfrom(BUFFER_SIZE)
            return response
        except socket.error:
            print("Error! {}".format(socket.error))
            exit()


def process(udp_clients):
    hash_codes = set()
    # PUT all users.
    for u in USERS:
        data_bytes, key = serialize_PUT(u)
        # TODO: PART II - Instead of going to server 0, use Naive hashing to split data into multiple servers
        #fix_me_server_id = 0
        ring = NodeRing(nodes=NODES)
        fix_me_server_id = NODES.index(ring.get_node(key))
        print(f"Server id: {fix_me_server_id}")
        response = udp_clients[fix_me_server_id].send(data_bytes)
        hash_codes.add(response)
        print(response)

    print(f"Number of Users={len(USERS)}\nNumber of Users Cached={len(hash_codes)}")


    # TODO: PART I
    # GET all users.
    for hc in hash_codes:
        print(f"GET:{hc}")
        data_bytes, key = serialize_GET(hc)
        #fix_me_server_id = 0
        ring = NodeRing(nodes=NODES)
        #
        fix_me_server_id = NODES.index(ring.get_node(key))
        response = udp_clients[fix_me_server_id].send(data_bytes)
        #print(deserialize(response))
        print(response)

        # DELETE all users
    for hc in hash_codes:
        # print(hc)
        data_bytes, key = serialize_DELETE(hc)
        # fix_me_server_id = 0
        ring = NodeRing(nodes=NODES)
        fix_me_server_id = NODES.index(ring.get_node(key))
        response = udp_clients[fix_me_server_id].send(data_bytes)
        print(response)

if __name__ == "__main__":
    clients = [
        UDPClient(server['host'], server['port'])
        for server in NODES
    ]
    print(f"clients :{clients}")
    process(clients)
