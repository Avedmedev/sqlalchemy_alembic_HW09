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


def update_contact(id):
    person = session.query(models.Person).filter(models.Person.id == id).first()

    fn = input(f'first_name [{person.first_name}]:')
    if fn:
        person.first_name = fn

    ln = input(f'last_name [{person.last_name}]:')
    if ln:
        person.last_name = ln

    for phone in person.phones:
        ph = input(f'phone_number [{phone.phone_number}]:')
        if ph:
            phone.phone_number = ph
        desc = input(f'phone description [{phone.description}]:')
        if desc:
            phone.description = desc

    for email in person.emails:
        em = input(f'email [{email.email}]:')
        if em:
            email.email = em
        desc = input(f'email description [{email.description}]:')
        if desc:
            email.description = desc

    bd = input(f'Birth date [{person.birth_date.strftime("%d.%m.%y") if isinstance(person.birth_date, datetime) else None }]:')
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




def get_contacts():
    contacts = session.query(models.Person).select_from(models.Person).\
        join(models.Phone).join(models.Email).group_by(models.Person.id).all()

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





