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
        self.loans = self.loadloans()
        self.add_widgets()
    def add_widgets(self):
        Label(self,text="Managed loans").grid(row=0)
        i = 0 # in case loop is empty
        for i,loan in enumerate(self.loans,1):
            Label(self, text=loan.name).grid(row=i,column=0)
            Button(self,text="Edit",command=lambda loan=loan: self.editloan(loan)).grid(row=i,column=1)
        Button(self,text="New loan",command=self.editloan).grid(row=i+1,column=0)
    def loadloans(self) -> list:
        try:
            with open('loans.dat', 'rb') as f:
                return pickle.load(f)
        except IOError as e:
            if e.errno == 2: # file does not exist
                return []
            else:
                raise e
    def saveloans(self):
        with open('loans.dat', 'wb') as f:
            pickle.dump(self.loans, f)
    def editloan(self,loan=None):
        """ Open a window for managing a single loan """
        window = LoanEditWindow(self.master,loan)
    def close(self):
        self.saveloans()
        self.master.destroy()

class LoanEditWindow(Toplevel):
    """Window for editing or creating a loan"""
    def __init__(self, master,loanobject=None):
        super(LoanEditWindow, self).__init__(master)
        self.master = master
        self.loan = loanobject
        self.loantype = IntVar()

        if self.loan:
            self.wm_title("Editing %s" % self.loan.name)
            self.loantype.set( self.loan.id )
        else:
            self.wm_title("Create new loan")
        
        self.geometry("300x200")
        self.grid()
        self.add_widgets()

    def add_widgets(self):
        self.inputfields=[]
        self.buttons = (
            Button(self,text='Save',command=self.save),
            Button(self,text='Cancel',command=self.destroy)
        ) # add to grid after input fields are added

        for i,loantype in enumerate(loan.types):
            Radiobutton(self, text=loantype.title, variable=self.loantype, command=self.set_fields, value=i).grid(row=0,column=i)

        self.set_fields()

    def set_fields(self):
        for fieldset in self.inputfields:
            for field in fieldset:
                field.destroy()
        self.inputfields.clear()

        for row, label in enumerate(loan.types[self.loantype.get()].fields, 1):
            labelfield = Label(self,text=label)
            entryfield = Entry(self)
            # entryfield.insert(0, content)
            labelfield.grid(row=row, column=0)
            entryfield.grid(row=row,column=1)
            self.inputfields.append((labelfield,entryfield))

        for i,button in enumerate(self.buttons):
            button.grid(row=row+1, column=i)

    def save(self):
        pass

root = Tk()
app = Application(root)
root.protocol('WM_DELETE_WINDOW', app.close)
root.mainloop()
