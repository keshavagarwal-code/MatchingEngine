from dataclasses import dataclass, fields

@dataclass
class Order:
    msgtype: int
    orderid: int
    side: int
    quantity: int
    price: int

    def visualize(self, print_fileds = ['orderid', 'quantity', 'price']):
        return [getattr(self, i) for i in print_fileds]
