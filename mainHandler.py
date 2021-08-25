import logging
import sys

from engine import OrderBook
from order import Order

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
log.addHandler(handler)

class InputOutputHandler:
    def __init__(self):
        self.orderBook = OrderBook()
        self.process_input()

    def process_input(self):
        log.info("\nuse PRINT to get current market depth or Q/CTRL-C to quit")
        for line in sys.stdin:
            if line.rstrip().lower() == 'print':
                print(self.orderBook)
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
            result = self.orderBook.addOrder(ord)
            if result:
                self.process_output(result)
        else:
            try:
                orderid = args[1]
                result = self.orderBook.cancelOrder(orderid)
                if not result:
                    log.error("Cancel order with orderid = %s not found" %(orderid))
            except IndexError:
                log.error("expected orderid with cancel order")

    def process_output(self, result):
        print("\n")
        for evts in result:
            print(evts)
        print("\n")

def main():
    ih = InputOutputHandler()
    '''
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