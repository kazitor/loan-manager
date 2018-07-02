from tkinter import *
from loan import Loan

class Application(Frame):
	"""Root window"""
	def __init__(self, master):
		super(Application, self).__init__(master)
		self.grid()
		self.add_widgets()
	def add_widgets(self):
		"""
		load file
		list loans
		add loan
		"""
		Button(self,text="Open file",command=self.loadfile).grid(row=0)
		for i,loan in enumerate(self.getloans()):
			Label(self, text=loan.name).grid(row=i+1,column=0)
			Button(self,text="Edit").grid(row=i+1,column=1)
	def loadfile(self):
		pass
	def getloans(self) -> list:
		# temporary
		return [Loan("technical debt",100000,1)]

root = Tk()
root.title("Loan manager")
app = Application(root)
root.mainloop()
