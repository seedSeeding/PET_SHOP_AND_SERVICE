import mysql.connector
from mysql.connector import Error


HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "pet_database"

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def open_connection(self):
        try:
            self.connection = mysql.connector.connect(
                host=HOST,
                user=USERNAME,
                password=PASSWORD,
                database=DATABASE
            )
            if self.connection.is_connected():
                print("Connection to MySQL database established successfully.")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def run_query(self, query, params=None):
        try:
            if self.connection and self.connection.is_connected():
                self.cursor = self.connection.cursor()
                if params:
                    self.cursor.execute(query, params)
                else:
                    self.cursor.execute(query)
                self.connection.commit()
                print("Query executed successfully.")
            else:
                print("Error: No active database connection.")
        except Error as e:
            print(f"Error executing query: {e}")
        finally:
            if self.cursor is not None:
                self.cursor.close()

    def close_connection(self):
        try:
            if self.connection and self.connection.is_connected():
                self.connection.close()
                print("Database connection closed.")
        except Error as e:
            print(f"Error closing the connection: {e}")

