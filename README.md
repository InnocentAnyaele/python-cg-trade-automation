# python-cg-trade-automation
A python script that automates trading on the CG trading website

#### this algorithm automates the trading of BTC/USDT on the cgzg trading website. The excel file contains a simple trading strategy. It begins with the first trade in Sheet2(Side 1) column which is a fall and bids the respective amount at the "Buy" column. If it's successful it follows a rise in the next line and bids the respective amount. If it successful it moves on the next. At any point the trade is not successful if begins the trade loop. The automation runs based on the length of data on the Stage column.
