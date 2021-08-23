from sortedarray import MinSortedArray, MaxSortedArray
from enum import IntEnum
from order import Order

import sys
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)


TradeEvent = 2
FullOrderFilled = 3
PartialOrderFilled = 4

class OrderBook:
    def __init__(self):
        self.buy = MaxSortedArray()
        self.sell = MinSortedArray()

class OrderMessage(OrderBook):
    def __init__(self):
        super(OrderMessage, self).__init__()
        log.info("\nuse PRINT to get current market depth or Q/CTRL-C to quit")
        for line in sys.stdin:
            if line.rstrip().lower() == 'print':
                print(self)
                continue

            if line.rstrip().lower() == 'q':
                sys.exit()
            clean_line = line.rstrip().split(",")
            try:
                clean_line = [int(i) for i in clean_line]
            except Exception:
                log.error("Unknown message: BADMESSAGE")
                continue
            self._parseMessage(*clean_line)
    
    def _parseMessage(self, *args, **kwargs):
        msgtype = args[0]
        if msgtype not in (0,1):
            log.error("Unknown message type: BADMESSAGE, expected 0 or 1, received %s" %(msgtype))
            return
        
        if msgtype == 0:
            ord = Order(*args)
            self.addOrder(ord)
        else:
            try:
                orderid = args[1]
                result = self.cancelOrder(orderid)
                if not result:
                    log.error("Cancel order with orderid = %s not found" %(orderid))
            except IndexError:
                log.error("expected orderid with cancel order")
    
    def __str__(self):
        all_buy = [i.visualize() for i in self.buy]
        all_sell = [i.visualize() for i in self.sell]

        i = 0
        j = 0
        
        ex_str = '-' * 13 + " BUY " + '-' * 14 + " | " + '-' * 13 + " SELL " + '-' * 13
        print("\n" + ex_str)
        
        log.info("{0} {1} {2} | {3} {4} {5} ".format('orderid'.rjust(10), 'quantity'.rjust(10),'price'.rjust(10), 'price'.rjust(10), 'quantity'.rjust(10),'orderid'.rjust(10)))
        while i < len(all_buy) or j < len(all_sell) :
            if i < len(all_buy) and j < len(all_sell):
                log.info("{0:>10} {1:>10} {2:>10} | {3:>10} {4:>10} {5:>10} ".format(*all_buy[i], *all_sell[j][::-1]))
            
            elif i < len(all_buy) and j >= len(all_sell) :
                log.info("{0:>10} {1:>10} {2:>10} | {3:>10} {4:>10} {5:>10} ".format(*all_buy[i], '--', '--', '--'))
            
            else:
                log.info("{0:>10} {1:>10} {2:>10} | {3:>10} {4:>10} {5:>10} ".format('---', '---', '---', *all_sell[j][::-1]))
            i += 1
            j += 1
        
        return ""
    
    def addOrder(self, order):
        aggresive_order = False
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
            self.buy, self.sell = mt.process(order.side)

    def cancelOrder(self, orderid, quantity=None):
        #Fix this, ideally we should be able to identify if its buy or sell
        result = self.buy.remove(orderid, quantity) or self.sell.remove(orderid, quantity)
        return result

        
class MatchingEngine:
    def __init__(self, buyBook, sellBook):
        self.buyBook = buyBook
        self.sellBook = sellBook
    
    def process(self, side, Trade=True):
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
                    log.info("{0}, {1}, {2}".format(TradeEvent, topSellOrder.quantity, tradePrice))
                    log.info("{0}, {1}".format(FullOrderFilled, topBuyOrder.orderid))
                    log.info("{0}, {1}".format(FullOrderFilled, topSellOrder.orderid))
                    
                #top buy quantity is less then sell quantity
                elif topBuyOrder.quantity > topSellOrder.quantity:
                    self.buyBook.remove(topBuyOrder.orderid, topSellOrder.quantity)
                    self.sellBook.pop()
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    #print("%s, %s, %s, %s, %s" ,(TradeEvent, topSellOrder.quantity, tradePrice))
                    log.info("{0}, {1}, {2}".format(TradeEvent, topSellOrder.quantity, tradePrice))
                    log.info("{0}, {1}, {2}".format(PartialOrderFilled, topBuyOrder.orderid, topBuyOrder.quantity))
                    log.info("{0}, {1}".format(FullOrderFilled, topSellOrder.orderid))

                else:
                    self.sellBook.remove(topSellOrder.orderid, topBuyOrder.quantity)
                    self.buyBook.pop()
                    #raise TradeEvent, 1 FullOrderFilledEvent, 1 PartialOrderFilledEvent
                    log.info("{0}, {1}, {2}".format(TradeEvent, topBuyOrder.quantity, tradePrice))
                    log.info("{0}, {1}, {2}".format(PartialOrderFilled, topSellOrder.orderid, topSellOrder.quantity))
                    log.info("{0}, {1}".format(FullOrderFilled, topBuyOrder.orderid))
        return self.buyBook, self.sellBook
                

def main():
    TradeExchange = OrderMessage()
    '''
    TradeExchange
    0,100000,1,1,1075  
    0,100001,0,9,1000  
    0,100002,0,30,975  
    0,100003,1,10,1050  
    0,100004,0,10,950  
    BADMESSAGE // An erroneous input  
    0,100005,1,2,1025  
    0,100006,0,1,1000  
    1,100004 // remove order  
    0,100007,1,5,1025 
    '''

main()
