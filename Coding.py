import mysql.connector
import bcrypt

table = [
    [" 1", "Login"],
    [" 2", "Register"],
    [" 3", "Forgot Password"],
    [" 4", "Admin"]
]

table2 = [
    [" 1", "Check Balance"],
    [" 2", "Withdraw"],
    [" 3", "Bank In to Your Account"],
    [" 4", "Transfer To Other Bank Account"],
    [" 5", "Transaction History"],
    [" 6", "Change Password"],
    [" 7", "Log Out"]
]

tableadmin = [
    [" 1", "Login Admin"],
    [" 2", "Register Admin"],
    [" 3", "Forgot Admin Password"],
    [" 4", "Back"],
]

adminsitab = [
    [" 1", "Check User Account"],
    [" 2", "Update User Account"],
    [" 3", "Update Admin Account"],
    [" 4", "Change Password"],
    [" 5", "Delete Account"],
    [" 6", "Check Money In All Account"],
    [" 7", "Log Out"]
]

count = 3

def database():
    return mysql.connector.connect(
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

        projectdatabase = database()
        mydbse = projectdatabase.cursor()

        mydbse.execute("CREATE TABLE IF NOT EXISTS user "
                       "(username VARCHAR(200), "
                       "password VARCHAR(200), "
                       "money DOUBLE)")

        mydbse.execute("CREATE TABLE IF NOT EXISTS admin "
                       "(username VARCHAR(200), "
                       "password VARCHAR(200)) ")

        mydbse.execute("CREATE TABLE IF NOT EXISTS history "
                       "(username VARCHAR(200), "
                       "detail VARCHAR(200), "
                       "money VARCHAR(200)) ")

    except mysql.connector.Error as err:
        print("Error: {}".format(err))

def register():
    print("\n-------------------------------------------------------------")
    print("                            Register")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",
                       (username,))
        sameinpt = mydbse.fetchone()

        if sameinpt:
            print("Your Account is Already Registered. Please Log In.")
            askuser=input("Do you want To Register Other Account ? [ Y to continue or any key to login ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                register()
            else :
                login(count)
        else:
            passwrd = input("Please enter your Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                money = 10
                mydbse.execute("INSERT INTO user"
                               "(username, password, money)"
                               "VALUES(%s, %s, %s)",
                               (username, passwrd, money))
                projectdatabase.commit()

                mydbse.execute("INSERT INTO history"
                               "(username, detail, money)"
                               "VALUES(%s, %s, %s)",
                               (username, "Register Account", "+RM {:.2f}".format(money)))
                projectdatabase.commit()
                print("Hey " + username + ", Your Account is registered.")

                choose2(money, username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same. please register again")
                register()

    except mysql.connector.Error as err:
        print("Failed to Insert data: {}".format(err))

def login(count):
    print("\n-------------------------------------------------------------")
    print("                             Log In")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM user WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your Password: ")
            if bcrypt.checkpw(passwrd.encode('utf-8'), user_data[1].encode('utf-8')):
                mydbse.execute("SELECT money FROM user WHERE username=%s",
                               (username,))
                money = mydbse.fetchone()[0]
                print("Welcome back, " + username + ".")
                choose2(money, username)
            else:
                if count == 1:
                    print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                    print("\n-------------------------------------------------------------")
                    choose()
                else:
                    count -= 1
                    print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
                    login(count)
        else:
            print("Your account is not in the database, please register first")
            askuser=input("Do you want To Login ? [ Y to continue or any key to register ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                login(count)
            else :
                register()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def forgotpass():
    print("\n-------------------------------------------------------------")
    print("                        Forgot Password")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
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
            askuser=input("Do you want To bank ? [ Y to back or any key to continue ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                print("\n-------------------------------------------------------------")
                choose()
            else :
                forgotpass()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def checkuser(username):
    print("\n-------------------------------------------------------------")
    print("                     Check User Account")
    print("-------------------------------------------------------------\n")
    username2 = input("Please enter your Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username2,))
        money = mydbse.fetchone()[0]
        print("Username : "+username2)
        print("Account Balance : RM {:.2f}".format(money))
        adminside(username)

    except :
        print("Failed to Find User ")
        adminside(username)

def updateuser(username):
    print("\n-------------------------------------------------------------")
    print("                     Update User Account")
    print("-------------------------------------------------------------\n")
    username1 = input("Please enter Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        
        mydbse.execute("SELECT money FROM user WHERE username=%s", (username1,))
        money = mydbse.fetchone()[0]
        
        print("Username:", username1)
        print("Account Balance: RM {:.2f}".format(money))
        
        askuser = input("Do you want to update the "+username1+" account? [Y or N]: ").upper()

        if askuser == "Y":
            print("-------------------------------------------------------------")
            print("Updating "+username1+" account...")
            print("-------------------------------------------------------------")
            print("Username : "+username1)
            passwrd = input("Please enter Password : ")
            passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
            money2 = float(input("Please Enter Your Amount: RM "))
            print("-------------------------------------------------------------")
            if money2 < 10:
                print("Please Enter Amount Bigger than RM 10")
            else :
                mydbse.execute("UPDATE user SET password=%s , money=%s WHERE username=%s",
                    (passwrd, money2, username1))
                projectdatabase.commit()

                mydbse.execute("INSERT INTO history"
                    "(username, detail, money)"
                    "VALUES(%s, %s, %s)",
                    (username1, "Account Update From Admin", "-RM {:.2f}".format(money)))
                projectdatabase.commit()

                mydbse.execute("INSERT INTO history"
                    "(username, detail, money)"
                    "VALUES(%s, %s, %s)",
                    (username1, "Account Update From Admin", "+RM {:.2f}".format(money2)))
                projectdatabase.commit()

                print("Updating "+username1+" account Sucsessfull")
                adminside(username)
        elif askuser == "N":
            print("Updating Canceled")
            adminside(username)
        else:
            print("You need to enter either Y or N !!!")
            adminside(username)

    except :
        print("User notfound")
        adminside(username)

def updateadmin(username):
    print("\n-------------------------------------------------------------")
    print("                     Update Admin Account")
    print("-------------------------------------------------------------\n")
    username1 = input("Please enter Username: ")
    print("\n-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()

        mydbse.execute("SELECT * FROM admin WHERE username=%s", (username1,))
        admin_data = mydbse.fetchone()

        if admin_data:
            print("Username:", username1)

            askuser = input(f"Do you want to update the {username1} account? [Y or N]: ").upper()

            if askuser == "Y":
                print("-------------------------------------------------------------")
                print("Updating", username1, "account...")
                print("-------------------------------------------------------------")
                print("Username : "+username1)
                passwrd = input("Please enter Password: ")
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                print("-------------------------------------------------------------")
                mydbse.execute("UPDATE admin SET password=%s WHERE username=%s",
                               (passwrd, username1))
                projectdatabase.commit()
                print("Updating", username1, "account Successful")
                adminside(username)
            elif askuser == "N":
                print("Updating Canceled")
                adminside(username)
            else:
                print("You need to enter either Y or N !!!")
                adminside(username)
        else:
            print("User not found")
            adminside(username)

    except mysql.connector.Error as err:
        print("Error:", err)
        adminside(username)

def adminchangepassword(username):
    print("\n-------------------------------------------------------------")
    print("                    Admin Change Password")
    print("-------------------------------------------------------------\n")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM admin WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your New Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("UPDATE admin SET password=%s WHERE username=%s",
                    (passwrd, username))
                projectdatabase.commit()
                print(username + ", Your Password have been changed.")
                adminside(username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same.")
                adminchangepassword(username)
        else:
            print("Your account is not in the database, please register first")
            adminrgister()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def deleteuser(username):
    print("\n-------------------------------------------------------------")
    print("                     Delete Account")
    print("-------------------------------------------------------------\n")
    category = input("Delete From User or Admin : ").lower()
    print("\n-------------------------------------------------------------\n")
    if category == "user" or category == "admin":
        username1 = input("Please enter Username: ")
        print("\n-------------------------------------------------------------")
        try:
            projectdatabase = database()
            mydbse = projectdatabase.cursor()

            if category == "user":
                mydbse.execute("SELECT * FROM user WHERE username=%s", (username1,))
            elif category == "admin":
                mydbse.execute("SELECT * FROM admin WHERE username=%s", (username1,))
            else:
                print("Invalid category. Please select either 'user' or 'admin'.")

            admin_data = mydbse.fetchone()

            if admin_data:
                print("Username:", username1)

                askuser = input(f"Do you want to Delete the {username1} account? [Y or N]: ").upper()

                if askuser == "Y":
                    print("-------------------------------------------------------------")
                    print("Deleting", username1, "account...")
                    print("-------------------------------------------------------------")
                    
                    if category == "user":
                        mydbse.execute("DELETE FROM user WHERE username=%s", (username1,))
                    elif category == "admin":
                        mydbse.execute("DELETE FROM admin WHERE username=%s", (username1,))
                    
                    projectdatabase.commit()
                    print("Deleting", username1, "account Successful")
                    adminside(username)

                elif askuser == "N":
                    print("Deletion Canceled")
                    adminside(username)
                else:
                    print("You need to enter either Y or N !!!")
                    adminside(username)
            else:
                print(f"{category.capitalize()} not found")
                adminside(username)

        except mysql.connector.Error as err:
            print("Error:", err)
            adminside(username)
    else:
        print("You need to enter either User Or Admin !!!!! ")
        deleteuser(username)

def checkmoneyinbank(username):
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user")
        money_records = mydbse.fetchall()
        money = sum(record[0] for record in money_records)
        print("Total Balance Account In All Account: RM {:.2f}".format(money))
        adminside(username)
    except mysql.connector.Error as err:
        print("Failed to count Money: {}".format(err))

def adminside(username):
    print("\n-------------------------------------------------------------")
    print("                  Admin Username: "+username                  )
    print("-------------------------------------------------------------\n")
    for row in adminsitab:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")

    try:
        userchoice = int(input("Please Choose [ 1 or 2 or 3 or 4 or 5 or 6 or 7 ]: "))
        print()
        if userchoice == 1 :
            checkuser(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice== 2:
            updateuser(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice== 3:
            updateadmin(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice== 4:
            adminchangepassword(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice== 5:
            deleteuser(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice== 6:
            checkmoneyinbank(username)
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        elif userchoice == 7 :
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
            admin()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 or 7 !!!")
            print("\n-------------------------------------------------------------\n")
            adminside(username)
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 or 4 or 5 or 6 or 7 !!!")
        print("\n-------------------------------------------------------------\n")
        adminside(username)

def adminlogin(count):
    print("\n-------------------------------------------------------------")
    print("                         Admin Log In")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM admin WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your Password: ")
            if bcrypt.checkpw(passwrd.encode('utf-8'), user_data[1].encode('utf-8')):
                print("Welcome back, " + username + ".")
                adminside(username)
            else:
                if count == 1:
                    print("Your password is wrong. Sorry You have reached the Maximum Limit which is 3 times. Please Try Again")
                    print("\n-------------------------------------------------------------")
                    choose()
                else:
                    count -= 1
                    print("Your password is wrong. Please try again. You only have " + str(count) + " chances left")
                    adminlogin(count)
        else:
            print("Your account is not in the database, please register first")
            askuser=input("Do you want To Login ? [ Y to continue or any key to register ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                adminlogin(count)
            else :
                adminrgister()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def adminrgister():
    print("\n-------------------------------------------------------------")
    print("                       Admin Register")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM admin WHERE username=%s",
                       (username,))
        sameinpt = mydbse.fetchone()

        if sameinpt:
            print("Your Account is Already Registered. Please Log In.")
            askuser=input("Do you want To Register Other Account ? [ Y to continue or any key to login ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                adminrgister()
            else :
                adminlogin(count)
        else:
            passwrd = input("Please enter your Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("INSERT INTO admin"
                               "(username, password)"
                               "VALUES(%s, %s)",
                               (username, passwrd))
                projectdatabase.commit()
                print("Hey " + username + ", Your Account is registered.")
                adminside(username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same. please register again")
                adminrgister()

    except mysql.connector.Error as err:
        print("Failed to Insert data: {}".format(err))

def adminforgot():
    print("\n-------------------------------------------------------------")
    print("                    Admin Forgot Password")
    print("-------------------------------------------------------------\n")
    username = input("Please enter your Username: ")

    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT * FROM admin WHERE username=%s",
                       (username,))
        user_data = mydbse.fetchone()

        if user_data:
            passwrd = input("Please enter your New Password: ")
            cpasswrd = input("Please confirm your New Password: ")

            if passwrd == cpasswrd : 
                passwrd = bcrypt.hashpw(passwrd.encode('utf-8'), bcrypt.gensalt())
                mydbse.execute("UPDATE admin SET password=%s WHERE username=%s",
                    (passwrd, username))
                projectdatabase.commit()
                print("Welcome back, " + username + ".")
                adminside(username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same. please register again")
                adminforgot()
        else:
            print("Your account is not in the database, please register first")
            askuser=input("Do you want To bank ? [ Y to back or any key to continue ] : ")
            askuser=askuser.upper()
            if askuser == "Y":
                print()
                admin()
            else :
                adminforgot()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def admin():
    print("-------------------------------------------------------------")
    for row in tableadmin:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")

    try:
        userchoice = int(input("Please Choose [ 1 or 2 or 3 or 4]: "))
        print()
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                adminlogin(count)
            elif userchoice == 2:
                adminrgister()
        elif userchoice== 3:
                adminforgot()
        elif userchoice== 4:
            print("-------------------------------------------------------------")
            choose()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
            print("\n-------------------------------------------------------------\n")
            admin()
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
        print("\n-------------------------------------------------------------\n")
        admin()

def choose():
    for row in table:
        for col in row:
            print(col, end="\t")
        print()
    print("-------------------------------------------------------------")
    
    try:
        userchoice = int(input("Please Choose [1 or 2 or 3 or 4]: "))
        print()
        if userchoice == 1 or userchoice == 2:
            if userchoice == 1:
                login(count)
            elif userchoice == 2:
                register()
        elif userchoice== 3:
            forgotpass()
        elif userchoice== 4:
            admin()
        else:
            print("\n-------------------------------------------------------------\n")
            print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
            print("\n-------------------------------------------------------------\n")
    except ValueError:
        print("\n-------------------------------------------------------------\n")
        print("     You just need to fill either 1 or 2 or 3 or 4 !!!")
        print("\n-------------------------------------------------------------\n")

def withdraw(username):
    try:
        projectdatabase = database()
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

                    mydbse.execute("INSERT INTO history"
                        "(username, detail, money)"
                        "VALUES(%s, %s, %s)",
                        (username, "Money Withdraw", "-RM {:.2f}".format(userwithdraw)))
                    projectdatabase.commit()

                    print("You have withdrawn RM {:.2f} from your account".format(userwithdraw))
                    print("Your account Balance: RM {:.2f}".format(money))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def checkbalance(username):
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()
        mydbse.execute("SELECT money FROM user WHERE username=%s",
                       (username,))
        money = mydbse.fetchone()[0]
        print("Your account Balance: RM {:.2f}".format(money))
    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def bankin(username):
    try:
        projectdatabase = database()
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

            mydbse.execute("INSERT INTO history"
                "(username, detail, money)"
                "VALUES(%s, %s, %s)",
                (username, "Bank In ", "+RM {:.2f}".format(bankinmoney)))
            projectdatabase.commit()

            print("You have banked in RM {:.2f} to your account".format(bankinmoney))
            print("Your account Balance: RM {:.2f}".format(money))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def transfer(username):
    try:
        projectdatabase = database()
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

                            mydbse.execute("INSERT INTO history"
                                "(username, detail, money)"
                                "VALUES(%s, %s, %s)",
                                (username, "Transfer To "+transferusername, "-RM {:.2f}".format(usertransfer)))
                            projectdatabase.commit()

                            mydbse.execute("INSERT INTO history"
                                "(username, detail, money)"
                                "VALUES(%s, %s, %s)",
                                (transferusername, "Transfer From "+username, "+RM {:.2f}".format(usertransfer)))
                            projectdatabase.commit()

                            print("You have Transfer to "+transferusername+" RM {:.2f}".format(usertransfer))
                            print("Your account Balance: RM {:.2f}".format(money))
                else:
                    print("Username not found.")
            except mysql.connector.Error as err:
                print("Failed to update data: {}".format(err))

    except mysql.connector.Error as err:
        print("Failed to update data: {}".format(err))

def changepassword(username):
    print("\n-------------------------------------------------------------")
    print("                        Change Password")
    print("-------------------------------------------------------------\n")

    try:
        projectdatabase = database()
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
                print(username + ", Your Password have been changed.")
                choose2(money, username)
            else :
                print("Please Make Sure Your Password and confirm passwrd is same.")
                changepassword(username)
        else:
            print("Your account is not in the database, please register first")
            register()

    except mysql.connector.Error as err:
        print("Failed to log in: {}".format(err))

def history(username):
    print("\n-------------------------------------------------------------")
    print("              "+username+" Transaction History:")
    print("-------------------------------------------------------------")
    try:
        projectdatabase = database()
        mydbse = projectdatabase.cursor()

        mydbse.execute("SELECT * FROM history WHERE username=%s", (username,))
        transaction_data = mydbse.fetchall()
        
        if transaction_data:
            for transaction in transaction_data:
                detail = transaction[1]
                money = transaction[2]
                
                print(detail +" "+ money)
        else:
            print("No Transaction History")
            
    except mysql.connector.Error as err:
        print("Failed to Find User: {}".format(err))
    
    print("-------------------------------------------------------------")


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
        userchoice2 = int(input("Please Choose [1 or 2 or 3 or 4 or 5 or 6 or 7]: "))
        print()
        if userchoice2 == 1 or userchoice2 == 2 or userchoice2 == 3 or userchoice2 == 4 or userchoice2 == 5 or userchoice2 == 6 :
            if userchoice2 == 1:
                checkbalance(username)
            elif userchoice2 == 2:
                withdraw(username)
            elif userchoice2 == 3:
                bankin(username)
            elif userchoice2 == 4:
                transfer(username)
            elif userchoice2 == 5:
                history(username)
            elif userchoice2 == 6:
                changepassword(username)
            
            contotext = input("\nDo you want to continue?\nInsert Y to Continue or press Enter to Exit: ")
            contotext = contotext.upper()
            if contotext == "Y":
                choose2(money, username)
            else:
                print("\n-------------------------------------------------------------")
                print("         Thank you "+username+" For Using Our System")
                print("-------------------------------------------------------------")
                choose()
        elif userchoice2 == 7:
            print("\n-------------------------------------------------------------")
            print("         Thank you "+username+" For Using Our System")
            print("-------------------------------------------------------------")
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
print("-------------------------------------------------------------")
while True:
    choose()
