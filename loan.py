class Loan(object):
    """A single loan"""
    title = 'Simple'
    fields = ('Name', 'Monthly payment', 'Amount paid', 'Total')

    def __init__(self, name, payment, paid, total):
        if paid == '':
            paid = 0.0
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
            self.formatMoney(self.payment),
            self.formatMoney(self.paid),
            self.formatMoney(self.total),
        )

    @property
    def left(self):
        return self.total - self.paid
    @property
    def left_nice(self):
        return '$'+self.formatMoney(self.left)

    @property
    def payoff_time(self):
        return self.left / self.payment if self.payment else None
    @property
    def payoff_time_nice(self):
        if self.left <= 0:
            return 'Paid!'
        elif self.payment == 0:
            return 'Never'
        else:
            time_ceil = -(-self.left // self.payment) # fun ceiling trick without importing math
            return '{0:.0f} {1}'.format( time_ceil, 'month' if time_ceil==1 else 'months' )

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
