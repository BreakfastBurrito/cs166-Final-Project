##########################################
# Kenley Arai
# Antoine Guerrero
# Group 20
##########################################

from datetime import datetime

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
