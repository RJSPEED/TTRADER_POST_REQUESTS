
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
    print(request.json)
    if not request.json or 'username' not in request.json or 'password' not in request.json:
        return jsonify({"error": "bad request"}), 400
    account = Account.login(request.json['username'], request.json['password'])
    if not account:
        return jsonify({"error": "access denied"})
    
    return jsonify({"username": account.username, "api_key": account.api_key})


"""

curl -d '{"username":"stuart_head", 
          "password":"password"}' 
-H "Content-Type: application/json" 
-X POST http://localhost:5000/api/get_api_key

"""
curl -d '{"username":"stuart_head", "password":"password"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/get_api_key

curl -d '{"api_key":"kdhsajdhsadown", "amount":"250.00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/deposit

curl -d '{"amount":"250.00"}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/PRHRSK1VI5TEDYV/deposit

curl -d '{"ticker": "tsla", "volume": 2}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/PRHRSK1VI5TEDYV/buy

curl -d '{"ticker": "tsla", "volume": 1}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/PRHRSK1VI5TEDYV/sell
