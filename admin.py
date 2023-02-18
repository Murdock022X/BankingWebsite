from models import Account, Alerts, Messages, Bank_Settings
from app import db
from datetime import datetime

class Admin_Tools():

    def modify_bank_settings(savings_ir = -1.0, savings_min = -1.0, checkings_ir = -1.0, checkings_min = -1.0):
        settings = Bank_Settings.query.get(1)

        if settings.savings_ir != -1.0:
            settings.savings_ir = savings_ir
        if settings.savings_min != -1.0:
            settings.savings_min = savings_min
        if settings.checkings_ir != -1.0:
            settings.checkings_ir = checkings_ir
        if settings.checkings_min != -1.0:
            settings.checkings_min = checkings_min

        db.session.commit()

        return True

    def compound():
        accs = Account.query.all()

        for acc in accs:
            acc.bal *= acc.ir
        
        db.session.commit()

        return True

    def send_alert(content):
        dt = datetime.now()
        
        alert = Alerts(date=datetime, content=content)

        db.session.add(alert)

        db.session.commit()

        return True
    
    def send_message(content, username):
        dt = datetime.now()

        message = Messages(date=dt, username=username, content=content)

        db.session.add(message)

        db.session.commit()

        return True
    
    def assemble_statement():
        pass
                
