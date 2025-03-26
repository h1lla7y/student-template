#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 20:14:24 2025

@author: hillary
"""

import pandas as pd
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
import time


def calculate_implied_volatility(ticker):
    try:
        stock = yf.Ticker(ticker)
        stock_history = stock.history(period="1y", interval="1d")
        stock_history['Daily Returns'] = stock_history['Adj Close'].pct_change()

        return stock_history[['Adj Close', 'Daily Returns']]

    except Exception as e:
        print(f"Error calculating daily returns for {ticker}: {e}")
        return None

stock_list = ['CHWY', 'APA', 'AMD', 'TXN', 'INTC', 'JPM', 'SBUX', 'MSFT', 'CAVA', 'STRL']

stock_returns = {}
stock_volatility = {}

for ticker in stock_list:
    sreturns_data = calculate_implied_volatility(ticker)
    if sreturns_data is not None:
        stock_returns[ticker] = sreturns_data
        stock_std = sreturns_data['Daily Returns'].std()
        annual_volatility = stock_std * np.sqrt(252)
        stock_volatility[ticker] = annual_volatility
        
        print(f"Daily returns for {ticker} calculated successfully.")
        time.sleep(20)  # Wait 20 seconds before next request
    else:
        print(f"Failed to calculate returns for {ticker}")


sorted_stocks = sorted(stock_volatility, key=stock_volatility.get, reverse=True)
print("Sorted stocks by implied volatility:", sorted_stocks)


top_stocks = sorted_stocks[:5]

class TradingProfessional:
    def __init__(self, stock_data):
        self.data = stock_data

    def calculate_bollinger_bands(self):
        self.data['BB_Middle'] = self.data['Close'].rolling(window=20).mean()
        self.data['BB_Upper'] = self.data['BB_Middle'] + (self.data['Close'].rolling(window=20).std() * 2)
        self.data['BB_Lower'] = self.data['BB_Middle'] - (self.data['Close'].rolling(window=20).std() * 2)

    def generate_signals(self):
        self.data['Signal'] = 0
        self.data.loc[self.data['Close'] > self.data['BB_Upper'], 'Signal'] = -1  # Sell
        self.data.loc[self.data['Close'] < self.data['BB_Lower'], 'Signal'] = 1   # Buy

    def backtest_strategy(self):
        # Calculate strategy returns
        self.data['Strategy Returns'] = self.data['Close'].pct_change() * self.data['Signal'].shift(1)
        self.data['Cumulative Returns'] = (1 + self.data['Strategy Returns']).cumprod()
        
        print(self.data[['Close', 'Signal', 'Strategy Returns', 'Cumulative Returns']].tail())

    def visualize_strategy(self, ticker):
        plt.figure(figsize=(14, 7))
        plt.plot(self.data['Close'], label='Close Price')
        plt.plot(self.data['BB_Middle'], label='Moving Average')
        plt.plot(self.data['BB_Upper'], label='Upper Band')
        plt.plot(self.data['BB_Lower'], label='Lower Band')

        plt.scatter(self.data[self.data['Signal'] == 1].index, self.data[self.data['Signal'] == 1]['Close'], marker='^', color='green', label='Buy Signal')
        plt.scatter(self.data[self.data['Signal'] == -1].index, self.data[self.data['Signal'] == -1]['Close'], marker='v', color='red', label='Sell Signal')

        plt.title(f'Bollinger Bands and Trading Signals for {ticker}')
        plt.legend()
        plt.show()


for ticker in top_stocks:
    stock_data = yf.download(ticker, period="1y")
    trading_prof = TradingProfessional(stock_data)
    trading_prof.calculate_bollinger_bands()
    trading_prof.generate_signals()
    trading_prof.backtest_strategy()
    trading_prof.visualize_strategy(ticker)

# When code is run, there is an error that the server failed and there are
# too many requests. I'm submitting this framework for the time being.

