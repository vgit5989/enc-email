from ext import gnupg
import sqlite3

gpg = gnupg.GPG(gpgbinary="C:\Program Files (x86)\GnuPG\\bin\gpg.exe", gnupghome='keyring', options=['--yes'])


def key_prod_store(name, email, pw):
    def gen_key(em, pw):
        input_data = gpg.gen_key_input(
            name_email=em,
            passphrase=pw,
        )
        key = gpg.gen_key(input_data)
        return key

    """
    email = input("Enter your email username(ex: jacob123): ")
    pw = input("Enter password: ")
    """

    # email += "@neutronmail.com"

    conn = sqlite3.connect('keystore.db')

    conn.execute('''create table if not exists keys
             (email char(50) primary key not null,
              name text not null,
              public_key text null);''')

    conn.execute("insert into keys (email, name) values(?,?)", (email, name))
    conn.commit()

    sel = conn.execute("select email from keys")
    for row in sel:
        em = row[0]
        # print(em)
        break

    key = gen_key(em, pw)
    del em

    ascii_armored_public_keys = gpg.export_keys(key.fingerprint)
    ascii_armored_private_keys = gpg.export_keys(
        keyids=key.fingerprint,
        secret=True,
        passphrase=pw,
    )
    del key
    del pw
    # print("Generated key purged")

    conn.execute("update keys set public_key  = ? where email = ?", [ascii_armored_public_keys, email]);
    conn.commit()
    del ascii_armored_public_keys

    conn.close()
    # rint("Public key stored and purged")

    db_name = email + ".db"

    conn = sqlite3.connect(db_name)

    # conn.execute("insert into profile (email, name) values(?,?)", (email, name))
    # conn.commit()

    conn.execute("update profile set private_key  = ? where email = ?", [ascii_armored_private_keys, email]);
    conn.commit()
    del ascii_armored_private_keys
    del email
    del name

    # print("Private key stored and purged")
    conn.close


def enc_data(data, email):
    conn = sqlite3.connect('keystore.db')
    sel = conn.execute("select public_key from keys")
    for row in sel:
        k = row[0]
        imp = gpg.import_keys(k)
        # print(imp.results)

    conn.close()
    # public_keys = gpg.list_keys()
    # print('public keys:\n', public_keys)

    encrypted_data = gpg.encrypt(data, email)
    # print('encrypted_data: ', encrypted_data)

    return encrypted_data

    # print('encrypted_data: ', encrypted_data)
    # print('ok: ', encrypted_data.ok)
    # print('status: ', encrypted_data.status)
    # print('stderr: ', encrypted_data.stderr)
    # print('unencrypted_string: ', data)


def dec_data(enc, email, pw):
    db_name = email + ".db"
    conn = sqlite3.connect(db_name)

    sel = conn.execute("select private_key from profile")
    for row in sel:
        k = row[0]
        imp = gpg.import_keys(k)
        # print(imp.results)

    decrypted_data = gpg.decrypt(enc, passphrase=pw)
    status = gpg.delete_keys(gpg.list_keys(True)[0]['fingerprint'], secret=True, passphrase=pw)
    del pw
    del enc
    del email

    # private_keys = gpg.list_keys(True)
    # print('private keys:\n', private_keys)
    conn.close()

    return decrypted_data

    # print('decrypted_data: ', decrypted_data)
    # print("\n" + 'ok: ', decrypted_data.ok)
    # print("\n" + 'status: ', decrypted_data.status)
    # print("\n" + 'stderr: ', decrypted_data.stderr)

    # print('decrypted_data: ', decrypted_data)

'''
key_prod_store("123", "123@neutronmail.com", "12345")
key_prod_store("1234", "1234@neutronmail.com", "12345")


data = "How was your day Rick?\n"\
       "With Regards\n"\
       "Glenn"

email = '1234@neutronmail.com'

pw = "12345"

enc = str(enc_data(data, email))
print("\n"+enc)


dec = dec_data(enc, email, pw)
print(dec)




public_keys = gpg.list_keys()
print('public keys:\n', public_keys)

private_keys = gpg.list_keys(True)
print('private keys:\n', private_keys)
'''