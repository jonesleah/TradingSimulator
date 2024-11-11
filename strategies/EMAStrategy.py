from strategies.baseStrategy import baseStrategy
import numpy as np
import matplotlib.pyplot as plt

# STRATEGY: more weight given to recent values than in SMA => more responsive to price changes
class EMAStrategy(baseStrategy):
    def __init__(self, stock, start, end, EMA_short, EMA_long, longBias):
        super().__init__(stock, start, end)
        self.EMA_short = EMA_short
        self.EMA_long = EMA_long
        self.longBias = longBias
    
    def strategy(self):
        # adjust=False sets the weight factor to 2/(span + 1)
        self.data["EMA_short"] = self.data.Close.ewm(span=self.EMA_short, min_periods=self.EMA_short).mean()
        self.data["EMA_long"] = self.data.Close.ewm(span=self.EMA_long, min_periods=self.EMA_long).mean()
        self.data.dropna(inplace=True)
        if self.longBias:
            self.data["position"] = np.where(self.data["EMA_short"] > self.data["EMA_long"], 1, 0)
        else:
            self.data["position"] = np.where(self.data["EMA_short"] > self.data["EMA_long"], 1, -1)

    def plotResults(self):
        # 1st graph: Short/Long EMA Strategy
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data.Close, label='Close Price')
        plt.plot(self.data.index, self.data.EMA_short, label=f'EMA {self.EMA_short}')
        plt.plot(self.data.index, self.data.EMA_long, label=f'EMA {self.EMA_long}')
        
        if self.longBias:
            plt.fill_between(self.data.index, self.data.Close, where=self.data.position == 0, color='yellow', label='Hold')
        plt.fill_between(self.data.index, self.data.Close, where=self.data.position == 1, color='green', label='Long')
        plt.fill_between(self.data.index, self.data.Close, where=self.data.position == -1, color='red', label='Short')

        plt.title(f'{self.stock} - EMA{self.EMA_short} | EMA{self.EMA_long}', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Price', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.show()

        # 2nd graph: Comparison of strategy returns to returns of buy/hold
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data.BuyHoldReturns, label="Buy and Hold Strategy")
        plt.plot(self.data.index, self.data.StrategyReturns, label='EMA Strategy')

        plt.title(f'{self.stock} - Cumulative Returns with EMA Strategy vs. Buy and Hold', fontsize=12)
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Cumulative Returns', fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True)
        plt.show()
