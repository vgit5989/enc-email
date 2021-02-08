import sqlite3
import os
from os import system

import aes_main
import pgp_enc


def signup_helper():
    while True:
        name = input("Please enter your name : ")
        email = input("Please enter your email without hostname(Must be unique) : ")
        email = email + "@neutronmail.com"
        while True:
            db_name = "./" + email + ".db"
            if (os.path.isfile(db_name) != True):
                break
            print("This [" + email + "] was already taken")
            email = input("Please enter a different email id: ")

        password = input("Enter password with uppercase, lowercase, numbers and symbols: ")
        system('cls')
        print("Entered Name: " + name)
        print("Entered email: " + email)
        con = input(
            "Please enter [Y/y] to process or [N/n] to edit or [E/e] to exit: ").lower()
        if (con == "y"):
            signupAPI(name, email, password)
            menu()
            break
        elif (con == 'e'):
            return


def signupAPI(name, email, password):
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS profile 
    (email CHAR(50) NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    password TEXT NULL,
    private_key TEXT NULL)
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS inbox 
    (id INTEGER NOT NULL PRIMARY KEY autoincrement,
    sender TEXT NOT NULL,
    receiver TEXT NOT NULL, 
    subject TEXT NULL,
    body TEXT NOT NULL)
    ''')

    c.execute("INSERT INTO profile (email, name) VALUES (?, ?)", [
        email, name])

    enc_pw = aes_main.enc_aes(password, password)

    c.execute("update profile set password = ? where email = ?", [enc_pw, email])
    conn.commit()
    conn.close()

    pgp_enc.key_prod_store(name, email, password)

    del name
    del email
    del password
    print('User created successfully!!!')


def doAuthenticate(email, password):
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    chk_pw = aes_main.enc_aes(password, password)

    c.execute("SELECT email FROM profile where email=? and password=?", [email, chk_pw])
    data = c.fetchone()
    #print(data[0])
    conn.close()
    if (data != None):
        return data[0]
    else:
        return 0


def signin():
    email = input("Please enter email id : ")

    while True:
        db_name = "./" + email + ".db"
        if (os.path.isfile(db_name) == True):
            break
        print("Invalid Email!!")
        email = input("Please enter a different email id: ")

    password = input("Please enter password : ")
    system('cls')

    userid = doAuthenticate(email, password)
    del password
    if (userid != 0):
        return email
    if ("0" == input("Invalid password, Enter 1 to retry or 0 to main menu\n")):
        return None


def send_email(_from, _to, subject, body):
    db_name = _to + ".db"
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    enc_body = pgp_enc.enc_data(body, _to)
    del body

    c.execute("INSERT INTO inbox (sender, receiver, subject, body) VALUES (?, ?, ?, ?)", [
        _from, _to, subject, str(enc_body)])
    conn.commit()
    conn.close()
    print('Email sent successfully!!!')


def compose_email(email):
    to = input("To : ")

    while True:
        db_name = "./" + email + ".db"
        if (os.path.isfile(db_name) == True):
            break
        print("Invalid Email!!")
        email = input("Please enter a different email id: ")

    subject = input("Subject : ")
    body = input("Body : ")
    action = input(
        "Press [S/s] to send email, press [D/d] to discard: ").lower()
    #print(action)
    if (action == "s"):
        send_email(email, to, subject, body)
        return
    elif (action == "d"):
        return


def view(email):
    pw = input("Enter your password for secondary verification: ")
    system('cls')
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)
    curr = conn.cursor()

    curr.execute("select id, sender, receiver, subject from inbox")
    print("Inbox:")
    print(curr.fetchall())

    s = input("Enter id number of email to view: ")
    enc = curr.execute("select body from inbox where id=?", [int(s)])

    enc_body = curr.fetchone()[0]

    #print("\n"+enc_body+"\n")

    print("\n\nBody:")
    print(pgp_enc.dec_data(enc_body, email, pw))
    print("\n\n")
    conn.close()


def email_menu(email):
    while True:
        option = input("1. Compose Email \n2. View Inbox \n3. Exit\n\n")
        if (option == "1"):
            compose_email(email)
        elif (option == "2"):
            view(email)
        elif (option == "3"):
            return

def menu():
    while True:
        print("Please enter menu number to select your option")
        option = input(
            "1. SIGNUP \n2. SIGNIN \n3. Exit \n\n")
        if (option == "1"):
            signup_helper()
            break
        elif (option == "2"):
            email = signin()
            if email != None:
                email_menu(email)
        elif (option == "3"):
            print("Thank you for using Neutronmail\n\n")
            break
        else:
            print("Invalid option")

menu()
