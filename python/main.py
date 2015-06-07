import psycopg2

def option_handler(option):
    if option == '1':
        return True

def login_handler(option):
    if option == "1":
        print('login')
    elif option == "2":
        print('register')
    return False

def prompt_handler(logged_in):
    if not logged_in:
        print('1. Login')
        print('2. Register')
        option = input('Please choose an option: ')
        return login_handler(option)
    elif logged_in: 
        print('1. Exit')
        option = input('Please choose an option: ')
        return option_handler(option)


def main():
    exit      = False
    logged_in = False

    while not exit:
        exit = prompt_handler(logged_in)

if __name__ == "__main__":
    main()
