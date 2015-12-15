import xmlrpclib
import os
import time
from threading import Thread

N = 1000


def master_only(coordinator, server1, storage):
    start = time.time()
    for i in range(N):
        coordinator.tick()
        server1.tick()
        server1.put(storage[i][0], storage[i][1])
    end = time.time()
    print "Master only test: {0:.2f}s".format(end - start)
    print "{0:.2f} requests per second".format(N/(end - start))


def master_and_backup(coordinator, server1, server2, data):
    start = time.time()
    for i in range(N):
        coordinator.tick()
        server1.tick()
        server2.tick()
        server1.put(data[i][0], data[i][1])
    end = time.time()
    print "Master and backp test: {0:.2f}s".format(end - start)
    print "{0:.2f} requests per second".format(N/(end - start))


def send_put_requests(server1, data):
    start = time.time()
    for i in data:
        server1.put(i[0], i[1])
    end = time.time()
    print "On copy test: {0:.2f}s".format(end - start)
    print "{0:.2f} requests per second".format(N/(end - start))


def on_copy(coordinator, server1, server2, data):
    for i in range(9 * N):
        coordinator.tick()
        server1.tick()
        server1.put(data[i][0], data[i][1])
    server2.tick()
    thread2 = Thread(target=send_put_requests, args=(server1, data[9 * N : 10 * N]))
    thread2.start()
    server1.tick()
    thread2.join()
    start = time.time()
    for i in data:
        if server1.get(i[0]) != i[1] or server2.get(i[0]) != i[1]:
            print "Error", i[0], i[1], server1.get(i[0]), server2.get(i[0])
    end = time.time()
    print "{0:.0f} get request: {1:.2f}s".format(10 * N, end - start)
    print "{0:.2f} get requests per second".format(N/(end - start))


def generate_data(size):
    return [[os.urandom(4).encode('hex'), os.urandom(4).encode('hex')] for i in xrange(size)]


def main():
    coord_name = "http://localhost:10000"
    srv1_name = "http://localhost:10001"
    srv2_name = "http://localhost:10002"

    coordinator = xmlrpclib.ServerProxy(coord_name)
    server1 = xmlrpclib.ServerProxy(srv1_name)
    server2 = xmlrpclib.ServerProxy(srv2_name)

    master_only(coordinator, server1, generate_data(N))
    server1.clear()
    server2.clear()
    master_and_backup(coordinator, server1, server2, generate_data(N))
    server1.clear()
    server2.clear()
    on_copy(coordinator, server1, server2, generate_data(10 * N))
    server1.clear()
    server2.clear()


if __name__ == "__main__":
    main()
