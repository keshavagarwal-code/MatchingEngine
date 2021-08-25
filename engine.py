from sortedarray import MinSortedArray, MaxSortedArray
from enum import IntEnum
from order import Order, TradeEvent, PartialOrderFilled, FullOrderFilled

import sys
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)

class OrderBook:
    def __init__(self):
        self.buy = MaxSortedArray()
        self.sell = MinSortedArray()
        
    def __str__(self):
        all_buy = [i.visualize() for i in self.buy]
        all_sell = [i.visualize() for i in self.sell]

        i = 0
        j = 0
        
        ex_str = '-' * 13 + " BUY " + '-' * 14 + " | " + '-' * 13 + " SELL " + '-' * 13
        log_str = "{0:>10} {1:>10} {2:>10} | {3:>10} {4:>10} {5:>10} "
        print("\n" + ex_str)
        headers = ['orderid', 'quantity', 'price']
        header_format = [h.rjust(10) for h in headers] + [h.rjust(10) for h in headers[::-1]]
        log.info("{0} {1} {2} | {3} {4} {5} ".format(*header_format))
        while i < len(all_buy) or j < len(all_sell) :
            if i < len(all_buy) and j < len(all_sell):
                log.info(log_str.format(*all_buy[i], *all_sell[j][::-1]))
            
            elif i < len(all_buy) and j >= len(all_sell) :
                log.info(log_str.format(*all_buy[i], '--', '--', '--'))
            
            else:
                log.info(log_str.format('---', '---', '---', *all_sell[j][::-1]))
            i += 1
            j += 1
        
        return ""
    
    def addOrder(self, order):
        aggresive_order = False
        result = None
        if order.side == 0:
            self.buy.add(order)
            if self.buy.peek().orderid == order.orderid:
                aggresive_order = True
        else:
            self.sell.add(order)
            if self.sell.peek().orderid == order.orderid:
                aggresive_order = True
        if aggresive_order:
            mt = MatchingEngine(self.buy, self.sell)
            self.buy, self.sell, result = mt.process(order.side)
        return result

    def cancelOrder(self, orderid, quantity=None):
        #Fix this, ideally we should be able to identify if its buy or sell
        result = self.buy.remove(orderid, quantity) or self.sell.remove(orderid, quantity)
        return result

        
class MatchingEngine:
    def __init__(self, buyBook, sellBook):
        self.buyBook = buyBook
        self.sellBook = sellBook
    
    def process(self, side, Trade=True):
        result = []
        while Trade and self.buyBook and self.sellBook:
            Trade = False
            topBuyOrder, topSellOrder = self.buyBook.peek(), self.sellBook.peek()
            if side == 0:
                tradePrice = topSellOrder.price
            else:
                tradePrice = topBuyOrder.price
                    
            if topBuyOrder.price >= topSellOrder.price:
                Trade = True
                #top buy and sell qty is same
                if topBuyOrder.quantity == topSellOrder.quantity:
                    self.buyBook.pop()
                    self.sellBook.pop()
                    #raise TradeEvent, 2 FullOrderFilledEvent
                    result.append(TradeEvent(topSellOrder.quantity, tradePrice))
                    result.append(FullOrderFilled(topBuyOrder.orderid))
                    result.append(FullOrderFilled(topSellOrder.orderid))
                    
                #top buy quantity is less then sell quantity
                elif topBuyOrder.quantity > topSellOrder.quantity:
                    self.buyBook.remove(topBuyOrder.orderid, topSellOrder.quantity)
                    self.sellBook.pop()
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    result.append(TradeEvent(topSellOrder.quantity, tradePrice))
                    result.append(PartialOrderFilled(topBuyOrder.orderid, topBuyOrder.quantity))
                    result.append(FullOrderFilled(topSellOrder.orderid))

                else:
                    self.sellBook.remove(topSellOrder.orderid, topBuyOrder.quantity)
                    self.buyBook.pop()
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    result.append(TradeEvent(topBuyOrder.quantity, tradePrice))
                    result.append(PartialOrderFilled(topSellOrder.orderid, topSellOrder.quantity))
                    result.append(FullOrderFilled(topBuyOrder.orderid))
                    
        return self.buyBook, self.sellBook, result
                

