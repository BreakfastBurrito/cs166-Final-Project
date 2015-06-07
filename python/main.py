import psycopg2

def valid_option(option, options):
    if option in options:
        return True
    print('\nInvalid option\n')
    return False

def option_handler(option):
    if option == '1':
        return True

def login(username, password, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT USERID, PASSWORD FROM USR WHERE USERID='%s' AND PASSWORD='%s'" % (username, password))
    except psycopg2.DatabaseError as e:
        print('\nIncorrect username or password\n')
        return False
    rows = cur.fetchall()
    print(rows[0] == (username,password))
    return rows[0] == (username, password) 

    

def login_handler(option, db_conn):
    if option == "1":
        username = input('Username: ')
        password = input('Password: ')
        return login(username, password, db_conn), False
    elif option == "2":
        print('register')
    elif option == "3":
        return False, True
    return False, False


def main():
    # Initialize Db
    try:
        db_conn = psycopg2.connect(
                               host     = '',
                               user     = '',
                               database = '',
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
            print('1. Exit')
            option = input('Please choose an option: ')

            if valid_option(option, "1"):
                exit = option_handler(option)


if __name__ == "__main__":
    main()
