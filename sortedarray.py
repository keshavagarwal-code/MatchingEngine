from heapq import heappush, heappop, heapreplace, heapify
import datetime

class SortedArray:
    def __init__(self):
        self.store = []
        self._index = 0

    def __getitem__(self, key):
        if key <= len(self.store) - 1:
            return self.store[key]

    def __len__(self):
        return len(self.store)

    def __iter__(self):
        return self

    def __next__(self):
        try:
            result = self.store[self._index][2]
        except IndexError:
            self._index = 0
            raise StopIteration
        self._index += 1
        return result
        
    def deleteByAttr(self, attr, value, multiple=False):
        found = False
        for idx, i in enumerate(self.store):
            if getattr(i[-1], attr) == value:
                found = True
                del self.store[idx]
                if not multiple:
                    break
        if not found:
            return False
        heapify(self.store)
        return True
    
    def pop(self):
        heappop(self.store)

    def peek(self):
        if self.store:
            return self.store[0][2]

    def replaceTopAttr(self, attr, value):
        setattr(self.store[0][-1], attr, value)

class MinSortedArray(SortedArray):
    def add(self, order):
        heappush(self.store, (order.price, datetime.datetime.now(), order))

class MaxSortedArray(SortedArray):
    def add(self, order):
        heappush(self.store, (-order.price, datetime.datetime.now(), order))


