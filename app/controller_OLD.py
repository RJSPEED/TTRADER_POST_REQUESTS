
from flask import Flask, render_template, request, redirect, session, jsonify
from app.account import Account
from app.position import Position
from app import views
from app import util
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "The session needs this!"

@app.route('/createaccount/<name>/<password>', methods=['GET'])
def createaccount(name, password):
    new_account = Account(username=name)
    new_account.set_password(password)
    ak = new_account.create_api_key()
    new_account.save()
    #msg = "Account successfully created"
    msg = "Account successfully created, API Key = {}".format(ak)
    return jsonify({'message':msg})

@app.route('/viewapikey/<name>/<password>', methods=['GET'])
def viewapikey(name, password):
    if not Account.login(name, password):
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.login(name, password).pk
        retrieve_ak = Account(pk=pk)
        msg = "Your API Key = {}".format(retrieve_ak.get_account().api_key)
    return jsonify({'message':msg})

# @app.route('/viewbalance/<name>/<password>', methods=['GET'])
# def viewbalance(name, password):
#     if not Account.login(name, password):
@app.route('/viewbalance/<key>', methods=['GET'])
def viewbalance(key):
    if Account.api_authenticate(key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        retrieve_bal = Account(pk=pk)
        msg = "Your current balance = {}".format(retrieve_bal.get_account().balance)
    return jsonify({'message':msg})

# @app.route('/deposit/<name>/<password>/<amount>', methods=['GET'])
# def deposit(name, password, amount):
#     if not Account.login(name, password):
@app.route('/deposit/<key>/<amount>', methods=['GET'])
def deposit(key, amount):
    if Account.api_authenticate(key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        account_deposit = Account(pk=pk)
        new_bal = account_deposit.deposit(float(amount))
        account_deposit.save()
        msg = "New Balance = {}".format(new_bal)
    return jsonify({'message':msg})    
    
@app.route('/lookupticker/<ticker>', methods=['GET'])
def lookupticker(ticker):    
    quote = util.get_price(ticker)
    if not quote: 
        msg = "The Ticker Symbol entered does not exist"
    else:
        msg = "Current price for Ticker Symbol: {} = ${}".format(ticker, quote)
    return jsonify({'message':msg})

@app.route('/lookupcompany/<company>', methods=['GET'])
def lookupcompany(company):
    companies = util.get_ticker(company)
    if not companies: 
        msg = "No matches for input Company Name"
    else:
        msg = {'company':[]}
        for co in companies:
            msg['company'].append(co)
    return jsonify({'message':msg})

# @app.route('/buy/<name>/<password>/<ticker>/<shares>', methods=['GET'])
# def buy(name,password,ticker,shares):
#     if not Account.login(name, password):
@app.route('/buy/<key>/<ticker>/<shares>', methods=['GET'])
def buy(key,ticker,shares):    
    if Account.api_authenticate(key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        buy_txn = Account(pk=pk)
        msg = buy_txn.buy(ticker, shares)
    return jsonify({'message':msg})  

# @app.route('/sell/<name>/<password>/<ticker>/<shares>', methods=['GET'])
# def sell(name,password,ticker,shares):
#     if not Account.login(name, password):
@app.route('/sell/<key>/<ticker>/<shares>', methods=['GET'])
def sell(key,ticker,shares):
    if Account.api_authenticate(key) == None:        
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        sell_txn = Account(pk=pk)
        msg = sell_txn.sell(ticker, shares)
    return jsonify({'message':msg})  

# @app.route('/trades/<name>/<password>/<ticker>', methods=['GET'])
# def trades(name, password, ticker):
#     if not Account.login(name, password):
@app.route('/trades/<key>/<ticker>', methods=['GET'])
def trades(key, ticker):
    if Account.api_authenticate(key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        user_trades = Account(pk=pk)
        trades = user_trades.get_trades_for(ticker)
        msg = {'trades':[]}
        for trade in trades:
            msg['trades'].append("Date/Time: {}, Ticker Symbol: {}, No. of Shares: {}, Price per Share: {}". \
                          format((datetime.fromtimestamp(trade.time) - \
                          timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), \
                          trade.ticker, trade.volume, trade.price))
    return jsonify({'message':msg}) 

# @app.route('/alltrades/<name>/<password>', methods=['GET'])
# def alltrades(name, password):
#     if not Account.login(name, password):
@app.route('/alltrades/<key>', methods=['GET'])
def alltrades(key):        
    if Account.api_authenticate(key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        user_trades = Account(pk=pk)
        trades = user_trades.get_trades()
        msg = {'trades':[]}
        for trade in trades:
            msg['trades'].append("Date/Time: {}, Ticker Symbol: {}, No. of Shares: {}, Price per Share: {}". \
                          format((datetime.fromtimestamp(trade.time) - \
                          timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), \
                          trade.ticker, trade.volume, trade.price))
    return jsonify({'message':msg}) 

# @app.route('/positions/<name>/<password>/<ticker>', methods=['GET'])
# def positions(name, password, ticker):
#     if not Account.login(name, password):
@app.route('/positions/<key>/<ticker>', methods=['GET'])
def positions(key, ticker):
    if Account.api_authenticate(key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        user_position = Account(pk=pk)
        position = user_position.get_position_for(ticker)
        valuation = Position()  
        getval = valuation.current_value(ticker, position.shares)      
        msg = "Ticker Symbol: {}, Shares: {}, Valuation: ${}".format(position.ticker, position.shares, getval)
    return jsonify({'message':msg}) 
            
# @app.route('/allpositions/<name>/<password>', methods=['GET'])
# def allpositions(name, password):
#     if not Account.login(name, password):
@app.route('/allpositions/<key>', methods=['GET'])
def allpositions(key):      
    if Account.api_authenticate(key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        #pk = Account.login(name, password).pk
        pk = Account.api_authenticate(key).pk
        user_positions = Account(pk=pk)
        positions = user_positions.get_positions()
        msg = {'positions':[]}
        for position in positions:
            valuation = Position()  
            getval = valuation.current_value(position.ticker, position.shares)     
            msg['positions'].append("Ticker Symbol: {}, Shares: {}, Valuation: ${}".format(position.ticker, position.shares, getval))
    return jsonify({'message':msg}) 

def run():
    app.run(debug=True)
