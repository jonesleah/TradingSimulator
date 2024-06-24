# TradingSimulator

This simulator currently supports backtesting SMA, EMA, and Mean Reversion trading strategies. It prints the return and risk and plots the results.

## Usage
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt
```
Run a backtest with the following command, replacing the <> placeholders with values.
Run python main.py -h for help.
```bash
python main.py <strategy> <stock> <start_date> <end_date> [--short <short_window>] [--long <long_window>] [--longBias <True/False>] [--period <period_window>]
```
## Example Input/Output
```bash
python main.py SMA AAPL 2020-01-01 2024-01-01 --short 20 --long 200
```
Strategy Return: 1.03, 
Strategy Risk (Std Dev): 0.28
<img width="809" alt="SMA_demo" src="https://github.com/jonesleah/tradingSimulator/assets/148723943/890f5515-c82b-4b73-8a6b-cb3a15fe9ef6">
