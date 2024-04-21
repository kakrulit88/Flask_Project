from datetime import timedelta


def get_annuity_loan_table(value, percent, loan_time, loan_time_type, loan_date):
    monthly_percent = percent / 1200
    if loan_time_type == 'года':
        loan_time *= 12
    print(value, percent, loan_time, loan_time_type, loan_date)

    monthly_payment = round(value * (
            monthly_percent * ((1 + monthly_percent) ** loan_time) / ((1 + monthly_percent) ** loan_time - 1)), 2)

    month_count = (loan_date + timedelta(weeks=loan_time * 4))
    total_loan_cost = 0
    all_payments = value
    loan_table = {'total_loan_cost': 0,
                  'all_payments': 0,
                  'table': [{'id': 0,
                             'payment date': str(loan_date),
                             'monthly_payment': "{0:0.2f}".format(0.00),
                             'overpay_loan': "{0:0.2f}".format(0.00),
                             'overpay_per': "{0:0.2f}".format(0.00),
                             'left': value}]
                  }
    for month in range(1, loan_time + 1):
        loan_date += timedelta(days=30)
        overpay_per = round(value * monthly_percent, 2)
        overpay_loan = round(monthly_payment - overpay_per, 2)
        value = round(value + overpay_per - monthly_payment, 2)
        total_loan_cost += overpay_per
        loan_table['table'].append({'id': month,
                                    'payment date': str(loan_date),
                                    'monthly_payment': monthly_payment,
                                    'overpay_loan': overpay_loan,
                                    'overpay_per': "{0:0.2f}".format(overpay_per),
                                    'left': "{0:0.2f}".format(value)})

    total_loan_cost = round(total_loan_cost)
    all_payments += total_loan_cost
    loan_table['total_loan_cost'] = total_loan_cost
    loan_table['all_payments'] = all_payments
    loan_table['table'][-1]['left'] = 0

    return loan_table


def get_different_loan_table(value, percent, loan_time, loan_time_type, loan_date):
    if loan_time_type == 'года':
        loan_time *= 12
    monthly_payment_without_pers = round(value / loan_time, 2)

    total_loan_cost = 0
    all_payments = value
    loan_table = {'total_loan_cost': 0,
                  'all_payments': 0,
                  'table': [{'id': 0,
                             'payment date': str(loan_date),
                             'monthly_payment': "{0:0.2f}".format(0.00),
                             'overpay_loan': "{0:0.2f}".format(0.00),
                             'overpay_per': "{0:0.2f}".format(0.00),
                             'left': value}]
                  }

    for month in range(1, loan_time + 1):
        loan_date += timedelta(days=30)
        monthly_pers = round((value * (percent / 100) * 30) / 365, 2)
        monthly_payment = round(monthly_payment_without_pers + monthly_pers, 2)
        total_loan_cost += monthly_pers
        value -= monthly_payment_without_pers
        loan_table['table'].append({'id': month,
                                    'payment date': str(loan_date),
                                    'monthly_payment': "{0:0.2f}".format(monthly_payment),
                                    'overpay_loan': monthly_payment_without_pers,
                                    'overpay_per': "{0:0.2f}".format(monthly_pers),
                                    'left': "{0:0.2f}".format(value)})

    total_loan_cost = round(total_loan_cost)
    all_payments += total_loan_cost
    loan_table['total_loan_cost'] = total_loan_cost
    loan_table['all_payments'] = all_payments
    loan_table['table'][-1]['left'] = 0

    return loan_table


def get_deposit_table(value, percent, deposit_time, deposit_time_type, loan_date):
    if deposit_time_type == 'года':
        deposit_time *= 12
    total_profit = 0
    current_value = value
    percent /= 100
    deposit_table = {'total_profit': 0,
                     'total_value': 0,
                     'table': [{'id': 0,
                                'payment date': str(loan_date),
                                'profit': "{0:0.2f}".format(0.00),
                                'current_value': value}]
                     }
    for month in range(1, deposit_time + 1):
        loan_date += timedelta(days=30)
        new_value = round(current_value * percent / 365 * 30, 2)
        total_profit += new_value
        current_value += new_value
        deposit_table['table'].append({
            'id': month,
            'payment date': str(loan_date),
            'profit': "{0:0.2f}".format(new_value),
            'current_value': "{0:0.2f}".format(current_value)
        })

    deposit_table['total_profit'] = round(total_profit, 2)
    deposit_table['total_value'] = round(value + total_profit, 2)

    return deposit_table
