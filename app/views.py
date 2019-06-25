
from datetime import datetime, timedelta
from pprint import pprint
import os

def get_input(param):
    print()
    print(param, " : ", end="")
    return input()

def generic_msg(param):
    print()
    print(param)
    print()

def stock_price(ticker, quote):
    #os.system('clear')
    print()
    print("Current price for Ticker Symbol: {} = ${}".format(ticker, quote))
    print()

def show_positions(position, getval):
    print()
    pprint("Ticker Symbol: {}, Shares: {}, Valuation: ${}".format(position.ticker, position.shares, getval))

def show_trades(trade):
    print()
    print("Date/Time: {}, Ticker Symbol: {}, No. of Shares: {}, Price per Share: {}". \
           format((datetime.fromtimestamp(trade.time) - \
                   timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), \
                   trade.ticker, trade.volume, trade.price))

def show_companies(co):
    print()
    print("Company Name: {}, Ticker Symbol: {}, Exchange: {}".format(co["Name"], co["Symbol"], co["Exchange"]))

def welcome_menu():
    print()
    print("1. Create Account")
    print()
    print("2. Login")
    print()
    print("3. Quit")
    print()
    
    selection = input().strip()
    try:
        selectionnum = int(selection)
    except ValueError:
        return None
    return selectionnum

def main_menu():
    print()
    print("1. View Balance & Positions")
    print()
    print("2. Deposit Money")
    print()
    print("3. Lookup Stock Price")
    print()
    print("4. Lookup Ticker Symbol")
    print()
    print("5. Buy Stock")
    print()
    print("6. Sell Stock")
    print()
    print("7. View Trade History")
    print()
    print("8. Exit")
    print()

    selection = input().strip()
    try:
        selectionnum = int(selection)
    except ValueError:
        return None
    return selectionnum

def position_menu():
    print()
    print("1. View position for a single stock")
    print()
    print("2. View all positions")
    print()
    print("3. Exit")
    print()
    
    pos_selection = input().strip()
    try:
        pos_selectionnum = int(pos_selection)
    except ValueError:
        return None
    return pos_selectionnum

def trades_menu():
    print()
    print("1. View trades for a single stock")
    print()
    print("2. View all trades")
    print()
    print("3. Exit")
    print()
    
    pos_selection = input().strip()
    try:
        pos_selectionnum = int(pos_selection)
    except ValueError:
        return None
    return pos_selectionnum