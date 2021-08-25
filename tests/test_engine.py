from order import Order
from engine import OrderBook, MatchingEngine
from dataclasses import astuple
    
test_sellOrder = Order(0,100000,1,1,1075)
test_buyOrder = Order(0,100001,0,1,1050)

class TestOrderBook:
    def setup(self):
        self.ob = OrderBook()

    def test_addOrder_buy(self):
        result_addOrder = self.ob.addOrder(test_buyOrder)
        assert self.ob.buy.peek().orderid ==  test_buyOrder.orderid

    def test_addOrder_sell(self):
        result_sellOrder = self.ob.addOrder(test_sellOrder)
        assert self.ob.sell.peek().orderid ==  test_sellOrder.orderid

    def test_cancelOrder_buy(self):
        #must run after test_addOrder
        if len(self.ob.buy) == len(self.ob.sell) == 0:
            self.test_addOrder_buy()
        le = len(self.ob.buy)
        assert test_buyOrder.orderid in self.ob.orderMap
        result = self.ob.cancelOrderByOrderId(test_buyOrder.orderid)
        assert len(self.ob.buy) == le - 1
        assert result == True
        assert test_buyOrder.orderid not in self.ob.orderMap

    def test_cancelOrder_sell(self):
        #must run after test_addOrder
        if len(self.ob.buy) == len(self.ob.sell) == 0:
            self.test_addOrder_sell()
        le = len(self.ob.sell)
        assert test_sellOrder.orderid in self.ob.orderMap
        result = self.ob.cancelOrderByOrderId(test_sellOrder.orderid)
        assert len(self.ob.sell) == le - 1
        assert result == True
        assert test_sellOrder.orderid not in self.ob.orderMap

    def test_cancelOrder_invalid(self):
        #must run after test_addOrder
        result = self.ob.cancelOrderByOrderId(12344)
        assert result == False

class TestMatchingEngine:
    def setup(self):
        self.me = MatchingEngine()

    def test_process_aggressiveBuy_FullOrderFilled(self):
        self.me.processOrder(0, astuple(test_sellOrder))
        self.me.processOrder(0, astuple(test_buyOrder))
        result = self.me.processOrder(0, (0,100020,0,1,1100))
        assert len(result) == 3
        assert (result[0].id, result[0].quantity, result[0].price) == (2, 1, 1075)
        assert (result[1].id,  result[1].orderid) == (3, 100020)
        assert (result[2].id,  result[2].orderid) == (3, 100000)

    def test_process_aggressiveBuy_partialOrderFilled(self):
        self.me.processOrder(0, astuple(test_sellOrder))
        self.me.processOrder(0, astuple(test_buyOrder))
        agg_buy_order = Order(0,100020,0,4,1100)
        result = self.me.processOrder(0, astuple(agg_buy_order))
        assert len(result) == 3
        assert (result[0].id, result[0].quantity, result[0].price) == (2, 1, test_sellOrder.price)
        assert (result[1].id, result[1].orderid, result[1].quantity)  == (4, agg_buy_order.orderid, 3)
        assert (result[2].id,  result[2].orderid) == (3, test_sellOrder.orderid)

    def test_process_aggressiveSell_FullOrderFilled(self):
        self.me.processOrder(0, astuple(test_sellOrder))
        self.me.processOrder(0, astuple(test_buyOrder))
        agg_sell_order = Order(0,100020,1,1,1000)
        result = self.me.processOrder(0, astuple(agg_sell_order))
        assert len(result) == 3
        assert (result[0].id, result[0].quantity, result[0].price) == (2, 1, 1050)
        assert (result[1].id,  result[1].orderid) == (3, 100001)
        assert (result[2].id,  result[2].orderid) == (3, 100020)

    def test_process_aggressiveSell_partialOrderFilled(self):
        self.me.processOrder(0, astuple(test_sellOrder))
        self.me.processOrder(0, astuple(test_buyOrder))
        agg_sell_order = Order(0,100020,1,4,1000)
        result = self.me.processOrder(0, astuple(agg_sell_order))
        assert len(result) == 3
        assert (result[0].id, result[0].quantity, result[0].price) == (2, 1, test_buyOrder.price)
        assert (result[1].id, result[1].orderid, result[1].quantity) == (4, agg_sell_order.orderid, 3)
        assert (result[2].id,  result[2].orderid) == (3, test_buyOrder.orderid)
