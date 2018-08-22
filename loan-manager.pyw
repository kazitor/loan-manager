from tkinter import *
from tkinter import messagebox # you tell me why this necessary
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
        Label(self,text="Managed loans").grid(row=0,column=0)
        Label(self,text="Time to pay off").grid(row=0,column=1)
        Label(self,text="Amount needed").grid(row=0,column=2)
        self.loanfields=[]
        self.new_button = Button(self,text="New loan",command=self.editloan)
        self.listloans()

    def listloans(self):
        for fieldset in self.loanfields:
            for widget in fieldset:
                widget.destroy()
        self.loanfields.clear()

        self.loans = self.loadloans()
        row = 0 # in case loop is empty
        for i,loan in enumerate(self.loans):
            row = i + 1
            fieldset = (
                Label(self, text=(loan.name[:27] + '...') if len(loan.name) > 30 else loan.name),
                Label(self, text=loan.payoff_time_nice),
                Label(self, text=loan.left_nice),
                Button(self,text="Edit",  command=lambda loanno=i: self.editloan(loanno)),
                Button(self,text="Delete",command=lambda loanno=i: self.deleteloan(loanno)),
            )
            for col,field in enumerate(fieldset):
                field.grid(row = row, column = col)

            self.loanfields.append(fieldset)

        self.new_button.grid(row=row+1,column=0)

    def editloan(self,loanno=None):
        """ Open a window for managing a single loan """
        window = LoanEditWindow(self.master,self.loans[loanno] if loanno is not None else None)
        if window.newloan:
            if loanno is None:
                self.loans.append(window.newloan)
            else:
                self.loans[loanno] = window.newloan
            self.saveloans()
            self.listloans()

    def deleteloan(self, loanno):
        self.loans.pop(loanno) # pop is by index, remove is by value
        self.saveloans()
        self.listloans()

    def loadloans(self) -> list:
        try:
            with open('loans.dat', 'rb') as f:
                return pickle.load(f)
        except IOError as e:
            if e.errno == 2: # file does not exist
                return []
            else:
                raise

    def saveloans(self):
        with open('loans.dat', 'wb') as f:
            pickle.dump(self.loans, f)

class LoanEditWindow(Toplevel):
    """Window for editing or creating a loan"""
    def __init__(self, master,loanobject=None):
        super(LoanEditWindow, self).__init__(master)
        self.transient(master)

        self.master = master
        self.oldloan = loanobject
        self.newloan = None
        self.loantype = IntVar()

        if self.oldloan:
            self.wm_title("Editing %s" % self.oldloan.name)
            self.loantype.set( self.oldloan.id )
        else:
            self.wm_title("Create new loan")
        
        self.geometry("300x200")
        self.focus_set()
        self.grab_set()
        self.grid()
        self.add_widgets()

        self.bind('<Return>', self.save)
        self.bind('<Escape>', self.close)

        self.wait_window(self)

    def add_widgets(self):
        self.inputfields=[]
        self.buttons = (
            Button(self,text='Save',command=self.save, default=ACTIVE),
            Button(self,text='Cancel',command=self.close)
        ) # add to grid after input fields are added

        for i,loantype in enumerate(loan.types):
            Radiobutton(self, text=loantype.title, variable=self.loantype, command=self.set_fields, value=i).grid(row=0,column=i)

        self.set_fields()

    def set_fields(self):
        for fieldset in self.inputfields:
            for field in fieldset:
                field.destroy()
        self.inputfields.clear()

        loanobj = loan.by_id(self.loantype.get())
        for i in range(len(loanobj.fields)):
            row = i + 1
            label = loanobj.fields[i]

            labelfield = Label(self,text=label)
            entryfield = Entry(self)
            if self.oldloan:
                entryfield.insert(0, self.oldloan.values[i])
            labelfield.grid(row=row, column=0, sticky=E)
            entryfield.grid(row=row,column=1)
            self.inputfields.append((labelfield,entryfield))

        for i,button in enumerate(self.buttons):
            button.grid(row=row+1, column=i)

    def save(self, event=None):
        values = [entry.get() for label, entry in self.inputfields]
        try:
            self.newloan = loan.by_id( self.loantype.get() )(*values) # pass values sequentially into loan constructor
        except ValueError as e:
            messagebox.showerror("Invalid values",e)
        else:
            self.close()

    def close(self, event=None):
        self.master.focus_set()
        self.destroy()

root = Tk()
icon = PhotoImage(file='icon.gif')
root.iconphoto(True, icon)
app = Application(root)
root.mainloop()
