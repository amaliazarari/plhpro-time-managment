import tkinter as tk
import tkinter
from tkinter import ttk
from tkinter import *

#κουμπιά
def logIn():
    output.delete("1.0",tk.END) #καθαρίζει το frame
    output.insert(tk.END, f"a. Για εισαγωγή νέων χρηστών: \nb. Σύνδεση χρήστη:\n")
    return

def b2pushed():
    output.delete("1.0", tk.END) #καθαρίζει το frame
    output.insert(tk.END,"KANE KATI\n\n")
    return

def b3pushed():
    output.delete("1.0", tk.END) #καθαρίζει το frame
    output.insert(tk.END,"KANE KATI\n")
    return

def b5pushed():
    window.destroy()#τερματισμός παραθύρου
    return

window = tk.Tk() #φτιάχνω παράθυρο
window.title("Project53 (Διαχείριση Χρόνου)") #τίτλος παραθύρου πάνω αριστερά
window.minsize(width=350, height=600) #ελάχιστο μέγεθος παραθύρου

left = tk.Frame(window)
left.pack(side = "left")

right = tk.Frame(window)
right.pack(side= "right")

tkinter.Label(window, text="Εφαρμογή Διαχείρισης Χρόνου Υποχρεώσεων & Ελεύθερου Χρόνου").pack()
tkinter.Label(window, text="\n=== MENOY ΔΙΑΧΕΙΡΙΣΗΣ ΧΡΟΝΟΥ ===").pack()

#Απλά κουμπιά print
btnTotal = tkinter.Button(left,text="Εισαγωγή Δεδομένων",command=logIn, width=40)
btnTotal.pack()
btnMaxMin = tkinter.Button(left,text="Push a)",command=b2pushed, width=40)
btnMaxMin.pack()
movingAvgBtn = tkinter.Button(left,text="Push b)",command=b3pushed, width=40)
movingAvgBtn.pack()
exitBtn = tkinter.Button(left,text="2. Έξοδος", bg='salmon', fg="white smoke",command=b5pushed, width=40)
exitBtn.pack()

output = tkinter.Text(right , width=60)
output.pack()

window.mainloop()