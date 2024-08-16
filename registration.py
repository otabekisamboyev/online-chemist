from datetime import datetime


class Registration:
    """Registration class"""
    def __init__(self, database, database_cursor):
        self.__database = database
        self.__database_cursor = database_cursor

        self.admin = "admin"
        self.admin_password = "admin"

        self.password = "SELECT password FROM `SIGN UP` WHERE login = %s"
        self.login = "SELECT login FROM `SIGN UP`"

    def login_password(self):
        """Ask user to login password"""
        login = input("Enter the login: ")
        password = input("Enter the password: ")
        return login, password

    def new_login_password(self):
        """Ask user to new login password"""
        new_login = input("Enter the new login: ")
        password = input("Enter the new password: ")
        balance = int(input("Enter the new balance: "))
        return new_login, password, balance

    def fetch_user_password(self, login):
        self.__database_cursor.execute(self.password, (login,))
        fetched_password = self.__database_cursor.fetchall()
        return fetched_password

    def fetch_user(self):
        self.__database_cursor.execute(self.login)
        fetched_login = self.__database_cursor.fetchall()
        return fetched_login

    def sign_up(self, login, password, bank_cash):
        """Insert new user into the database"""
        logins = set(value[0] for value in self.fetch_user())
        value_exists = login in logins

        if bank_cash < 0 or bank_cash > 100:
            print("\nAccount not created!")
            print("Bank cash must be between $1 and $100\n")
        else:
            if value_exists:
                print("This login already exists!")
            else:
                sql = f"INSERT INTO `SIGN UP` (login, password, balance) VALUES (%s, %s, %s)"
                val = (login, password, bank_cash)
                self.__database_cursor.execute(sql, val)
                self.__database.commit()
                print("Successfully registered! Now you can login.")

    def sign_in(self, login, password):
        """Insert exist user into the database"""
        logins = set(value[0] for value in self.fetch_user())
        value_exists = login in logins

        passwords = set(value[0] for value in self.fetch_user_password(login))
        password_exist = password in passwords

        if login == "admin" and password == "admin":
            print("You are an Admin")
            return True
        elif value_exists:
            if password_exist:
                datetime_str = datetime.now().strftime("%d-%m-%Y %I:%M %p")
                datetime_obj = datetime.strptime(datetime_str, "%d-%m-%Y %I:%M %p")
                mysql_date_time = datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

                sql = f"INSERT INTO `sign in` (login, date) VALUES (%s, %s)"
                val = (login, mysql_date_time)
                self.__database_cursor.execute(sql, val)
                self.__database.commit()
                print(f"Successfully logged into {login}")
                return True
            else:
                print("Wrong password!")
                return False
        else:
            print("This user does not exist!")
            return False
