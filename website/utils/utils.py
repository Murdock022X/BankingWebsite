from website.models import Messages, Alerts, Statements
from flask import Response, url_for
from website.utils.format import format_statement_filename, format_date_1
from pathlib import Path
from flask import flash

def get_alerts():
    """Get all alerts in the system, since alerts are meant to be system-wide 
    rather than be targeted at one user like messages we simply retrieve all 
    the alerts. Returns a list of formatted dictionarys with each attribute in 
    string form linked to their values.

    Returns:
        list[dict[str: str]]: The string of the attribute keys linked to the 
        formatted string value of that attribute, each "alert" dictionary is 
        added to a list and returned.
    """    

    # Get all alert objects.
    alerts = Alerts.query.all()

    # Add all formatted alerts to a list
    res = []
    for alert in alerts:
        formatted = {}
        formatted['date'] = format_date_1(alert.date)
        formatted['content'] = alert.content

        res.append(formatted)

    return res

def get_messages(username):
    """Gets all messages associated with a username.

    Args:
        username (str): The username of the person we want to get messages for.

    Returns:
        list[dict[str: str]]: Returns a list of all messages formatted with 
        relevant information in a dictionary. The keys for the dictionary 
        being the same as the attributes of the message but strings. These 
        keys are linked to formatted dates and the content and id for the 
        message.
    """    

    # Get messages.
    messages = Messages.query.filter_by(username=username)

    # Turn each message into formatted elements with attributes in a 
    # dictionary and add to list.
    res = []
    for message in messages:
        formatted = {}
        formatted['date'] = format_date_1(message.date)
        formatted['content'] = message.content
        formatted['id'] = message.id

        res.append(formatted)

    return res

def term_interest(apy, term_len=52):
    """Calculate the yield over the term based on term length and apy.

    Args:
        apy (float): The apy for the account.
        term_len (int, optional): The number of terms in a year. 
        Defaults to 52. (52 weeks in a year)

    Returns:
        float: The term yield.
    """    

    return apy / term_len
