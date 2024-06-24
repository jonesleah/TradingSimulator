# TradingSimulator

This simulator currently supports backtesting SMA, EMA, and Mean Reversion trading strategies. It prints the return and risk and plots the results.

## Usage
Clone the repository and install the dependencies:
```bash
pip install -r requirements.txt

Run a backtest with the following command, replacing the <> placeholders with values.
Run python main.py -h for help.
```bash
python main.py <strategy> <stock> <start_date> <end_date> [--short <short_window>] [--long <long_window>] [--longBias <True/False>] [--period <period_window>]
