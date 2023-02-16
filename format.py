def format_acc(acc):
    # Format all aspects of account
    acc.acc_no = format_acc_no(acc.acc_no)
    acc.bal = format_money(acc.bal)
    acc.min_bal = format_money(acc.min_bal)
    acc.ir = format_ir(acc.ir)
    acc.acc_type = format_acc_type(acc.acc_type)

def format_acc_no(num):
    # Account numbers are 8 digits, fill in zeros for formatting
    return str(num).zfill(8)

def format_money(num):
    # Display money balances correctly
    return '$' + ('%.2f' % num)

def format_ir(num):
    # Display interest rate correctly
    return '%.2f' % num + '%'

def format_acc_type(num):
    if num == 0:
        return 'Savings'
    else:
        return 'Checkings'
    
def format_rates(rates):
    rates.savings_ir = format_ir(rates.savings_ir)
    rates.savings_min = format_money(rates.savings_min)
    rates.checkings_ir = format_ir(rates.checkings_ir)
    rates.checkings_min = format_money(rates.checkings_min)

def deep_format_acc(acc):
    res = {}
    res['acc_no'] = format_acc_no(acc.acc_no)
    res['acc_type'] = format_acc_type(acc.acc_type)
    res['ir'] = format_ir(acc.ir)
    res['bal'] = format_money(acc.bal)
    res['min_bal'] = format_money(acc.min_bal)
    res['acc_int'] = acc.acc_no

    return res