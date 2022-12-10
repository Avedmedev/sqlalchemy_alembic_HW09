from datetime import datetime

from database.db import session
from database import models


def get_user_by_login(login):
    return session.query(models.Owner).filter(models.Owner.login == login).first()


def add_contact(name, phone, email):
    first_name, last_name = name.split()
    contact = models.Person(first_name=first_name, last_name=last_name,
                            phones=[models.Phone(phone_number=phone)],
                            emails=[models.Email(email=email)])
    session.add(contact)
    session.commit()


def add_person_phone(id):
    phone_number = input("New phone number: ")
    description = input("Description: ")
    phone = models.Phone(phone_number=phone_number, description=description, person_id=id)
    session.add(phone)
    session.commit()


def add_person_email(id):
    email = input("New email: ")
    description = input("Description: ")
    em = models.Email(email=email, description=description, person_id=id)
    session.add(em)
    session.commit()


def remove_phone_number(id):
    phone = session.query(models.Phone).filter(models.Phone.id == id).first()
    session.delete(phone)
    session.commit()


def remove_email(id):
    email = session.query(models.Email).filter(models.Email.id == id).first()
    session.delete(email)
    session.commit()


def update_contact(id):
    person = session.query(models.Person).filter(models.Person.id == id).first()

    fn = input(f'first_name [{person.first_name}]:')
    if fn:
        person.first_name = fn

    ln = input(f'last_name [{person.last_name}]:')
    if ln:
        person.last_name = ln

    for phone in person.phones:
        ph = input(f'phone_number [{phone.phone_number}/del]:')
        if ph == 'del':
            remove_phone_number(phone.id)
            continue
        if ph:
            phone.phone_number = ph
        desc = input(f'phone description [{phone.description}]:')
        if desc:
            phone.description = desc

    while True:
        if input("add phone number [y/n]") == 'y':
            add_person_phone(id)
        else:
            break

    for email in person.emails:
        em = input(f'email [{email.email}/del]:')
        if em == 'del':
            remove_email(email.id)
            continue
        if em:
            email.email = em
        desc = input(f'email description [{email.description}]:')
        if desc:
            email.description = desc

    while True:
        if input("add email [y/n]") == 'y':
            add_person_email(id)
        else:
            break

    bd = input(f'Birth date [{person.birth_date}]:')
    if bd:
        person.birth_date = datetime.strptime(bd, "%d.%m.%y")

    pn = input(f'post [{person.post_name}]:')
    if pn:
        person.post_name = pn

    co = input(f'Company name [{person.work_place}]:')
    if co:
        person.work_place = co

    session.commit()
    return (person.id, person.fullname,
             [(ph.phone_number, ph.description) for ph in person.phones],
             [(em.email, em.description) for em in person.emails],
             person.description)


def get_contact(id):
    person = session.query(models.Person).filter(models.Person.id == id).first()
    return (person.id, person.fullname,
             [(ph.phone_number, ph.description) for ph in person.phones],
             [(em.email, em.description) for em in person.emails],
             person.description)


def get_contacts():
    contacts = session.query(models.Person).all()

    return [(el.id, el.fullname,
             [(ph.phone_number, ph.description) for ph in el.phones],
             [(em.email, em.description) for em in el.emails],
             el.description)
            for el in contacts]


def remove_contact(id):
    contact = session.query(models.Person).filter(models.Person.id == id).first()
    session.delete(contact)
    session.commit()
    return True
