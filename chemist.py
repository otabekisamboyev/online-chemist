class Chemist:
    def __init__(self, database, database_cursor):
        """Chemist constructor."""
        self.__database = database
        self.__database_cursor = database_cursor

    # def is_med_exist(self, med_name):
    #     medicines = set(value[0] for value in self.med_names)
    #     medicine_exist = med_name in medicines
    #     return medicine_exist

    def add_new_med(self, med_name, quantity, price):
        """Add new med to database."""
        query = "INSERT INTO `LIST OF MEDICINE` (`med_name`, `quantity`, `price`) VALUES (%s, %s, %s)"
        values = (med_name, quantity, price)
        self.__database_cursor.execute(query, values)
        self.__database.commit()

    def add_existing_med(self, med_name, quantity):
        """Add a new med to database"""

        # Fetch the current quantity of the medicine
        query = "SELECT quantity FROM `LIST OF MEDICINE` WHERE med_name = %s"
        self.__database_cursor.execute(query, (med_name,))
        medicine = self.__database_cursor.fetchone()

        new_quantity = medicine[0] + quantity

        # Update the quantity in the database
        update_query = "UPDATE `LIST OF MEDICINE` SET quantity = %s WHERE med_name = %s"
        self.__database_cursor.execute(update_query, (new_quantity, med_name))

        # Commit the transaction
        self.__database.commit()

    def fetch_quantity(self, med_name):
        self.__database_cursor.execute("SELECT quantity FROM `LIST OF MEDICINE` WHERE med_name = %s", (med_name,))
        fetched_quantity = self.__database_cursor.fetchall()
        return fetched_quantity

    def is_quantity_sufficient(self, med_name, user_quantity):
        med_quantity = self.fetch_quantity(med_name)
        if med_quantity[0][0] < user_quantity:
            if med_quantity > 0:
                print(f"Insufficient quantity. There is {med_quantity} med.")
                buy_all_med = input("Do you want to buy all meds? (y/n): ")
                if buy_all_med.lower() == "y":
                    return True
                elif buy_all_med.lower() == "n":
                    pass
                else:
                    print("Wrong input.")
            else:
                print("This medicine quantity is not sufficient.")
            return False
        return True

    def remove_med(self, med_name, quantity):
        """Remove an exist med from database"""
        # Fetch the current quantity of the medicine
        query = "SELECT quantity FROM `LIST OF MEDICINE` WHERE med_name = %s"
        self.__database_cursor.execute(query, (med_name,))
        medicine = self.__database_cursor.fetchone()

        new_quantity = medicine[0] - quantity

        # Update the quantity in the database
        update_query = "UPDATE `LIST OF MEDICINE` SET quantity = %s WHERE med_name = %s"
        self.__database_cursor.execute(update_query, (new_quantity, med_name))

        # Commit the transaction
        self.__database.commit()

    def fetch_medicines(self):
        # Re-fetch the data from the database
        self.__database_cursor.execute("SELECT * FROM `LIST OF MEDICINE`")
        med_names = self.__database_cursor.fetchall()
        return med_names

    def report_med(self):
        """Print a report of all medicine"""
        for med in self.fetch_medicines():
            print(f"Med-name: {med[1]}. Quantity: {med[2]}. Price: ${med[3]}")
