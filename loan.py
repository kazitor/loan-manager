class Loan(object):
    """A single loan"""
    payed=0
    def __init__(self, name, total, interest, period = (1,'y')):
        self.name = name
        self.total = total
        self.interest = interest
        self.period = period

if __name__ == '__main__':
    exit()

