from tkinter import *
from loan import Loan

class Application(Frame):
    """Root window"""
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.master=master
        self.master.title("Loan manager")
        self.master.geometry("400x200")
        self.grid()
        self.add_widgets()
    def add_widgets(self):
        Button(self,text="Open file").grid(row=0)
        for i,loan in enumerate(self.getloans()):
            Label(self, text=loan.name).grid(row=i+1,column=0)
            Button(self,text="Edit",command=lambda loan=loan: self.editloan(loan)).grid(row=i+1,column=1)
            Button(self,text="New loan",command=self.editloan).grid(row=i+2,column=0)
    def getloans(self) -> list:
        # temporary
        return [Loan("technical debt",100000,1),Loan("My house",9999899,10)]
    def editloan(self,loan=None):
        """ Open a window for managing a single loan """
        window = LoanEditWindow(self.master,loan)

class LoanEditWindow(Toplevel):
    """Window for editing or creating a loan"""
    def __init__(self, master,loan=None):
        super(LoanEditWindow, self).__init__(master)
        self.master = master
        self.loan = loan
        self.geometry("300x200")
        self.grid()
        self.add_widgets()
    def add_widgets(self):
        self.fields={}
        Label(self,text="Loan total").grid(row=0,column=0)
        self.fields['Total'] = Entry(self)
        for i,field in enumerate(self.fields):
            self.fields[field].grid(row=i,column=1)
        if self.loan:
            self.wm_title("Editing %s" % self.loan.name)
        else:
            self.wm_title("Create new loan")

root = Tk()
app = Application(root)
root.mainloop()
