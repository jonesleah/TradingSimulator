from strategies.baseStrategy import baseStrategy
import numpy as np
import matplotlib.pyplot as plt

# STRATEGY: if SMA_short > SMA_long, go long (buy the asset, expect its value to increase)
#           Otherwise, go short (sell the asset, expect its value to decrease)
class SMAStrategy(baseStrategy):
    def __init__(self, stock, start, end, SMA_short, SMA_long, longBias):
        super().__init__(stock, start, end)
        self.SMA_short = SMA_short
        self.SMA_long = SMA_long
        self.longBias = longBias # long bias sets position to 0 (hold) when SMA_short < SMA_long
    
    def strategy(self):
        self.data["SMA_short"] = self.data.Close.rolling(self.SMA_short).mean()
        self.data["SMA_long"] = self.data.Close.rolling(self.SMA_long).mean()
        self.data.dropna(inplace=True)
        if self.longBias:
            self.data["position"] = np.where(self.data["SMA_short"] > self.data["SMA_long"], 1, 0)
        else:
            self.data["position"] = np.where(self.data["SMA_short"] > self.data["SMA_long"], 1, -1)

    def plotResults(self):
        # 1st graph: Short/Long SMA Strategy
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data.Close, label='Close Price')
        plt.plot(self.data.index, self.data.SMA_short, label=f'SMA {self.SMA_short}')
        plt.plot(self.data.index, self.data.SMA_long, label=f'SMA {self.SMA_long}')
        
        if self.longBias:
            plt.fill_between(self.data.index, self.data.Close, where=self.data.position == 0, color='yellow', alpha=0.1, label='Hold')
        plt.fill_between(self.data.index, self.data.Close, where=self.data.position == 1, color='green', alpha=0.1, label='Long')
        plt.fill_between(self.data.index, self.data.Close, where=self.data.position == -1, color='red', alpha=0.1, label='Short')

        plt.title(f'{self.stock} - SMA{self.SMA_short} | SMA{self.SMA_long}', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.show()

        # 2nd graph: Comparison of strategy returns to returns of buy/hold
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data.BuyHoldReturns, label="Buy and Hold Strategy")
        plt.plot(self.data.index, self.data.StrategyReturns, label='SMA Strategy')

        plt.title(f'{self.stock} - Cumulative Returns with SMA Strategy vs. Buy and Hold', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Returns', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.show()