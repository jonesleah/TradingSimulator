from strategies.baseStrategy import baseStrategy
import numpy as np
import matplotlib.pyplot as plt

# STRATEGY: Since an asset will eventually move toward its average,
#           - go long when the RSI is less than 30 and its price is less than 2 std devs away from its movingAvg
#           - go short when the RSI is greater than 70 and its price is more than 2 std devs from the movingAvg

class meanReversionStrategy(baseStrategy):
    def __init__(self, stock, start, end, range):
        super().__init__(stock, start, end)
        self.range = range

    def getRSI(self):
        # Get the RSI over the defualt 14 day period ==> 100 - 100/(1 + avgGain/avgLoss))
        priceChange = self.data["Close"].diff()
        EMA_gain = priceChange.where(priceChange > 0, 0).ewm(span=14, min_periods=14).mean()
        EMA_loss = (-priceChange).where(priceChange < 0, 0).ewm(span=14,min_periods=14).mean()
        RSI = 100 - 100/(1 + EMA_gain/EMA_loss)
        return RSI

    def strategy(self):
        self.data["movingAvg"] = self.data.Close.rolling(self.range).mean()
        self.data["stdDev"] = self.data.Close.rolling(self.range).std()
        self.data["upperBound"] = self.data.movingAvg + (2 * self.data.stdDev)
        self.data["lowerBound"] = self.data.movingAvg - (2 * self.data.stdDev)
        self.data["RSI"] = self.getRSI()
        self.data["position"] = np.where((self.data["RSI"] < 30) & (self.data["Close"] < self.data["lowerBound"]), 1, 0)
        self.data["position"] = np.where((self.data["RSI"] > 70) & (self.data["Close"] > self.data["upperBound"]), -1, 0)
        
    def plotResults(self):
        plt.figure(figsize=(12, 8))
        plt.plot(self.data.index, self.data['Close'], label='Close Price')
        plt.fill_between(self.data.index, self.data['upperBound'], self.data['lowerBound'], label = 'Upper/Lower Bounds', color='lightgray')
        plt.scatter(self.data[self.data["position"] == 1].index, self.data[self.data["position"] == 1]['Close'], marker='^', color='green', label='Buy Signal')
        plt.scatter(self.data[self.data["position"] == -1].index, self.data[self.data["position"] == -1]['Close'], marker='v', color='red', label='Sell Signal')
        plt.title('{} - Mean Reversion Strategy'.format(self.stock))
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        plt.grid(True)
        plt.show()