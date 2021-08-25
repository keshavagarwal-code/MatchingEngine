# Prerequisite:
    Python 3.7++
    pytest
    mock

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

1> For better matching aggressive orders eithr 
    a> Use invertedHeap and append aggressive order for constant time operation
    b> Match aggressive trade before pushing it to OrderBook
    
2> use float/double for Order Price
