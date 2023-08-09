import mysql.connector
import bcrypt

table = [
    [" 1", "Login"],
    [" 2", "Register"],
    [" 3", "Forgot Password"]
]

table2 = [
    [" 1", "Check Balance"],
    [" 2", "Withdraw"],
    [" 3", "Bank In to Your Account"],
    [" 4", "Transfer To Other Bank Account"],
    [" 5", "Log Out"]
]

count = 3

projectdatabase = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="bank")

def createdatabase():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        
        myprojectdb = mydb.cursor()
        myprojectdb.execute("CREATE DATABASE IF NOT EXISTS bank")


        mydbse = projectdatabase.cursor()
        mydbse.execute("CREATE TABLE IF NOT EXISTS user "
                       "(username VARCHAR(200), "
                       "password VARCHAR(200), "
                       "money DOUBLE)")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))

def register():
    print("\n-------------------------------------------------------------")
    print("                            Register")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")
    passwrd = input("Please enter your Password: ")
    cpasswrd = input("Please confirm your New Password: ")

    if passwrd == cpasswrd : 
        passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
        money = 10

        try:
            mydbse = projectdatabase.cursor()
            mydbse.execute("SELECT * FROM user WHERE username=%s",
                           (username,))
            sameinpt = mydbse.fetchone()

            if sameinpt:
                print("Your Account is Already Registered. Please Log In.")
                print("\n-------------------------------------------------------------")
                print("                             Log In")
                print("-------------------------------------------------------------\n")
                login(count)
            else:
                mydbse.execute("INSERT INTO user"
                               "(username, password, money)"
                               "VALUES(%s, %s, %s)",
                               (username, passwrd, money))
                projectdatabase.commit()
                print("Hey " + username + ", Your Account is registered.")
                choose2(money, username)

        except mysql.connector.Error as err:
            print("Failed to Insert data: {}".format(err))
    else :
        print("Please Make Sure Your Password and confirm passwrd is same. please register again")
        register()

def login(count):
    print("\n-------------------------------------------------------------")
    print("                             Log In")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")
    passwrd = input("Please enter your Password: ")

    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            if bcrypt.checkpw(passwrd.encode('utf-8'), user_data[1].encode('utf-8')):
                mydbse.execute("SELECT money FROM user WHERE username=%s",
                               (username,))
                money = mydbse.fetchone()[0]
                print("Welcome back, " + username + ".")
                choose2(money, username)
            else:
                if count == 1:
                    print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                    choose()
                else:
                    count -= 1
                    print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
                    print("\n-------------------------------------------------------------")
                    print("                             Log In")
                    print("-------------------------------------------------------------\n")
                    login(count)
        else:
            print("Your account is not in the database, please register first")
            print("\n-------------------------------------------------------------")
            print("                            Register")
            print("-------------------------------------------------------------\n")
            register()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def forgotpass():
    print("\n-------------------------------------------------------------")
    print("                        Forgot Password")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your New Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("UPDATE user SET password=%s WHERE username=%s",
                    (passwrd, username))
                projectdatabase.commit()
                mydbse.execute("SELECT money FROM user WHERE username=%s",
                    (username,))
                money = mydbse.fetchone()[0]
                print("Welcome back, " + username + ".")
                choose2(money, username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same. please register again")
                forgotpass()
        else:
            print("Your account is not in the database, please register first")
            print("\n-------------------------------------------------------------")
            print("                            Register")
            print("-------------------------------------------------------------\n")
            register()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def choose():
    print("\n-------------------------------------------------------------")
    for row in table:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice = int(input("Please Choose Login or Register or Forgot Password [1 or 2 or 3]: "))
        print()
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                login(count)
            elif userchoice == 2:
                register()
        elif userchoice== 3:
            forgotpass()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 !!!")
            print("\n-------------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 !!!")
        print("\n-------------------------------------------------------------\n")

def withdraw(username):
    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]

        if money <= 10:
            print("Your Account Balance is not enough to withdraw")
        else:
            userwithdraw = float(input("Please Enter Your Withdraw Amount: RM "))
            if userwithdraw > money:
                print("There is not enough money in your account to withdraw")
            elif userwithdraw <= 0:
                print("Please enter a valid withdraw amount.")
            else:
                money -= userwithdraw
                if money < 10:
                    print("There is not enough money in your account to withdraw. Minumum in your account must have RM 10")
                else:
                    mydbse.execute("UPDATE user SET money=%s WHERE username=%s",
                                   (money, username))
                    projectdatabase.commit()

                    print("You have withdrawn RM {:.2f} from your account".format(userwithdraw))
                    print("Your account Balance: RM {:.2f}".format(money))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def checkbalance(username):
    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]
        print("Your account Balance: RM {:.2f}".format(money))
    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def bankin(username):
    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]

        bankinmoney = float(input("Please Enter Your Bankin Amount: RM "))
        if bankinmoney <= 0:
            print("Please Insert Amount Bigger than RM 0")
        else:
            money += bankinmoney
            mydbse.execute("UPDATE user SET money=%s WHERE username=%s",
                           (money, username))
            projectdatabase.commit()

            print("You have banked in RM {:.2f} to your account".format(bankinmoney))
            print("Your account Balance: RM {:.2f}".format(money))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def transfer(username):
    try:
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]

        if money == 0:
            print("Your Account Balance is not enough to transfer")

        else:
            transferusername = input("Please Enter the Username you want to transfer: ")
            try:
                mydbse = projectdatabase.cursor()
                mydbse.execute("SELECT * FROM user WHERE username=%s",
                    (transferusername,))
                user_data = mydbse.fetchone()

                if user_data:
                    usertransfer = float(input("Please Enter Your Transfer Amount: RM "))
                    if usertransfer > money:
                        print("There is not enough money in your account to Transfer")
                    elif usertransfer <= 0:
                        print("Please enter a valid transfer amount.")
                    else:
                        money -= usertransfer
                        if money < 10:
                            print("There is not enough money in your account to withdraw. Minumum in your account must have RM 10")
                        else:
                            mydbse.execute("UPDATE user SET money=%s WHERE username=%s",
                                           (money, username))
                            projectdatabase.commit()

                            mydbse = projectdatabase.cursor()
                            mydbse.execute("SELECT money FROM user WHERE username=%s",
                                (transferusername,))
                            transfermoney = mydbse.fetchone()[0]
                            transfermoney += usertransfer
                            mydbse.execute("UPDATE user SET money=%s WHERE username=%s",
                                           (transfermoney, transferusername))
                            projectdatabase.commit()

                            print("You have Transfer to "+transferusername+" RM {:.2f}".format(usertransfer))
                            print("Your account Balance: RM {:.2f}".format(money))
                else:
                    print("Username not found.")
            except mysql.connector.Error as err:
                print("Failed to update data: {}".format(err))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def choose2(money, username):
    print("\n-------------------------------------------------------------")
    print("                 Account Username: "+username                 )
    print("-------------------------------------------------------------")
    for row in table2:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice2 = int(input("Please Choose [1 or 2 or 3 or 4 or 5]: "))
        print()
        if userchoice2 == 1 or userchoice2 == 2 or userchoice2 == 3 or userchoice2 == 4:
            if userchoice2 == 1:
                checkbalance(username)
            elif userchoice2 == 2:
                withdraw(username)
            elif userchoice2 == 3:
                bankin(username)
            elif userchoice2 == 4:
                transfer(username)
            
            contotext = input("\nDo you want to continue?\nInsert Y to Continue or press Enter to Exit: ")
            contotext = contotext.upper()
            if contotext == "Y":
                choose2(money, username)
            else:
                choose()
        elif userchoice2 == 5:
            choose()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 or 4 or 5 !!!")
            print("\n-------------------------------------------------------------\n")
            choose2(money, username)
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 or 4 or 5 !!!")
        print("\n-------------------------------------------------------------\n")
        choose2(money, username)

createdatabase()
while True:
    choose()
