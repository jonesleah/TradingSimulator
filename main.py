from strategies.SMAStrategy import SMAStrategy
from strategies.EMAStrategy import EMAStrategy
from strategies.meanReversionStrategy import meanReversionStrategy
from datetime import date

def main():
    stock = 'AAPL'
    start_date = '2019-01-01'
    end_date = '2020-07-01'
    SMA_short = 50
    SMA_long = 100
    longBias = True

    strategy = meanReversionStrategy(stock, start_date, end_date, 100)
    returns, stdDev, data = strategy.backtest()
    strategy.plotResults()

    print(f"Strategy Return: {returns:.2f}")
    print(f"Strategy Risk (Std Dev): {stdDev:.2f}")


if __name__ == "__main__":
    main()