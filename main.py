from strategies.SMAStrategy import SMAStrategy
from strategies.EMAStrategy import EMAStrategy
from strategies.meanReversionStrategy import meanReversionStrategy
from datetime import date
import argparse
import sys

def parseInput():
    parser = argparse.ArgumentParser(description='Backtest a trading strategy')
    parser.add_argument('strategy', type=str, choices=['SMA', 'EMA', 'meanReversion'], help='Trading strategy to use')
    parser.add_argument('stock', type=str, help='Stock ticker symbol')
    parser.add_argument('start', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('end', type=str, help='End date in YYYY-MM-DD format')
    parser.add_argument('--short', type=int, default=20, help='Short window for SMA/EMA strategies (Default=50)')
    parser.add_argument('--long', type=int, default=200, help='Long window for SMA/EMA strategies (Default=200)')
    parser.add_argument('--longBias', type=bool, default=False, help='Long bias, doesn\'t go short (Default=False)')
    parser.add_argument('--period', type=int, default=50, help='Timeframe window for Mean Reversion strategy (Default=50)')

    try:
        args = parser.parse_args()
        return args
    except argparse.ArgumentError as err:
        print(f'Parsing error: {err}')
        parser.print_help()
        sys.exit(2)

def main():
    args = parseInput()

    if args.strategy == 'SMA':
        strategy = SMAStrategy(args.stock, args.start, args.end, args.short, args.long, args.longBias)
    elif args.strategy == 'EMA':
        strategy = EMAStrategy(args.stock, args.start, args.end, args.short, args.long, args.longBias)
    elif args.strategy == 'meanReversion':
        strategy = meanReversionStrategy(args.stock, args.start, args.end, args.period)
    else:
        print("No valid strategy was entered")

    stratReturn, buyHoldReturn, stratStdDev, buyHoldStdDev, data = strategy.backtest()
    print(f"Cumulative Buy/Hold Return: {buyHoldReturn:.2f}")
    print(f"Cumulative {args.strategy} Return: {stratReturn:.2f}")
    print(f"{args.strategy} Risk (Std Dev): {stratStdDev:.2f}")
    print(f"Buy/Hold Risk (Std Dev): {buyHoldStdDev:.2f}")
    strategy.plotResults()
    

if __name__ == "__main__":
    main()