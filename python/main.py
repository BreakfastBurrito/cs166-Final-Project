from datetime import datetime
import psycopg2


def valid_option(option, options):
    if option in options:
        return True
    print('\nInvalid option\n')
    return False

def option_handler(option):
    if option == '8':
        return False, False 
    elif option == '9':
        return True, True

def login(username, password, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT USERID, PASSWORD FROM USR WHERE USERID='%s' AND PASSWORD='%s'" % (username, password))
    except psycopg2.DatabaseError as e:
        return False
    row = cur.fetchone()
    return row == (username, password) 

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


def register(username, password, name, dob, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("INSERT INTO USR VALUES ('%s', '%s', '%s', '%s')" % (username, password, name, dob))
    except psycopg2.DatabaseError as e:
        print('Error user already exists')
        return False
    return True

def login_handler(option, db_conn):
    if option == "1":
        username = input('Username: ')
        password = input('Password: ')
        if login(username, password, db_conn):
            return True, False
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
        return register(username, password, name, dob, db_conn), False

    elif option == "3":
        return False, True
    return False, False


def main():
    # Initialize Db
    try:
        db_conn = psycopg2.connect(
                               host     = 'breakfastburrito.io',
                               user     = 'db',
                               database = 'db',
                               password = '',
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

            if valid_option(option, "123"):
                logged_in, exit = login_handler(option, db_conn)
            
        elif logged_in:
            print('8. Logout')
            print('9. Exit')
            option = input('Please choose an option: ')

            if valid_option(option, "89"):
                exit, logged_in = option_handler(option)


if __name__ == "__main__":
    main()
