from flask_restful import Resource, abort
from flask import jsonify, redirect
from data.data_parser import deposit_parser, loan_parser
from data.calculators import get_deposit_table, get_different_loan_table, get_annuity_loan_table
from datetime import datetime


class LoanApi(Resource):
    def get(self):
        return redirect('/api')

    def post(self):
        args = loan_parser.parse_args()

        value = int(args['value'])
        percent = float(args['percent'])
        loan_time = int(args['loan_time'])
        pay_type = args['pay_type']
        loan_date = datetime(*list(map(int, args['loan_date'].split('-'))))
        if pay_type.lower() == 'аннуитетный':
            return jsonify(get_annuity_loan_table(value, percent, loan_time, '', loan_date))
        return jsonify(get_different_loan_table(value, percent, loan_time,
                                                '', loan_date))


class DepositApi(Resource):
    def get(self):
        return redirect('/api')

    def post(self):
        args = deposit_parser.parse_args()

        value = int(args['value'])
        percent = float(args['percent'])
        deposit_time = int(args['deposit_time'])
        deposit_date = datetime(*list(map(int, args['deposit_date'].split('-'))))
        return jsonify(get_deposit_table(value, percent, deposit_time, '', deposit_date))
