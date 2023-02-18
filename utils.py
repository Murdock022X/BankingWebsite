from models import Messages, Alerts, Statements
from fpdf import HTMLMixin, FPDF
from flask import Response
from format import format_statement_filename

def get_alerts():
    return Alerts.query.all()

def get_messages(username):
    return Messages.query.filter_by(username=username)

class MyFPDF(FPDF, HTMLMixin):
    pass

def get_statements(username):
    return Statements.query.filter_by(username=username)

def get_statement(id):
    return Statements.query.get(id)