from tkinter import *

class Application(Frame):
	"""Root window"""
	def __init__(self, master):
		super(Application, self).__init__(master)

root = Tk()
root.title("Loan manager")
app = Application(root)
root.mainloop()
