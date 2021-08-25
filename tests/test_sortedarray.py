from sortedarray import MinSortedArray, MaxSortedArray
from order import Order

class TestMinMaxSortedArray:
    def setup(self):
        self.minArray = MinSortedArray()
        self.maxArray = MaxSortedArray()
        self.ord1 = Order(0,100000,1,1,1075)
        self.ord2 = Order(0,100012,1,1,1075)
        self.ord3 = Order(0,100001,1,1,1050)
        self.ord4 = Order(0,100013,1,1,1050)
    
    def test_min_duplicate_add_pop(self):
        self.minArray.add(self.ord1)
        self.minArray.add(self.ord2)
        self.minArray.add(self.ord3)
        self.minArray.add(self.ord4)
        assert self.minArray.peek().orderid == self.ord3.orderid
        result = self.minArray.pop()
        assert self.minArray.peek().orderid == self.ord4.orderid

    def test_max_duplicate_add_pop(self):
        self.maxArray.add(self.ord1)
        self.maxArray.add(self.ord2)
        self.maxArray.add(self.ord3)
        self.maxArray.add(self.ord4)
        assert self.maxArray.peek().orderid == self.ord1.orderid
        result = self.maxArray.pop()
        assert self.maxArray.peek().orderid == self.ord2.orderid