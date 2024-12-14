import tkinter as tk
from tkinter import *
from tkinter import PhotoImage
from tkinter import messagebox, simpledialog
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime
from playsound import playsound
import threading
from Transaction import *
from Service import Service
import mysql.connector

service = Service()
active_user = None

userindex = 0
adminindex = 0

name_list = []
pass_list = []
adname_list = []
adpass_list = []
full_name_list =[]
email_list = []
contact_list = []
gender_list = []

entry1 = None
entry2 = None
c_entry1 = None
c_entry2 = None
o_entry0 = None
o_entry1 = None
o_entry2 = None
o_entry3 = None
product_entry = None
service_entry = None
pprice_entry = None
sprice_entry = None
pin_e = None
total_order = 0
total_price = 0
total_p_o = 0

#Fixed values list
combine_product = []
combine_service = []

#THIS WILL HOLD THE ORDERS OF PARTICULAR CUSTOMER
user_carts = {}
schedule_dict = {}
quantity_dict = {}
loc_dict = {}
pin = {}
amount = {}
transaction_bank = {} #THIS IS FOR CASHIN
transaction_order = {} #THIS IS FOR CASHOUT

product_list = ["Cat food", "Dog food", "Catnip"]
service_list = ["Pet Grooming", "Pet Training", "Pet Sitter"]
product_price = [250, 250, 150]
service_price = [1000, 3000, 2000]

if product_list:
    for x in range(len(product_list)):
        combine_product.append(f"{product_list[x]} - P{product_price[x]}")

if service_list:
    for x in range(len(service_list)):
        combine_service.append(f"{service_list[x]} - P{service_price[x]}")


#FOR PRODUCTS
# Update the ComboBox with the latest product and price data
def update_combo_options(combo_product):
    combo_product['values'] = combine_product
    combo_product.set('Select a product')

#FOR SERVICE
def update_combo_options1(combo_service):
    combo_service['values'] = combine_service
    combo_service.set('Select a service')


# Function to update\delete a product\services' name and price based on the selected item in ComboBox
def delete_products(combo_product,ids):
    global service
    product_selected = combo_product.get()

    if product_selected:
        # Check if the service_selected exists in combo_service values
        try:
            index = combo_product['values'].index(product_selected)
            service.delete_product(ids[index])
            update_combo_options1(combo_product)
            messagebox.showinfo("Success", f"{product_selected} deleted successfully.")
        except ValueError:
            messagebox.showwarning("Delete Error", f"Service '{product_selected}' not found in the options.")
    else:
        messagebox.showwarning("Delete Error", "Please select a service to delete.")

def update_products(combo_product, ids):
    global product_entry, pprice_entry
    product_change = product_entry.get()
    price_change = pprice_entry.get()


    if product_change and price_change.isdigit():
        price_change = int(price_change)

        product_selected = combo_product.get()
        if product_selected:
            try:

                index = combo_product['values'].index(product_selected)
                service.update_product(ids[index],product_change,price_change)
                update_combo_options(combo_product)


                product_entry.delete(0, tk.END)
                pprice_entry.delete(0, tk.END)

                messagebox.showinfo("Success", f"Product '{product_selected}' updated successfully.")
            except ValueError:
                messagebox.showwarning("Update Error", f"Product '{product_selected}' not found in the options.")
        else:
            messagebox.showwarning("Selection Error", "Please select a product to update.")
    else:
        messagebox.showwarning("Input Error", "Please enter valid product name and price.")

def delete_services(combo_service, ids):
    global service
    service_selected = combo_service.get()

    if service_selected:

        try:
            index = combo_service['values'].index(service_selected)
            service.delete_service(ids[index])
            update_combo_options1(combo_service)
            messagebox.showinfo("Success", f"{service_selected} deleted successfully.")
        except ValueError:
            messagebox.showwarning("Delete Error", f"Service '{service_selected}' not found in the options.")
    else:
        messagebox.showwarning("Delete Error", "Please select a service to delete.")


def update_services(combo_service, ids):
    global service_entry, sprice_entry
    service_change = service_entry.get()
    price_change = sprice_entry.get()


    if service_change and price_change.isdigit():
        price_change = int(price_change)

        service_selected = combo_service.get()
        if service_selected:
            try:

                index = combo_service['values'].index(service_selected)
                service.update_service(ids[index],service_change,price_change)

                update_combo_options1(combo_service)


                service_entry.delete(0, tk.END)
                sprice_entry.delete(0, tk.END)

                messagebox.showinfo("Success", f"Service '{service_selected}' updated successfully.")
            except ValueError:
                messagebox.showwarning("Update Error", f"Service '{service_selected}' not found in the options.")
        else:
            messagebox.showwarning("Selection Error", "Please select a service to update.")
    else:
        messagebox.showwarning("Input Error", "Please enter valid service name and price.")


def add_info(roots, user_name):
    global o_entry0, o_entry1, o_entry2, o_gender, name_size,active_user

    name = o_entry0.get()
    contact = o_entry1.get()
    email = o_entry2.get()
    gender = o_gender

    try:
        index = name_list.index(user_name)
    except ValueError:
        pass
        # messagebox.showerror("Error", "User not found in list.")
        # return

    if gender:  # Gender is set when either "Male" or "Female" is selected
        if contact:
            if name:
                # Update the associated lists with the new information
                # full_name_list[index] = name
                # contact_list[index] = contact
                # gender_list[index] = gender
                # email_list[index] = email if email else "  "
                res  = service.update_user_info(active_user.username,name,contact,email,gender)
                if res :
                    # Clear the entry fields after successful input
                    if o_entry0.winfo_exists():
                        o_entry0.delete(0, tk.END)
                    if o_entry1.winfo_exists():
                        o_entry1.delete(0, tk.END)
                    if o_entry2.winfo_exists():
                        o_entry2.delete(0, tk.END)

                    messagebox.showinfo("Add Info.", "Successfully Added Information!")
                    user_define(roots, None)
                else :
                    print("user not found")
            else:
                messagebox.showerror("Name error", "Please provide your full name.")
        else:
            messagebox.showerror("Contact Error", "Please provide a contact number.")
    else:
        messagebox.showerror("Gender error", "Please select a gender (Male or Female).")

def set_gender(gender_choice):
    global o_gender
    o_gender = gender_choice  # Update the gender when a radio button is clicked

def other_info(oroot, user_name):
    global o_entry0, o_entry1, o_entry2, o_gender
    o_gender = None  # Initialize the gender variable

    oroot.geometry("840x640")
    oroot.title("Add information")
    image4 = tk.PhotoImage(file=r"./Images/Add_.png")
    canvas = tk.Canvas(oroot, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image4, anchor="nw")

    text0 = tk.Label(oroot, text="Full name:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text0.place(x=450, y=245)
    o_entry0 = tk.Entry(oroot, bg="white", width=30)
    o_entry0.place(x=530, y=245)

    text1 = tk.Label(oroot, text="Contact:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text1.place(x=450, y=290)
    o_entry1 = tk.Entry(oroot, bg="white", width=30)
    o_entry1.place(x=530, y=290)

    text2 = tk.Label(oroot, text="Email:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text2.place(x=450, y=335)
    o_entry2 = tk.Entry(oroot, bg="white", width=30)
    o_entry2.place(x=530, y=340)

    text3 = tk.Label(oroot, text="Sex:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text3.place(x=450, y=380)

    male_rb = tk.Radiobutton(oroot, text="Male", value="Male", variable=o_gender, fg="cadet blue", bg='white', font=("Arial", 10, "bold"), command=lambda: set_gender("Male"))
    male_rb.place(x=530, y=375)

    female_rb = tk.Radiobutton(oroot, text="Female", value="Female", variable=o_gender, fg="cadet blue", bg='white', font=("Arial", 10, "bold"), command=lambda: set_gender("Female"))
    female_rb.place(x=600, y=375)

    exit_button = tk.Button(oroot, text="Exit", bg="IndianRed1", fg="white", width=8, font=("Arial", 9, "bold"),
                            command=lambda: exit_command(oroot))
    exit_button.place(x=560, y=490)

    back_button = tk.Button(oroot, text="Back", width=8, bg="SteelBlue3", fg="white", font=("Arial", 9, "bold"),
                            command=lambda: user_define(oroot, None))
    back_button.place(x=560, y=460)

    create_account_b = tk.Button(oroot, text="Add", width=8, bg="SteelBlue3", fg="white", font=("Arial", 8, "bold"),
                                 command=lambda: add_info(oroot, user_name))
    create_account_b.place(x=560, y=425)

    oroot.mainloop()


def exit_command(window):
    window.destroy()

#ADD NEW ELEMENT TO LIST
def add_button(user_c, user_name):
    global c_entry1, c_entry2, userindex, active_user

    userindex += 1

    username = c_entry1.get()
    password = c_entry2.get()

    if username and password:
        active_user = service.create_user(username,password)
        if active_user:
            messagebox.showinfo("Account Created", "Account successfully created!")
            other_info(user_c, username)
        # name_list.append(username)
        # pass_list.append(password)

        # full_name_list.append(" ")
        # gender_list.append(" ")
        # email_list.append(" ")
        # contact_list.append(" ")
    else:
        messagebox.showerror("Error", "Please enter both username and password.")


def log_in(log_user):
    global entry1, entry2, name_size, active_user

    name_size = entry1.get()
    pass_size = entry2.get()

    if name_size and pass_size:
        res = service.login_user(name_size,pass_size)
        if res:
            active_user = res
            if active_user.check_details():
                messagebox.showinfo("Log in", "Successfully logged in!")
                profile(log_user, name_size, pass_size)
            else:
                messagebox.showerror('Missing', 'Incomplete Details.')
                other_info(log_user, name_size)
                return
        else:
            messagebox.showerror("Error", "Invalid username/password. Please try again.")
    else:
        messagebox.askquestion("Error", "Please input name/password first.")

#FROM DEF USER
def profile(prof, nameu, passu):
    global  active_user
    prof.geometry("840x640")
    prof.title("YOUR ACCOUNT")
    products = []
    services =[]
    for prod in service.get_products():
        products.append(prod.full_text())
    for ser in  service.get_services():
        services.append(ser.full_text())
    loc_address = 0
    current_money = 0
    loc_idx = 0
    name = active_user.username
    fname = active_user.fullname
    email = active_user.email
    gender = active_user.sex
    contact = active_user.contact
    #
    # if name not in loc_dict:
    #     loc_dict[name] = {'products': []}
    #     loc_dict[name]['products'] = ['No address yet.']
    # if name not in amount:
    #     amount[name] = {"amounts": 0}
    # if name not in user_carts:
    #     user_carts[name] = {'products': [], 'services': []}
    # if name not in transaction_bank:
    #     transaction_bank[name] = {'Date': [], 'Cashin': []}
    # if name not in transaction_order:
    #     transaction_order[name] = {'Date': [], 'Cashout': []}

    canvas = tk.Canvas(prof, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)

    if gender.lower() == "female" or gender.lower() == "girl":
        imageG = tk.PhotoImage(file=r"./Images/ifgirl.png")
        canvas.create_image(0, 0, image=imageG, anchor="nw")
        prof.imageG = imageG
    elif gender.lower() == "male" or gender.lower() == "boy":
        imageB = tk.PhotoImage(file=r"./Images/ifboy.png")
        canvas.create_image(0, 0, image=imageB, anchor="nw")
        prof.imageB = imageB

    name_label = tk.Label(prof, text=f"Welcome, {fname}!", fg="black", bg="white", font=("Arial", 20, "bold"))
    name_label.place(x=240, y=220)

    prodcombo = ttk.Combobox(prof, text='Product' ,value=products, width=35)
    prodcombo.place(x=60, y=350)
    servcombo = ttk.Combobox(prof, text='Service' ,value=services, width=35)
    servcombo.place(x=345, y=350)


    b1 = tk.PhotoImage(file=r"./Images/cart1.png")
    b2 = tk.PhotoImage(file=r"./Images/remove_.png")
    b3 = tk.PhotoImage(file=r"./Images/location1.png")
    b4 = tk.PhotoImage(file=r"./Images/logout.png")
    b5 = tk.PhotoImage(file=r"./Images/addbasket.png")
    b6 = tk.PhotoImage(file=r"./Images/bank.png")

    def transaction(tran):
        global service,active_user
        transaction_window = tk.Toplevel()
        transaction_window.title("TRANSACTION HISTORY")
        transaction_window.geometry("400x600")
        transaction_window.config(bg="#104787")

        canvas = tk.Canvas(transaction_window, bg="#104787")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(transaction_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.configure(yscrollcommand=scrollbar.set)

        frame = tk.Frame(canvas, bg="#104787")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        original_image_in = Image.open(r"./Images/ticket.png")
        resized_image_in = original_image_in.resize((350, 80))
        photo_image_in = ImageTk.PhotoImage(resized_image_in)

        original_image_out = Image.open(r"./Images/cashout.png")
        resized_image_out = original_image_out.resize((350, 80))
        photo_image_out = ImageTk.PhotoImage(resized_image_out)

        combined_transactions = []
        user_transactions = service.get_user_transaction(active_user.id)
        for transac in user_transactions:
            if transac.type == TranType.CASH_IN.value:
                combined_transactions.append({
                    'date': transac.date,
                    'amount': transac.amount,
                    'type':  transac.type
                })

        for transac in user_transactions:
            if transac.type == TranType.CASHO_UT.value:
                combined_transactions.append({
                    'date': transac.date,
                    'amount': transac.amount,
                    'type': transac.type
                })

        combined_transactions.sort(key=lambda x: x['date'])

        for transaction in combined_transactions:
            record_frame = tk.Frame(frame, width=350, height=80, bg="#104787")
            record_frame.pack_propagate(False)

            if  transaction['type'] == TranType.CASH_IN.value:
                img_label = tk.Label(record_frame, image=photo_image_in, bg="#104787")
            elif  transaction['type'] == TranType.CASHO_UT.value:
                img_label = tk.Label(record_frame, image=photo_image_out, bg="#104787")

            img_label.place(x=10, y=5)

            if  transaction['type'] == TranType.CASH_IN.value:
                date_label = tk.Label(record_frame, text=f"Date: {transaction['date']}", bg="#104787", fg='white',
                                      font=('arial', 7))
                date_label.place(x=190, y=13)
                amount_label = tk.Label(record_frame, text=f"Amount: P{transaction['amount']}", bg="white",
                                        fg='#104787', font=("arial", 12, "bold"), justify='center')
            elif  transaction['type'] == TranType.CASHO_UT.value:
                date_label = tk.Label(record_frame, text=f"Date: {transaction['date']}", bg="#FC5786", fg='white',
                                      font=('arial', 7))
                date_label.place(x=190, y=13)
                amount_label = tk.Label(record_frame, text=f"Amount: -P{transaction['amount']}", bg="white",
                                        fg='#FC5786', font=("arial", 12, "bold"), justify='center')

            amount_label.place(x=180, y=40)
            record_frame.pack(fill="x", pady=5)

        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        transaction_window.mainloop()

    def update_time1(rwindow, transaction_type):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if transaction_type == 'Cashin':
            transaction_bank[name]['Date'].append(current_time)
        elif transaction_type == 'Cashout':
            transaction_order[name]['Date'].append(current_time)

    def cash_in(cashin):
        global  service, active_user
        while True:
            current_cash = simpledialog.askinteger("Cash In", "Enter amount: ")
            if current_cash:
                # amount[name]['amounts'] += current_cash
                service.add_update_bank(active_user.id,0,current_cash)
                update_cash_label()
                # update_time1(cashin, 'Cashin')
                # transaction_bank[name]['Cashin'].append(str(current_cash))
                service.add_transaction(active_user.id,current_cash,TranType.CASH_IN.value)
                break
            else:
                messagebox.showerror("Error", "Please enter an amount first.")

    def update_cash_label():
        global  active_user, service
        cash_amount_label.config(text=service.get_user_card(active_user.id).balance)

    def bank_account(bankact,pins):
        bankact.geometry("400x600")
        card = service.get_card(active_user.id,pins)
        canvas = tk.Canvas(bankact, width=400, height=600)
        canvas.place(relheight=1, relwidth=1)
        bank_image = tk.PhotoImage(file=r"./Images/bank_account.png")
        canvas.create_image(0, 0, image=bank_image, anchor="nw")
        bankact.bank_image = bank_image

        # BUTTON IMAGES
        tran = tk.PhotoImage(file=r"./Images/transaction.png")
        cashin = tk.PhotoImage(file=r"./Images/cash_in_.png")
        cashout = tk.PhotoImage(file=r"./Images/cash_out.png")
        home = tk.PhotoImage(file=r"./Images/home_.png")

        # LABEL WIDGET
        global cash_amount_label
        cash_amount_label = tk.Label(bankact, text=str(card.balance), bg='#033877', fg='white',
                                     font=('Arial', 25, 'bold'))
        cash_amount_label.place(x=165, y=140)

        # BUTTON WIDGETS
        tk.Button(bankact, image=tran, width=60, height=55, borderwidth=0, command=lambda:transaction(bankact)).place(x=55, y=505)
        tk.Button(bankact, image=cashin, width=60, height=55, borderwidth=0, command=lambda:cash_in(bankact)).place(x=170, y=505)
        tk.Button(bankact, image=cashout, width=60, height=55, borderwidth=0).place(x=290, y=505)
        tk.Button(bankact, image=home, width=70, height=65, borderwidth=0, command=lambda:profile(prof, nameu, passu)).place(x=30, y=23)

        bankact.mainloop()

    def validate_pin_input(input_value):
        return input_value.isdigit()

    def create_pin():
        global  service ,active_user
        while True:
            new_pin = simpledialog.askinteger("PIN", "Enter your PIN[0000]: ")
            if new_pin is None:
                messagebox.showerror("Error PIN", "You must enter a PIN.")
                return

            if len(str(new_pin)) != 4:
                messagebox.showerror("Error PIN", "Please enter a valid 4-digit PIN.")
            else:
                service.add_update_bank(active_user.id,new_pin)
                break

    def trypin(passwindow):
        global pin_e, active_user
        pins = pin_e.get()
        if not pins:
            messagebox.showerror('Error', 'Please enter your PIN first.')
            return
        if len(pins) != 4:
            messagebox.showerror('Error', 'Please enter a valid 4-digit PIN.')
            return

        if pins:
           if service.get_card(active_user.id,pins):
               messagebox.showinfo('Verified', 'Log in successfully!')
               pin_e.delete(0, tk.END)
               bank_account(passwindow,pins)
           else:
               messagebox.showerror('Error', 'The PIN you have entered doesn\'t exist. Please try again.')
               return

    def bank_login(bwindow):
        global pin_e, active_user
        bwindow.geometry("400x600")

        canvas = tk.Canvas(bwindow, width=400, height=600)
        canvas.place(relheight=1, relwidth=1)
        bank = tk.PhotoImage(file=r"./Images/bank_login.png")
        canvas.create_image(0, 0, image=bank, anchor="nw")
        bwindow.bank = bank

        bank_b = tk.PhotoImage(file=r"./Images/bank_button_login.png")


        tk.Button(bwindow, text='Back', fg='white', bg='#000060', borderwidth=0, highlightthickness=0,font=('arial', 10, 'bold'), command=lambda:profile(bwindow, nameu, passu)).place(x=10, y=10)

        if name not in pin:
            pin[name] = {'pins' : []}

        vcmd = (bwindow.register(validate_pin_input), "%S")
        pin_e= tk.Entry(bwindow, text='Enter your pin', bg='#140C75', fg='white', width=20, font=("Arial", 12),
                        validate="key", validatecommand=vcmd, justify='center')
        pin_e.place(x=110, y=330)
        tk.Button(bwindow, image=bank_b, width=135, height=55, highlightthickness=0, command=lambda:trypin(bwindow)).place(x=130,y=460)
        tk.Button(bwindow, text="Create PIN", bg="#311C92", fg="white", borderwidth=0, highlightthickness=0, font=("Arial", 10),
                  command=create_pin).place(x=160, y=550)

        bwindow.mainloop()

    def add_to_cart():
        global  service, active_user
        product = prodcombo.get()
        _service = servcombo.get()

        if product:
            while True:
                qt = simpledialog.askinteger("PRODUCT", "Please enter quantity: ")
                if qt is None or qt <= 0:
                    messagebox.showerror("Product error", "Please input a quantity.")
                else:
                    service.add_product_cart(active_user.id,product,qt)
                    messagebox.showinfo("Succesfully added", f"Added {product} to your cart!")
                    break

        if _service:
           # user_carts[name]['services'].append(_service)
           # # if name not in schedule_dict:
           # #     schedule_dict[name] = {'services': []}
           def submit(schedules, combo_year, combo_month, combo_day, entry_time, combo_am_pm):
               selected_year = combo_year.get()
               selected_month = combo_month.get()
               selected_day = combo_day.get()
               selected_time = entry_time.get()
               selected_am_pm = combo_am_pm.get()
               if selected_year and selected_month and selected_day and selected_time and selected_am_pm:
                   # schedule_dict[name]['services'].append(
                   #     f'{selected_month}/{selected_day}/{selected_year} {selected_time} {selected_am_pm}')
                   messagebox.showinfo("Succesfully added", f"Added {_service} to your cart!")
                   service.add_service_cart(active_user.id,_service,f'{selected_month}/{selected_day}/{selected_year} {selected_time} {selected_am_pm}')
                   schedules.destroy()
                   profile(None, nameu, passu)
               else:
                   messagebox.showerror('Schedule',
                                        'The schedule you have submitted is not enough. Please provide more details.')

           def choose_sched():
               schedules = tk.Tk()
               schedules.title("Scheduling GUI")
               schedules.geometry("350x230")

               # Create the labels for each combobox
               label_year = tk.Label(schedules, text="Year:", font=('arial', 10, 'bold'))
               label_year.grid(row=0, column=0, padx=10, pady=5)

               label_month = tk.Label(schedules, text="Month:", font=('arial', 10, 'bold'))
               label_month.grid(row=1, column=0, padx=10, pady=5)

               label_day = tk.Label(schedules, text="Day:", font=('arial', 10, 'bold'))
               label_day.grid(row=2, column=0, padx=10, pady=5)

               label_time = tk.Label(schedules, text="Time (HH:MM):", font=('arial', 10, 'bold'))
               label_time.grid(row=3, column=0, padx=10, pady=5)

               label_am_pm = tk.Label(schedules, text="AM/PM:", font=('arial', 10, 'bold'))
               label_am_pm.grid(row=4, column=0, padx=10, pady=5)

               # Year combobox with a range from 2024 to 2030
               years = [str(year) for year in range(2024, 2030)]
               combo_year = ttk.Combobox(schedules, values=years)
               combo_year.grid(row=0, column=1, padx=10, pady=5)

               # Month combobox with values from 1 to 12
               months = [str(month) for month in range(1, 13)]
               combo_month = ttk.Combobox(schedules, values=months)
               combo_month.grid(row=1, column=1, padx=10, pady=5)

               # Day combobox with values from 1 to 31
               days = [str(day) for day in range(1, 32)]
               combo_day = ttk.Combobox(schedules, values=days)
               combo_day.grid(row=2, column=1, padx=10, pady=5)

               # Combined Entry for Hour and Minute (HH:MM format)
               entry_time = tk.Entry(schedules)
               entry_time.grid(row=3, column=1, padx=10, pady=5)

               # AM/PM combobox
               am_pm = ["AM", "PM"]
               combo_am_pm = ttk.Combobox(schedules, values=am_pm)
               combo_am_pm.grid(row=4, column=1, padx=10, pady=5)

               # Submit button
               submit_button = tk.Button(schedules, text="Submit", font=('arial', 10, 'bold'),
                                         command=lambda: submit(schedules, combo_year, combo_month, combo_day,
                                                                entry_time, combo_am_pm))
               submit_button.grid(row=6, column=0, columnspan=3, pady=14)

               schedules.mainloop()

           choose_sched()


        if product or _service:
            messagebox.showinfo("Succesfully added", f"Added {product} and {_service} to your cart!")
        elif product:
            messagebox.showinfo("Succesfully added", f"Added {product} to your cart!")
        elif _service:
            messagebox.showinfo("Succesfully added", f"Added {_service} to your cart!")
        else:
            messagebox.showerror('Order error', 'Please choose any products and services you desire.')

    def get_product_price(product_str):
        if product_str:
            parts = product_str.split(' - P')
            if len(parts) == 2:
                try:
                    return int(parts[1])
                except ValueError:
                    return 0
        return 0

    def get_service_price(service_str):
        if service_str:
            parts = service_str.split(' - P')
            if len(parts) == 2:
                try:
                    return int(parts[1])
                except ValueError:
                    return 0
        return 0

    def validation(fwindow, total_amount):
        global total_order, active_user,service
        if 'No address yet.' in active_user.location:
            messagebox.showerror('No Location', 'Please provide a location first.')
            checkoutf(fwindow, total_order)
            return

        if service.get_user_card(active_user.id).balance == 0:
            messagebox.showerror('No Balance', 'Please insert a balance in your bank account.')
            checkoutf(fwindow, total_order)
            return

        if total_order == 0:
            messagebox.showerror('No order', 'Please choose any products or services you desire first.')
            return

        if service.get_user_card(active_user.id).balance < total_order:
            messagebox.showerror('Insufficient Balance', 'Your balance is not enough to pay for the total order.')
            return

        pay = simpledialog.askinteger("Payment", "Payment: ")

        if pay is not None:
            if pay < total_order:
                messagebox.showerror('Not enough',
                                     'The amount you have entered isn\'t enough to pay the total bill. Please enter a correct amount.')
                return

            if pay > service.get_user_card(active_user.id).balance:
                messagebox.showerror('Insufficient Balance', 'Your payment exceeds the available balance.')
                return

            deduc_balance = pay - service.get_user_card(active_user.id).balance
            change = pay - total_order
            pass_order = total_order
            new_balance = change - deduc_balance
            # transaction_order[name]['Cashout'].append(total_amount)
            service.add_transaction(active_user.id,total_amount,TranType.CASHO_UT.value)
            # update_time1(fwindow, 'Cashout')
            service.update_balance(active_user.id,new_balance)

            reciept(fwindow, pass_order, change, new_balance)

            total_order = 0
            #reset the total_order

        else:
            messagebox.showerror('Invalid Payment', 'Please enter a valid payment amount.')

    def play_sound():
        playsound(r'C:\Users\Nestor\Music\thankyou.mp3')

    def update_time(rwindow, time_label):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_label.config(text=current_time)

    def reciept(rwindow, total_amount_order, change, current_balance):
        rwindow.geometry("400x600")
        rwindow.title("RECEIPT")

        threading.Thread(target=play_sound, daemon=True).start()

        canvas = tk.Canvas(rwindow, width=400, height=600)
        canvas.place(relheight=1, relwidth=1)
        photo = tk.PhotoImage(file=r"./Images/recieptfinal.png")
        canvas.create_image(0, 0, image=photo, anchor="nw")
        rwindow.photo = photo

        tk.Label(rwindow, text=total_amount_order, bg='#181818', fg='white', font=('arial', 20, 'bold')).place(x=165, y=190)#TOTAL ORDER
        tk.Label(rwindow, text=change, bg='#181818', fg='white', font=('arial', 20, 'bold')).place(x=165, y=260)#CHANGE
        tk.Label(rwindow, text=fname, bg= '#181818', fg='white', font=("arial", 10, "bold")).place(x=220, y=430) #NAME
        tk.Label(rwindow, text=contact, bg='#181818', fg='white', font=("arial",10, "bold")).place(x=220 ,y=355) #CONTACT
        tk.Label(rwindow, text=f'P{current_balance}', bg='#181818', fg='white', font=('arial', 10, 'bold')).place(x=60, y=440)
        time_label = tk.Label(rwindow, bg='#181818', fg='white', font=("arial", 10, "bold"))
        time_label.place(x=60, y=360)
        update_time(rwindow, time_label)
        tk.Button(rwindow, text='Done', bg='#181818', fg='white', font=('arial', 12, 'bold'), command=lambda:profile(rwindow, nameu, passu)).place(x=160, y=490)#BACK TO PROFILE

        user_carts[name]['products'].clear()
        user_carts[name]['services'].clear()
        quantity_dict[name]['products'].clear()
        schedule_dict[name]['services'].clear()

        rwindow.mainloop()

    if name in amount and 'amounts' in amount[name] and amount[name]['amounts'] > 0:
        current_money = 1

    def checkoutf(cwindow, total):
        global active_user,service
        cwindow.geometry("400x600")
        cwindow.title("CHECKOUT")

        global cash_amount_label
        total_amount = 0

        canvas = tk.Canvas(cwindow, width=400, height=600)
        canvas.place(relheight=1, relwidth=1)
        bgcout = tk.PhotoImage(file=r"./Images/bgnow.png")
        canvas.create_image(0, 0, image=bgcout, anchor="nw")
        cwindow.bgcout = bgcout

        buynow = tk.PhotoImage(file=r"./Images/buynow.png")
        backnow = tk.PhotoImage(file=r"./Images/backnow.png")

        total_amount = total

        tk.Label(cwindow, text=f"P{total_amount}", bg="white", font=("Arial", 24, "bold")).place(x=70, y=530)
        tk.Button(cwindow, image=buynow, width=160, height=40, command=lambda:(validation(cwindow, total_amount))).place(x=210,y=530)
        tk.Button(cwindow, image=backnow, width=40, height=20, command=lambda:view_cart(cwindow)).place(x=10, y=10)
        tk.Label(cwindow, text=f"Name: {fname}", bg='white', font=('arial', 12, 'bold')).place(x=30,y=250)
        tk.Label(cwindow, text=f"Email: {email}", bg='white', font=('arial', 12, 'bold')).place(x=30, y=280)
        tk.Label(cwindow, text=f"Contact: {contact}", bg='white', font=('arial', 12, 'bold')).place(x=30, y=310)
        cash_amount_label = tk.Label(cwindow, text=f"Balance: {service.get_user_card(active_user.id).balance}", bg='white', font=('arial', 12, 'bold')).place(x=30, y=340)
        location_text = active_user.location
        tk.Label(cwindow, text="Location: " + location_text, bg='white', font=('arial', 12, 'bold')).place(x=30, y=370)

        cwindow.mainloop()

    def addloc():
        while True:
            location = simpledialog.askstring("Location", "Please enter your location: ")
            if loc_dict[name]['products']:
                loc_dict[name]['products'][0] = location
                messagebox.showinfo("Location", "Succesfully changed location!")
                break
            elif location and location.strip() != "":
                loc_dict[name]['products'].append(location)
                messagebox.showinfo("Location", "Succesfully added location!")
                break
            else:
                messagebox.showerror("Invalid location", "Please enter your location")

    def removecart(rwindow):
        global  service, active_user
        removeval = None

        if service.get_user_cart(active_user.id).service is None and service.get_user_cart(active_user.id).product is None:
            messagebox.showerror('No order', 'Order any products or services you want first.')
            return

        else:
            removeval = simpledialog.askstring('Remove', 'Enter the ID of the product/service: ')

        if removeval:
            removeval_lower = removeval.lower()
            product_found = False
            service_found = False

            if service.remove_cart(removeval):
                messagebox.showinfo("Removed", f"Removed {removeval} from your cart.")
                view_cart(rwindow)
            else:
                messagebox.showerror("Not found", f"{removeval} not found in your cart.")
            # # Remove the product from the cart if it matches the input
            # for i, p in enumerate(user_carts[name]['products']):
            #     if p.lower() == removeval_lower:
            #         user_carts[name]['products'].remove(p)
            #         if removeval_lower in [p.lower() for p in user_carts[name]['products']]:
            #             quantity_dict[name]['products'].remove(quantity_dict[name]['products'][i])
            #         messagebox.showinfo("Removed", f"Removed {p} from your cart.")
            #         product_found = True
            #         view_cart(rwindow)
            #         break
            #
            # # If product wasn't found, check for services
            # if not product_found:
            #     for i, service in enumerate(user_carts[name]['services']):
            #         if service.lower() == removeval_lower:
            #             user_carts[name]['services'].remove(service)
            #             if removeval_lower in [service.lower() for service in user_carts[name]['services']]:
            #                 schedule_dict[name]['services'].remove(schedule_dict[name]['services'][i])
            #             messagebox.showinfo("Removed", f"Removed {service} from your cart.")
            #             service_found = True
            #             view_cart(rwindow)
            #             break

                # If neither product nor service was found
                # if not service_found:

        else:
            messagebox.showerror("Input error", "Please enter a valid product or service name.")

    def format_id(_id):
        return f"{_id:03}"

    def view_cart(cart_window):
        global total_order , service, active_user
        total_order = 0

        photobg = tk.PhotoImage(file=r"./Images/viewcart_.png")
        checkoutbutton = tk.PhotoImage(file=r"./Images/checkout2.png")
        backnow = tk.PhotoImage(file=r"./Images/backnow.png")
        print(service.get_user_cart(active_user.id).product)
        total_price = 0
        cart_content = "                                YOUR CART :\n\n"
        if service.get_user_cart(active_user.id).product:
             cart_content += "                               PRODUCTS:\n"
             _products =  service.get_user_cart(active_user.id).product
             for prod in _products:
                product_price = prod.get_price()
                total_price += product_price * prod.quantity
                cart_content += f"P{format_id(prod.id)} - {prod.product} (Quantity: {prod.quantity}, Total: P{product_price * prod.quantity})\n"
                total_order += product_price * prod.quantity

        if service.get_user_cart(active_user.id).service:
            cart_content += "                                SERVICES:\n"
            _service = service.get_user_cart(active_user.id).service
            for ser in _service:
                  service_price = ser.get_price()
                  total_price += service_price
                  cart_content += f"S{format_id(ser.id)} - {ser.service} (Scheduled: {ser.details})\n"
                  total_order += service_price

        cart_window.geometry("400x600")

        canvas1 = tk.Canvas(cart_window, width=400, height=600)
        canvas1.place(relheight=1, relwidth=1)

        cart_window.photobg = photobg
        canvas1.create_image(0, 0, image=photobg, anchor="nw")

        frame = tk.Frame(cart_window, bg="white", width=380, height=400)
        frame.place(x=10, y=140)

        tk.Button(cart_window, image=backnow, width=40, height=20, command=lambda: profile(cart_window, nameu, passu)).place(x=10, y=10)
        tk.Button(cart_window, text='Remove', fg='#3A54B1', bg='white', font=('arial', 10, 'bold'), command=lambda:removecart(cart_window)).place(x=330, y=10)

        cart_label = tk.Label(frame, text=cart_content, bg="white", fg="RoyalBlue3", font=("Comic Sans MS", 10),
                              justify="left")
        cart_label.pack(padx=10, pady=10, fill="both", expand=True)

        checkouts = tk.Button(cart_window, image=checkoutbutton, height=20, width=70,
                              command=lambda: checkoutf(cart_window, total_order))
        cart_window.checkoutbutton_image = checkoutbutton
        checkouts.place(x=290, y=565)

        total_order_label = tk.Label(cart_window, text=f"P{total_order}", bg="white", fg="RoyalBlue3",
                                     font=("Comic Sans MS", 11))
        total_order_label.place(x=150, y=565)

        cart_window.mainloop()

    dep = tk.Button(prof, image=b6, height=40, width=100, command=lambda:bank_login(prof))
    dep.place(x=650, y=315)
    add = tk.Button(prof, image=b5, height=40, width=100, command=add_to_cart)
    add.place(x=650, y=390)
    cart = tk.Button(prof, image=b1, height=40, width=100, command=lambda:view_cart(prof))
    cart.place(x=650, y=460)
    loc = tk.Button(prof, image=b3, height=40, width=100, command=addloc)
    loc.place(x=650, y=530)
    logout = tk.Button(prof, image=b4, height=40, width=100, command=lambda: user_define(prof, None))
    logout.place(x=700, y=10)

    prof.mainloop()
# END OF PROFILE FUNCTION


def create_account(user_c):
    global c_entry1, c_entry2
    user_c.geometry("840x640")
    user_c.title("Sign Up Account")

    name_list = []
    pass_list = []

    image3 = tk.PhotoImage(file=r"./Images/Catcat.png")
    canvas = tk.Canvas(user_c, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image3, anchor="nw")

    text1 = tk.Label(user_c, text="Username:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text1.place(x=450, y=290)
    c_entry1 = tk.Entry(user_c, bg="white", width=30)
    c_entry1.place(x=530, y=290)
    text2 = tk.Label(user_c, text="Password:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text2.place(x=450, y=335)
    c_entry2 = tk.Entry(user_c, bg="white", width=30)
    c_entry2.place(x=530, y=340)
    exit_button = tk.Button(user_c, text="Exit", bg="IndianRed1", fg="white", width=8, font=("Arial", 9, "bold"),
                            command=lambda: exit_command(user_c))
    exit_button.place(x=560, y=445)
    back_button = tk.Button(user_c, text="Back", width=8, bg="SteelBlue3", fg="white", font=("Arial", 9, "bold"),
                            command=lambda: user_define(user_c, None))
    back_button.place(x=560, y=410)

    create_account_b = tk.Button(user_c, text="Create", width=8, bg="SteelBlue3", fg="white", font=("Arial", 8, "bold"), command=lambda: add_button(user_c, c_entry1))
    create_account_b.place(x=560, y=375)

    user_c.mainloop()


def user_define(user, menu=None):
    global entry1, entry2
    #WINDOW
    if menu is not None:
       menu.destroy()
    else:
        pass
    user.geometry("840x640")
    user.title("USER")

    image2 = tk.PhotoImage(file=r"./Images/pupu.png")
    canvas = tk.Canvas(user, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image2, anchor="nw")

    # MAIN BODY
    text1 = tk.Label(user, text="Username:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text1.place(x=450, y=290)
    entry1 = tk.Entry(user, bg="white", width=30)
    entry1.place(x=530, y=290)
    text2 = tk.Label(user, text="Password:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text2.place(x=450, y=335)
    entry2 = tk.Entry(user, bg="white", width=30)
    entry2.place(x=530, y=340)
    login_account_b = tk.Button(user, text="Log In", bg="SteelBlue3", fg="white", width=8, font=("Arial", 9, "bold"), command=lambda:log_in(user))
    login_account_b.place(x=560, y=375)
    exit_button = tk.Button(user, text="Exit", bg="IndianRed1", fg="white", width=8, font=("Arial", 9, "bold"),
                            command=lambda: exit_command(user))
    exit_button.place(x=560, y=445)
    back_button = tk.Button(user, text="Back", width=8, bg="SteelBlue3", fg="white", font=("Arial", 9, "bold"), command=lambda:role_function(user))
    back_button.place(x=560, y=410)

    create_account_b = tk.Button(user, text="Sign up", width=7, bg="white", fg="SteelBlue3", borderwidth=0,
                                 highlightthickness=0, font=("Arial", 8, "bold"), command=lambda:create_account(user))
    create_account_b.place(x=605, y=500)
    tk.Label(user, text="Don't have an account? ", bg="white", fg="gray").place(x=480, y=500)

    user.mainloop()

#START OF FUNCTION FOR ADMIN ADD/DELETE PRODUCTS
def delproducts(delete):
    global service
    delete.geometry("840x640")
    delete.title("ADD PRODUCTS")
    image7 = tk.PhotoImage(file=r"./Images/deletewindow.png")

    canvas = tk.Canvas(delete, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image7, anchor="nw")
    products = []
    ids = []
    for prod in service.get_products():
        products.append(prod.full_text())
        ids.append(prod.id)
    combo_product = ttk.Combobox(delete, values=products, width=50)
    combo_product.set("Select a product")
    combo_product.place(x=100, y=150)

    delpro = tk.PhotoImage(file=r"./Images/deleteb.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    b1 = tk.Button(delete, image=delpro, width=100, height=40, command=lambda: delete_products(combo_product,ids)).place(
        x=590, y=310)
    b2 = tk.Button(delete, image=backpro, width=100, height=40, command=lambda: delete_f(delete)).place(x=590, y=390)

    delete.mainloop()

def upproducts(update):
    global product_entry, pprice_entry
    update.geometry("840x640")
    update.title("ADD PRODUCTS")
    image7 = tk.PhotoImage(file=r"./Images/updatewindow_.png")

    canvas = tk.Canvas(update, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image7, anchor="nw")

    addpro = tk.PhotoImage(file=r"./Images/addprod.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    product_entry = tk.Entry(update, width=30)
    product_entry.place(x=550, y=280)
    pprice_entry = tk.Entry(update, width=30)
    pprice_entry.place(x=550, y=330)
    products = []
    ids = []
    for prod in service.get_products():
        products.append(prod.full_text())
        ids.append(prod.id)
    combo_product = ttk.Combobox(update, values=products, width=50)
    combo_product.set("Select a product")
    combo_product.place(x=100, y=150)

    b1 = tk.Button(update, image=addpro,  width=100, height=40, command=lambda:update_products(combo_product,ids)).place(x=590, y=380)
    b2 = tk.Button(update, image=backpro, width=100, height=40, command=lambda:update_f(update)).place(x=590, y=460)

    update.mainloop()
#END

#START OF FUNCTION FOR ADMIN ADD/DELETE SERVICES
def delservices(delete):
    global service
    delete.geometry("840x640")
    delete.title("DELETE SERVICES")
    image7 = tk.PhotoImage(file=r"./Images/deletewindow.png")

    canvas = tk.Canvas(delete, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image7, anchor="nw")
    services = []
    ids = []
    for ser in service.get_services():
        services.append(ser.full_text())
        ids.append(ser.id)

    combo_service = ttk.Combobox(delete, values=services, width=50)
    combo_service.set("Select a services")
    combo_service.place(x=100, y=150)

    delpro = tk.PhotoImage(file=r"./Images/deleteb.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    b1 = tk.Button(delete, image=delpro, width=100, height=40, command=lambda: delete_services(combo_service,ids)).place(
        x=590, y=310)
    b2 = tk.Button(delete, image=backpro, width=100, height=40, command=lambda: delete_f(delete)).place(x=590, y=390)

    delete.mainloop()

def upservices(update):
    global service_entry, sprice_entry
    update.geometry("840x640")
    update.title("ADD PRODUCTS")
    image7 = tk.PhotoImage(file=r"./Images/updatewindow_.png")

    canvas = tk.Canvas(update, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image7, anchor="nw")

    addser = tk.PhotoImage(file=r"./Images/addser_.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    service_entry = tk.Entry(update, width=30)
    service_entry.place(x=550, y=280)
    sprice_entry = tk.Entry(update, width=30)
    sprice_entry.place(x=550, y=330)
    services = []
    ids = []
    for ser in service.get_services():
        services.append(ser.full_text())
        ids.append(ser.id)
    combo_service = ttk.Combobox(update, values=services, width=50)
    combo_service.set("Select a product")
    combo_service.place(x=100, y=150)

    b1 = tk.Button(update, image=addser, width=100, height=40, command=lambda: update_services(combo_service,ids)).place(
        x=590, y=380)
    b2 = tk.Button(update, image=backpro, width=100, height=40, command=lambda: update_f(update)).place(x=590, y=460)

    update.mainloop()
#END


#START OF FUNCTIONS FOR UPDATE AND DELETE
def delete_f(delete):
    delete.geometry("840x640")
    delete.title("ADMIN DELETE")
    image6 = tk.PhotoImage(file=r"./Images/ask.png")

    canvas = tk.Canvas(delete, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image6, anchor="nw")

    pro = tk.PhotoImage(file=r"./Images/product.png")
    ser = tk.PhotoImage(file=r"./Images/Services.png")
    back = tk.PhotoImage(file=r"./Images/backagain.png")

    b1 = tk.Button(delete, image=ser, width=100, height=40, command=lambda: delservices(delete)).place(x=270, y=300)
    b2 = tk.Button(delete, image=pro, width=100, height=40, command=lambda: delproducts(delete)).place(x=100, y=300)
    b3 = tk.Button(delete, image=back, width=100, height=40, command=lambda: admin_define(delete, None)).place(x=440,
                                                                                                               y=300)

    delete.mainloop()

def update_f(update):
    update.geometry("840x640")
    update.title("ADMIN UPDATE")
    image6 = tk.PhotoImage(file=r"./Images/ask.png")

    canvas = tk.Canvas(update, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image6, anchor="nw")

    pro = tk.PhotoImage(file=r"./Images/product.png")
    ser = tk.PhotoImage(file=r"./Images/Services.png")
    back = tk.PhotoImage(file=r"./Images/backagain.png")

    #BUTTONS OF LOCATION TO UPDATE
    b1 = tk.Button(update, image=ser, width=100, height=40, command=lambda:upservices(update)).place(x=270, y=300)
    b2 = tk.Button(update, image=back, width=100, height=40, command=lambda:admin_define(update, None)).place(x=440, y=300)
    b3 = tk.Button(update, image=pro, width=100, height=40, command=lambda:upproducts(update)).place(x=100, y=300)

    update.mainloop()
#END

#START OF FUNCTION FOR ADD SERVICE
def add_products(combo_product):
    global product_entry, pprice_entry
    product = product_entry.get()
    price = pprice_entry.get()

    if product and price:

        service.add_product(product,price)
        update_combo_options(combo_product)
        product_entry.delete(0, tk.END)
        pprice_entry.delete(0, tk.END)
        messagebox.showinfo("Add Info.", f"\"{product}\" successfully Added!")
    else:
        messagebox.showerror("Error", "Please provide any new product and price.")
def add_services(combo_service):
    global service_entry, sprice_entry, service
    _service = service_entry.get()
    price = sprice_entry.get()

    if _service and price:
        # service_list.append(service)
        # service_price.append(price)
        service.add_service(_service,price)
        combine_service.append(f"{_service} - P{price}")
        update_combo_options1(combo_service)
        service_entry.delete(0, tk.END)
        sprice_entry.delete(0, tk.END)
        messagebox.showinfo("Add Info.", f"\"{_service}\" successfully Added!")
    else:
        messagebox.showerror("Error", "Please provide new service and price.")

def add_product(add):
    global product_entry, pprice_entry
    add.geometry("840x640")
    add.title("ADD PRODUCTS")
    image = tk.PhotoImage(file=r"./Images/addproducts.png")

    canvas = tk.Canvas(add, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image, anchor="nw")

    addser1 = tk.PhotoImage(file=r"./Images/addprod.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    product_entry = tk.Entry(add, width=30)
    product_entry.place(x=550, y=280)
    pprice_entry = tk.Entry(add, width=30)
    pprice_entry.place(x=550, y=330)
    products = []
    for prod in service.get_products():
        products.append(prod.full_text())
    combo_product = ttk.Combobox(add, values=products, width=50)
    combo_product.set("Add a product")
    combo_product.place(x=100, y=150)

    b1 = tk.Button(add, image=addser1, width=100, height=40, command=lambda: add_products(combo_product)).place(
        x=590, y=380)
    b2 = tk.Button(add, image=backpro, width=100, height=40, command=lambda: admin_define(add, None)).place(x=590,
                                                                                                            y=460)
    add.mainloop()

def add_service(add):
    global service_entry, sprice_entry
    add.geometry("840x640")
    add.title("ADD SERVICES")
    image = tk.PhotoImage(file=r"./Images/addservice.png")

    canvas = tk.Canvas(add, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image, anchor="nw")

    addser1 = tk.PhotoImage(file=r"./Images/addser_.png")
    backpro = tk.PhotoImage(file=r"./Images/back.png")

    service_entry = tk.Entry(add, width=30)
    service_entry.place(x=550, y=280)
    sprice_entry = tk.Entry(add, width=30)
    sprice_entry.place(x=550, y=330)
    services = []
    for ser in service.get_services():
        services.append(ser.full_text())
    combo_service = ttk.Combobox(add, values=services, width=50)
    combo_service.set("Add a service")
    combo_service.place(x=100, y=150)

    b1 = tk.Button(add, image=addser1, width=100, height=40, command=lambda: add_services(combo_service)).place(
        x=590, y=380)
    b2 = tk.Button(add, image=backpro, width=100, height=40, command=lambda: admin_define(add, None)).place(x=590,
                                                                                                            y=460)

    add.mainloop()
#END

#START OF ADMIN ROLE
def add_button_ad(create, c_entry1, c_entry2):
    name_size = c_entry1.get()
    pass_size = c_entry2.get()

    if name_size and pass_size:
        # adname_list.append(name_size)
        # adpass_list.append(pass_size)
        if service.create_admin(name_size,pass_size):
            c_entry1.delete(0, tk.END)
            c_entry2.delete(0, tk.END)
            messagebox.showinfo("Sign up", "Successfully Created Account!")
            admin_log_in(create, None)
        else:
            messagebox.showwarning("error", "something went wrong.")
    else:
        messagebox.askquestion("Error", "Please input name/password first.")


def adlogin(login, entry1, entry2):
    global service
    name_size = entry1.get()
    pass_size = entry2.get()

    if name_size and pass_size:
        if service.login_admin(name_size,pass_size):
            messagebox.showinfo("Log in", "Successfully Logged In!")
            entry1.delete(0, tk.END)
            entry2.delete(0, tk.END)
            admin_define(login, None)
        else:
            messagebox.showerror("Error", "Invalid password/username. Please try again.")
    else:
        messagebox.askquestion("Error", "Please input name/password first.")

images = None
def addcreate(create):
    global images
    create.geometry("840x640")
    create.title("Sign Up Account")

    if images is None:
       images = tk.PhotoImage(file=r"./Images/Catcat.png")

    canvas = tk.Canvas(create, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=images, anchor="nw")

    text1 = tk.Label(create, text="Username:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text1.place(x=450, y=290)
    c_entry1 = tk.Entry(create, bg="white", width=30)
    c_entry1.place(x=530, y=290)
    text2 = tk.Label(create, text="Password:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text2.place(x=450, y=335)
    c_entry2 = tk.Entry(create, bg="white", width=30)
    c_entry2.place(x=530, y=340)

    exit_button = tk.Button(create, text="Exit", bg="IndianRed1", fg="white", width=8, font=("Arial", 9, "bold"),
                            command=create.quit)  # Close window on exit
    exit_button.place(x=560, y=445)

    back_button = tk.Button(create, text="Back", width=8, bg="SteelBlue3", fg="white", font=("Arial", 9, "bold"),
                            command=lambda: user_define(create, None))
    back_button.place(x=560, y=410)

    create_account_b = tk.Button(create, text="Create", width=8, bg="SteelBlue3", fg="white", font=("Arial", 8, "bold"),
                                 command=lambda: add_button_ad(create, c_entry1, c_entry2))
    create_account_b.place(x=560, y=375)


def admin_log_in(login, menu=None):
    if menu is not None:
        menu.destroy()

    login.geometry("840x640")
    login.title("Admin Login")

    image = tk.PhotoImage(file=r"./Images/pupu.png")
    canvas = tk.Canvas(login, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image, anchor="nw")

    text1 = tk.Label(login, text="Username:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text1.place(x=450, y=290)
    entry1 = tk.Entry(login, bg="white", width=30)
    entry1.place(x=530, y=290)

    text2 = tk.Label(login, text="Password:", fg="cadet blue", bg="white", font=("Arial", 10, "bold"))
    text2.place(x=450, y=335)
    entry2 = tk.Entry(login, bg="white", width=30)
    entry2.place(x=530, y=340)

    login_account_b = tk.Button(login, text="Log In", bg="SteelBlue3", fg="white", width=8, font=("Arial", 9, "bold"),
                                command=lambda: adlogin(login, entry1, entry2))
    login_account_b.place(x=560, y=375)

    exit_button = tk.Button(login, text="Exit", bg="IndianRed1", fg="white", width=8, font=("Arial", 9, "bold"),
                            command=lambda: exit_command(login))  # Exit button command
    exit_button.place(x=560, y=445)

    back_button = tk.Button(login, text="Back", width=8, bg="SteelBlue3", fg="white", font=("Arial", 9, "bold"),
                            command=lambda: role_function(login))  # Back button command
    back_button.place(x=560, y=410)

    create_account_b = tk.Button(login, text="Sign up", width=7, bg="white", fg="SteelBlue3", borderwidth=0,
                                 highlightthickness=0, font=("Arial", 8, "bold"),
                                 command=lambda: addcreate(login))
    create_account_b.place(x=605, y=500)

    tk.Label(login, text="Don't have an account? ", bg="white", fg="gray").place(x=480, y=500)

    login.mainloop()

def admin_define(admin, menu=None):

    if menu is not None:
        menu.destroy()
    else:
        pass
    admin.geometry("840x640")
    admin.title("ADMIN")
    image5 = tk.PhotoImage(file=r"./Images/adminpart.png")
    canvas = tk.Canvas(admin, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image5, anchor="nw")

    #IMAGES FOR BUTTONS
    add_ser = tk.PhotoImage(file=r"./Images/addser_.png")
    add_prod = tk.PhotoImage(file=r"./Images/addprod.png")
    delete = tk.PhotoImage(file=r"./Images/deleteb.png")
    update = tk.PhotoImage(file=r"./Images/updateb.png")
    view_user = tk.PhotoImage(file=r"./Images/viewuser.png")
    back = tk.PhotoImage(file=r"./Images/back.png")
    #END

    button1 = tk.Button(admin, image=add_ser, width=100, height=40, command=lambda:add_service(admin)).place(x=250,y=290)
    button2 = tk.Button(admin, image=add_prod, width=100, height=40, command=lambda:add_product(admin)).place(x=250,y=380)
    button3 = tk.Button(admin, image=delete, width=100, height=40, command=lambda:delete_f(admin)).place(x=250,y=470)
    button4 = tk.Button(admin, image=update, width=100, height=40, command=lambda:update_f(admin)).place(x=450,y=290)
    button5 = tk.Button(admin, image=view_user, width=100, height=40).place(x=450,y=380)
    button6 = tk.Button(admin, image=back, width=100, height=40, command=lambda:role_function(admin)).place(x=450,y=470)

    admin.mainloop()

def file1(root1):
    root1.geometry("950x470")
    root1.title("www.FurryPetS.com")

    image = tk.PhotoImage(file=r"./Images/about.png")
    image = image.subsample(3, 3)

    canvas = tk.Canvas(root1, width=840, height=660)
    canvas.place(relheight=1, relwidth=1)

    canvas.create_image(0, 0, image=image, anchor="nw")

    menu = tk.Menu(root1)
    root1.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="About", menu=filemenu)
    filemenu.add_command(label="Back to role selection", command=lambda: role_function(root1))
    filemenu.add_separator()

    root1.mainloop()


root0 = tk.Tk()
root0.geometry("500x223")
# to open window + .
"""
● ○ ▢ × –
"""

def role_function(root):
    root.geometry("840x640")
    root.title("www.FurryPetShop.com")

    b1 = tk.PhotoImage(file=r"./Images/admin.png")
    b2 = tk.PhotoImage(file=r"./Images/user.png")

    image1 = tk.PhotoImage(file=r"./Images/doggiephone3.png")
    canvas = tk.Canvas(root, width=840, height=640)
    canvas.place(relheight=1, relwidth=1)
    canvas.create_image(0, 0, image=image1, anchor="nw")

    #LABELS
    admin_button = tk.Button(root,image=b1,width = 120, height=60,borderwidth=0,
                                 highlightthickness=0, font = ("Comic Sans MS", 8, "bold"), command =lambda: admin_log_in(root, menu))
    admin_button.place(x=570, y=270)
    student_button = tk.Button(root, image=b2,width = 120, height=60, borderwidth=0,
                                 highlightthickness=0,font = ("Comic Sans MS", 8, "bold"), command = lambda:user_define(root, menu))
    student_button.place(x=570,y=350)
    #MENU
    menu = tk.Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    menu.add_cascade(label="About", menu=filemenu)
    filemenu.add_command(label="Shop", command=lambda:file1(root))
    filemenu.add_separator()
    root.mainloop()

role_function(root0)

root0.mainloop()