from tkinter import *
import loan

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
        return [loan.Loan("technical debt",100000),loan.CompoundLoan("Mortgage",9999899,1,10)]
    def editloan(self,loan=None):
        """ Open a window for managing a single loan """
        window = LoanEditWindow(self.master,loan)

class LoanEditWindow(Toplevel):
    """Window for editing or creating a loan"""
    def __init__(self, master,loanobject=None):
        super(LoanEditWindow, self).__init__(master)
        self.master = master
        self.loan = loanobject

        self.forcompound = BooleanVar()
        self.forcompound.set( type(loanobject) == loan.CompoundLoan )
        
        self.geometry("300x200")
        self.grid()
        self.add_widgets()
    def add_widgets(self):
        self.basefields={}
        self.extrafields={}

        basefields = {'name':'Name','amount':'Loan total'} # separate to class dict of field objects

        Radiobutton(self,text="Simple", variable=self.forcompound, command=self.set_fields, value=False).grid(row=0,column=0)
        Radiobutton(self,text="Compound", variable=self.forcompound, command=self.set_fields, value=True).grid(row=0,column=1)
        for i,name in enumerate(basefields):
            labelfield = Label(self,text=basefields[name])
            labelfield.grid(row=i+1,column=0)
            entryfield = Entry(self)
            entryfield.grid(row=i+1,column=1)
            self.basefields[name] = (labelfield, entryfield)

        self.set_fields()

        if self.loan:
            self.wm_title("Editing %s" % self.loan.name)
        else:
            self.wm_title("Create new loan")
    def set_fields(self):
        for fieldset in self.extrafields:
            for field in self.extrafields[fieldset]:
                field.destroy()
        self.extrafields = {}

        if self.forcompound.get():
            extrafields = {'interest':'Interest','period':'Period'}

            for i,name in enumerate(extrafields):
                labelfield = Label(self,text=extrafields[name])
                labelfield.grid(row=i+3,column=0)
                entryfield = Entry(self)
                entryfield.grid(row=i+3,column=1)
                self.extrafields[name] = (labelfield, entryfield)

root = Tk()
app = Application(root)
root.mainloop()
