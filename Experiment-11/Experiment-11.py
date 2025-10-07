import hashlib

file="users.txt"

def password_hasher(password):
    return hashlib.sha256(password.encode()).hexdigest()  


def register_user(username, password):
    hashed_password = password_hasher(password)
    user_exists = False
    try:
        with open(file, 'r') as f:
            for line in f:
                if line.strip().split(',')[0] == username:
                    user_exists = True
                    break
    except FileNotFoundError:
        pass

    if user_exists:
        print("Username already exists. Please choose a different one.")
        return
    
    with open(file, 'a') as f:
        f.write(f"{username},{hashed_password}\n")
    print("User registered successfully.")


def authenticate_user(username, password):
    hashed_password = password_hasher(password)
    with open(file, 'r') as f:
        users = f.readlines()
    for user in users:
        stored_username, stored_hashed_password = user.strip().split(',')
        if stored_username == username and stored_hashed_password == hashed_password:
            print("Authentication successful.")
            return True
    print("Authentication failed.")
    return False


if __name__=="__main__":
    while True:
        ch=input("1. Register\n2. Login\n3. Exit\nEnter choice: ")
        if ch=='1':
            username=input("Enter username:")
            password=input("Enter password:")
            register_user(username, password)
        elif ch=='2':
            username=input("Enter username:")
            password=input("Enter password:")
            authenticate_user(username, password)
        elif ch=='3':
            break
        else:
            print("Invalid choice. Please try again.")