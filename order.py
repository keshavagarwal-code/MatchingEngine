from dataclasses import dataclass

@dataclass
class Order:
    msgtype: int
    orderid: int
    side: int
    quantity: int
    price: int

    def visualize(self, print_fileds = ['orderid', 'quantity', 'price']):
        return [getattr(self, i) for i in print_fileds]

@dataclass
class TradeEvent:
    quantity: int
    price: int
    id: int = 2

    def __str__(self):
        return("{}, {}, {}".format(self.id, self.quantity, self.price))

@dataclass
class FullOrderFilled:
    orderid: int
    id: int = 3

    def __str__(self):
        return("{}, {}".format(self.id, self.orderid))

@dataclass
class PartialOrderFilled:
    orderid: int
    quantity: int
    id: int = 4

    def __str__(self):
        return("{}, {}, {}".format(self.id, self.orderid, self.quantity))
