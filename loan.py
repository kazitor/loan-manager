import datetime

class Term(object):
    """Date information of a loan"""
    def __init__(self, startdate=None, enddate=None):
        self.startdate = startdate
        self.enddate = enddate
    def timeleft(self):
        return self.enddate - datetime.date.today

class Loan(object):
    """A single loan"""
    title = 'Simple'
    fields = ('Name', 'Total', 'Monthly payment', 'Paid')

    def __init__(self, name, total, payment, paid=0):
        if paid == '':
            paid = 0
        else:
            paid = self.parseMoney(paid)

        total = self.parseMoney(total)
        payment = self.parseMoney(payment)

        if total < 0 or payment < 0 or paid < 0:
            raise ValueError("Values cannot be less than 0")

        if paid > total:
            raise ValueError("Cannot pay off more than the total amount")


        self.name = name
        self.total = total
        self.payment = payment
        self.paid = paid
    
    def __str__(self):
        return '{0.name}: ${0.total:.2f}, {0.progress:.0%} paid'.format(self)

    @property
    def values(self):
        return (
            self.name,
            self.formatMoney(self.total),
            self.formatMoney(self.payment),
            self.formatMoney(self.paid),
        )

    @property
    def left(self):
        return self.total - self.paid

    @property
    def progress(self):
        return self.paid / self.total

    @staticmethod
    def parseMoney(value: str) -> float:
        original = value
        value = value.strip('$ ')
        try:
            value = float(value)
        except ValueError as e:
            raise ValueError(original + " is not a valid amount.") from e # nicer error message
        value = round(value, 2)

        return value

    @staticmethod
    def formatMoney(value: float) -> str:
        if value.is_integer():
            return '{0:.0f}'.format(value) # don't display cents
        else:
            return '{0:.2f}'.format(value)

# Classes relating to compounding loans

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

class CompoundLoan(Loan):
    """Loan that undergoes compound interest"""
    title = 'Compounding'
    def __init__(self, name, total, interest):
        super().__init__(name,total)
        if type(interest) != Interest:
            raise TypeError('interest must be an instance of Interest')
        self.interest = interest
    def amountLeft(self,repayment,periods):
        return None
        interest=1+self.interest
        return self.total*interest**periods - repayment*interest*(1-interest**periods)/(1-interest)

types = (Loan,)
for i,loan in enumerate(types):
    loan.id = i

def by_id(id):
    return types[id]

if __name__ == '__main__':
    exit()
