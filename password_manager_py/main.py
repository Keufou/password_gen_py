import random
import json
from cryptography.fernet import Fernet

import os

def write_key():
    if not os.path.exists("key.key"):
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
    main()
def load_key():
    return open("key.key", "rb").read()

def encrypt_password(password, key):
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()

def decrypt_password(encrypted_password, key):
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()

def pass_gen():
    key = load_key()
    site = input('Sur quel site voulez-vous utiliser ce mot de passe ? : ')
    username = input('Quel est votre nom d\'utilisateur ? : ')
    choix = int(input('Combien de caractères voulez-vous ? : '))
    pass_chars = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()'
    password = ''

    for i in range(choix):
        password += random.choice(pass_chars)
    print('Voici votre mot de passe : ' + password)
    encrypted_password = encrypt_password(password, key)
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
    passwords[site] = {"username": username, "password": encrypted_password}
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)
    print('Votre mot de passe a été sauvegardé !')
def view_pass():
    key = load_key()
    site = input('Quel mot de passe voulez-vous voir ? (recherche par site): ')
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
    encrypted_password = passwords[site]['password']
    username = passwords[site]['username']
    decrypted_password = decrypt_password(encrypted_password, key)
    print(username + ":" + decrypted_password)
def del_pass():
    with open('passwords.json', 'r') as f:
        passwords = json.load(f)
    site = input('Quel mot de passe voulez-vous supprimer ? (recherche par site): ')
    del passwords[site]
    with open('passwords.json', 'w') as f:
        json.dump(passwords, f)
    print('Votre mot de passe a été supprimé !')
def main():
    menu = int(input('Que voulez-vous faire ?\n1. Générer un mot de passe\n2. Voir vos mots de passe\n3. Supprimer un mot de passe\n4. Quitter\n'))
    if menu == 1:
        pass_gen()
    elif menu == 2:
        view_pass()
    elif menu == 3:
        del_pass()
    elif menu == 4:
        exit()
    else:
        print('Erreur, veuillez réessayer.')
        main()  
write_key()
if __name__ == "__main__":
    main()