from models import Messages, Alerts, Statements
from fpdf import HTMLMixin, FPDF
from flask import Response
from format import format_statement_filename, format_date

def get_alerts():
    alerts = Alerts.query.all()

    res = []

    for alert in alerts:
        formatted = {}
        formatted['date'] = format_date(alert.date)
        formatted['content'] = alert.content

        res.append(formatted)

    return res

def get_messages(username):
    messages = Messages.query.filter_by(username=username)

    res = []

    for message in messages:
        formatted = {}
        formatted['date'] = format_date(message.date)
        formatted['content'] = message.content
        formatted['id'] = message.id

        res.append(formatted)

    return res

class MyFPDF(FPDF, HTMLMixin):
    pass

def get_statements(username):
    return Statements.query.filter_by(username=username)

def get_statement(id):
    return Statements.query.get(id)