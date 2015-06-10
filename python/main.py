##########################################
# Kenley Arai
# Antoine Guerrero
# Group 20
##########################################

import psycopg2
import getpass
from user import *
from helper import *

def search(db_conn):
    again = True
    while again:
        again = False
        display_menu('search')
        search_name = input('\nSearch: ')
        print("")
        cur = db_conn.cursor()

        try:
            cur.execute("SELECT NAME FROM USR WHERE NAME ILIKE '%s%%' LIMIT 10" % search_name)
        except psycopg2.DatabaseError as e:
            return True

        people = cur.fetchall()

        if len(people) > 0:
            for row in people:
                print(row[0])
            print("\n")
        else:
            print("Sorry, %s not found" % search_name)

        choice = input("\nWould you like to search again? (y/n): ")

        if str.lower(choice) == 'y':
            again = True

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

def get_msgid(db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT max(msgid) FROM MESSAGE")
    except psycopg2.DatabaseError as e:
        print(e)
        return False
    row = cur.fetchone()
    if row != None:
        return int(row[0])
    else:
        return -1

def send_message(db_conn, sender):
    receiver = input("Enter receiverid: ")
    msg = input("Enter your message: ")
    msgid = get_msgid(db_conn) + 1

    if user_exist(db_conn, receiver):
        delete_status = 0
        status = 'Sent'
    else:
        delete_status = 2
        status = 'Failed to deliver'

    cur = db_conn.cursor()

    try:
        print(sender)
        print(receiver)
        print(status)

        cur.execute("INSERT INTO MESSAGE(msgid, senderId, receiverId, contents, sendTime, deleteStatus, status) \
            VALUES('%d', '%s', '%s', '%s', '%s', '%d', '%s')" % (msgid, sender, receiver, msg, datetime.now(), delete_status, status))
    except psycopg2.DatabaseError as e:
        print(e)
        return False
    return True

def user_exist(db_conn, uid):
    cur = db_conn.cursor()

    try:
        cur.execute("SELECT userid FROM USR WHERE userId ='%s'" % uid)
    except psycopg2.DatabaseError as e:
        print(e)
        return False

    return cur.fetchone() != None

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
    if str.lower(option) == 'y':
        delete_message_sender(db_conn, uname, input("Message ID: "))
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
    if str.lower(option) == 'y':
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

def show_profile(db_conn, uname):
    if user_exist(db_conn, uname):
        cur = db_conn.cursor()
        try:
            cur.execute("SELECT * FROM USR WHERE userid='%s'" % uname)
            user_data = cur.fetchone()

            cur.execute("SELECT * FROM WORK_EXPR WHERE userid='%s'" % uname)
            work_expr = cur.fetchall()

            cur.execute("SELECT * FROM EDUCATIONAL_DETAILS WHERE userid='%s'" % uname)
            educ_details = cur.fetchall()

        except psycopg2.DatabaseError as e:
            print(e)
            return True

        print("***** Basic Information *****")
        print("Name: %s" % user_data[3])
        print("Email: %s" % user_data[2])
        print("DOB: %s" % user_data[4])

        print("***** Work Experience *****")
        if work_expr != None:
            for row in work_expr:
                print("Company: %s" % row[1])
                print("Role: %s" %row[2])
                print("Location: %s" % row[3])
                print("Startdate: %s" % row[4])
                print("Enddate: %s\n" % row[5])
        else:
            print ("N/A")

        print("\nEducation: \n")
        if educ_details!= None:
            for row in educ_details:
                print("Name: %s" % row[1])
                print("Major: %s" % row[2])
                print("Degree: %s" % row[3])
                print("Startdate: %s" % row[4])
                print("Enddate: %s" % row[5])
        else:
            print ("N/A")

        return show_friends(db_conn, uname, True)


def show_friends(db_conn, uname, from_profile_print):
    print("\n****** Friends ******")

    cur = db_conn.cursor()
    try:
        cur.execute("SELECT connectionid FROM CONNECTION_USR WHERE userid='%s' AND status != 'Reject' AND STATUS != 'Request'" % uname)
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    friends = cur.fetchall()
    if len(friends) > 0:
        for row in friends:
            for item in row:
                print(item)
    if not from_profile_print and len(friends) > 0:
        print()
        print("****** Friend Options ******")
        print()
        again = True
        while again:
            again = False
            print()
            option = input("Would you like to view a profile or send a message? (y/n): ")
            if str.lower(option) == 'y':
                print()
                print("1. View profile")
                print("2. Send message")
                option = input('Select option: ')
                if option == '1':
                    again = True
                    option = input('Select userid from above: ')
                    show_profile(db_conn, option)
                elif option == '2':
                    again = True
                    send_message(db_conn, uname)
    else:
        print("\nSorry, no friends :(")

    return True

def get_friend_list(db_conn, uname):
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT connectionid FROM CONNECTION_USR WHERE userid='%s' AND status != 'Reject' AND STATUS != 'Request'" % uname)
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    friend_list = cur.fetchall()

    if friend_list is None:
        return set()
    else:
        friend_set = set()
        for f in friend_list:
            friend_set.add(f[0])
        return friend_set

def request_friend(db_conn, uname):
    print("\n*************************************************")
    print("*\t\tSend Friend Request\t\t*")
    print("*************************************************\n")

    friend_opts = set()
    new_friend = input("Send request to: ")

    # This is a set
    friend_lvl0 = get_friend_list(db_conn, uname)

    # First level friends of friends
    if len(friend_lvl0) > 0:
        friend_lvl1 = set()
        friend_lvl2 = set()
        friend_lvl3 = set()

        #  level 1 friends
        for f in friend_lvl0:
            friend_lvl1 = friend_lvl1 | get_friend_list(db_conn, f)
        friend_opts = friend_opts | friend_lvl1

        # level 2 friends
        for f in friend_lvl1:
            if f not in friend_opts:
                friend_lvl2 = friend_lvl2 | get_friend_list(db_conn, f)
        friend_opts = friend_opts | friend_lvl2

        # level 3 friends
        for f in friend_lvl2:
            if f not in friend_opts:
                friend_lvl3 = friend_lvl3 | get_friend_list(db_conn, f)
        friend_opts = friend_opts | friend_lvl3

    if new_friend in friend_opts:
        cur = db_conn.cursor()
        try:
            cur.execute("INSERT INTO CONNECTION_USR VALUES ('%s', '%s', 'Request')" % (uname, new_friend))
            cur.commit()
        except psycopg2.DatabaseError as e:
            print(e)
            return True
        print("Friend request sent to %s." % new_friend)
    else:
        print()
        print("Friend request failed")

def accept_request(db_conn, receiver, sender):
    cur = db_conn.cursor()
    try:
        cur.execute("UPDATE CONNECTION_USR SET status='Accept' WHERE userid='%s' AND connectionid='%s'" % (sender, receiver))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        return False

def reject_request(db_conn, receiver, sender):
    cur = db_conn.cursor()
    try:
        cur.execute("UPDATE CONNECTION_USR SET status='Reject' WHERE userid='%s' AND connectionid='%s'" % (sender, receiver))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        return False

def process_requests(db_conn, uname):
    choice = input("\nWould you like to accept/deny any requests? (y/n): ")

    if str.lower(choice) == 'y':
        print("1. Accept")
        print("2. Reject")
        print("3. Cancel")
        choice = input("Select option: ")

        while not valid_option(choice, '123'):
            choice = input("Select option: ")

        if choice == '1':
            sender = input("Request to accept: ")
            accept_request(db_conn, uname, sender)
        elif choice == '2':
            sender = input("Request to reject: ")
            reject_request(db_conn, uname, sender)
        else:
            pass

def view_friend_requests(db_conn, uname):
    display_menu('view_requests')
    cur = db_conn.cursor()
    try:
        cur.execute("SELECT * FROM CONNECTION_USR  WHERE connectionid='%s' AND status='Request'" % (uname))
    except psycopg2.DatabaseError as e:
        print(e)
        return True

    requests = cur.fetchall()
    for request in requests:
        print("From: '%s'" % request[0])

    if len(requests) > 0:
        process_requests(db_conn, uname)

    return True

def messaging_menu():
    print()
    print('1. View Sent')
    print('2. View Received')
    print('3. View drafts')
    print('4. Send Message')

def option_handler(option, db_conn, uname):

    if option == '1':
        messaging_menu()
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
            return send_message(db_conn, uname.username)

    elif option == '2':
        return search(db_conn)
    elif option == '3':
        display_menu('change')
        #username = input('Username: ')
        password = getpass.getpass()
        reauth_success = login(uname.username, password, db_conn)
        if reauth_success:
            print("\nEnter new password")
            new_password = getpass.getpass()
            print("\nEnter new password again")
            new_password2 = getpass.getpass()
            while not pass_check(new_password, new_password2):
                print("\nPasswords do not match")
                print("\nEnter new password")
                new_password = getpass.getpass()
                print("\nEnter new password again")
                new_password2 = getpass.getpass()
            return change_password(uname.username, new_password, db_conn)
        else:
            print("\nReauthentication failed!")
            return True
    elif option == '4':
        return show_friends(db_conn, uname.username, False)
    elif option == '5':
        request_friend(db_conn, uname.username)
        return True
    elif option == '6':
        return view_friend_requests(db_conn, uname.username)
    elif option == '7':
        uname.username = ""
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
        print("\nPassword change successful!")
    except psycopg2.DatabaseError as e:
        return False

    return True


def register(username, password, email, name, dob, db_conn):
    cur = db_conn.cursor()
    try:
        cur.execute("INSERT INTO USR VALUES ('%s', '%s', '%s', '%s', '%s')" % (username, password, email, name, dob))
        db_conn.commit()
    except psycopg2.DatabaseError as e:
        print('Error user already exists')
        return False
    return False

def display_menu(prompt_type):
    if prompt_type == 'registration':
        print("\n*************************************************")
        print("*\t\tUser Registration\t\t*")
        print("*************************************************\n")
    elif prompt_type == 'login':
            print("\n*****************************************")
            print("*\t\tLogin Menu\t\t*")
            print("*****************************************\n")
            print('1. Login')
            print('2. Register')
            print('3. Exit')
    elif prompt_type == 'change':
        print("\n*****************************************")
        print("*\t\tChange Password\t\t*")
        print("*****************************************\n")
        print('\nPlease reauthenticate')
    elif prompt_type == 'view_requests':
        print("\n*************************************************")
        print("*\t\tPending requests\t\t*")
        print("*************************************************\n")

def login_handler(option, db_conn, uname):
    if option == "1":
        print()
        username = input('Username: ')
        password = getpass.getpass()
        if login(username, password, db_conn):
            uname.username = username
            return True
        else:
            print('\nIncorrect username or password\n')

    elif option == "2":
        display_menu('registration')
        username  = input('Username: ')
        password = getpass.getpass()
        password2 = getpass.getpass()

        while not pass_check(password, password2):
            print("Passwords do not match")
            password = getpass.getpass()
            password2 = getpass.getpass()

        email = input('Email: ')
        name = input('Full Name: ')

        while not name_space_check(name):
            print("Please input your full name with spaces")
            name = input('Full Name')
        dob = input("Date of birth (yyyy/mm/dd): ")

        while not date_format_check(dob):
            dob = input('Date of birth (yyyy/mm/dd): ')
        return register(username, password, email, name, dob, db_conn)
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
            display_menu('login')
            option = input('Please choose an option: ')

            if option == "3":
                exit = True
            elif valid_option(option, "12"):
                logged_in = login_handler(option, db_conn, username)

        elif logged_in:
            print("\n*******************************************")
            print("*\t\tAction Menu\t\t*")
            print("*******************************************\n")
            print('1. Messaging Options')
            print('2. Search for people')
            print('3. Change password')
            print('4. Show friends')
            print('5. Send Friend Request')
            print('6. View Friend Requests')
            print('7. Logout')
            print('8. Exit')
            option = input('Please choose an option: ')

            if option == '8':
                exit = True
            elif valid_option(option, "1234567"):
                logged_in = option_handler(option, db_conn, username)

if __name__ == "__main__":
    main()
