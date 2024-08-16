import mysql.connector
# Connect to the MySQL server
database = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password"
)
database_cursor = database.cursor()

# Create the database if it doesn't exist
database_cursor.execute("CREATE DATABASE IF NOT EXISTS chemist")

# Close the initial connection
database_cursor.close()
database.close()

# Reconnect to the newly created database
database = mysql.connector.connect(
    host="localhost",
    user="user",
    password="password",
    database="chemist"
)
database_cursor = database.cursor()

# Create the `List of Medicine` table
database_cursor.execute('''CREATE TABLE IF NOT EXISTS `List of Medicine` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            med_name VARCHAR(255),
                            quantity INT,
                            price INT)
''')

# Create the `SIGN UP` table
database_cursor.execute('''CREATE TABLE IF NOT EXISTS `SIGN UP` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            login VARCHAR(255),
                            password VARCHAR(255),
                            bank_cash INT)
''')

# Create the `SIGN IN` table
database_cursor.execute('''CREATE TABLE IF NOT EXISTS `SIGN IN` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            login VARCHAR(255),
                            date DATETIME)
''')
database_cursor.execute('''CREATE TABLE IF NOT EXISTS `LIST OF ORDERS` (
                            id INT AUTO_INCREMENT PRIMARY KEY,
                            login VARCHAR(255),
                            med_name_quantity_price VARCHAR(255),
                            all_price INT)
''')

# Commit the changes
database.commit()

# Close the connection
# database_cursor.close()
# database.close()
