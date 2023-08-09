import mysql.connector
import bcrypt

table = [
    [" 1", "Login"],
    [" 2", "Register"]
]

table2 = [
    [" 1", "Check Balance"],
    [" 2", "Withdraw"],
    [" 3", "Bank In to Your Account"],
    [" 4", "Log Out"]
]

count=3

def createdatabase():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="")
        
        myprojectdb = mydb.cursor()
        myprojectdb.execute("CREATE DATABASE IF NOT EXISTS bank")

        projectdatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank")

        mydbse = projectdatabase.cursor()
        mydbse.execute("CREATE TABLE IF NOT EXISTS user "
                       "(username VARCHAR(200), "
                       "password VARCHAR(200), "
                       "money DOUBLE)")
    except mysql.connector.Error as err:
        print("Error: {}".format(err))

def register():
    username = input("Please enter your Username: ")
    passwrd = input("Please enter your Password: ")

    # Hash the password using bcrypt
    passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
    money = 0

    try:
        projectdatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank")

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

def login(count):
    username = input("Please enter your Username: ")
    passwrd = input("Please enter your Password: ")

    try:
        projectdatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank")

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
                if count==1:
                    print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                    choose()
                else:
                    count-=1
                    print("Your password is wrong. Please try again. You only have "+str(count)+" chances left")
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

def choose():
    print("\n-------------------------------------------------------------")
    for row in table:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice = int(input("Please Choose Login or Register [1 or 2]: "))
        print()
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                login(count)
            elif userchoice == 2:
                register()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 !!!")
            print("\n--------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 !!!")
        print("\n--------------------------------------------------------\n")

def withdraw(username):
    try:
        projectdatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank")

        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]

        if money == 0:
            print("Your Account Balance is not enough to withdraw")

        else:
            userwithdraw = float(input("Please Enter Your Withdraw Amount: RM "))
            if userwithdraw > money:
                print("There is not enough money in your account to withdraw")
            else:
                money -= userwithdraw
                mydbse.execute("UPDATE user SET money=%s WHERE username=%s",
                               (money, username))
                projectdatabase.commit()

                print("You have withdrawn RM {:.2f} from your account".format(userwithdraw))
                print("Your account Balance: RM {:.2f}".format(money))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def checkbalance(money):
    print("Your account Balance: RM {:.2f}".format(money))

def bankin(username):
    try:
        projectdatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="bank")

        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]

        bankinmoney = float(input("Please Enter Your Bankin Amount: RM "))
        if bankinmoney < 0:
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

def choose2(money, username):
    print("\n-------------------------------------------------------------")
    for row in table2:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice2 = int(input("Please Choose [1 or 2 or 3 or 4]: "))
        print()
        if userchoice2 == 1 or userchoice2 == 2 or userchoice2 == 3:
            if userchoice2 == 1:
                checkbalance(money)
            elif userchoice2 == 2:
                withdraw(username)
            elif userchoice2 == 3:
                bankin(username)
            
            contotext = input("\nDo you want to continue?\nInsert Y to Continue or press Enter to Exit: ")
            contotext = contotext.upper()
            if contotext == "Y":
                choose2(money, username)
            else:
                choose()
        elif userchoice2 == 4:
            choose()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 !!!")
            print("\n--------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 !!!")
        print("\n--------------------------------------------------------\n")

createdatabase()
while True:
    choose()
