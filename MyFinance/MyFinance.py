import preprocess as prep
import re
import datetime
import csv
import math
data = prep.process_bank_statements('S1_20170101_20170520.CSV')
class SEntry(object):
   
    def __init__(self, debit=0, credit=0):
        self.debit = debit
        self.credit = credit
        self.cat_list = {}
        self.debug = []
    def balance(self):
        self.balance = self.credit-self.debit
    def out(self):
        return [-self.debit, self.credit, self.balance, self.cat_list, self.debug]

def pull_date(date, offset=0):

    if(offset!=0):
        date += datetime.timedelta(days=offset)
 

    return str(re.search('(^\d+-\d+-\d+)', (date).isoformat()).group(0)).strip()

def spread(data):
    smooth_data = {}
    data.sort(key=lambda x: x.eff_date)
    for row in data:
        if(row.internal):
            continue
        for day in range(round(row.days)):
            date = pull_date(row.eff_date, day)
            if(date not in smooth_data):
                smooth_data[date] = SEntry() 
            if(row.ledger == 'credit'):
                smooth_data[date].credit += row.per_day  
            elif(row.ledger == 'debit'):
                smooth_data[date].debit += row.per_day               
            else:
                print('freakout', vars(row))
            try:
                smooth_data[date].cat_list[row.subcat] += 1
            except:
                smooth_data[date].cat_list[row.subcat] = 1
            smooth_data[date].debug.append(row.out())

    for day in smooth_data:
        smooth_data[day].balance()
        
    return smooth_data

def export(data, flag="smooth"):
    try:
        with open('export.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['date', 'expense', 'income', 'balance'])
            for day in data:         

                writer.writerow([day]+smooth_data[day].out())
    except TypeError as e:
        print(e)

def print_spread(data):

    for day in data:

        print(day, data[day].credit, data[day].debit, data[day].balance, data[day].cat_list, data[day].debug)

def print_data(data, internal=False):
    for row in data:
        if(not row.internal):
            print(row.out())

smooth_data = spread(data)
#print_data(data)
#print_spread(smooth_data)


export(smooth_data)
    #print(vars(key))
    #print(vars(row))
    #if(not row.internal):
        #print(row.text+" | "+row.cat+" | "+row.subcat+" | ", row.amount)