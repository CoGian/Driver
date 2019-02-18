from collections import deque


class Frontier(object):

    def __init__(self, method):


            'FIFO'
            self.queue = deque()


            'LIFO'
            self.stack = deque()

            'PRIORITY QUEUE'
            self.heap = []

    def __contains__(self, item):

        # custom method compares only configs#
        if self.queue:
            for element in self.queue:
                if item.config == element.config:
                    return True
        elif self.stack:
            for element in self.stack:
                if item.config == element.config:
                    return True
        else:
            for element in self.heap:
                if item.config == element[1].config:
                    return True
        return False


class Explored(object):

    def __init__(self):
        self.set = set()




