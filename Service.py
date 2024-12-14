from Database import Database
from mysql.connector import Error
from User import User
from offer import Offer
from Cart import ProductCart,ServiceCart, Cart
from Transaction import CardTransaction, TranType
from Card import Card
class Service:
    def __init__(self):
        self.database = Database()

    # User
    def create_user(self, username, password):
        try:
            self.database.open_connection()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            res = self.database.run_query(query, (username, password))
            user = User(username,password)
            return user
        except Error as e:
            print(f"Error creating user: {e}")
        finally:
            self.database.close_connection()

    def update_user_info(self, username, fullname, contact, email, sex):
        print("username:",username)
        try:
            print(f"Opening database connection...")
            self.database.open_connection()
            print(f"Executing query to update user info: {username}, {fullname}, {contact}, {email}, {sex}")
            query = "UPDATE users SET fullname = %s, contact = %s, email = %s, sex = %s WHERE username = %s"
            self.database.run_query(query, (fullname, contact, email, sex, username))
            print("User Information updated successfully.")
            return True
        except Error as e:
            print(f"Error updating user Information: {e}")
            return False
        finally:
            self.database.close_connection()

    def update_user_location(self, _id, new_location):
        try:
            self.database.open_connection()
            query = "UPDATE users SET location = %s WHERE id = %s"
            self.database.run_query(query, (new_location, _id))
            print("User location updated successfully.")
        except Error as e:
            print(f"Error updating user location: {e}")
        finally:
            self.database.close_connection()

    def login_user(self, username, password):
        try:

            self.database.open_connection()
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (username, password))
            result = self.database.cursor.fetchone()
            if result:
                user = User(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7])
                print("Login successful.")
                return user
            else:
                print("Invalid username or password.")
                return False
        except Error as e:
            print(f"Error logging in: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    # Admin
    def create_admin(self, username, password):
        try:
            self.database.open_connection()
            query = "INSERT INTO admins (username, password) VALUES (%s, %s)"
            self.database.run_query(query, (username, password,))
            print("Admin created successfully.")
            return True
        except Error as e:
            print(f"Error creating admin: {e}")
            return False
        finally:
            self.database.close_connection()

    def login_admin(self, username, password):
        try:
            self.database.open_connection()
            query = "SELECT * FROM admins WHERE username = %s AND password = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (username, password))
            result = self.database.cursor.fetchone()
            if result:
                print("Admin login successful.")
                return True
            else:
                print("Invalid admin username or password.")
                return False
        except Error as e:
            print(f"Error logging in as admin: {e}")
            return False
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    # Product
    def add_product(self, name, price):
        try:
            self.database.open_connection()
            query = "INSERT INTO products (name, price) VALUES (%s, %s)"
            self.database.run_query(query, (name, price))
            print("Product added successfully.")
        except Error as e:
            print(f"Error adding product: {e}")
        finally:
            self.database.close_connection()

    def delete_product(self, product_id):
        try:
            self.database.open_connection()
            query = "DELETE FROM products WHERE id = %s"
            self.database.run_query(query, (product_id,))
            print("Product deleted successfully.")
        except Error as e:
            print(f"Error deleting product: {e}")
        finally:
            self.database.close_connection()

    def update_product(self, product_id, name, price):
        try:
            self.database.open_connection()
            query = "UPDATE products SET name = %s, price = %s WHERE id = %s"
            self.database.run_query(query, (name, price, product_id))
            print("Product updated successfully.")
        except Error as e:
            print(f"Error updating product: {e}")
        finally:
            self.database.close_connection()

    def get_products(self):
        try:
            products = []
            self.database.open_connection()
            query = "SELECT * FROM products"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query)
            results = self.database.cursor.fetchall()
            for result in results:
                products.append(Offer(result[0],result[1],result[2]))
            return products

        except Error as e:
            print(f"Error retrieving products: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    # Service
    def add_service(self, name, price):
        try:
            self.database.open_connection()
            query = "INSERT INTO services (name, price) VALUES (%s, %s)"
            self.database.run_query(query, (name, price))
            print("Service added successfully.")
        except Error as e:
            print(f"Error adding service: {e}")
        finally:
            self.database.close_connection()

    def delete_service(self, service_id):
        try:
            self.database.open_connection()
            query = "DELETE FROM services WHERE id = %s"
            self.database.run_query(query, (service_id,))
            print("Service deleted successfully.")
        except Error as e:
            print(f"Error deleting service: {e}")
        finally:
            self.database.close_connection()

    def update_service(self, service_id, name, price):
        try:
            self.database.open_connection()
            query = "UPDATE services SET name = %s, price = %s WHERE id = %s"
            self.database.run_query(query, (name, price, service_id))
            print("Service updated successfully.")
        except Error as e:
            print(f"Error updating service: {e}")
        finally:
            self.database.close_connection()

    def get_services(self):
        try:
            services = []
            self.database.open_connection()
            query = "SELECT * FROM services"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query)
            results = self.database.cursor.fetchall()
            for result in results:
                services.append(Offer(result[0],result[1],result[2]))
            return services
        except Error as e:
            print(f"Error retrieving services: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    # cart

    def add_service_cart(self, user_id, service, details):
        try:
            self.database.open_connection()
            query = "INSERT INTO cart_service (user_id, service, details, date) VALUES (%s, %s, %s, NOW())"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (user_id, service, details))
            self.database.connection.commit()
        except Error as e:
            print(f"Error adding service to cart: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    def add_product_cart(self, user_id, product, quantity):
        try:
            self.database.open_connection()
            query = "INSERT INTO cart_product (user_id, product, quantity, date) VALUES (%s, %s, %s, NOW())"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (user_id, product, quantity))
            self.database.connection.commit()
        except Error as e:
            print(f"Error adding product to cart: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    def get_service_cart(self,user_id):
        try:
            carts = []
            self.database.open_connection()
            query = "SELECT * FROM cart_service WHERE user_id = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query,(user_id,))
            result = self.database.cursor.fetchall()
            if result:
                for res in result:
                    carts.append(ServiceCart(res[0],res[1],res[2],res[3],res[4]))
                return carts
        except Error as e:
            print(f"Error retrieving service cart: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    def get_exact_id(self, _id):
        return int(str(_id).replace("s","").replace("p",''))
    def remove_cart(self, _id):
        try:
            _id = str(_id).lower()
            self.database.open_connection()
            # print("=a=",str(_id)[0])
            if str(_id)[0] == "p":
                query = "DELETE FROM cart_product WHERE id = %s"
            else:
                query = "DELETE FROM cart_service WHERE id = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (self.get_exact_id(_id),))
            self.database.connection.commit()
            return True
        except Error as e:
            print(f"Error removing cart: {e}")
            return False


        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    def remove_service_cart(self, user_id, service_name):
        try:
            self.database.open_connection()
            query = "DELETE FROM cart_service WHERE user_id = %s AND service = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (user_id, service_name))
            self.database.connection.commit()
        except Error as e:
            print(f"Error removing service from cart: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    def get_product_cart(self,user_id):
        try:
            carts = []
            self.database.open_connection()
            query = "SELECT * FROM cart_product WHERE user_id = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (user_id,))
            result = self.database.cursor.fetchall()
            if result:
                for res in result:
                    carts.append(ProductCart(res[0], res[1], res[2], res[3], res[4]))
                return carts
        except Error as e:
            print(f"Error retrieving product cart: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    def get_user_cart(self,user_id):
        product = self.get_product_cart(user_id)
        service = self.get_service_cart(user_id)
        cart = Cart(service,product)
        return cart

    # bank
    def get_user_card(self,user_id):
        try:
            self.database.open_connection()
            self.database.cursor = self.database.connection.cursor()

            query = "SELECT user_id, balance, pin FROM bank WHERE user_id = %s"
            self.database.cursor.execute(query, (user_id,))
            result = self.database.cursor.fetchone()

            if result:
                card = Card(result[0], result[1], result[2])
                return card
            else:
                return False

        except Error as e:
            print(f"Error in get_card: {e}")
            return {"error": "An error occurred while retrieving the card information."}
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    def get_card(self, user_id, pin):
        try:
            self.database.open_connection()
            self.database.cursor = self.database.connection.cursor()

            query = "SELECT user_id, balance, pin FROM bank WHERE user_id = %s"
            self.database.cursor.execute(query, (user_id,))
            result = self.database.cursor.fetchone()

            if result:
                card = Card(result[0],result[1],result[2])
                if card.pin == pin:
                    return card
                else:
                    return False
            else:
                return False

        except Error as e:
            print(f"Error in get_card: {e}")
            return {"error": "An error occurred while retrieving the card information."}
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()
    def update_balance(self,user_id,new_balance):
        try:
            self.database.open_connection()
            query = "UPDATE bank SET balance = %s WHERE user_id = %s"
            self.database.run_query(query, (new_balance,user_id,))
            print("Card updated successfully.")
        except Error as e:
            print(f"Error updating Card: {e}")
        finally:
            self.database.close_connection()
    def add_update_bank(self, user_id, pin=0,amount=0.0):

        try:
            print("data ::", user_id, pin,amount)
            self.database.open_connection()
            self.database.cursor = self.database.connection.cursor()

            query = "SELECT balance FROM bank WHERE user_id = %s"
            self.database.cursor.execute(query, (user_id,))
            result = self.database.cursor.fetchone()

            if result:

                new_balance = result[0] + amount
                update_query = "UPDATE bank SET balance = %s WHERE user_id = %s"
                self.database.cursor.execute(update_query, (new_balance, user_id))
                message = f"Balance updated successfully. New balance: {new_balance}"
            else:

                insert_query = "INSERT INTO bank (user_id, balance, pin) VALUES (%s, %s, %s)"
                self.database.cursor.execute(insert_query, (user_id, amount, pin,))
                message = f"Bank account created successfully with balance: {amount}"


            self.database.connection.commit()

            return message
        except Error as e:
            self.database.connection.rollback()
            print(f"Error in add_update_bank: {e}")
            return "An error occurred while processing the bank transaction."
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    # transactions
    def get_user_transaction(self,user_id):
        try:
            transactions = []
            self.database.open_connection()
            query = "SELECT * FROM transactions WHERE user_id = %s"
            self.database.cursor = self.database.connection.cursor()
            self.database.cursor.execute(query, (user_id,))
            result = self.database.cursor.fetchall()
            if result:
                for res in result:
                    transactions.append(CardTransaction(res[1],res[2],res[3],res[4]))
                return transactions
        except Error as e:
            print(f"Error retrieving transactions: {e}")
        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()

    def add_transaction(self, user_id, amount, type):
        try:
            self.database.open_connection()
            self.database.cursor = self.database.connection.cursor()
            query = """
                INSERT INTO transactions (user_id, amount, type, date)
                VALUES (%s, %s, %s, NOW())
            """
            self.database.cursor.execute(query, (user_id, amount, type))
            self.database.connection.commit()
            return True

        except Error as e:
            self.database.connection.rollback()
            print(f"Error in add_transaction: {e}")
            return False

        finally:
            if self.database.cursor is not None:
                self.database.cursor.close()
            self.database.close_connection()