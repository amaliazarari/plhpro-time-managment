import tkinter as tk
import tkinter
from tkinter import ttk
# from tkinter import *

class Graphics():
    def __int__(self, master):
        #frame = Frame(master)
        #frame.pack()
        self.master

window = tk.Tk() #φτιάχνω παράθυρο
window.title("Project53 (Διαχείριση Χρόνου)") #τίτλος παραθύρου πάνω αριστερά
window.minsize(width=800, height=600) #ελάχιστο μέγεθος παραθύρου


left = tk.Frame(window)
left.pack(side = "left")

right = tk.Frame(window)
right.pack(side= "right")

tkinter.Label(window, text="Hello! \nΕφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου").pack()

output = tkinter.Text(right , width=45)
output.pack()

window.mainloop()