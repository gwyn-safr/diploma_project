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


def run():
	
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
	
if __name__ == "__main__":
  key = generate_key()
  public_key = create_public_key(key)
  private_key = create_private_key(key)
  filename = None

  print("pub : ", type(public_key), " --- ", public_key)
  print("pri : ", type(private_key), " --- ", private_key)

  run()