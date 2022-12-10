import argparse

import bcrypt

from database.db import session
from database.repository import get_user_by_login, add_contact, update_contact, get_contacts, remove_contact, \
    get_contact

parser = argparse.ArgumentParser(description='Personal organizer')
parser.add_argument('--action', '-a', help='Command: add, update, list, remove, get', required=True)
parser.add_argument('--login')
parser.add_argument('--id')
parser.add_argument('--name')
parser.add_argument('--phone')
parser.add_argument('--email')

args = vars(parser.parse_args())

action = args.get('action')
id = args.get('id')
login = args.get('login')
name = args.get('name')
phone = args.get('phone')
email = args.get('email')



def main():
    match action:
        case 'add':
            add_contact(name, phone, email)
        case 'update':
            person = update_contact(id)
            print(person)
        case 'list':
            contacts = get_contacts()
            if contacts:
                [print(el) for el in contacts]
            else:
                print("List is empty")
        case 'get':
            person = get_contact(id)
            print(person)
        case 'remove':
            result = remove_contact(id)
            print(f'Result: {bool(result)}')
        case '_':
            print('Unknown command')


if __name__ == '__main__':
    owner = get_user_by_login(login)
    if owner:
        password = input('Password: ')
        if bcrypt.checkpw(password.encode('utf-8'), owner.hash):
            main()
            print('Successful!')
        else:
            print('Wrong password!')
    session.close()
