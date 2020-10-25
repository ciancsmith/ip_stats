# import tkinter module 
from tkinter import * 
from tkinter import Entry

  
# creating main tkinter window/toplevel 
master = Tk()
master.geometry("500x500")
master.title("Ip Assignment 1")
master.iconphoto(False, PhotoImage(file='logo.png'))


checks = LabelFrame(master, text="Output", background="black").grid()


def stats():
    ip = e1.get()
    subnet = e2.get()
    print(ip, subnet)

#this will check if the value of the checkButtons
def show():
    myLabel1 = Label(master, text=var1.get()).grid(row=4, column=4)
    mylabel2 = Label(master, text=var2.get()).grid(row=5, column=4)
  
# this wil create a label widget 
l1 = Label(master, text = "IP ADDRESS:") 
l2 = Label(master, text = "SUBNET MASK:") 
  
# grid method to arrange labels in respective 
# rows and columns as specified 
l1.grid(row = 0, column = 0, sticky = W, pady = 2, padx = 2) 
l2.grid(row = 1, column = 0, sticky = W, pady = 2, padx= 2) 
  
# entry widgets, used to take entry from user 
e1 = Entry(master, width=30, bd=5) 
e2 = Entry(master, width=30, bd=5)


# this will arrange entry widgets 
e1.grid(row = 0, column = 1, pady = 2) 
e2.grid(row = 1, column = 1, pady = 2)
e1.insert(0,"e.g: (192.168.10.0)")
e2.insert(0, "e.g: (255.255.255.192)")

#this will arrange the checkboxes to enable different functions
var1 = IntVar()
var2 = IntVar()
c1 = Checkbutton(checks, text="get_ip_stats", variable=var1).grid(row = 0, column= 2, padx=2, pady=2, sticky=W)
c2 = Checkbutton(checks, text="get_subnet_stats", variable=var2).grid(row = 1, column = 2, padx=2, pady=2, sticky=W)
myButton = Button(checks, text="test", command=show, width = 10).grid(row = 2, column=2)

# infinite loop which can be terminated by keyboard 
# or mouse interrupt 
action = Button(master, text="Process", command=stats, width=10).grid(row=2, column=1, sticky=W)
quit = Button(master, text="Quit", command=master.quit, width=10).grid(row=3, column=1, sticky=W)
mainloop() 