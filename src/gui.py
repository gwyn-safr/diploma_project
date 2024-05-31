from Crypto import Random
from Crypto.Cipher import AES
import tkinter
from tkinter import filedialog, messagebox

from encrypting import encrypt_data, decrypt_data, generate_key, create_private_key, create_public_key

def pad(s):
  return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message):
  global public_key
  message = pad(message)
  iv = Random.new().read(AES.block_size)
  return iv + encrypt_data(message, public_key)

def decrypt(ciphertext):
  global private_key
  iv = Random.new().read(AES.block_size)
  print(len(private_key)," --- ", private_key)
  plaintext = decrypt_data(ciphertext, private_key)
  return plaintext.rstrip(b"\0")

def encrypt_file(filename):
  with open(filename, 'rb') as f:
    plaintext = f.read()
  enc = encrypt(plaintext)
  print("wrote: ", enc)
  with open(filename + ".enc", 'wb') as f:
    f.write(enc)

def decrypt_file(filename):
  with open(filename, 'rb') as f:
    ciphertext = f.read()
  dec = decrypt(ciphertext)
  with open(filename, 'wb') as f:
    f.write(dec)

def load_file():
  global filename
  text_file = filedialog.askopenfile()
  if text_file.name != None:
    filename = text_file.name

def encrypt_the_file():
  global filename
  if filename != None:
    encrypt_file(filename)
  else:
    messagebox.showerror(title="Error:", message = "There was no file loaded to encrypt")

def decrypt_the_file():
  global filename
  if filename != None:
    decrypt_file(filename)
  else:
    messagebox.showerror(title="Error:", message = " There was no file loaded to decrypt")


def run_file_encryption():
  filename = None

  key = generate_key()
  public_key = create_public_key(key)
  private_key = create_private_key(key)

  root = tkinter.Tk()
  root.title("Cryptofile")
  root.minsize(width=200, height=150)
  root.maxsize(width=200, height=150)

  loadButton = tkinter.Button(root, text="Load Text File", command=load_file)
  loadButton.grid(column = 3, row = 1, padx=50, pady=10)
  encryptButton = tkinter.Button(root, text="Encrypt File", command=encrypt_the_file)
  encryptButton.grid(column = 3, row= 2, padx=50, pady=10)
  decryptButton = tkinter.Button(root, text="Decrypt the file", command=decrypt_the_file)
  decryptButton.grid(column = 3, row = 3, padx=50, pady=10)

  root.grid_columnconfigure(7, minsize=700)
  #loadButton.pack()
  #encryptButton.pack()
  #decryptButton.pack()


  root.mainloop()	


def run_string_encryption():
  key = generate_key()
  
  public_key = create_public_key(key)
  private_key = create_private_key(key)

  root = tkinter.Tk() 
  root.title("CRYPTOGRAPHY") 
  root.geometry("425x100") 

  def encryptMessage():                    
    pt = e1.get()
    ct = encrypt_data(bytes(pt, 'utf-8'), public_key) 
    e2.insert(0, str(ct)[2:-1]) 
    
  def decryptMessage():                  
    ct1 = e3.get() 
    # this whole thing is a byproduct of passing actually usefull output when encoding
    # because decryptMessage receives a string that previously was a bytes string
    # and gets encoded into bytes string and gets double backslashes
    # example: b'\x04\xe8\xc7'  --->  '\x04\xe8\xc7'   ---> b'\\x04\\xe8\\xc7'
    # whish are removed with whole unicode_escape thing
    pt1 = decrypt_data(bytes(ct1, 'utf-8').decode('unicode_escape').encode("raw_unicode_escape"), private_key) 
    e4.insert(0, pt1) 
        
  # creating labels and positioning them on the grid 
  label1 = tkinter.Label(root, text ='plain text')                
  label1.grid(row = 10, column = 1) 
  label2 = tkinter.Label(root, text ='encrypted text') 
  label2.grid(row = 11, column = 1) 
  l3 = tkinter.Label(root, text ="cipher text") 
  l3.grid(row = 10, column = 10) 
  l4 = tkinter.Label(root, text ="decrypted text") 
  l4.grid(row = 11, column = 10) 
    
  # creating entries and positioning them on the grid 
  e1 = tkinter.Entry(root) 
  e1.grid(row = 10, column = 2) 
  e2 = tkinter.Entry(root) 
  e2.grid(row = 11, column = 2) 
  e3 = tkinter.Entry(root) 
  e3.grid(row = 10, column = 11) 
  e4 = tkinter.Entry(root) 
  e4.grid(row = 11, column = 11) 
    
  # creating encryption button to produce the output 
  ent = tkinter.Button(root, text = "encrypt", bg ="red", fg ="white", command = encryptMessage) 
  ent.grid(row = 13, column = 2) 
    
  # creating decryption button to produce the output 
  b2 = tkinter.Button(root, text = "decrypt", bg ="green", fg ="white", command = decryptMessage) 
  b2.grid(row = 13, column = 11) 
    
    
  root.mainloop()

import db_gui

def run_db_interface():
  db_gui.main().mainloop()


if __name__ == "__main__":
  run_db_interface()