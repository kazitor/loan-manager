import math

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

        if total > 1e15 or payment > 1e15:
            # 1e15 = 1 quadrillion (short) or 1000 billion (long)
            raise ValueError("There's no way you have that kind of money.")
            # also it screws up the interface and might not be stored accurately, but nobody needs to know that

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
        if self.left is not None:
            return '$'+self.formatMoney(self.left)
        return ''

    @property
    def payoff_time(self):
        return self.left / self.payment if self.payment else None
    @property
    def payoff_time_nice(self):
        if self.left == 0:
            return 'Paid!'
        elif self.payoff_time is None:
            return 'Never'
        else:
            time_ceil = -(-self.payoff_time // 1) # fun ceiling trick without importing math
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
    fields = ('Name', 'Monthly payment', 'Monthly interest', 'Amount outstanding')

    def __init__(self, name, payment, interest, total):
        super().__init__(name, payment, '0', total)

        original_interest = interest
        interest = interest.strip('% ')
        try:
            interest = float(interest)
        except ValueError as e:
            raise ValueError(original_interest + "is not a valid interest amount.") from e
        if interest < 0:
            raise ValueError("Interest cannot be less than 0")

        self.interest = interest / 100

    @property
    def values(self):
        return (
            self.name,
            self.formatMoney(self.payment),
            str(self.interest * 100),
            self.formatMoney(self.total),
        )

    @property
    def left(self):
        time = self.payoff_time
        if time is None:
            return None
        return time * self.payment

    @property
    def payoff_time(self):
        if self.payment == 0:
            return None

        P, I, R = self.total, 1+self.interest, self.payment
        try:
            # verfied by maths and GeoGebra
            time = (math.log(R) + math.log(I) - math.log(-(P*I - P - R*I)))/math.log(I)
        except ValueError as e:
            # repayments are not large enough
            time = None
        return time

types = (Loan, CompoundLoan)
for i,loan in enumerate(types):
    loan.id = i

def by_id(id):
    return types[id]

if __name__ == '__main__':
    exit()
