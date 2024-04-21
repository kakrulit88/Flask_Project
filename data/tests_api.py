from requests import get, post, delete
from flask import request
from data.api_resources import LoanApi, DepositApi

try:
    test1 = post('http://127.0.0.1:8080/api/calc_loan', json={
        "value": 1000000,
        "percent": 5.00,
        "loan_time": 36,
        "pay_type": "аннуитетный",
        "loan_date": "2024-04-21"
    })

    test2 = post('http://127.0.0.1:8080/api/calc_loan', json={
        "value": 1000000,
        "percent": 5.00,
        "loan_time": 36,
        "pay_type": "",
        "loan_date": "2024-04-21"
    })

    test3 = post('http://127.0.0.1:8080/api/calc_deposit', json={
        "value": 1000000,
        "percent": 5.00,
        "deposit_time": 36,
        "deposit_date": "2024-04-21"
    })
    print(test3.json())
except Exception:
    print(test3)
