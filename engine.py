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
        self.orderMap = dict()
        
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
        if order.orderid not in self.orderMap:
            if order.side == 0:
                self.buy.add(order)
            else:
                self.sell.add(order)
            self.orderMap[order.orderid] = order
        else:
            log.error("Order id %s already exists in OrderBook" %(order.orderid))
        
    def cancelOrderByOrderId(self, orderid):
        if orderid in self.orderMap:
            if self.orderMap[orderid].side == 0:
                self.buy.deleteByAttr('orderid', orderid)
            else:
                self.sell.deleteByAttr('orderid', orderid)
            del self.orderMap[orderid]
            return True
        return False

    def popOrder(self, side):
        if side == 0:
            del self.orderMap[self.buy.peek().orderid]
            self.buy.pop()
        else:
            del self.orderMap[self.sell.peek().orderid]
            self.sell.pop()

    def modifyTopOrderQuantity(self, side, new_qty):
        if side == 0:
            self.buy.replaceTopAttr('quantity', new_qty)
        else:
            self.sell.replaceTopAttr('quantity', new_qty)
        
class MatchingEngine:
    def __init__(self):
        self.orderbook = OrderBook()

    def printBook(self):
        return self.orderbook
    
    def processOrder(self, msgtype, args):
        order_queue = None
        if msgtype == 0:
            try:
                ord = Order(*args)
            except Exception:
                log.error("Unknown message: BADMESSAGE")
                return order_queue
            self.orderbook.addOrder(ord)
            order_queue = self.process(ord.side)
        else:
            try:
                orderid = args[1]
                result = self.orderbook.cancelOrderByOrderId(orderid)
                if not result:
                    log.error("Cancel order with orderid = %s not found" %(orderid))
            except IndexError:
                log.error("expected orderid with cancel order")
        return order_queue
    
    def process(self, side, Trade=True):
        result = []
        while Trade and self.orderbook.buy and self.orderbook.sell:
            Trade = False
            topBuyOrder, topSellOrder = self.orderbook.buy.peek(), self.orderbook.sell.peek()
            if side == 0:
                tradePrice = topSellOrder.price
            else:
                tradePrice = topBuyOrder.price
                    
            if topBuyOrder.price >= topSellOrder.price:
                Trade = True
                #top buy and sell qty is same
                if topBuyOrder.quantity == topSellOrder.quantity:
                    self.orderbook.popOrder(topBuyOrder.side)
                    self.orderbook.popOrder(topSellOrder.side)
                    #raise TradeEvent, 2 FullOrderFilledEvent
                    result.append(TradeEvent(topSellOrder.quantity, tradePrice))
                    result.append(FullOrderFilled(topBuyOrder.orderid))
                    result.append(FullOrderFilled(topSellOrder.orderid))
                    
                #top buy quantity is less then sell quantity
                elif topBuyOrder.quantity > topSellOrder.quantity:
                    self.orderbook.modifyTopOrderQuantity(topBuyOrder.side, topBuyOrder.quantity - topSellOrder.quantity)
                    self.orderbook.popOrder(topSellOrder.side)
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    result.append(TradeEvent(topSellOrder.quantity, tradePrice))
                    result.append(PartialOrderFilled(topBuyOrder.orderid, topBuyOrder.quantity))
                    result.append(FullOrderFilled(topSellOrder.orderid))

                else:
                    self.orderbook.modifyTopOrderQuantity(topSellOrder.side, topSellOrder.quantity - topBuyOrder.quantity)
                    self.orderbook.popOrder(topBuyOrder.side)
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    result.append(TradeEvent(topBuyOrder.quantity, tradePrice))
                    result.append(PartialOrderFilled(topSellOrder.orderid, topSellOrder.quantity))
                    result.append(FullOrderFilled(topBuyOrder.orderid))
                    
        return result
                

