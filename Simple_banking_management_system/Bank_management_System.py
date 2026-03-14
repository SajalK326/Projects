import tkinter as tk
import random
import mysql.connector as sql
from tkinter import *
from bank_config import ADMIN_PASSWORD, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER

def setup_database():
    my_db = sql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Successfully Connected...")
    my_cur = my_db.cursor()
    my_cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    my_cur.execute(f"USE {DB_NAME}")
    my_cur.execute(
        "CREATE TABLE IF NOT EXISTS customer (Account_No bigint, Name VARCHAR(100), Mobile_No bigint, Account_Type VARCHAR(20), Amount bigint)"
    )
    my_db.commit()
    print("Database Initializaion Successful...")

    return my_db, my_cur

mydb, mycur = setup_database()

class AccountGenerator:
    def __init__(self):
        self.generated_accounts = set()

    def generate_account_number(self):
        while True:
            account_number = random.randint(10000, 99999)
            if account_number not in self.generated_accounts:
                self.generated_accounts.add(account_number)
                return account_number

account_generator = AccountGenerator()

class Account:
    accNo = 0
    name = ""
    deposit = 0
    atype = ""

    def createAccount():
        cr = Tk()
        cr.title("Create Account")
        cr.configure(width=200, height=100, bg='GREEN')

        account_number = account_generator.generate_account_number()

        l1 = Label(cr, text="Your Account no. is: " + str(account_number), bg="YELLOW", relief="ridge", fg="RED", font=("Times", 12), width=50)
        l1.grid(row=1, column=2, sticky=W, padx=10, pady=10)

        l2 = Label(cr, text="Enter Your Name", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
        e2 = Entry(cr, font=("Times", 12))
        l2.grid(row=2, column=2, sticky=W, padx=10, pady=10)
        e2.grid(row=2, column=3, padx=10, pady=10)

        l3 = Label(cr, text="Enter Your Mobile no.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
        e3 = Entry(cr, font=("Times", 12))
        l3.grid(row=3, column=2, sticky=W, padx=10, pady=10)
        e3.grid(row=3, column=3, padx=10, pady=10)

        l4 = Label(cr, text="Enter Your Account Type", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
        e4 = Entry(cr, font=("Times", 12))
        l4.grid(row=4, column=2, sticky=W, padx=10, pady=10)
        e4.grid(row=4, column=3, padx=10, pady=10)

        l5 = Label(cr, text="Enter Amount to Deposit", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
        e5 = Entry(cr, font=("Times", 12))
        l5.grid(row=5, column=2, sticky=W, padx=10, pady=10)
        e5.grid(row=5, column=3, padx=10, pady=10)

        l6 = Label(cr, text="Please Save/Write Your Account No. Carefully For Future Reference", bg="YELLOW", relief="ridge", fg="RED", font=("Times", 12), width=50)
        l6.grid(row=6, column=2, sticky=W, padx=10, pady=10)

        def wrt():
            accNo = account_number
            name = e2.get()
            y = int(e3.get())
            atype = e4.get()
            z = int(e5.get())
            mycur.execute("INSERT INTO customer VALUES(%s, %s, %s, %s, %s)", (accNo, name, y, atype, z))
            mydb.commit()
        bcr = Button(cr, text="Submit", command=lambda: [wrt(), cr.destroy()])
        bcr.grid(row=7, column=2, padx=10, pady=10)

        cr.mainloop()


def displayAll():
    dal = Tk()
    dal.title("All Account Holders List")
    dal.configure(width=200, height=100, bg='GREEN')

    ldal = Label(dal, text="Enter Administrator Password", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    edal = Entry(dal, font=("Times", 12))
    ldal.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    edal.grid(row=1, column=3, padx=10, pady=10)

    def dispall():
        x = edal.get()
        if x == ADMIN_PASSWORD:
            mycur.execute("SELECT * FROM customer")
            d = mycur.fetchall()
            ldal1 = Label(dal, text="(Account No., Name, Mobile No., Account Type, Account Balance)", bg="red", relief="ridge", fg="white", font=("Times", 12), width=50)
            ldal1.grid(row=3, column=2, sticky=W, padx=10, pady=10)
            c = 3
            for i in d:
                la = Label(dal, text=str(i), bg="red", relief="ridge", fg="white", font=("Times", 12), width=50)
                c += 1
                la.grid(row=c, column=2, sticky=W, padx=10, pady=10)

    bdal = Button(dal, text="Submit", command=lambda: dispall())
    bdal.grid(row=2, column=2, padx=10, pady=10)


def displaySp(num):
    disp = Tk()
    disp.title("Balance Enquiry")
    disp.configure(width=200, height=100, bg='GREEN')

    ldsp = Label(disp, text="Enter Your Account no.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    edsp = Entry(disp, font=("Times", 12))
    edsp.insert(0, "0")
    ldsp.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    edsp.grid(row=1, column=3, padx=10, pady=10)

    def subm():
        num1 = edsp.get()
        num = int(num1)
        mycur.execute("SELECT Account_No FROM customer WHERE Account_No=%s", (num,))
        d = mycur.fetchall()

        if (num,) in d:
            mycur.execute("SELECT Amount FROM customer WHERE Account_No=%s", (num,))
            d = mycur.fetchall()
            current_amount = d[0][0]
            ldsp1 = Label(disp, text="Your Current Account Balance is: " + str(current_amount), bg="red", relief="ridge", fg="white", font=("Times", 12), width=50)
            ldsp1.grid(row=3, column=2, sticky=W, padx=10, pady=10)
            bdsp1 = Button(disp, text="   OK   ", command=lambda: disp.destroy())
            bdsp1.grid(row=4, column=2, padx=10, pady=10)

        else:
            ldsp2 = Label(disp, text="No records to Search", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
            ldsp2.grid(row=3, column=2, sticky=W, padx=10, pady=10)

    bdsp = Button(disp, text="Submit", command=lambda: subm())
    bdsp.grid(row=2, column=2, padx=10, pady=10)


def depositAndWithdraw(num1, num2):
    daw = Tk()
    daw.title("Deposit And Withdraw")
    daw.configure(width=200, height=100, bg='GREEN')

    ld1 = Label(daw, text="Enter Your Account no.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    ed1 = Entry(daw, font=("Times", 12))
    ed1.insert(0, "0")
    ld1.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    ed1.grid(row=1, column=3, padx=10, pady=10)

    def on_button_click():
        num1 = ed1.get()
        b = int(num1)
        mycur.execute("SELECT Account_No FROM customer WHERE Account_No=%s", (b,))
        data = mycur.fetchall()

        if (b,) in data:

            if num2 == 1:

                ld2 = Label(daw, text="Enter the amount to deposit: ", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
                ed2 = Entry(daw, font=("Times", 12))
                ld2.grid(row=3, column=2, sticky=W, padx=10, pady=10)
                ed2.grid(row=3, column=3, padx=10, pady=10)

                def dep():
                    amount = ed2.get()
                    x = int(amount)
                    mycur.execute("UPDATE customer SET Amount = Amount + %s WHERE Account_No = %s", (x, num1))

                bd1 = Button(daw, text="Submit", command=lambda: [dep(), daw.destroy()])
                bd1.grid(row=4, column=2, padx=10, pady=10)

            elif num2 == 2:

                ld3 = Label(daw, text="Enter the amount to withdraw: ", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
                ed3 = Entry(daw, font=("Times", 12))
                ld3.grid(row=3, column=2, sticky=W, padx=10, pady=10)
                ed3.grid(row=3, column=3, padx=10, pady=10)

                def wit():
                    amount = ed3.get()
                    x = int(amount)
                    mycur.execute("SELECT Amount FROM customer WHERE Account_No=%s", (b,))
                    y = mycur.fetchall()

                    if y:
                        current_amount = y[0][0]
                        if x <= current_amount:
                            a = current_amount - x
                            mycur.execute("UPDATE customer SET Amount = %s WHERE Account_No = %s", (a, num1))
                        else:
                            ld4 = Label(daw, text="You cannot withdraw larger amount", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
                            ld4.grid(row=2, column=2, sticky=W, padx=10, pady=10)

                bd2 = Button(daw, text="Submit", command=lambda: [wit(), daw.destroy()])
                bd2.grid(row=4, column=2, padx=10, pady=10)

        else:
            ld5 = Label(daw, text="No Records To Search", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
            ld5.grid(row=2, column=2, sticky=W, padx=10, pady=10)

    bd = Button(daw, text="Submit", command=lambda: on_button_click())
    bd.grid(row=2, column=2, padx=10, pady=10)


def deleteAccount(num):
    dcc = Tk()
    dcc.title("Delete Account")
    dcc.configure(width=200, height=100, bg='GREEN')

    ldcc = Label(dcc, text="Enter Your Account no.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    edcc = Entry(dcc, font=("Times", 12))
    edcc.insert(0, "0")
    ldcc.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    edcc.grid(row=1, column=3, padx=10, pady=10)

    def subd():
        num1 = edcc.get()
        num = int(num1)
        mycur.execute("SELECT Account_No FROM customer WHERE Account_No=%s", (num,))
        d = mycur.fetchall()

        if (num,) in d:
            mycur.execute("DELETE FROM customer WHERE Account_No=%s", (num,))
            ldcc1 = Label(dcc, text="Your Current Account Has Been Closed", bg="red", relief="ridge", fg="white", font=("Times", 12), width=50)
            ldcc1.grid(row=3, column=2, sticky=W, padx=10, pady=10)
            ldcc2 = Label(dcc, text="Have A Nice Day!!!", bg="red", relief="ridge", fg="white", font=("Times", 12), width=50)
            ldcc2.grid(row=4, column=2, sticky=W, padx=10, pady=5)
            bdcc1 = Button(dcc, text="  Done  ", command=lambda: dcc.destroy())
            bdcc1.grid(row=5, column=2, padx=10, pady=10)

        else:
            ldcc3 = Label(dcc, text="No records to Search", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
            ldcc3.grid(row=3, column=2, sticky=W, padx=10, pady=10)
            bdcc2 = Button(dcc, text="  Done  ", command=lambda: dcc.destroy())
            bdcc2.grid(row=4, column=2, padx=10, pady=10)

    bdcc = Button(dcc, text="Submit", command=lambda: subd())
    bdcc.grid(row=2, column=2, padx=10, pady=10)


def modifyAccount(num):
    dma = Tk()
    dma.title("Modify Mobile Number")
    dma.configure(width=200, height=100, bg='GREEN')

    ldma = Label(dma, text="Enter Your Account no.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    edma = Entry(dma, font=("Times", 12))
    edma.insert(0, "0")
    ldma.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    edma.grid(row=1, column=3, padx=10, pady=10)

    def subd():
        num1 = edma.get()
        num = int(num1)
        mycur.execute("SELECT Account_No FROM customer WHERE Account_No=%s", (num,))
        d = mycur.fetchall()

        if (num,) in d:
            ldma1 = Label(dma, text="Enter New Mobile No.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
            ldma1.grid(row=3, column=2, sticky=W, padx=10, pady=10)
            edma1 = Entry(dma, font=("Times", 12))
            edma1.grid(row=3, column=3, padx=10, pady=10)

            def modmob():
                mobile = edma1.get()
                x = int(mobile)
                mycur.execute("UPDATE customer SET Mobile_No = %s WHERE Account_No = %s", (x, num))

            bdma1 = Button(dma, text="Submit", command=lambda: [modmob(), dma.destroy()])
            bdma1.grid(row=4, column=2, padx=10, pady=10)

        else:
            ldma3 = Label(dma, text="No records to Search", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
            ldma3.grid(row=3, column=2, sticky=W, padx=10, pady=10)

    bdma = Button(dma, text="Submit", command=lambda: subd())
    bdma.grid(row=2, column=2, padx=10, pady=10)


num = 0

def first(var):
    ch = var

    if ch == "1":
        Account.createAccount()

    elif ch == "2":
        num = 0
        depositAndWithdraw(num, 1)

    elif ch == "3":
        num = 0
        depositAndWithdraw(num, 2)

    elif ch == "4":
        num = 0
        displaySp(num)

    elif ch == "5":
        displayAll()

    elif ch == "6":
        num = 0
        deleteAccount(num)

    elif ch == "7":
        num = 0
        modifyAccount(num)

    else:
        def inval():
            inv = Tk()
            inv.title("Invalid Choice")
            inv.configure(width=200, height=100, bg='GREEN')

            linv = Label(inv, text="Invalid Choice, Enter A No. Between 1 To 7", bg="red", relief="ridge", fg="white", font=("Times", 15), width=40)
            linv.grid(row=1, column=2, sticky=W, padx=10, pady=30)

            def desfunc():
                inv.destroy()

            binv = Button(inv, text="   OK   ", command=desfunc)
            binv.grid(row=2, column=2, padx=10, pady=20)

        inval()


def main():

    def getfunc():
        var = entry1.get()
        first(var)

    def mydb_cls():
        mydb.commit()
        mycur.close()
        mydb.close()
        print("Connection Has Been Successfully Closed And Changes Have Been Saved !!!")

    root = Tk()
    root.title("IPS Bank Online banking System")
    root.configure(width=2000, height=1000, bg='sea green')

    lab0 = Label(root, text="IPS Bank Online Banking System", bg="black", fg="white", font=("Times", 60), anchor="center")
    lab1 = Label(root, text="MAIN MENU", bg="black", fg="white", font=("Times", 40))
    lab2 = Label(root, text="1. NEW ACCOUNT", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    lab3 = Label(root, text="2. DEPOSIT AMOUNT", bd="2", relief="ridge", height="1", bg="red", fg="white", font=("Times", 12), width=35)
    lab4 = Label(root, text="3. WITHDRAW AMOUNT", bd="2", relief="ridge", bg="red", fg="white", font=("Times", 12), width=35)
    lab5 = Label(root, text="4. BALANCE ENQUIRY", bd="2", relief="ridge", bg="red", fg="white", font=("Times", 12), width=35)
    lab6 = Label(root, text="5. ALL ACCOUNT HOLDER LIST", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    lab7 = Label(root, text="6. CLOSE AN ACCOUNT", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    lab8 = Label(root, text="7. MODIFY/CHANGE MOBILE NO.", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    lab10 = Label(root, text="Enter Your Option (1-7)", bg="red", relief="ridge", fg="white", font=("Times", 12), width=35)
    entry1 = Entry(root, font=("Times", 12))
    b = Button(root, text="Submit", command=getfunc)
    b1 = Button(root, text="  Quit  ", command=lambda: [mydb_cls(), root.destroy()])

    lab0.grid(columnspan=8, padx=10, pady=10)
    lab1.grid(row=1, column=2, sticky=W, padx=10, pady=10)
    lab2.grid(row=2, column=1, sticky=W, padx=10, pady=10)
    lab3.grid(row=3, column=1, sticky=W, padx=10, pady=10)
    lab4.grid(row=4, column=1, sticky=W, padx=10, pady=10)
    lab5.grid(row=5, column=1, sticky=W, padx=10, pady=10)
    lab6.grid(row=6, column=1, sticky=W, padx=10, pady=10)
    lab7.grid(row=7, column=1, sticky=W, padx=10, pady=10)
    lab8.grid(row=8, column=1, sticky=W, padx=10, pady=10)
    lab10.grid(row=4, column=2, sticky=W, padx=10, pady=10)
    entry1.grid(row=5, column=2, padx=40, pady=10)
    b.grid(row=6, column=2, padx=10, pady=10)
    b1.grid(row=7, column=2, padx=10, pady=10)


def Main_Menu():
    rootwn = tk.Tk()
    rootwn.geometry("1600x500")
    rootwn.title("IPS Bank - The Bank Of International Public School")
    rootwn.configure(background='orange')

    fr1 = tk.Frame(rootwn)
    fr1.pack(side="top")
    bg_image = tk.PhotoImage(file="pile1.gif")
    x = tk.Label(image=bg_image)
    x.place(y=-400)
    l_title = tk.Message(text="IPS BANK \n ONLINE BANKING SYSTEM", relief="raised", width=2000, padx=600, pady=0, fg="white", bg="black", justify="center", anchor="center")
    l_title.config(font=("Courier", "50", "bold"))
    l_title.pack(side="top")

    imgstrt = tk.PhotoImage(file="imgstrtgif.gif")
    newimgstrt = imgstrt.subsample(3, 3)

    b2 = tk.Button(image=newimgstrt, width=200, height=100, command=main)
    b2.image = imgstrt
    img6 = tk.PhotoImage(file="quit.gif")
    myimg6 = img6.subsample(2, 2)

    b6 = tk.Button(image=myimg6, command=rootwn.destroy)
    b6.image = myimg6
    b2.place(x=800, y=200)
    b6.place(x=920, y=400)

    rootwn.mainloop()


Main_Menu()
