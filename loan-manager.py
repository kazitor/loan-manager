from tkinter import *
import pickle
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
        #Button(self,text="Open file").grid(row=0)
        Label(self,text="Managed loans").grid(row=0)
        i = 0 # in case loop is empty
        for i,loan in enumerate(self.getloans(),1):
            Label(self, text=loan.name).grid(row=i,column=0)
            Button(self,text="Edit",command=lambda loan=loan: self.editloan(loan)).grid(row=i,column=1)
        Button(self,text="New loan",command=self.editloan).grid(row=i+1,column=0)
    def getloans(self) -> list:
        try:
            with open('loans.dat', 'rb') as f:
                return [loan.Loan("technical debt",100000),loan.CompoundLoan("Mortgage",9999899,1,10)]
        except IOError as e:
            if e.errno == 2: # file not found
                return []
            else:
                raise e
        
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

        if self.loan:
            self.wm_title("Editing %s" % self.loan.name)
        else:
            self.wm_title("Create new loan")

        Radiobutton(self,text="Simple", variable=self.forcompound, command=self.set_fields, value=False).grid(row=0,column=0)
        Radiobutton(self,text="Compound", variable=self.forcompound, command=self.set_fields, value=True).grid(row=0,column=1)

        self.addtorow(1,'name','Name',self.basefields, self.loan.name if self.loan else None)
        self.addtorow(2,'amount','Loan total',self.basefields, self.loan.total if self.loan else None)

        self.set_fields()

    def set_fields(self):
        for fieldset in self.extrafields:
            for field in self.extrafields[fieldset]:
                field.destroy()
        self.extrafields = {}

        endrow=3
        if self.forcompound.get():
            endrow=5
            self.addtorow(3,'interest','Interest rate',self.extrafields, self.loan.interest if self.loan and type(self.loan) == loan.CompoundLoan else None)
            self.addtorow(4,'period','Compound period',self.extrafields, self.loan.period if self.loan and type(self.loan) == loan.CompoundLoan else None)

        savebutton =Button(self,text='Save')
        savebutton.grid(row=endrow,column=0)
        cancelbutton =Button(self,text='Cancel')
        cancelbutton.grid(row=endrow,column=1)

        self.extrafields['buttons'] = (savebutton,cancelbutton) # this is a very bad hack

    def addtorow(self,row,name,label,fieldlist=None,content=None):
        '''Adds a label and entry to a particular row'''
        labelfield = Label(self,text=label)
        entryfield = Entry(self)
        labelfield.grid(row=row,column=0)
        entryfield.grid(row=row,column=1)
        if content:
            entryfield.delete(0, END)
            entryfield.insert(0, content)
        if fieldlist is not None: # empty dict is falsy
            fieldlist[label] = (labelfield,entryfield)

root = Tk()
app = Application(root)
root.mainloop()
