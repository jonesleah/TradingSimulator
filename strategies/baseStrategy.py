# Base class to run strategy backtesting
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class baseStrategy:
    def __init__(self, stock, start, end):
        self.stock = stock
        self.start = start
        self.end = end
        self.data = None

    def getData(self):
        self.data = yf.download(self.stock, start=self.start, end=self.end)
        self.data = self.data.Close.to_frame()
        self.data['returns'] = np.log(self.data['Close'] / self.data['Close'].shift(1))


    def backtest(self):
        self.getData()
        self.strategy()
        self.data["strategy"] = self.data["returns"] * self.data["position"].shift(1)
        self.data.dropna(inplace=True)
        stratReturn = np.exp(self.data["strategy"].sum())
        buyHoldReturn = np.exp(self.data["returns"].sum())
        stratStdDev = self.data["strategy"].std() * np.sqrt(252)
        buyHoldStdDev = self.data["returns"].std() * np.sqrt(252)
        self.data["BuyHoldReturns"] = self.data["returns"].cumsum().apply(np.exp)
        self.data["StrategyReturns"] = self.data["strategy"].cumsum().apply(np.exp)
        return stratReturn, buyHoldReturn, stratStdDev, buyHoldStdDev, self.data