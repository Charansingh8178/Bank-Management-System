import mysql.connector as sql
# Establishing the connection to the database
conn = sql.connect(host='localhost', user='root', passwd='charansingh', database='bank')
c1 = conn.cursor()

if conn.is_connected():
    print("Connection is successful")
else:
    print("ERROR IN CONNECTING DATABASE")

def new_user():
    a = """
    Welcome to the bank!
    Thanks for choosing us.
    For Opening New Account we would need a few details kindly fill them.
    """
    print(a)
    name = input("Enter Your Name:-> ")
    contact = int(input("Enter Your Contact Number:-> "))
    dob = input("Enter Your Birthday (YYYY-MM-DD):-> ")
    unique_id = input("Enter your identification number:-> ")
    city = input("Enter your current city:-> ")
    deposit = input("Enter The Amount To Be Deposited:-> ")
    print("YOU NEED TO SET UP A 5-DIGIT PIN ::")
    password = input("Enter Your Password:-> ")
    
    c1.execute("SELECT * FROM user WHERE unique_id = %s OR contact = %s", (unique_id, contact,))
    existing_user = c1.fetchone()
    if existing_user:
        print("An Account with this Unique_id or contact number already exists. Kindly login.")
        login()
    else:
        insertion = """INSERT INTO user(name, contact, dob, unique_id, city, deposit, password) 
                       VALUES(%s, %s, %s, %s, %s, %s, %s)"""
        c1.execute(insertion, (name, contact, dob, unique_id, city, deposit, password))
        conn.commit()
        print("New user has been added successfully!")

def after_login():
    ab = """
    1. Fetch Bank Details
    2. Transfer Money
    """
    print(ab)
    order = int(input("Enter your choice: "))
    operations(order)

def operations(order):
    if order == 1:
        fetch()
    elif order == 2:
        transfer()
    else:
        print("Invalid choice! Please try again.")
        after_login()

def fetch():
    name = input("Enter your name: ")
    unique_id = input("Enter your unique ID: ")
    ser = """SELECT name, deposit FROM user WHERE name = %s AND unique_id = %s"""
    c1.execute(ser, (name, unique_id))
    aa = c1.fetchone()
    if aa:
        print(f"Name: {aa[0]}, Deposit: {aa[1]}")
    else:
        print("No such user found.")
    after_login()

def transfer():
    from_user = input("Enter your unique ID: ")
    to_user = input("Enter recipient's unique ID: ")
    amount = int(input("Enter amount to transfer: "))
    
    # Deduct amount from from_user's account
    c1.execute("UPDATE user SET deposit = deposit - %s WHERE unique_id = %s", (amount, from_user))
    conn.commit()
    
    # Add amount to to_user's account
    c1.execute("UPDATE user SET deposit = deposit + %s WHERE unique_id = %s", (amount, to_user))
    conn.commit()
    
    print(f"Successfully transferred {amount} to {to_user}")

def login():
    print("Welcome user! Kindly enter the details to login into your existing account:")
    unique_id = input("Enter your unique ID: ")
    password = input("Enter your Password:-> ")
    c1.execute("SELECT * FROM user WHERE unique_id = %s AND password = %s", (unique_id, password))
    loginn = c1.fetchone()
    if loginn:
        print(f"Welcome {loginn[1]}")
        after_login()
    else:
        print("No such user exists.")

def choice(inputt):
    if inputt == '1':
        new_user()
    elif inputt == '2':
        login()
    else:
        print("Invalid choice! Please try again.")

def main():
    while True:
        print("\nWelcome To Bank Management System")
        print("Kindly choose the number corresponding to the operation you want to perform:")
        menu = """
        1. Open Bank Account
        2. Login
        3. Exit
        """
        print(menu)
        inputt = input("ENTER YOUR CHOICE: ")
        if inputt == '3':
            print("Exiting the system. Thank you!")
            break
        choice(inputt)

main()
2
