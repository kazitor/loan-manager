import datetime

class Term(object):
    """Date information of a loan"""
    def __init__(self, startdate=None, enddate=None):
        self.startdate = startdate
        self.enddate = enddate
    def timeleft(self):
        return self.enddate - datetime.date.today

class Interest(object):
    """Interest information of a compound loan"""
    def __init__(self, rate, period, compound_period = None):
        self.rate = rate
        self.period = period
        self.compound_period = compound_period if compound_period else period
        self.compound_rate = self.rate / (self.period / self.compound_period)

class Period(object):
    """Period of time suitable for finance, measured in days, months and years"""
    def __init__(self, days=0, months=0, years=0):
        self.days = days
        self.months = months
        self.years = years

class Loan(object):
    """A single loan"""
    def __init__(self, name, total):
        self.payed=0
        self.name = name
        self.total = total

class CompoundLoan(Loan):
    """Loan that undergoes compound interest"""
    def __init__(self, name, total, interest):
        super().__init__(name,total)
        if type(interest) != Interest:
            raise TypeError('interest must be an instance of Interest')
        self.interest = interest
    def amountLeft(self,repayment,periods):
        return None
        interest=1+self.interest
        return self.total*interest**periods - repayment*interest*(1-interest**periods)/(1-interest)

if __name__ == '__main__':
    exit()
