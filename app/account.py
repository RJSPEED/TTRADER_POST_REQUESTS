
import sqlite3
import random
import string
from app.orm import ORM
from app.util import hash_password
from app.util import get_price
from app.position import Position
from app.trade import Trade

class Account(ORM):

    tablename = "accounts"
    fields = ["username", "password_hash", "balance", "api_key"]

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.get('pk')
        self.username = kwargs.get('username')
        self.password_hash = kwargs.get('password_hash')
        self.balance = kwargs.get('balance')
        self.api_key = kwargs.get('api_key')

    @classmethod
    def login(cls, username, password):
        return cls.select_one_where("WHERE username = ? AND password_hash = ?",
                                    (username, hash_password(password)))
    @classmethod
    def api_authenticate(cls, key):
        ak_account = cls.select_one_where("WHERE api_key = ?", (key, ))
        if ak_account is None:
            return None
        return ak_account

    def create_api_key(self):
        self.api_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
        return self.api_key

    def set_password(self, password):
        self.password_hash = hash_password(password)

    def get_account(self):
        return Account.select_one_where("WHERE pk = ?", (self.pk,))       

    def deposit(self, deposit_amount):
        cur_balance = Account.select_one_where("WHERE pk = ?", (self.pk,))
        
        self.username = cur_balance.username
        self.password_hash = cur_balance.password_hash
        if cur_balance.balance is None:
            self.balance = deposit_amount
            self.api_key = cur_balance.api_key
            return deposit_amount
        else:
            self.balance = round(cur_balance.balance + deposit_amount,2)
            self.api_key = cur_balance.api_key
            return round(cur_balance.balance + deposit_amount, 2)

    def get_positions(self):
        return Position.select_many_where("WHERE accounts_pk = ?", (self.pk, ))

    def get_position_for(self, ticker):
        position = Position.select_one_where(
            "WHERE ticker = ? AND accounts_pk = ?", (ticker, self.pk))
        if position is None:
            return Position(ticker=ticker, accounts_pk=self.pk, shares=0)
        return position

    def get_trades(self):
        return Trade.select_many_where("WHERE accounts_pk = ? ORDER BY time DESC", (self.pk, ))

    def get_trades_for(self, ticker):
        return Trade.select_many_where("WHERE accounts_pk = ? and ticker = ? \
                                        ORDER BY time DESC", (self.pk, ticker))

    def buy(self, ticker, amount):
        #Get account details
        account = self.get_account()
        #Check stock exists and if so retrieve current price
        quote_price = get_price(ticker)
        if not quote_price: 
        #    raise KeyError
            msg = "Input Ticker doesn't exist"
        else:
            #Check sufficient funds
            quote_price = float(quote_price)
            amount = float(amount)
            if not account.balance >= amount*quote_price:
                #raise ValueError
                msg = "Insufficient funds"
            else:
                #Insert Trade row
                new_trade = Trade(accounts_pk=self.pk, ticker=ticker, \
                                  volume=amount, price=quote_price)
                new_trade.save()
                
                #Update or Insert Position row
                position = self.get_position_for(ticker)
                if position.shares == 0:
                    #Insert
                    new_position = Position(accounts_pk=self.pk, ticker=ticker, shares=amount)
                else:
                    #Update 
                    new_position = Position(pk=position.pk, accounts_pk=self.pk, ticker=ticker, \
                                            shares=position.shares + amount)
                new_position.save()
                    
                #Update balance on Account row
                new_balance = Account(pk=self.pk, username=account.username, \
                                    password_hash=account.password_hash, \
                                    balance=account.balance - (amount*quote_price), \
                                    api_key=account.api_key)
                new_balance.save()
                msg = "Buy transaction completed successfully"
        return msg

    def sell(self, ticker, amount):
        #Get account and positions details
        account = self.get_account()
        position = self.get_position_for(ticker)
        amount = int(amount)
        #Check stock exists and if so retrieve current price
        quote_price = get_price(ticker)
        if not quote_price: 
        #    raise KeyError
            msg = "Input Ticker doesn't exist"
        else:
            #Check sufficient shares
            if position.shares == 0 or amount > position.shares :
            #    raise ValueError
                msg = "Insufficient shares"
            else:
                #Insert Trade row
                new_trade = Trade(accounts_pk=self.pk, ticker=ticker, \
                                  volume=amount*-1, price=quote_price)
                new_trade.save()
                
                #Update Position row
                new_position = Position(pk=position.pk, accounts_pk=self.pk, ticker=ticker, \
                                        shares=position.shares - amount)
                new_position.save()
                    
                #Update balance on Account row
                new_balance = Account(pk=self.pk, username=account.username, \
                                    password_hash=account.password_hash, \
                                    balance=account.balance + (amount*quote_price), \
                                    api_key=account.api_key)
                new_balance.save()
                msg = "Sell transaction completed successfully"
        return msg
        
        