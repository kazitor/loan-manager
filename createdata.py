import loan, pickle

data = [
    loan.Loan('Technical debt', 120000, 80000)
]

with open('loans.dat', 'wb') as f:
    pickle.dump(data, f)
