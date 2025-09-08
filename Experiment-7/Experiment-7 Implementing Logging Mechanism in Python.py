# import logging 

# logger=logging.getLogger("experiment_logger")
# logger.setLevel(logging.DEBUG)

# handler=logging.FileHandler("experiment.log")

# formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# handler.setFormatter(formatter)

# logger.addHandler(handler)

# logger.debug("This is a debug message.")  # This won't be displayed
# logger.info("This is an info message.")   # This will be displayed
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")
# logger.critical("This is a critical message.")

# print("Logging complete. Check 'experiment.log' for log messages.")


import logging 

def new_user(username,password):
    try:
        if len(password)<6:
            logging.warning(f"Password for user {username} is too short.")
        else:
            logging.info(f"User {username} created successfully.")

        with open("users.txt","a") as f:
            #hashed_password=hashlib.sha256(password.encode()).hexdigest()
            f.write(f"{username},{password}\n")
            logging.info(f"User {username} and password {password} added to users.txt file.")
    except Exception as e:
        logging.exception(f"An error occurred while creating user {username}: {e}")



def login(username,password):
    try:
        with open("users.txt","r") as f:
            users=f.readlines()
            for user in users:
                stored_username,stored_password=user.strip().split(",")
                if stored_username==username and stored_password==password:
                    logging.info(f"User {username} logged in successfully.")
                    return True
            logging.warning(f"Login failed for user {username}. Incorrect username or password.")
            return False
    except FileNotFoundError:
        logging.error("users.txt file not found. No users exist.")
        return False
    except Exception as e:
        logging.exception(f"An error occurred during login for user {username}: {e}")
        return False
    
if __name__=="__main__":
    logging.basicConfig(filename="app.log",level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    new_user("alice","password123")
    new_user("bob","pass")
    login("alice","password123")
    login("bob","wrongpass")
    login("charlie","nopass")
    print("Sucessfully executed. Check app.log for details.")