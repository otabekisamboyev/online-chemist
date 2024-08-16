class BankAccount:
    def __init__(self, database, database_cursor):
        self.__database = database
        self.__database_cursor = database_cursor
        self.price_query = "SELECT price FROM `LIST OF MEDICINE` WHERE med_name = %s"
        self.balance_query = "SELECT balance FROM `SIGN UP` WHERE login = %s"

    def is_transaction_successful(self, med_name, med_quantity, login):
        """Returns True if the transaction was successful. Else returns False."""
        self.__database_cursor.execute(self.price_query, (med_name,))
        med_price = self.__database_cursor.fetchall()
        final_price = med_price[0][0] * med_quantity

        self.__database_cursor.execute(self.balance_query, (login,))
        user_balance = self.__database_cursor.fetchall()[0][0]

        if final_price > user_balance:
            print("Your bank account balance is not sufficient to order this med.")
            return False
        return True

    def report_balance(self, login):
        """Print a report of all medicine"""
        self.__database_cursor.execute(f"SELECT balance FROM `SIGN UP` WHERE login = '{login}'")
        balances = self.__database_cursor.fetchall()
        for balance in balances:
            print(f"Your balance is ${balance[0]}")
