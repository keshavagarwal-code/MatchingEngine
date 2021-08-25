from order import Order
from engine import OrderBook, MatchingEngine
    
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
        result = self.ob.cancelOrder(test_buyOrder.orderid)
        assert len(self.ob.buy) == le - 1
        assert result == True

    def test_cancelOrder_sell(self):
        #must run after test_addOrder
        if len(self.ob.buy) == len(self.ob.sell) == 0:
            self.test_addOrder_sell()
        le = len(self.ob.sell)
        result = self.ob.cancelOrder(test_sellOrder.orderid)
        assert len(self.ob.sell) == le - 1
        assert result == True

    def test_cancelOrder_invalid(self):
        #must run after test_addOrder
        result = self.ob.cancelOrder(12344)
        assert result == False

class TestMatchingEngine:
    def setup(self):
        self.ob = OrderBook()

    def test_process_aggressiveBuy_FullOrderFilled(self):
        self.ob.addOrder(test_sellOrder)
        self.ob.addOrder(test_buyOrder)
        agg_buy_order = Order(0,100020,0,1,1100)
        result = self.ob.addOrder(agg_buy_order)
        assert len(result) == 3
        assert result[0] == ['TradeEvent', 1, 1075]
        assert result[1] == ['FullOrderFilled', 100020]
        assert result[2] == ['FullOrderFilled', 100000]

    def test_process_aggressiveBuy_partialOrderFilled(self):
        self.ob.addOrder(test_sellOrder)
        self.ob.addOrder(test_buyOrder)
        agg_buy_order = Order(0,100020,0,4,1100)
        result = self.ob.addOrder(agg_buy_order)
        assert len(result) == 3
        assert result[0] == ['TradeEvent', 1, test_sellOrder.price]
        assert result[1] == ['PartialOrderFilled', agg_buy_order.orderid, 3]
        assert result[2] == ['FullOrderFilled', test_sellOrder.orderid]

    def test_process_aggressiveSell_FullOrderFilled(self):
        self.ob.addOrder(test_sellOrder)
        self.ob.addOrder(test_buyOrder)
        agg_sell_order = Order(0,100020,1,1,1000)
        result = self.ob.addOrder(agg_sell_order)
        assert len(result) == 3
        assert result[0] == ['TradeEvent', 1, 1050]
        assert result[1] == ['FullOrderFilled', 100001]
        assert result[2] == ['FullOrderFilled', 100020]

    def test_process_aggressiveSell_partialOrderFilled(self):
        self.ob.addOrder(test_sellOrder)
        self.ob.addOrder(test_buyOrder)
        agg_sell_order = Order(0,100020,1,4,1000)
        result = self.ob.addOrder(agg_sell_order)
        assert len(result) == 3
        assert result[0] == ['TradeEvent', 1, test_buyOrder.price]
        assert result[1] == ['PartialOrderFilled', agg_sell_order.orderid, 3]
        assert result[2] == ['FullOrderFilled', test_buyOrder.orderid]
