# Prerequisite:
    Python 3.7++
    pytest
    mock

# Expected Message Types

MessageType
-----------
There are five types of message involved in this problem, two messages your
application shall accept as input and three that it will produce as output.
The
message types are identified by integer IDs: 
0: AddOrderRequest (input)
1: CanceOrderRequest (input)
2: TradeEvent (output)
3: OrderFullyFilled (output)
4: OrderPartiallyFilled (output)

Input Types
-----------
There are two input message types (requests):
AddOrderRequest: msgtype,orderid,side,quantity,price (e.g. 0,123,0,9,1000)
 msgtype = 0
 orderid = unique positive integer to identify each order;
 used to reference existing orders for cancel and fill messages
 side = 0 (Buy) or 1 (Sell)
 quantity = maximum quantity to buy/sell (positive integer)
 price = max price at which to buy/min price to sell (decimal number)
CancelOrderRequest: msgtype,orderid (e.g. 1,123)
 msgtype = 1
 orderid = ID of the order to remove 

# Inputs

Inputs are expected in the form of 

The following messages on stdin:  

0,100000,1,1,1075  
0,100001,0,9,1000  
0,100002,0,30,975  
0,100003,1,10,1050   
0,100004,0,10,950  
BADMESSAGE // An erroneous input. 
0,100005,1,2,1025   
0,100006,0,1,1000  
1,100004 // remove order   
0,100007,1,5,1025 // Original standing order book from Details  
0,100009,1,10,999 // Matches! Triggers trades  

The final message should cause your program to produce the following ouput on  
stdout:  

2, 9, 1000  
4, 100009, 1  
3, 100001  
2, 1, 1000  
3, 100006  
3, 100009  

Special Inputs created:  

PRINT to get current market depth  

```
------------- BUY -------------- | ------------- SELL -------------
   orderid   quantity      price |      price   quantity    orderid 
    100002         30        975 |       1025          2     100005 
       ---        ---        --- |       1025          5     100007 
       ---        ---        --- |       1050         10     100003 
       ---        ---        --- |       1075          1     100000 

```

Q to exit the program  

# How to Run:

$ python3.8 mainHandler.py

# Performance:

Bid(Buy) and ask(sell) are maintained using Heap, as a result worst performance is below  

| Operation         | Performance |
| ----------------- | ----------- |
| AddOrder          | O(log N)    |
| cancelOrder       | O(N)        |
| AggresiveBuy/Sell | O(1)        |
-----------------------------------

# Enchancements

1> For better matching aggressive orders either  
    a> Use invertedHeap and append aggressive order for constant time operation  
    b> Match aggressive trade before pushing it to OrderBook  
    
2> use float/double for Order Price
