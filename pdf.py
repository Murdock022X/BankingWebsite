from pathlib import Path
from fpdf import FPDF
from models import Transactions
from format import format_acc_no, format_date_4, format_money

class PDF(FPDF):

    def __init__(self, state_data, project_root):
        """
        My pdf class inheriting from FPDF. Used to write e-statements.

        Args:
            state_data (Statement_Data): Statement_Data object defined in 
            admin.py, contains information required to make e-statement.
            project_root (Path): The path to the root of the project.
        """    

        FPDF.__init__(self)
        self.state_data = state_data
        self.project_root = project_root

    def header(self):
        """
        Write the header on every page of the pdf statement.
        """           

        self.set_font('Helvetica', 'B', 20)

        y = self.get_y()

        self.image(self.project_root / Path('static/favicon.ico'), w=15, h=15)

        w = self.get_string_width('Statement For ' + self.state_data.date)

        self.set_y(y + 5)

        self.set_x((210 - w) / 2)

        self.cell(w=w + 6, h=10, txt='Statement For ' + self.state_data.date, 
                  border='B', ln=1, align='C')

    def overview(self, y_start = 30.0):
        """
        Shows an overview of user, displays username, Savings totals, 
        and Checkings totals.

        Args:
            y_start (float, optional): The starting y position for 
            the overview. Defaults to 30.0.
        """                      
        self.set_font('Helvetica', '', 12)

        self.set_y(y_start)

        self.cell(w=100, h=5, txt='Name: ' + self.state_data.name, 
                  ln=1, align='L')

        self.cell(w=100, h=5, 
                  txt='Savings Total: ' + self.state_data.savings_total, 
                  ln=1, align='L')

        self.cell(w=100, h=5, 
                  txt='Checkings Total: ' + self.state_data.checkings_total, 
                  ln=0, align='L')

        self.ln(15)

    def acc_summary(self):
        """
        Creates an overview of accounts, shows starting and ending balance 
        for this term as well as total deposits and withdrawals.
        """        
        self.set_font('Helvetica', '', 12)

        self.cell(w=190, h=5, txt='Accounts Summary', ln=0, align='C')

        self.ln(10)

        x = 10.0
        self.cell(w=36, h=5, txt='Account', border='B', ln=0, align='C')

        x += 38.5
        self.set_x(x)
        self.cell(w=36, h=5, txt='Starting Balance', border='B', 
                  ln=0, align='C')

        x += 38.5
        self.set_x(x)
        self.cell(w=36, h=5, txt='Withdrawals', border='B', ln=0, align='C')

        x += 38.5
        self.set_x(x)
        self.cell(w=36, h=5, txt='Deposits', border='B', ln=0, align='C')

        x += 38.5
        self.set_x(x)
        self.cell(w=36, h=5, txt='Ending Balance', border='B', ln=0, align='C')

        self.ln(10)

        pg = 0

        self.set_font('Helvetica', '', 10)

        for acc in self.state_data.accounts:
            acc_type = 'Savings'
            if acc.acc_type == 1:
                acc_type = 'Checkings'

            x = 10.0
            self.cell(w=36, h=5, 
                      txt=acc_type + ' ' + format_acc_no(acc.acc_no), 
                      ln=0, align='C')

            x += 38.5
            self.set_x(x)
            self.cell(w=36, h=5, 
                      txt=self.state_data.acc_metrics[acc.acc_no].start_bal, 
                      ln=0, align='C')

            x += 38.5
            self.set_x(x)
            
            self.set_text_color(255, 0, 0)
            self.cell(w=36, h=5, 
                      txt=self.state_data.acc_metrics[acc.acc_no].withdrawal_total, 
                      ln=0, align='C')
            
            self.set_text_color(0, 0, 0)

            x += 38.5
            self.set_x(x)
            self.cell(w=36, h=5, 
                      txt=self.state_data.acc_metrics[acc.acc_no].deposit_total, 
                      ln=0, align='C')

            x += 38.5
            self.set_x(x)
            self.cell(w=36, h=5, 
                      txt=self.state_data.acc_metrics[acc.acc_no].end_bal, 
                      ln=0, align='C')
            
            self.ln(10)

        self.ln(15)

    def account_transactions(self):
        """
        In depth account transactions. Creates a table of each transaction 
        for each account for this user.
        """        

        # Creates a transaction layout on the pdf.

        # Set font to Helvetica size 12.
        self.set_font('Helvetica', '', 12)

        # Set fill color to light gray.
        self.set_fill_color(211, 211, 211)

        # Create cell with account transactions title spanning the page.
        self.cell(w=190, h=10, txt='Account Transactions', border='', ln=0, 
                  align='C')

        # Change font size to 10.
        self.set_font('Helvetica', '', 10)

        # Line break 10mm.
        self.ln(10)

        # Iterate over each account in state_data.
        for acc in self.state_data.accounts:

            # Set font size back to 10 (size changed to 8 in loop below).
            self.set_font('Helvetica', '', 10)

            # Get type of account.
            acc_type = 'Savings'
            if acc.acc_type == 1:
                acc_type = 'Checkings'

            # Create a transaction block title spanning the page with 
            # acc_type followed by account number.
            self.cell(w=190, h=5, 
                      txt=acc_type + ' ' + format_acc_no(acc.acc_no), 
                      border='TLRB', ln=1, align='C', fill=True)
            
            # Start creating a transaction table for this account.

            # Create a column header for date column.
            self.cell(w=23.75, h=5, txt='Date', border='TBLR', ln=0, 
                      align='C', fill=True)

            # Create a column header for withdrawals.
            self.cell(w=23.75, h=5, txt='Withdrawals', border='TBLR', ln=0, 
                      align='C', fill=True)

            # Create a column header for deposits.
            self.cell(w=23.75, h=5, txt='Deposits', border='TBLR', ln=0, 
                      align='C', fill=True)

            # Create a column header for balances.
            self.cell(w=23.75, h=5, txt='Balance', border='TBLR', ln=0, 
                      align='C', fill=True)

            # Create a column header for descriptions.
            self.cell(w=95, h=5, txt='Description', border='TBLR', ln=1, 
                      align='C', fill=True)

            # Get number of transactions and start counting.
            cnt = 1
            l = len(self.state_data.acc_metrics[acc.acc_no].transactions)

            # Set font size to 8.
            self.set_font('Helvetica', '', 8)

            # Border string to be used to define cell borders.
            border_str = ''

            # Iterate over transactions for this account.
            for transaction in \
                self.state_data.acc_metrics[acc.acc_no].transactions:

                # Set withdrawal and deposit strings to empty.
                withdraw_str = ''
                deposit_str = ''

                # If this is a withdrawal then format it 
                # as a withdrawal string.
                if transaction.withdrawal_deposit == 0:
                    withdraw_str = format_money(transaction.amt)

                # If this is a deposit then format it as a deposit string.
                elif transaction.withdrawal_deposit == 1:
                    deposit_str = format_money(transaction.amt)

                # If last transaction create a bottom border.
                if l == cnt:
                    border_str += 'B'

                # Create a cell with the transaction date.
                self.cell(w=23.75, h=5, txt=format_date_4(transaction.date), border=border_str + 'LR', ln=0, align='C', fill=True)

                # Create a cell with the withdrawal string.
                self.cell(w=23.75, h=5, txt=withdraw_str, border=border_str + 'LR', ln=0, align='C', fill=True)

                # Create a cell with the deposit string.
                self.cell(w=23.75, h=5, txt=deposit_str, border=border_str + 'LR', ln=0, align='C', fill=True)

                # Create a cell with the ending balance.
                self.cell(w=23.75, h=5, txt=format_money(transaction.end_bal), border=border_str + 'LR', ln=0, align='C', fill=True)

                # Create a cell with the description for the transaction.
                self.cell(w=95, h=5, txt=transaction.description, border=border_str + 'LR', ln=1, align='C', fill=True)

                cnt += 1

            self.ln(5)

                