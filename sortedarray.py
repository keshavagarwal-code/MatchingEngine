from heapq import heappush, heappop
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
        
    
    def remove(self, orderid, qty=None):
        found = False
        for idx, i in enumerate(self.store):
            if i[-1].orderid == orderid:
                found = True
                if qty:
                    self.store[idx][-1].quantity = self.store[idx][-1].quantity - qty
                else:
                    del self.store[idx]
                break
        if not found:
            return False
        return True
    
    def pop(self):
        heappop(self.store)

    def peek(self):
        if self.store:
            return self.store[0][2]

class MinSortedArray(SortedArray):
    def add(self, order):
        heappush(self.store, (order.price, datetime.datetime.now(), order))

class MaxSortedArray(SortedArray):
    def add(self, order):
        heappush(self.store, (-order.price, datetime.datetime.now(), order))


