from Crypto.Cipher import AES
import hashlib
import Padding
import sqlite3

ival=10
iv = hex(ival)[2:8].zfill(16)

def encrypt(plaintext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.encrypt(plaintext))

def decrypt(ciphertext,key, mode,iv):
	encobj = AES.new(key,mode,iv)
	return(encobj.decrypt(ciphertext))

def enc_aes(plaintext, password):
	key = hashlib.sha256(password.encode()).digest()

	plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)

	ciphertext = encrypt(plaintext.encode(),key,AES.MODE_CBC,iv.encode())
	#print (binascii.hexlify(bytearray(ciphertext)).decode())
	return ciphertext

def dec_aes(ciphertext, password):
	key = hashlib.sha256(password.encode()).digest()
	plaintext = decrypt(ciphertext,key,AES.MODE_CBC,iv.encode())
	plaintext = Padding.removePadding(plaintext.decode(),mode=0)
	return plaintext

def check(email, password):
	db_name = email + ".db"
	conn = sqlite3.connect(db_name)
	c = conn.cursor()

	chk_pw = enc_aes(password, password)
	c.execute("update profile set password = ? where email = ?", [chk_pw, email])


	s = c.execute("SELECT email FROM profile where email=? and password=?", [email, chk_pw])

	data = c.fetchone()
	if(len(data) != 0):
		return data[0]
	else:
		return 0