import psycopg2
def option_handler(option):
    if option == '1':
        return True

def login(username, password, db_conn):
    cur = db_conn.cursor()
    cur.execute("SELECT USER_ID, PASSWORD FROM USR WHERE password=%s AND USER_ID=%s" % username, password)
    rows = cur.fetchall()
    print(rows[0])
    return True
    

def login_handler(option, db_conn):
    if option == "1":
        login    = input('Username: ')
        password = input('Password: ')
        return login(username, password, db_conn)
    elif option == "2":
        print('register')
    return False

def prompt_handler(logged_in, db_conn):
    if not logged_in:
        print('1. Login')
        print('2. Register')
        option = input('Please choose an option: ')
        return login_handler(option, db_conn)
    elif logged_in: 
        print('1. Exit')
        option = input('Please choose an option: ')
        return option_handler(option)


def main():
    # Initialize Db
    try:
    db_conn = psycopg2.connect(
                               host     = ""
                               user     = ""
                               database = ""
                               password = ""
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
