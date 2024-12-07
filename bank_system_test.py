# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:52:07 2024

@author: KS
"""
import re
import tkinter
from tkinter import messagebox, simpledialog
from customer_account_test import CustomerAccount
from admin_test import Admin

accounts_list = []
admins_list = []

class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        self.overdraft_limits = {}
        self.load_bank_data()
        
        self.mw = tkinter.Tk()
        self.mw.title("Bank System")
        self.mw.geometry("500x125")
        self.mw.grab_set()
        
        self.frame_1 = tkinter.Frame(self.mw)
        
        tkinter.Label(self.mw, text="Welcome to the Python Bank System", font=("Arial", 14)).pack(pady=10)
        login_button = tkinter.Button(self.mw, text="Admin Login", command=self.run_main_options)
        quit_button = tkinter.Button(self.mw, text="Quit", command=self.mw.quit)
        
        login_button.pack(side="top")
        quit_button.pack(side="top")
        
        self.frame_1.pack()
        self.mw.mainloop()
    
    def load_bank_data(self):
        
        file_1 = r"C:\Users\crmut\OneDrive\Desktop\Software development\customers.txt"
        customer_file = open("{}".format(file_1), 'r')
        read_customer_file = customer_file.readline()
        while read_customer_file != "":
            i = re.split(r',\s*(?![^[]*\])', read_customer_file)
            fname = i[0]
            lname = i[1]
            address_list = i[2]
            address = eval(address_list)
            balance = float(i[4])
            account_no = i[3]
            account_name = i[5]
            interest_rate = i[6]
            overdraft_limit = float(i[7])
            customer = CustomerAccount(fname, lname, address, account_no, balance, account_name, interest_rate, overdraft_limit)
            self.accounts_list.append(customer)
            self.overdraft_limits[account_no] = overdraft_limit
            read_customer_file = customer_file.readline()
        customer_file.close()
        print("Customer data is successfully uploaded")
        
        file_2 = r"C:\Users\crmut\OneDrive\Desktop\Software development\admins.txt"
        admin_file = open("{}".format(file_2), 'r')
        read_admin_file = admin_file.readline()
        while read_admin_file != "":
            i = read_admin_file.strip()
            fname, lname, address, user_name, password, full_rights = eval(i)
            full_rights = bool(full_rights)
            admin = Admin(fname, lname, address, user_name, password, full_rights)
            self.admins_list.append(admin)
            read_admin_file = admin_file.readline()
        admin_file.close()
        print("Admin data is successfully uploaded")
        
    def export_customer_data(self):
        count = 0
        file = open(r"C:\Users\crmut\OneDrive\Desktop\Software development\banktest.txt", 'w')
        for i in self.accounts_list:
            last_name = i.get_last_name()
            customer_account = self.search_customers_by_name(last_name)
            if customer_account != None:
                file.write(customer_account.upload_to_file())
            count += 1
        file.close()
        print(f"\nExported {count} customer records")
        
    def management_report(self):
        count = 0
        total_money = 0
        total_interest_rate = 0
        total_od_used = 0
        for i in self.accounts_list:
            account_no = i.get_account_no()
            customer_account = self.search_customers_by_account_no(account_no)
            if customer_account != None:
                money = i.get_balance()
                sum_interest_rate = i.get_balance() * (int(i.get_interest_rate()) / 100)
                total_money += money
                total_interest_rate += sum_interest_rate
            count += 1
            if account_no in self.overdraft_limits:
                od_limits = self.overdraft_limits[account_no]
                print(od_limits)
                total_od = od_limits - i.get_overdraft_limit()
                total_od_used += total_od
        print(f"\nTotal number of customers in the system: {count}")
        print(f"Sum of all money the customers currently have in their bank account: {total_money}")
        print(f"Total interest rate payable: {total_interest_rate}")
        print(f"Total overdrafts used: {total_od_used}")

    def search_admins_by_name(self, admin_username):
        #STEP A.2
        found_admin = None
        for a in self.admins_list:
            username = a.get_username()
            if username == admin_username:
                found_admin = a
                break
        if found_admin == None:
            print("\n The Admin %s does not exist! Try again...\n" %admin_username)
            
        return found_admin
    
    def search_admins_password(self, password):
        found_password = None
        for b in self.admins_list:
            userpassword = b.get_password()
            if userpassword == password:
                found_password = b
                break
        if found_password == None:
            print("\n The Password %s does not exist! Try again...\n" %password)
            
        return found_password
        
    def search_customers_by_name(self, customer_lname):
        #STEP A.3
        found_customer = None
        for b in self.accounts_list:
            last_name = b.get_last_name()
            if last_name == customer_lname:
                found_customer = b
                break
        if found_customer == None:
            print("\n The Customer %s does not exist! Try again...\n" %customer_lname)
            
        return found_customer
    
    def search_customers_by_account_no(self, account_no):
        found_customer = None
        for c in self.accounts_list:
            acc_no = c.get_account_no()
            if acc_no == account_no:
                found_customer = c
                break
        if found_customer == None:
            print("\n The Account Number %s does not exist! Try again...\n" %account_no)
            
        return found_customer

    '''def main_menu(self):
        #print the options you have
        print()
        print()
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("Welcome to the Python Bank System")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Admin login")
        print ("2) Quit Python Bank System")
        print (" ")
        option = int(input ("Choose your option: "))
        return option'''


    def run_main_options(self):
        '''loop = 1  
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input ("\n Please input admin username: ")
                password = input ("\n Please input admin password: ")
                msg, admin_obj, password = self.admin_login(username, password)
                print(msg)
                if admin_obj != None and password != None:
                    self.run_admin_options(admin_obj)
                else:
                    loop = 1
            elif choice == 2:
                loop = 0
        print ("\n Thank-You for stopping by the bank!")'''
        #self.lw = tkinter.Tk()
        login_window = tkinter.Toplevel(self.mw)
        login_window.transient(self.mw)
        login_window.title("Admin Login")
        login_window.geometry("400x275")
        login_window.grab_set()

        tkinter.Label(login_window, text="Admin Login", font=("Arial", 14)).pack(pady=10)

        tkinter.Label(login_window, text="Username:", font=("Arial", 10)).pack(anchor="w", padx=20)
        username_entry = tkinter.Entry(login_window, font=("Arial", 10))
        username_entry.pack(padx=20, fill="x")

        tkinter.Label(login_window, text="Password:", font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10, 0))
        password_entry = tkinter.Entry(login_window, font=("Arial", 10), show="*")
        password_entry.pack(padx=20, fill="x")

        def attempt_login():
            username = username_entry.get()
            password = password_entry.get()
            if not username or not password:
                messagebox.showwarning("Warning", "Both fields are required.", parent=login_window)
                return

            msg, admin_obj, password_correct = self.admin_login(username, password)
            messagebox.showinfo("Login Status", msg, parent=login_window)

            if admin_obj and password_correct:
                self.run_admin_options(admin_obj, login_window)
                self.mw.destroy()

        login_button = tkinter.Button(login_window, text="Login", font=("Arial", 12), command=attempt_login)
        login_button.pack(pady=20)

        cancel_button = tkinter.Button(login_window, text="Cancel", font=("Arial", 12), command=login_window.destroy)
        cancel_button.pack()


    def transferMoney(self, sender_account_no, receiver_account_no, amount):
        #ToDo
        customer_account_sender = self.search_customers_by_account_no(sender_account_no)
        customer_lname = customer_account_sender.get_last_name()
        if customer_account_sender != None:
            transferrable_amount = customer_account_sender.get_balance()
            if amount < transferrable_amount:
                customer_account_receiver = self.search_customers_by_account_no(receiver_account_no)
                if customer_account_receiver != None:
                    customer_account_receiver.deposit(amount)
                    messagebox.showinfo("Transaction Status", "The transaction is successful")
                customer_account_sender.withdraw(amount)
                messagebox.showinfo("Balance", "The %s balance is %s" %(customer_lname, customer_account_sender.get_balance()))
            else:
                messagebox.showinfo("Transaction status", "Failed: Amount exceeds balance, overdraft amount is not transferrable.")
            
        
    def admin_login(self, username, password):
		  #STEP A.1
        found_admin = self.search_admins_by_name(username)
        found_password = self.search_admins_password(password)
        msg = "Login failed"
        if found_admin != None:
            if found_password != None:
                msg = "Login successful"
        return msg, found_admin, found_password

    '''def admin_menu(self, admin_obj):
        #print the options you have
         print (" ")
         print ("Welcome Admin %s %s : Available options are:" %(admin_obj.get_first_name(), admin_obj.get_last_name()))
         print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
         print ("1) Transfer money")
         print ("2) Customer account operations & profile settings")
         print ("3) Delete customer")
         print ("4) Print all customers detail")
         print ("5) Export all customers detail")
         print ("6) Update admin name")
         print ("7) Update admin address")
         print ("8) Show admin details")
         print ("9) Build management report")
         print ("10) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option'''


    def run_admin_options(self, admin_obj, login_window):                                
        '''loop = 1
        while loop == 1:
            choice = self.admin_menu(admin_obj)
            if choice == 1:
                print("\nNote: Overdraft is not transferrable but can be withdrawn")
                sender_account_no = input("\n Please input sender account number: ")
                receiver_account_no = input("\n Please input receiver account number: ")
                amount = float(input("\n Please input the amount to be transferred: "))
                self.transferMoney(sender_account_no, receiver_account_no, amount)
                    
            elif choice == 2:
                #STEP A.4
                account_number = input("\nPlease input customer account number : ")
                customer_account = self.search_customers_by_account_no(account_number)
                if customer_account != None:
                    customer_account.run_account_options()
            
            elif choice == 3:
                #Todo
                if admin_obj.has_full_admin_right() == True:
                    customer_name = input("\nPlease input customer surname to be deleted : ")
                    customer_account = self.search_customers_by_name(customer_name)
                    if customer_account != None:
                        for i in self.accounts_list:
                            lname = i.get_last_name()
                            if(lname == customer_name):
                                self.accounts_list.remove(i)
                                print("The Customer %s is successfully deleted" %customer_name)
                                break
                else:
                    print("\nThe admin %s don't have full rights to delete the customer" %admin_obj.get_last_name())
            
            elif choice == 4:
                #Todo
                count = 0
                for i in self.accounts_list:
                    last_name = i.get_last_name()
                    customer_account = self.search_customers_by_name(last_name)
                    if customer_account != None:
                        customer_account.print_details()
                    count += 1
                print(f"There are {count} customer records")
                
            elif choice == 5:
                self.export_customer_data()
            
            elif choice == 6:
                fname = input("\n Enter new admin first name: ")
                admin_obj.update_first_name(fname)
                sname = input("\n Enter new admin last name: ")
                admin_obj.update_last_name(sname)
                print("\n The admin name has been changed")
                
            elif choice == 7:
                admin_obj.addr = []
                print("\nPlease provide the address details to be updated")
                house_number = input("\nPlease enter the house number: ")
                admin_obj.addr.append(house_number)
                street_name = input("\nPlease enter the street name: ")
                admin_obj.addr.append(street_name)
                city_name = input("\nPlease enter the name of the city: ")
                admin_obj.addr.append(city_name)
                post_code = input("\nPlease enter the post code: ")
                admin_obj.addr.append(post_code)
                
                admin_obj.update_address(admin_obj.addr)
                print("\nThe Address has been updated successfully as per your request")
            
            elif choice == 8:
                admin_obj.print_details()
                
            elif choice == 9:
                self.management_report()
                
            elif choice == 10:
                loop = 0
        print ("\n Exit account operations")'''

        #self.aw = tkinter.Tk()
        admin_window = tkinter.Toplevel(login_window)
        admin_window.transient(login_window)
        admin_window.title("Admin Menu")
        admin_window.geometry("500x400")
        admin_window.grab_set()

        tkinter.Label(admin_window, text=f"Welcome Admin {admin_obj.get_first_name()} {admin_obj.get_last_name()}", font=("Arial", 14)).pack(pady=10)
        tkinter.Label(admin_window, text="Available Options:", font=("Arial", 12)).pack(pady=5)

        options = [
            "Transfer money",
            "Customer account operations & profile settings",
            "Delete customer",
            "Print all customers detail",
            "Export all customers detail",
            "Update admin name",
            "Update admin address",
            "Show admin details",
            "Build management report",
            "Sign out"
        ]

        selected_option = tkinter.IntVar(value=1)
        
        def create_transfer_widgets(self):
            transfer_window = tkinter.Toplevel(admin_window)
            transfer_window.transient(admin_window)
            transfer_window.title("Transfer Money")
            transfer_window.geometry("325x175")
            transfer_window.grab_set()
            
            self.sender_account_label = tkinter.Label(transfer_window, text="Sender Account Number:")
            self.sender_account_label.grid(row=0, column=0, padx=10, pady=10)
            self.sender_account_entry = tkinter.Entry(transfer_window)
            self.sender_account_entry.grid(row=0, column=1, padx=10, pady=10)

            # Receiver Account Number
            self.receiver_account_label = tkinter.Label(transfer_window, text="Receiver Account Number:")
            self.receiver_account_label.grid(row=1, column=0, padx=10, pady=10)
            self.receiver_account_entry = tkinter.Entry(transfer_window)
            self.receiver_account_entry.grid(row=1, column=1, padx=10, pady=10)

            # Amount to transfer
            self.amount_label = tkinter.Label(transfer_window, text="Amount to Transfer:")
            self.amount_label.grid(row=2, column=0, padx=10, pady=10)
            self.amount_entry = tkinter.Entry(transfer_window)
            self.amount_entry.grid(row=2, column=1, padx=10, pady=10)
            
            def attempt_transfer():
                sender_account_no = self.sender_account_entry.get()
                receiver_account_no = self.receiver_account_entry.get()
                amount = int(self.amount_entry.get())
                
                self.transferMoney(sender_account_no, receiver_account_no, amount)

            # Transfer button
            self.transfer_button = tkinter.Button(transfer_window, text="Transfer", command=attempt_transfer)
            self.cancel_button = tkinter.Button(transfer_window, text="Cancel", command=transfer_window.destroy)
            self.transfer_button.grid(row=3, column=0, columnspan=2, pady=10)
            self.transfer_button.grid(row=4, column=0, columnspan=2, pady=10)

        for idx, option in enumerate(options, start=1):
            tkinter.Radiobutton(admin_window, text=option, variable=selected_option, value=idx, font=("Arial", 10)).pack(anchor="w")

        def execute_option():
            choice = selected_option.get()

            if choice == 1:
                create_transfer_widgets(self)
            elif choice == 2:
                messagebox.showinfo("Action", "Customer account operations selected.")
            elif choice == 3:
                messagebox.showinfo("Action", "Delete customer selected.")
            elif choice == 4:
                messagebox.showinfo("Action", "Print all customers detail selected.")
            elif choice == 5:
                self.export_customer_data()
            elif choice == 6:
                fname = simpledialog.askstring("Update Admin Name", "Enter new first name:")
                lname = simpledialog.askstring("Update Admin Name", "Enter new last name:")
                admin_obj.update_first_name(fname)
                admin_obj.update_last_name(lname)
                messagebox.showinfo("Success", "Admin name updated successfully.")
            elif choice == 7:
                address = []
                address.append(simpledialog.askstring("Update Address", "Enter house number:"))
                address.append(simpledialog.askstring("Update Address", "Enter street name:"))
                address.append(simpledialog.askstring("Update Address", "Enter city name:"))
                address.append(simpledialog.askstring("Update Address", "Enter post code:"))
                admin_obj.update_address(address)
                messagebox.showinfo("Success", "Admin address updated successfully.")
            elif choice == 8:
                admin_obj.print_details()
            elif choice == 9:
                self.management_report()
            elif choice == 10:
                admin_window.destroy()

        tkinter.Button(admin_window, text="Execute", command=execute_option, font=("Arial", 12)).pack(pady=10)


    def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.accounts_list:
                i+=1
                print('\n %d. ' %i, end = ' ')
                c.print_details()
                print("------------------------")
            
       
app = BankSystem()
app.run_main_options()