
import csv
from datetime import *
import re

class JE(object):

    def __init__(self, pay_date, eff_date, narrative, error_code, amount, balance):
        self.pay_date = pay_date
        self.eff_date = eff_date
        self.text = narrative
        self.error_code = error_code
        self.amount = amount
        self.balance = balance

    def set_cat(self, cat='', subcat='', type='', days = 1):
        self.cat = cat
        self.subcat = subcat  
        self.type = type
        self.days = days

def process_bank_statements(file_name):    
    with open(file_name) as file:
        raw_data = [ row for row in csv.reader(file)]
    
    data = []
    for row in raw_data[1:]:
        if len(row) == 6:
            data.append(JE(row[0], row[1], row[2], row[3], row[4],row[5]))
        else:
            print('ded')
    
    for row in data:
    
        if(row.amount):
            row.amount = float(row.amount)
        else:
            row.amount = 0
        if(row.amount < 0 ):
            row.amount = abs(row.amount)
            row.type = 'debit'
        else:
            row.type = 'credit'
        if(not row.eff_date):
            row.eff_date = row.pay_date
        row.eff_date = datetime.strptime(row.eff_date, '%d %b %Y')
        row.pay_date = datetime.strptime(row.pay_date, '%d %b %Y')
        row.entry_date = datetime.today()
        if( re.search('TFR\s+\w+\s+220003S16',row.text) is not None):
            row.internal = True
            #print('-----'+row.text)
        else:
            row.internal = False
            #print('+++++'+row.text)
    
        if(re.search('KPMG.*93291', row.text) is not None):
            row.set_cat('General Living', 'Salary', 'Fixed', 14)
    
        elif(re.search('Ref:.+rent.*', row.text) is not None):
            row.set_cat('General Living', 'Rent', 'Fixed', 14)
        elif(re.search('RENTCARDPAYMENT', row.text) is not None):
            row.set_cat('General Living', 'Rent', 'Fixed', 14)
        elif(re.search('Powershop', row.text) is not None):
            row.set_cat('General Living', 'Electricity', 'Fixed')
        elif(re.search('ATM OPERATOR FEE', row.text) is not None or re.search('non bcu ATM trans fee', row.text) is not None):
            row.set_cat('Other', 'ATM Fee', 'Variable')
        elif(re.search('MISSION', row.text) is not None):
            row.set_cat('Other', 'Charity', 'Expense')
        elif(re.search('personal product fee', row.text) is not None):
            row.set_cat('Other', 'Bank Fees', 'Expense')
        elif(re.search('TRANSPORT FOR NSW SYDNEY', row.text) is not None):
            row.set_cat('General Living', 'Transport', 'Expense')
        elif(re.search('ICE SKATING', row.text) is not None):
            row.set_cat('Leasure', 'Ice Skating', 'Expense')
        else:
            row.set_cat()
    
        #if(row.eff_date == ''):
           # print(row.pay_date)
    return data


    

        




