class Loan(object):
    """A single loan"""
    payed=0
    def __init__(self, name, total):
        self.name = name
        self.total = total

class CompoundLoan(Loan):
    def __init__(self, name, total, interest, period = (1,'y')):
        super().__init__(name,total)
        self.interest = interest
        self.period = period
    def amountLeft(self,repayment,periods):
        interest=1+self.interest
        return self.total*interest**periods - repayment*interest*(1-interest**periods)/(1-interest)

if __name__ == '__main__':
    exit()
