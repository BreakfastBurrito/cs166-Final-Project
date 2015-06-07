import psycopg2
def option_handler(option):
    if option == '1':
        return True

def login(username, password, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT USER_ID, PASSWORD FROM USR WHERE password=%s AND USER_ID=%s" % (username, password))
    except psycopg2.DatabaseError as e:
        print('Incorrect username or password\n')
        return False
    rows = cur.fetchall()
    print(rows[0])
    return True
    

def login_handler(option, db_conn):
    if option == "1":
        username = input('Username: ')
        password = input('Password: ')
        return login(username, password, db_conn)
    elif option == "2":
        print('register')
    return False

def prompt_handler(logged_in, db_conn):
    if not logged_in:
        print('1. Login')
        print('2. Register')
        print('3. Exit')
        option = input('Please choose an option: ')
        
        if option not in "123":
            print("\nIncorrect option\n")

        if option == '3':
            return True
        logged_in = login_handler(option, db_conn)
    elif logged_in: 
        print('1. Exit')

        if option not in "123":
            print("\nIncorrect option\n")

        option = input('Please choose an option: ')
        return option_handler(option)


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
        exit = prompt_handler(logged_in, db_conn)

if __name__ == "__main__":
    main()
