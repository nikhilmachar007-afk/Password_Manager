from cryptography.fernet import Fernet
import hashlib
import os
import time

def hash_password(master_pwd):
    return hashlib.sha256(master_pwd.encode()).hexdigest()

if not os.path.exists("Master.key"):
    with open("Master.key","w") as f:
        master_pwd=input("Master Password: ")
        f.write(hash_password(master_pwd))

print("\n------PASSWORD MANAGER------")

i=0
while i<3:
    atmptd_m_pwd=input("Master Password is required: ")
    print()
    with open("Master.key","r") as f:
        m_pwd=f.readline()

    if hash_password(atmptd_m_pwd)!=m_pwd:
        print("Wrong Master Password. Please Try again.")
    else:
        break
    if i==2:
        print("Maximum Wrong attempts. Please wait for 10 seconds to try again.")
        for j in range(0,10):
            print(f"Time remaining [{j}]s",end="\r")
            time.sleep(1)
        i=0
    i+=1



if not os.path.exists("Key.key"):
    with open("Key.key", "wb") as f:
        key=Fernet.generate_key()
        f.write(key)

with open("Key.key","rb") as f:
    Key=f.read()

cipher=Fernet(Key)

def search_pwd(website_name):
    if os.path.exists("passwords.txt"):
        with open("passwords.txt","r") as f:
            for line in f:
                words=line.split("|")
                if words[0]==website_name:
                    return True
            return False
    else:
        return False

def encrypted_pwd(password):
    return cipher.encrypt(password.encode()).decode()

def add():
    website=input("Website: ")
    username=input("Username: ")
    password=input("Password: ")

    if  search_pwd(website):
        print("Password already exists.")
    else:
        with open("passwords.txt","a") as f:
            f.write(f"{website}|{username}|{encrypted_pwd(password)}\n")
            print(f"{website}'s password was added successfully.")


def decrypt_pwd(encrypted_pwd):
    return cipher.decrypt(encrypted_pwd.strip().encode()).decode()

def view():
    if os.path.exists("passwords.txt"):
        with open("passwords.txt","r") as f:
            print("\n"+"-"*70+"\n")
            for line in f:
                words=line.split("|")
                print(f"Website: {words[0]} | Username: {words[1]} | Password: {decrypt_pwd(words[2])}")
            print("\n"+"-"*70+"\n")
    else:
        print("No passwords are added yet.")

def delete():
    if os.path.exists("passwords.txt"):
        website_name=input("Website: ")
        if not search_pwd(website_name):
            print("Given website does not exists")
        else:
            with open("passwords.txt", "r") as f:
                content=f.readlines()
            
            with open("passwords.txt","w") as f:
                for line in content:
                    words=line.split("|")
                    if not words[0]==website_name:
                        f.write(line)
            print(f"{website_name}'s password deleted successfully.")
    else:
        print("File does not exist.")


def update():
    if os.path.exists("passwords.txt"):
        website=input("Website: ")
        new_pwd=input("New Password: ")

        if search_pwd(website):
            with open("passwords.txt","r") as f:
                content=f.readlines()
            
            with open("passwords.txt","w") as f:
                for line in content:
                    words=line.split("|")
                    if words[0]==website:
                        words[2]=encrypted_pwd(new_pwd)
                        line=words[0]+"|"+words[1]+"|"+words[2]+"\n"
                    f.write(line)
            print(f"New Password for {website} updated successfully.")
        else:
            print(f"{website}'s passwords does not exist.")
    else:
        print("File does not exists.")



while True:
    print("--------PASSWORD MANAGER-------")
    print("1. View Passwords.")
    print("2. Add Passwords.")
    print("3. Delete Password.")
    print("4. Update Password.")
    print("5. Quit.")
    
    try:
        choice=int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid input.")
        continue


    match choice:
        case 1: 
            view()
        case 2: 
            add()
        case 3: 
            delete()
        case 4: 
            update()
        case 5:
            print("Closing Password Manager...",end="\r")
            time.sleep(1)
            print("Closed."+" "*30)
            exit(0)
        case _: print("Invalid input. Please enter a valid input.")

