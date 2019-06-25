
from flask import Flask, render_template, request, redirect, session, jsonify
from app.account import Account
from app.position import Position
from app import views
from app import util
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "The session needs this!"

@app.route('/api/get_api_key', methods=['POST'])
def get_api_key():
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({"error": "bad request"}), 400
    account = Account.login(request.json['username'], request.json['password'])
    if not account:
        return jsonify({"error": "access denied"})
    
    return jsonify({"username": account.username, "api_key": account.api_key})

@app.route('/api/<api_key>/balance', methods=['GET'])
def balance(api_key):
    if Account.api_authenticate(api_key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.api_authenticate(api_key).pk
        retrieve_bal = Account(pk=pk)
        msg = "Your current balance = {}".format(retrieve_bal.get_account().balance)
    return jsonify({'message':msg})

@app.route('/api/<api_key>/deposit', methods=['POST'])
def deposit(api_key):
    if Account.api_authenticate(api_key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        if not request.json or 'amount' not in request.json:
            return jsonify({"error": "bad request"}), 400
        pk = Account.api_authenticate(api_key).pk
        account_deposit = Account(pk=pk)
        new_bal = account_deposit.deposit(float(request.json['amount']))
        account_deposit.save()
        msg = "New Balance = {}".format(new_bal)
    return jsonify({'message':msg})    

@app.route('/api/price/<ticker>', methods=['GET'])
def price(ticker):    
    quote = util.get_price(ticker)
    if not quote: 
        msg = "The Ticker Symbol entered does not exist"
    else:
        msg = "Current price for Ticker Symbol: {} = ${}".format(ticker, quote)
    return jsonify({'message':msg})

@app.route('/api/<api_key>/buy', methods=['POST'])
def buy(api_key):    
    if Account.api_authenticate(api_key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        if not request.json or 'ticker' not in request.json or 'volume' not in request.json:
            return jsonify({"error": "bad request"}), 400
        pk = Account.api_authenticate(api_key).pk
        buy_txn = Account(pk=pk)
        msg = buy_txn.buy(request.json['ticker'], request.json['volume'])
    return jsonify({'message':msg}) 

@app.route('/api/<api_key>/sell', methods=['POST'])
def sell(api_key):
    if Account.api_authenticate(api_key) == None:        
        msg = "Invalid login credentials, pls retry"
    else: 
        if not request.json or 'ticker' not in request.json or 'volume' not in request.json:
            return jsonify({"error": "bad request"}), 400
        pk = Account.api_authenticate(api_key).pk
        sell_txn = Account(pk=pk)
        msg = sell_txn.sell(request.json['ticker'], request.json['volume'])
    return jsonify({'message':msg})  

@app.route('/api/<api_key>/trades/<ticker>', methods=['GET'])
def trades(api_key, ticker):
    if Account.api_authenticate(api_key) == None:
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.api_authenticate(api_key).pk
        user_trades = Account(pk=pk)
        trades = user_trades.get_trades_for(ticker)
        msg = {'trades':[]}
        for trade in trades:
            msg['trades'].append("Date/Time: {}, Ticker Symbol: {}, No. of Shares: {}, Price per Share: {}". \
                          format((datetime.fromtimestamp(trade.time) - \
                          timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), \
                          trade.ticker, trade.volume, trade.price))
    return jsonify({'message':msg}) 

@app.route('/api/<api_key>/trades', methods=['GET'])
def alltrades(api_key):        
    if Account.api_authenticate(api_key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.api_authenticate(api_key).pk
        user_trades = Account(pk=pk)
        trades = user_trades.get_trades()
        msg = {'trades':[]}
        for trade in trades:
            msg['trades'].append("Date/Time: {}, Ticker Symbol: {}, No. of Shares: {}, Price per Share: {}". \
                          format((datetime.fromtimestamp(trade.time) - \
                          timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S'), \
                          trade.ticker, trade.volume, trade.price))
    return jsonify({'message':msg}) 

@app.route('/api/<api_key>/positions', methods=['GET'])
def allpositions(api_key):      
    if Account.api_authenticate(api_key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.api_authenticate(api_key).pk
        user_positions = Account(pk=pk)
        positions = user_positions.get_positions()
        msg = {'positions':[]}
        for position in positions:
            valuation = Position()  
            getval = valuation.current_value(position.ticker, position.shares)     
            msg['positions'].append("Ticker Symbol: {}, Shares: {}, Valuation: ${}".format(position.ticker, position.shares, getval))
    return jsonify({'message':msg}) 

@app.route('/api/<api_key>/positions/<ticker>', methods=['GET'])
def positions(api_key, ticker):
    if Account.api_authenticate(api_key) == None:    
        msg = "Invalid login credentials, pls retry"
    else: 
        pk = Account.api_authenticate(api_key).pk
        user_position = Account(pk=pk)
        position = user_position.get_position_for(ticker)
        valuation = Position()  
        getval = valuation.current_value(ticker, position.shares)      
        msg = "Ticker Symbol: {}, Shares: {}, Valuation: ${}".format(position.ticker, position.shares, getval)
    return jsonify({'message':msg}) 

@app.route('/api/company/<company>', methods=['GET'])
def company(company):
    companies = util.get_ticker(company)
    if not companies: 
        msg = "No matches for input Company Name"
    else:
        msg = {'company':[]}
        for co in companies:
            msg['company'].append(co)
    return jsonify({'message':msg})

@app.route('/api/createaccount/<name>/<password>', methods=['GET'])
def createaccount(name, password):
    new_account = Account(username=name)
    new_account.set_password(password)
    ak = new_account.create_api_key()
    new_account.save()
    msg = "Account successfully created, API api_key = {}".format(ak)
    return jsonify({'message':msg})

def run():
    app.run(debug=True)
