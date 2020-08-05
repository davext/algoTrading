import requests
import json
import yfinance as yf
import asyncio
import os
import random
import time

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import alpaca_trade_api as tradeapi


#VARIABLES:

alpacaPaperApiKeyID = os.getenv("alpacaPaperApiKeyID")
alpacaPaperSecretKey = os.getenv("alpacaPaperSecretKey")
paperBaseUrl = os.getenv("paperBaseUrl")


api = tradeapi.REST(alpacaPaperApiKeyID, alpacaPaperSecretKey, base_url=paperBaseUrl)






"""

2 ticker arrays
    
    OWN = things we own
        {symbol:MST,
        Shares:10,
        priceAcquired:5.06}
    SEARCH = things we check (we don't own)
              symbol
    
    currentEquity double.
    
    
    
    Actual algo
    threading + threadSafety for arrays
    
    lock = asyncio.Lock()
        # ... later
        await lock.acquire()
        try:
            # access shared state
        finally:
            lock.release()
    
    
    create workers
        buy worker("tkr","quantity")
        {
        Contact Alpaca with tkr & quantity.then(take money out of currentEquity 
        && add the tkr and quantity to OWN using locks) 
        }
        sell worker("tkr","quantity")
        {
         Contact Alpaca with tkr & quantity.then(put money in  currentEquity 
        && add the tkr to SEARCH using locks) 
        }
        
        looking for hits to buy
            loops SEARCH for hits
                if RSI is under 20% && Last MACD signal is Buy
                    {
                    getPrice()
                    sharesToBuy = see how many shares we can buy using 5% of currentEquity
                    call buy worker("tkr",sharesToBuy)
                    }
        looking for things to sell
            loops OWN for hits
                if Last MACD signal is sell || ( RSI is over 80% && obj.priceAcquired < getPrice() ) 
                    {
                    call sell worker("tkr","max")
                    }
        
        
        
        
        
    
    

"""


'''
Alpaca Documentation

https://alpaca.markets/docs/trading-on-alpaca/orders/

Type

we will use Market Order for now 

Time in Force
day : (9:30am - 4:00pm ET). if unfilled then canceled. If submitted after, it's queued for next trading day.
gtc : good till canceled.
opg : market on open” (MOO) and “limit on open" (pre opening i'm guessing)
cls : on close 
ioc : immediate or cancel
fok : fill or kill (only if all can fill otherwise kill)


sample order
api.submit_order(
    symbol='AAPL',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
)

'''


'''
how would getPrice work

'''


'''
how would get quantity to buy

percentageToBuy = "5"


getEquity = 

moneyToSpendOnShares = (percentageToBuy/100) * getEquity
'''


def computeRSI(data, time_window):
    diff = data.diff(1).dropna()  # diff in one field(one day)

    # this preservers dimensions off diff values
    up_chg = 0 * diff
    down_chg = 0 * diff

    # up change is equal to the positive difference, otherwise equal to zero
    up_chg[diff > 0] = diff[diff > 0]

    # down change is equal to negative deifference, otherwise equal to zero
    down_chg[diff < 0] = diff[diff < 0]

    # check pandas documentation for ewm
    # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.ewm.html
    # values are related to exponential decay
    # we set com=time_window-1 so we get decay alpha=1/time_window
    up_chg_avg = up_chg.ewm(com=time_window - 1, min_periods=time_window).mean()
    down_chg_avg = down_chg.ewm(com=time_window - 1, min_periods=time_window).mean()

    rs = abs(up_chg_avg / down_chg_avg)
    rsi = 100 - 100 / (1 + rs)
    return rsi


# msft = yf.download("MSFT", period="1d", interval="1m")
#
# df = msft
#
# df['RSI'] = computeRSI(df['Adj Close'], 14)
#
# print(df)


# api.list_positions()


# Set buying powers from Alpaca

current_equity = 0


def set_buying_power():
    global current_equity
    account = api.get_account()
    current_equity = account.buying_power
    print("Buying power: $" + account.buying_power)


async def buying_worker(tkr,period,interval):
    while True:
        tkrdata = yf.download(tkr,period=period,interval=interval)
        tkrdata['RSI'] = computeRSI(tkrdata['Adj Close'], 14)
        #if tkrdataRSI < 20%:
            #check MACD if last signal is buy:
                #caluclate 5% of equity
                #transalte to shares
                #grab lock for equity
                    #await submit albaca order
                        #if failed:
                            #unlcok
                            #continue:
                # update equity
                #unlock
                #call selling_worker(tkr)
                #break


async def selling_worker(tkr,period,interval):
    while True:
        tkrdata = yf.download(tkr, period=period, interval=interval)
        tkrdata['RSI'] = computeRSI(tkrdata['Adj Close'], 14)
        #if tkrdataRSI >






set_buying_power()
