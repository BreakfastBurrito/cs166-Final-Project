import psycopg2

def option_handler(option):
    if option == "1":
        return True

def main():
    exit = False
    while exit != True:
        print("1. Exit")
        option = input("Please choose an option: ")

        exit = option_handler(option)  

if __name__ == "__main__":
    main()
