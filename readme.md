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

The final message should cause your program to produce the following ouput on. 
stdout:  
0,100009,1,10,999
2, 9, 1000
4, 100009, 1
3, 100001
2, 1, 1000
3, 100006
3, 100009

Special Inputs created:  

<PRINT> to get current market depth. 
<Q> to exit the program  

# How to Run:

$ python3.8 mainHandler.py
