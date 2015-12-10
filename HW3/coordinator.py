class View:
    def __init__(self, master, backup, number):
        self.master = master
        self.backup = backup
        self.number = number


class Coordinator:
    def __init__(self):
        self.new_view = View(None, None, 0)
        self.cur_view = View(None, None, 0)
        self.dead = False
        self.deadPings = 5
        self.confirmed = True
        self.servers = []

    def __find_server(self, not_allowed):
        for i in self.servers:
            if not (i in not_allowed) and i[1] > 0:
                return i
        return None

    def __updateView(self):
        self.cur_view = self.new_view
        self.new_view = View(None, None, 0)

    def __view_for_ans(self):
        if self.cur_view.master is None:
            master = None
        else:
            master = self.cur_view.master[0]
        if self.cur_view.backup is None:
            backup = None
        else:
            backup = self.cur_view.backup[0]
        return View(master, backup, self.cur_view.number)

    def ping(self, number, name):
        serv = None
        for i in self.servers:
            if i[0] == name:
                i[1] = self.deadPings
                serv = i
                break
        if serv is None:
            if self.cur_view.master is not None and self.cur_view.master[0] == name:
                self.servers.append(self.cur_view.master)
                self.cur_view.master[1] = self.deadPings
            elif self.cur_view.backup is not None and self.cur_view.backup[0] == name:
                self.servers.append(self.cur_view.backup)
                self.cur_view.backup[1] = self.deadPings
            else:
                self.servers.append([name, self.deadPings])
        if self.cur_view.backup is None and self.cur_view.master is not None:

            self.new_view.master = self.cur_view.master
            self.new_view.backup = self.__find_server([self.new_view.master])
            if self.new_view.backup is not None:
                self.new_view.number = self.cur_view.number + 1
            else:
                self.new_view.number = self.cur_view.number
            if self.confirmed:
                self.__updateView()
                self.confirmed = False
            if name == self.cur_view.master[0]:
                if number == 0:
                    print "Error"
                    exit(1)
                if number == self.cur_view.number:
                    self.confirmed = True
            return self.__view_for_ans()
        if self.cur_view.master is None:

            self.cur_view.master = self.__find_server([])
            if self.cur_view.master is not None:
                self.cur_view.number += 1
                self.confirmed = True
            return self.__view_for_ans()

        if name == self.cur_view.master[0]:
            if number == self.cur_view.number:
                self.confirmed = True
            if number == 0:
                self.new_view.master = self.cur_view.backup
                self.new_view.backup = self.__find_server([self.new_view.master])
                self.new_view.number = self.cur_view.number + 1
                if self.confirmed:
                    self.__updateView()
                    self.confirmed = False
        if name == self.cur_view.backup[0]:
            if number == 0:
                self.new_view.master = self.cur_view.master
                self.new_view.backup = self.__find_server([self.new_view.master])
                self.new_view.number = self.cur_view.number + 1
                if (self.confirmed):
                    self.__updateView()
                    self.confirmed = False
        return self.__view_for_ans()

    def master(self):
        return self.cur_view.master

    def tick(self):
        for i in range(len(self.servers)):
            self.servers[i][1] -= 1
        if self.cur_view.master is not None and self.cur_view.master[1] == 0:
            self.new_view.master = self.cur_view.backup
            self.new_view.backup = self.__find_server([self.new_view.master])
            self.new_view.number = self.cur_view.number + 1
            if self.confirmed:
                self.__updateView()
                self.confirmed = False

        if self.cur_view.backup is not None and self.cur_view.backup[1] == 0:
            self.new_view.master = self.cur_view.master
            self.new_view.backup = self.__find_server([self.new_view.master])
            self.new_view.number = self.cur_view.number + 1
            if self.confirmed:
                self.__updateView()
                self.confirmed = False
        self.servers = [a for a in self.servers if a[1] > 0]
        return
