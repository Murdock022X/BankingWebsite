from datetime import datetime, date

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

def format_statement_filename(username):
    return 'STATEMENT_' + username + '_' + date.today().strftime('%m_%d_%y') + '.pdf'

def format_date(dt: datetime):

    weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 
                   4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

    month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May',
                 6: 'June', 7: 'July', 8: 'August', 9: 'September',
                 10: 'October', 11: 'November', 12: 'December'}

    weekday = weekday_map[dt.weekday()]
    month = month_map[dt.month]

    hour = dt.hour

    period = 'AM'
    if dt.hour >= 12:
        period = 'PM'
    
    if dt.hour >= 13:
        hour -= 12
    
    elif dt.hour < 1:
        hour += 12

    time_str = '%d:%d:%d %s' % (hour, dt.minute, dt.second, period) 

    res = "%s, %s %d, %d %s" % (weekday, month, dt.day, dt.year, time_str)

    return res

    