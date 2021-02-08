import sqlite3
import os

import aes_main
import pgp_enc

def signup_helper(name, email, password):
    email = email + "@neutronmail.com"

    db_name = "./" + email + ".db"
    if (os.path.isfile(db_name) == True):
        return 2

    signupAPI(name, email, password)
    return 0

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

def signin(email, password):
    db_name = "./" + email + ".db"
    if (os.path.isfile(db_name) != True):
       return 1


    auth_code = doAuthenticate(email, password)
    del password
    if (auth_code != 0):
        return 0
    else:
        return 2

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

def compose_email(email, to, subject, body):
    db_name = "./" + to + ".db"
    if (os.path.isfile(db_name) != True):
        return 2

    send_email(email, to, subject, body)
    return 0

def view(email):
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)
    curr = conn.cursor()

    ext = curr.execute("select id, sender, receiver, subject from inbox")
    rows = curr.fetchall()
    #print("Inbox:")
    #print(curr.fetchall())
    return rows

def view_body(email, pw, id):
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)
    curr = conn.cursor()
    enc = curr.execute("select body from inbox where id=?", [id])
    enc_body = curr.fetchone()[0]
    body = pgp_enc.dec_data(enc_body, email, pw)
    #print(enc_body)
    #print("nextline\n")
    return body
