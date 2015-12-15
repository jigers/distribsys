
import xmlrpclib
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Server():
    def __init__(self, name, coord_name):
        self.coordinator = xmlrpclib.ServerProxy(coord_name)
        self.name = name
        self.view_number = 0
        self.storage = {}

    def add(self, key, value):
        self.storage[key] = value

    def get(self, key):
        return self.storage[key]

    def put(self, key, value):
        if self.coordinator.master() is not None and self.name == self.coordinator.master():
            self.add(key, value)
            self.put_backup(key, value)
        else:
            raise Exception()

    def put_backup(self, key, value):
        if self.coordinator.backup() is not None and not self.name == self.coordinator.backup():
            backup = xmlrpclib.ServerProxy(self.coordinator.backup())
            backup.add(key, value)

    def tick(self):
        new_view_number = self.coordinator.ping(self.view_number, self.name)['number']
        if self.view_number != new_view_number:
            for key, value in self.storage.items():
                self.put_backup(key, value)
            self.view_number = self.coordinator.ping(new_view_number, self.name)['number']

    def clear(self):
        self.storage = {}


def run_server(address, host):
    server = SimpleXMLRPCServer((address, int(host)), allow_none=True)
    server.register_instance(Server('http://' + address + ':' + host, "http://localhost:10000"))
    print 'Server started at http://' + address + ':' + host
    server.serve_forever()


def main():
    run_server(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()