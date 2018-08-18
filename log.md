# Blog log
The task this program is being written for requires a log of progress. It follows, you might be interested in it.

## 2018-08-18
Currently working on making the loan objects themselves specify relevant information about themselves (user-friendly name, fields) rather than harcoding it in the main program. Apart from being good practice, I can also easily remove the compounding functionality if time constraints do not allow it. Hopefully it won't get to that point.

## 2018-08-10
Trying to sort out dates and all their intricacies is something I need time to sort out, so until then it now has the necessary functionality of saving all data on closing and initialising it when next run.

## 2018-08-03
Began basic implementation of separate objects for tracking interest and periods. They mostly exist just to collect all relevant data in a single object that can be passed as a single parameter. Later `Term` will need to use `Period` to determine dates of individual payments, this is necessary because the `timedelta` object only deals with distinct lengths up to a maximum of days, but fincances typically use varying periods like months or years.

## 2018-07-27
Rather than passing a bunch of parameters to the `__init__`s of the `Loan` classes, I've started a separate `Term` class to contain the relevant fields. At the moment it just takes a start and end date and copies them, but later it will do validation on those dates and also allow for a compounding period, and possibly also methods for things like next period, time until end, etc.

## 2018-07-12
GUI is being painful, unsurprisingly. I had to resolve an issue with the `grid` method not being chainable, i.e. it doesn't return the object it was called on (or anything for that matter).

The GUI should be mostly done now. The edit window will display accurate data when editing a loan and has buttons. I *must* sort out a proper way of storing the fields for manipulating them, the current `dict`-based method is not suitable (though close to a proper, functioning system).

The buttons are currently non-functional, but making them work comes later in the plan. Later the main window should display some additional data. It definitely needs to update the list of existing objects.

I tried to add the fields based on a simple harcoded object, but that doesn't allow for each field's specialties and so has been changed.

Once that's all out of the way, I will get to work on the `Loan` objects. I think I placed "calculation" too soon in my planning, as it's hard to do that without a functioning program. The intention there was just to do some maths soon because that's more interesting or something.

I'm already feeling the technical debt... it's the first sample loan I added for a reason :) Although I feel better about the GUI's state of affairs now.

## 2018-07-04
Did some maths and calculated the formula for amount left after repayments on a compounding loan: total x interest^periods - repayment x interest x (1-interest^periods)/(1-interest)
Implemented it in the `Loan` class so I don't forget it.

## 2018-07-02

After some unexpected busyness, I finally made a start on writing today.

Added:
* A window
* Button (non-functional) to load a file (this is future functionality)
* Basic object for modelling a loan
* Dialog for editing/creating a loan
  * List of all loans with a button to edit each
  * Button to add a new one

A brief issue was in the `add_widgets` method, when adding the label and button for each loan. I had something like
```python
for i,loan in enumerate(self.getloans()):
    Button(self,text="Edit",command=lambda: self.editloan(loan)).grid(
```

The issue was that `editloan` was always being called with the last loan. [This Stack Overflow answer](https://stackoverflow.com/questions/16559764/assign-variable-to-local-scope-of-function-in-python#16562246) provided a method of providing a closure for the `loan` variable when the function was created: change it to `lambda loan=loan: self.editloan(loan)`


I will need to continue to think about how best to organise the code, rather than putting everything under the root `Application` as tends to happen.

The next task is to be able to enter important information for a loan (total value, amount already payed, interest, etc.) and calculate how long it will take and cost. This will not be saved to a file yet, what is important is that the values can be produced.
