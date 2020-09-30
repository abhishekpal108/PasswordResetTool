#importing modules definitions
import getpass
import random
import string
import pyodbc
import pandas as pd
import tkinter as tk
from tkinter import *


#defining the functions
def serverselect(srvr):
	global var
	var = str(srvr)
	textvar.set(var)
	conn = pyodbc.connect(DSN=serverip[var])
	cus=conn.cursor()
	query = "SEL username FROM DBC.USERSV where username like('"+str(username)+"%') and username not like all('%6','%2');"
	cus.execute(query)
	for row in cus.fetchone():
		useroption.set(row)
	tduserID.configure(fg='blue',font=('arial',10,'bold'))
	if(str(var) == 'M15'):
		M15.configure(foreground='Green')
		M16.configure(foreground='red')
	elif(str(var) == 'M16'):
		M15.configure(fg='red')
		M16.configure(foreground='green')
	status.set("Server Selected.. \nPlease choose your Action !!")

def passwordGeneration():
    letters_and_digits = string.ascii_letters + string.digits
    newpassword = ''.join((random.choice(letters_and_digits) for i in range(9)))
    return newpassword
	
def PwdReset():
	conn = pyodbc.connect(DSN=serverip[var])
	cus=conn.cursor()
	query = "modify user "+str(useroption.get())+" as password =\""+str(new_password)+"\";"
	print(query)
	#cus.execute(query)
	cus.close()
	query = "insert into SYSDBA.PwdRstAdtLog values('"+str(var)+"','"+str(username)+"','"+str(useroption.get())+"','Password Reset',CURRENT_TIMESTAMP);"
	print(query)
	status.set("Password reset is complete!!")
	
	


def Releaselock():
	conn = pyodbc.connect(DSN=serverip[var])
	cus=conn.cursor()
	query = "modify user "+str(useroption.get())+" as release password lock;"
	print(query)
	#cus.execute(query)
	cus.close()
	query = "insert into SYSDBA.PwdRstAdtLog values('"+str(var)+"','"+str(username)+"','"+str(useroption.get())+"','Release Lock',CURRENT_TIMESTAMP);"
	print(query)
	status.set("Password lock is released!!")
	
#creating the instance class and initializing the variables
win = Tk()
win.title("Teradata Password Reset Tool")
var = ""
textvar = StringVar()
status = StringVar()
username = getpass.getuser()
useroption = StringVar()
new_password = passwordGeneration()

serverip = {"M15":"python_connect","M16":"python_connect"}

#setting up the tool
#row1 :: Server selection and User details

userLBL = Label(win,font=('arial',10,'bold'),text=" User : "+username)
userLBL.grid(row=0,column=0,columnspan=3)
tduserIDLBL = Label(win,font=('arial',10,'bold'),text="Teradata ID: ")
tduserIDLBL.grid(row=0,column=4)
tduserID = Label(win,width=10,textvariable=useroption)
tduserID.grid(row=0,column=5,columnspan=2)

BlankLine = Label(win,text="").grid(row=1)

PswdLBL = Label(win,text="New Password : "+new_password)
PswdLBL.grid(row=2,columnspan=7)

BlankLine = Label(win,text="").grid(row=3)

serverLBL = Label(win,font=('arial',10,'bold'),text="Server Selected ")
serverLBL.grid(row=5,column=4,columnspan=3)
serverdisp = Label(win,font=('arial',10),width=5,textvariable=textvar)
serverdisp.grid(row=6,column=4,columnspan=3)



serveroptionLBL = Label(win,font=('arial',10,'bold'),text="Servers ")
serveroptionLBL.grid(row=5,column=0,columnspan=3)
M15 = Button(win,width=12,font=('arial',10),text="PROD-M15",command=lambda:serverselect('M15'))
M15.grid(row=6,column=0)
M16 = Button(win,width=12,font=('arial',10),text="DEV/QA-M16",command=lambda:serverselect('M16'))
M16.grid(row=6,column=1)


OptnLBL = Label(win,font=('arial',10,'bold'),text="Actions ")
OptnLBL.grid(row=8,column=0,columnspan=3)
PwdRst = Button(win,width=12,font=('arial',10),text="Password Reset",command=lambda:PwdReset())
PwdRst.grid(row=9,column=0)
Rlslock = Button(win,width=12,font=('arial',10),text="Release Lock",command=lambda:Releaselock())
Rlslock.grid(row=9,column=1)




statusLBL	=	Label(win,font=('arial',10,'bold'),text="Action Process").grid(row=8,column=4,columnspan=3)

status.set("Please.. Select server !!")
StatusLBL = Label(win,textvariable = status)
StatusLBL.grid(row=9,column=4,columnspan=3)

BlankLine = Label(win,text="").grid(row=10)



win.mainloop()
