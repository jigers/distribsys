import xmlrpclib
import sys
from SimpleXMLRPCServer import SimpleXMLRPCServer


class Server():
    def __init__(self, name, coord_name):
        self.coordinator = xmlrpclib.ServerProxy(coord_name)
        self.name = name
        self.view_number = 0
        self.storage = {}
        self.master = None
        self.backup = None

    def add(self, key, value):
        self.storage[key] = value

    def get(self, key):
        return self.storage[key]

    def put(self, key, value):
        if self.master is not None and self.name == self.master:
            #print "put to master"
            self.add(key, value)
            self.put_backup(key, value)
        else:
            raise Exception()

    def put_backup(self, key, value):
        if self.backup is not None and not self.name == self.backup:
            #print "put to backup"
            backup = xmlrpclib.ServerProxy(self.backup)
            backup.add(key, value)

    def tick(self):
        new_view = self.coordinator.ping(self.view_number, self.name)
        self.backup = new_view['backup']
        self.master = new_view['master']
        if self.view_number != new_view['number']:
            for key, value in self.storage.items():
                self.put_backup(key, value)
            new_view = self.coordinator.ping(new_view['number'], self.name)
            self.backup = new_view['backup']
            self.master = new_view['master']
            self.view_number = new_view['number']

    def clear(self):
        self.storage = {}
        self.master = None
        self.backup = None


def run_server(address, host):
    server = SimpleXMLRPCServer((address, int(host)), allow_none=True)
    server.register_instance(Server('http://' + address + ':' + host, "http://localhost:10000"))
    print 'Server started at http://' + address + ':' + host
    server.serve_forever()


def main():
    run_server(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    main()