from datetime import datetime
import psycopg2

def pass_check(pass1,pass2):
    return pass1 == pass2

def name_space_check(name):
    return " " in name

def date_format_check(d):
    try:
        return datetime.strptime(d, '%Y/%m/%d')
    except ValueError:
        print("Incorrect dateformat: ")
        return False


def valid_option(option, options):
    if option in options:
        return True
    print('\nInvalid option\n')
    return False

def search(db_conn):
    search_name = input('\nSearch: ')
    print("")
    cur = db_conn.cursor()

    try:
        cur.execute("SELECT NAME FROM USR WHERE NAME LIKE '%s%%' LIMIT 10" % search_name)
    except psycopg2.DatabaseError as e:
        return True, False
    
    for row in cur.fetchall():
        print(row[0])
    print("\n")
    return True, False
    

def option_handler(option, db_conn):
    # Change password
    if option == '3':
        return search(db_conn) 
    elif option == '4':
        print('\nPlease reauthenticate')
        username = input('Username: ')
        password = input('Password: ')
        reauth_success = login(username, password, db_conn)
        if reauth_success:
            new_password = input('New Password: ')
            new_password2 = input('Renter new password: ')
            while not pass_check(new_password, new_password2):
                print("Passwords do not match")
                new_password = input('New Password: ')
                new_password2 = input('Renter new password: ')
            return change_password(username, new_password, db_conn)
        else:
            return False
    elif option == '8':
        return False

def login(username, password, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT USERID, PASSWORD FROM USR WHERE USERID='%s' AND PASSWORD='%s'" % (username, password))
    except psycopg2.DatabaseError as e:
        return False
    row = cur.fetchone()
    return row == (username, password)

def change_password(username, password, db_conn):
    success = False

    cur = db_conn.cursor()
    try:
        cur.execute("UPDATE USR SET password='%s' WHERE USERID='%s'" % (password, username))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        return False

    return True


def register(username, password, name, dob, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("INSERT INTO USR VALUES ('%s', '%s', '%s', '%s', '%s')" % (username, password, email, name, dob))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print('Error user already exists')
        return False
    return True

def login_handler(option, db_conn):
    if option == "1":
        username = input('Username: ')
        password = input('Password: ')
        if login(username, password, db_conn):
            return True
        else:
            print('\nIncorrect username or password\n')

    elif option == "2":
        username  = input('Username: ')
        password  = input('Password: ')
        password2 = input('Renter Password: ')

        while not pass_check(password, password2):
            print("Passwords do not match")
            password = input('Password: ')
            password2 = input('Renter Password: ')

        email = input('Email: ')
        name = input('Full Name: ')

        while not name_space_check(name):
            print("Please input your full name with spaces")
            name = input('Full Name')
        dob = input("Date of birth (yyyy/mm/dd): ")

        while not date_format_check(dob):
            dob = input('Date of birth (yyyy/mm/dd): ')
        return register(username, password, name, dob, db_conn) 

    return False


def main():
    # Initialize Db
    try:
        db_conn = psycopg2.connect(
                               host     = 'breakfastburrito.io',
                               user     = 'db',
                               database = 'db',
                               password = 'userdbabc',
                               )
    except psycopg2.DatabaseError as e:
        raise e
        sys.exit(1)
    exit      = False
    logged_in = False

    while not exit:
        if not logged_in:
            print('1. Login')
            print('2. Register')
            print('3. Exit')
            option = input('Please choose an option: ')

            if option == "3":
                exit = True
            elif valid_option(option, "12"):
                logged_in = login_handler(option, db_conn)

        elif logged_in:
            print('3. Search for people')
            print('4. Change password')
            print('8. Logout')
            print('9. Exit')
            option = input('Please choose an option: ')

            if option == '9':
                exit = True
            elif valid_option(option, "348"):
                logged_in = option_handler(option, db_conn)

if __name__ == "__main__":
    main()
