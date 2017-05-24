import preprocess as prep

class simple_date(object):

    def __init__(self, date= None, amount=0):
        self.date = date
        self.amount = amount

data = prep.process_bank_statements('S1_20170101_20170520.CSV')


def spread(data):
    smooth_data = []
    for row in data:
        smooth_data.append(simple_date(row.eff_date, 0))

        
   # date_diff = data[-1].eff_date -data[0].eff_date


    return smooth_data

spread_data = spread(data)
for key in spread_data:
    print(vars(key))
    pass
    #print(vars(row))
    #if(not row.internal):
        #print(row.text+" | "+row.cat+" | "+row.subcat+" | ", row.amount)