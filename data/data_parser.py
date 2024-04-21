from flask_restful import reqparse

deposit_parser = reqparse.RequestParser()
deposit_parser.add_argument('value', required=True)
deposit_parser.add_argument('percent', required=True)
deposit_parser.add_argument('deposit_time', required=True)
deposit_parser.add_argument('deposit_date', required=True)

loan_parser = reqparse.RequestParser()
loan_parser.add_argument('value', required=True)
loan_parser.add_argument('percent', required=True)
loan_parser.add_argument('loan_time', required=True)
loan_parser.add_argument('pay_type', required=True)
loan_parser.add_argument('loan_date', required=True)
