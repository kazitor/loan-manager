# Blog log
The task this program is being written for requires a log of progress. It follows, you might be interested in it.

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
    Button(self,text="Edit",command=lambda: self.editloan(loan)).grid()
```

The issue was that `editloan` was always being called with the last loan. [This Stack Overflow answer](https://stackoverflow.com/questions/16559764/assign-variable-to-local-scope-of-function-in-python#16562246) provided a method of providing a closure for the `loan` variable when the function was created: change it to `lambda loan=loan: self.editloan(loan)`


I will need to continue to think about how best to organise the code, rather than putting everything under the root `Application` as tends to happen.

The next task is to be able to enter important information for a loan (total value, amount already payed, interest, etc.) and calculate how long it will take and cost. This will not be saved to a file yet, what is important is that the values can be produced.