
        print("File does not exists.")



while True:
    print("----Welcome to Password Manager.----")
    print("1. View Passwords.")
    print("2. Add Passwords.")
    print("3. Delete Password.")
    print("4. Update Password.")
    print("5. Quit.")
    choice=int(input("Enter your choice: "))

    match choice:
        case 1: 
            view()
        case 2: 
            add()
        case 3: 
            delete()
        case 4: 