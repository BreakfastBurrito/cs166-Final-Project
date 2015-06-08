import psycopg2
from user import *
from helper import *

def search(db_conn):
    search_name = input('\nSearch: ')
    print("")
    cur = db_conn.cursor()

    try:
        cur.execute("SELECT NAME FROM USR WHERE NAME LIKE '%s%%' LIMIT 10" % search_name)
    except psycopg2.DatabaseError as e:
        return True

    for row in cur.fetchall():
        print(row[0])
    print("\n")
    return True

def print_message(mesg):
    print("Message ID: %s" % mesg[0])
    print("Sender: %s" % mesg[1])
    print("Receiver: %s" % mesg[2])
    print("Timestamp: %s" % mesg[4])
    print("Status: %s" % mesg[6])
    print("Contents:")
    print(mesg[3])
    print("\n")

def send_message(db_conn, sender):
    receiver = input("Enter receiverid: ")
    msg = input("Enter your message: ")

    if user_exist(receiver):
        print('yay')
        #cur = db_conn.cursor()
        #cur.execute("INSERT INTO MESSAGE(senderId, receiverId, contents, sendTime, deleteStatus, status)
            #VALUES('%s', '%s', '%s', '%s', '%d', '%s')" % (sender, receiver, datetime.now(), msg, 0, 0))
    #

def user_exist(db_conn, uid):
    cur = db_conn.cursor()

    try:
        cur.execute("SELECT userid FROM USR WHERE NAME ='%s'" % uid)
    except psycopg2.DatabaseError as e:
        return False

    print(cur.fetchone()[0] == uid)
    return cur.fetchone()[0] == uid


def get_sent_messages(db_conn, uname):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM MESSAGE WHERE senderid='%s' AND status != 'Draft'" % uname.username)
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    for row in cur.fetchall():
        if str(row[5]) in "02":
            print_message(row)
    option = input("Delete any messages? y/n")
    if option == 'y':
        delete_message_sender(input("Message ID: "))
    return True

def get_received_messages(db_conn, uname):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM MESSAGE WHERE receiverid='%s' AND status !='Draft' AND status != 'Failed to Deliver'" % uname.username)
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    for row in cur.fetchall():
        if str(row[5]) in "01":
            print_message(row)

    option = input("Delete any messages? y/n: ")
    if option == 'y':
        delete_message_rec(db_conn, uname, input("Message ID: "))
    return True

def get_drafts(db_conn, uname):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM MESSAGE WHERE senderid='%s' AND status = 'Draft'" % uname.username)
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    for row in cur.fetchall():
        if str(row[5]) in "02":
            print_message(row)
    return True

def delete_message_sender(db_conn, uname, mid):

    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM MESSAGE WHERE msgid='%s'" % mid)
        row = cur.fetchone()
        new_delete_status = int(row[5]) | 1
        cur.execute("UPDATE MESSAGE SET deletestatus = '%s' WHERE senderid='%s' AND msgid=%s" % (new_delete_status, uname.username, mid))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        return True

def delete_message_rec(db_conn, uname, mid):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM MESSAGE WHERE msgid='%s'" % mid)
        row = cur.fetchone()
        new_delete_status = int(row[5]) | 2
        cur.execute("UPDATE MESSAGE SET deletestatus = '%s' WHERE receiverid='%s' AND msgid=%s" % (new_delete_status, uname.username, mid))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        return True


def option_handler(option, db_conn, uname):
    # Change password

    if option == '1':
        print('1. View Sent')
        print('2. View Received')
        print('3. View drafts')
        print('4. Send Message')
        mesg_type = input('Select option: ')
        print('\n')
        while not valid_option(mesg_type, "1234"):
            mesg_type = input('Select option: ')
            print('\n')
        if mesg_type == '1':
            return get_sent_messages(db_conn, uname)
        elif mesg_type == '2':
            return get_received_messages(db_conn, uname)
        elif mesg_type == '3':
            return get_drafts(db_conn, uname)
        elif mesg_type == '4':
            return send_message(db_conn, uname)


    elif option == '3':
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
    return False

def login_handler(option, db_conn, uname):
    if option == "1":
        username = input('Username: ')
        password = input('Password: ')
        if login(username, password, db_conn):
            uname.username = username
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
    username = User()

    while not exit:
        if not logged_in:
            print('1. Login')
            print('2. Register')
            print('3. Exit')
            option = input('Please choose an option: ')

            if option == "3":
                exit = True
            elif valid_option(option, "12"):
                logged_in = login_handler(option, db_conn, username)

        elif logged_in:
            print('1. Show Messages')
            print('3. Search for people')
            print('4. Change password')
            print('8. Logout')
            print('9. Exit')
            option = input('Please choose an option: ')

            if option == '9':
                exit = True
            elif valid_option(option, "1348"):
                logged_in = option_handler(option, db_conn, username)

if __name__ == "__main__":
    main()
