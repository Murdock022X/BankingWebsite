from datetime import datetime, date

def format_acc(acc):
    """Format attributes in an account object to prepare for html.

    Args:
        acc (Account): The account object to format.
    """    

    # Format all aspects of account
    acc.acc_no = format_acc_no(acc.acc_no)
    acc.bal = format_money(acc.bal)
    acc.min_bal = format_money(acc.min_bal)
    acc.apy = format_apy(acc.apy)
    acc.acc_type = format_acc_type(acc.acc_type)

def format_acc_no(num):
    """Format an account number into the 8 digit form it 
    should be in when displayed.

    Args:
        num (int): The account number

    Returns:
        str: The zero filled string with 8 digits.
    """    

    # Account numbers are 8 digits, fill in zeros for formatting
    return str(num).zfill(8)

def format_money(num):
    """Format monetary values into a string that nicely represents them.

    Args:
        num (float): The monetary amount.

    Returns:
        str: The string formatted to show that it is a monetary amount. $xx.xx
    """    

    # Display money balances correctly
    if num < 0:
        return '-$%.2f' % abs(num)

    return '$%.2f' % num

def format_apy(num):
    """Format an interest rate amount to appear like an interest rate.

    Args:
        num (float): The raw floating point amount that represents 
        the interest rate.

    Returns:
        str: The formatted string. xx.x%.
    """    

    # Display interest rate correctly
    return '%.2f' % num + '%'

def format_acc_type(num):
    """Format account typing. 0 -> Savings, 1 -> Checkings.

    Args:
        num (int): The number that represents the type of account.

    Returns:
        str: 'Savings' or 'Checkings' based on account typing.
    """    

    if num == 0:
        return 'Savings'
    else:
        return 'Checkings'
    
def format_status(status):
    """Format the status of the account. False -> 'Closed', True -> 'Open'.

    Args:
        status (boolean): False means a closed account, True means an open 
        account.

    Returns:
        str: 'Closed' or 'Open' based on status of account.
    """    

    if status:
        return 'Open'
    return 'Closed'

def format_rates(rates):
    """Create a dictionary representing the formatted Bank Settings.

    Args:
        rates (Bank_Settings): The rates for savings and checkings.

    Returns:
        dict: A dictionary with the string representation of rates 
        attributes mapped to formatted rates.
    """    

    res = {}

    res['savings_apy'] = format_apy(rates.savings_apy)
    res['savings_min'] = format_money(rates.savings_min)
    res['checkings_apy'] = format_apy(rates.checkings_apy)
    res['checkings_min'] = format_money(rates.checkings_min)

    return res

def deep_format_acc(acc):
    """Format an account mapping account attribute to formatted attribute 
    values.

    Args:
        acc (Account): The account we need to format.

    Returns:
        dict: A dictionary with attribute strings mapped to formatted 
        attribute values.
    """    

    res = {}
    res['acc_no'] = format_acc_no(acc.acc_no)
    res['acc_type'] = format_acc_type(acc.acc_type)
    res['apy'] = format_apy(acc.apy)
    res['bal'] = format_money(acc.bal)
    res['min_bal'] = format_money(acc.min_bal)
    res['acc_int'] = acc.acc_no
    res['status'] = format_status(acc.status)

    return res

def format_statement_filename(username):
    """Format the filename for a statement. Format: 
    'STATEMENT_username_mm_dd_yy.pdf', mm = month, dd = day, yy = year.

    Args:
        username (str): The username we need to create the filename for.

    Returns:
        str: The new formatted filename.
    """    

    return 'STATEMENT_' + username + '_' + date.today().strftime('%m_%d_%y') \
        + '.pdf'

def format_date_1(dt: datetime):
    """Format the date in the format: 
    weekday, month, (day of the month), 
    year hour:minute:second (am/pm) UTC. 

    Args:
        dt (datetime): A datetime object to be formatted into a special string.

    Returns:
        str: The string formatted in the format specified in descriptor.
    """    

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

    # Format a string with times with 2 digit places.
    time_str = f'{hour:02}:{dt.minute:02}:{dt.second:02} {period}'

    return f'{weekday}, {month}, {dt.day:02}, {dt.year} {time_str} UTC'


def format_date_2(dt):
    """Format datetime object in format %m-%d-20%y.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: The string in the format described in the descriptor.
    """    
    return dt.strftime("%m-%d-20%y")

def format_date_3(dt):
    """Return datetime object formatted in format month day(followed by st, 
    nd, rd, th as appriopriate), year.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: The string formatted as described in the descriptor.
    """    

    day_map = {0: '0th', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 
               5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th'}
    
    month_map = {1: 'January', 2: 'Feburary', 3: 'March', 4: 'April', 
                 5: 'May', 6: 'June', 7: 'July', 8: 'August', 
                 9: 'September', 10: 'October', 11: 'November', 
                 12: 'December'}
    
    res = month_map[dt.month] + ' '

    if dt.day // 10:
        res += str(dt.day)[0]

    # If day is a teenth then we always use th as the ending otherwise we 
    # use the appropriate ending.
    if dt.day // 10 == 1:
        res += str(dt.day)[-1] + 'th,' + str(dt.year) 
    else:
        res += day_map[int(str(dt.day)[-1])] + ', ' + str(dt.year)

    return res

def format_date_4(dt):
    """Format datetime object in form mm/dd/20yy.

    Args:
        dt (datetime): The datetime object to be formatted.

    Returns:
        str: The string in format as described in the descriptor.
    """    
    return dt.strftime('%m/%d/20%y')