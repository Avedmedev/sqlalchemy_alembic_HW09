import bcrypt

from database import models
from database.db import session


def main(login, password):
    owner = models.Owner(login=login, hash=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=10)))
    session.add(owner)
    session.commit()


if __name__ == '__main__':
    login = input('Login: ')
    password = input('Password: ')
    main(login, password)
