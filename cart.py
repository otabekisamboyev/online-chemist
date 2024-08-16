import json


class Cart:
    def __init__(self, database, database_cursor):
        self.cart = {}
        self.__database = database
        self.__database_cursor = database_cursor
        self.order_query = "SELECT med_name_quantity_price FROM `LIST OF ORDERS` ORDER BY id DESC LIMIT 1"
        self.price_query = "SELECT all_price FROM `LIST OF ORDERS` ORDER BY id DESC LIMIT 1"
        self.bank_balance = "SELECT balance FROM `SIGN UP` WHERE login = %s"

    def add_to_cart(self, med_name, quantity):
        self.__database_cursor.execute("SELECT price FROM `LIST OF MEDICINE` WHERE med_name = %s", (med_name,))
        price = self.__database_cursor.fetchone()
        if med_name not in self.cart:
            self.cart[med_name] = {
                "quantity": quantity,
                "price_per_med": price[0]
            }
        else:
            self.cart[med_name]["price_per_med"] = price[0]
            self.cart[med_name]["quantity"] += quantity
        print("Successfully added to your card")

    def calculate_price(self):
        price = 0
        for med_name in self.cart:
            price += self.cart[med_name]["price_per_med"] * self.cart[med_name]["quantity"]
        return price

    def add_to_database(self, login):
        query = "INSERT INTO `LIST OF ORDERS` (`login`, `med_name_quantity_price`, `all_price`) VALUES (%s, %s, %s)"
        json_data = json.dumps(self.cart)
        value = (login, json_data, self.calculate_price())
        self.__database_cursor.execute(query, value)
        self.__database.commit()

    def remove_bank_balance(self, login):
        self.__database_cursor.execute(self.bank_balance, (login,))
        user_balance = self.__database_cursor.fetchall()[0][0]
        med_price = self.calculate_price()
        user_balance -= med_price

        update_query = "UPDATE `SIGN UP` SET balance = %s WHERE login = %s"
        self.__database_cursor.execute(update_query, (user_balance, login,))
        self.__database.commit()

    def fetch_ordered_products(self):
        self.__database_cursor.execute(self.order_query)
        ordered_products = self.__database_cursor.fetchone()
        return ordered_products

    def fetch_price(self):
        self.__database_cursor.execute(self.price_query)
        total_price = self.__database_cursor.fetchone()
        return total_price

    def report_cart(self, login):
        try:
            ordered_products = self.fetch_ordered_products()
            total_price = self.fetch_price()

            print(f"Login: {login}")
            print("Order:")
            if ordered_products:
                for product in ordered_products:
                    # Assuming product has (med_name, quantity, price) tuple structure
                    print(f"  {product}")
            else:
                print("  No products ordered.")

            if total_price:
                print(f"Total Price: ${total_price[0]}")
            else:
                print("Price information unavailable.")
        except Exception as e:
            print(f"Error fetching cart information: {e}")
