''' ------------------- Already Existing Code Starts --------------------- '''

import re
import os
import ast
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, simpledialog
from customer_account import CustomerAccount
from admin import Admin

accounts_list = []
admins_list = []

class Page(tk.Frame):
    def __init__(self, parent, main_view):
        tk.Frame.__init__(self, parent)
        self.main_view = main_view

    def show(self):
        self.lift()

class MainView(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.title("Bank System")
        self.bank_system = BankSystem()
        self.admin_obj = None
        self.customer_obj = None

        self.pages = {}
        for PageClass in (Page1, Page2, Page3, Page4):
            page = PageClass(parent=self, main_view=self)
            self.pages[PageClass] = page
            page.place(x=0, y=0, relwidth=1, relheight=1)

        self.show_page(Page1)

    def show_page(self, page_class, admin_obj=None):
        if page_class == Page3:
            self.admin_obj = admin_obj
            page = self.pages[page_class]
            page.refresh(admin_obj)
        self.pages[page_class].show()
        
    def show_page_1(self, page_class, customer_obj=None):
        if page_class == Page4:
            self.customer_obj = customer_obj
            page = self.pages[page_class]
            page.refresh(customer_obj)
        self.pages[page_class].show()

class Page1(Page):
    def __init__(self, parent, main_view):
        Page.__init__(self, parent, main_view)
        
        tk.Label(self, text="Welcome to the Python Bank System", font=("Helvetica", 12, "bold")).pack(pady=50)
        tk.Button(self, text="Load Data", command=self.load_data_message).pack(pady=10)
        self.admin_button = tk.Button(self, text="Admin Login", bg="sky blue", state=tk.DISABLED, command=self.before_admin_login)
        self.admin_button.pack(pady=10)
        tk.Button(self, text="Quit", command=main_view.root.destroy, bg="red", fg="white", font=("Helvetica", 8, "bold")).pack(pady=10)
        
        self.message_field = tk.Label(self, text="Load the data before login", font=("Helvetica", 8, "bold"), bg="yellow", padx=10, pady=5)
        self.message_field.pack_forget()

        self.admin_button.bind("<Enter>", self.show_message_field)
        self.admin_button.bind("<Leave>", self.hide_message_field)
        
    def load_data_message(self):
        self.main_view.bank_system.load_bank_data()
        if self.main_view.bank_system.is_loaded_data():
            self.admin_button.config(state=tk.NORMAL)
            
    def before_admin_login(self):
        if not self.main_view.bank_system.is_loaded_data():
            messagebox.showerror("Error", "Please load the data before proceeding to Admin Login.")
        else:
            self.main_view.show_page(Page2)
            
    def show_message_field(self, event):
        if self.admin_button.cget("state") == "disabled":
            self.message_field.pack(pady=(5, 0))

    def hide_message_field(self, event):
        self.message_field.pack_forget()

class Page2(Page):
    def __init__(self, parent, main_view):
        Page.__init__(self, parent, main_view)
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        '''tk.Label(self, text="Username").pack(pady=5)
        tk.Entry(self, textvariable=self.username).pack(pady=5)
        tk.Label(self, text="Password").pack(pady=5)
        tk.Entry(self, textvariable=self.password, show="*").pack(pady=5)
        tk.Button(self, text="Login", command=self.login).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: main_view.show_page(Page1)).pack(pady=10)'''
        
        frame = tk.Frame(self)
        frame.pack(expand=True)

        # Username label and entry
        tk.Label(frame, text="Username").pack(pady=5)
        tk.Entry(frame, textvariable=self.username).pack(pady=5)
        
        # Password label and entry
        tk.Label(frame, text="Password").pack(pady=5)
        tk.Entry(frame, textvariable=self.password, show="*").pack(pady=5)
        
        # Login and back buttons
        tk.Button(frame, text="Login", command=self.login, bg="sky blue").pack(pady=10)
        tk.Button(frame, text="Back", command=lambda: main_view.show_page(Page1)).pack(pady=10)

    def login(self):
        username = self.username.get()
        passwrd = self.password.get()
        if username == "" and passwrd == "":
            messagebox.showerror("Login Failed", "Username and password are mandatory")
        msg, admin_obj, password = self.main_view.bank_system.admin_login(username, passwrd)

        #messagebox.showinfo("Login", msg)
        if admin_obj != None and password != None:
            messagebox.showinfo("Login", msg)
            self.main_view.show_page(Page3, admin_obj)
        elif (username == "" and passwrd == ""):
            pass
        elif (admin_obj != username and password != passwrd) or (username == "" and password != passwrd) or (passwrd == "" and admin_obj != username): 
            messagebox.showerror("Login Failed", "Invalid username or password. Try again...")
            self.password.set("")
            
    def clear_fields(self):
        self.username.set("")
        self.password.set("")

class Page3(Page):
    def __init__(self, parent, main_view):
        Page.__init__(self, parent, main_view)
        self.label = tk.Label(self, text="Welcome Admin")
        self.label.pack(pady=10)

        self.options = [
            "Transfer money",
            "Customer account operations & profile settings",
            "Delete customer",
            "Print all customers detail",
            "Update admin name",
            "Update admin address",
            "Show admin details",
            "Build management report",
        ]
        self.selected_option = tk.IntVar(value=1)

        for idx, option in enumerate(self.options, start=1):
            tk.Radiobutton(self, text=option, variable=self.selected_option, value=idx).pack(anchor="w")

        tk.Button(self, text="Execute", command=self.execute_option, bg="sky blue").pack(pady=10)
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Export", command=self.is_exported).pack(side="left", padx=5)
        tk.Button(button_frame, text="Sign out", command=self.go_back, bg="red", fg="white", font=("Helvetica", 8, "bold")).pack(side="left", padx=5)

    def refresh(self, admin_obj):
        if admin_obj:
            self.label.config(text=f"Welcome Admin {admin_obj.get_first_name()} {admin_obj.get_last_name()}")
            self.data_exported = False
            self.data_modified = False

    def go_back(self):
        if self.data_exported == False and self.data_modified == True:
            response = messagebox.askyesno(
                "Export Data",
                "You haven't exported the customer data yet.\n"
                "Would you like to export before signing out?\n\n"
                "If Yes, modified data will be updated to the loaded file.\n"
                "If No, modified data will not be updated to the loaded file."
            )
            if response:
                self.is_exported()
            else:
                messagebox.showinfo("Sign-out", "You are signing out without exporting data.")
                self.main_view.pages[Page2].clear_fields()
                self.main_view.show_page(Page2)
        else:
            self.main_view.pages[Page2].clear_fields()
            self.main_view.show_page(Page2)
        
    def is_exported(self):
        try:
            self.main_view.bank_system.export_customer_data()
            self.data_exported = True
            self.data_modified = False
            messagebox.showinfo("Export Success", "Customer and Admin data has been successfully exported!")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred during export: {e}")
        
    def execute_option(self):
        choice = self.selected_option.get()
        admin = self.main_view.admin_obj
        #customer = self.main_view.customer_obj

        if choice == 1:
            sender_acc_no = None
            while not sender_acc_no:
                sender_acc_no = simpledialog.askstring("Transfer Money", "Enter sender account number:")
                if sender_acc_no is None:
                    return
                if sender_acc_no == "":
                    messagebox.showerror("Error", "Sender account number should not be empty!")
                    sender_acc_no = None
                elif not sender_acc_no.isdigit():
                    messagebox.showerror("Error", "Account number must be numeric!")
                    sender_acc_no = None
                else:
                    sender = self.main_view.bank_system.search_customers_by_account_no(sender_acc_no)
                    if sender is None:
                        messagebox.showerror("Error", "Sender account number does not exist!")
                        sender_acc_no = None

            reciever_acc_no = None
            while not reciever_acc_no:
                reciever_acc_no = simpledialog.askstring("Transfer Money", "Enter receiver account number:")
                if reciever_acc_no is None:
                    return
                if reciever_acc_no == "":
                    messagebox.showerror("Error", "Receiver account number should not be empty!")
                    reciever_acc_no = None
                elif sender_acc_no == reciever_acc_no:
                    messagebox.showerror("Error", "Sender and receiver account numbers should not be the same!")
                    reciever_acc_no = None
                elif not reciever_acc_no.isdigit():
                    messagebox.showerror("Error", "Account number must be numeric!")
                    reciever_acc_no = None
                else:
                    receiver = self.main_view.bank_system.search_customers_by_account_no(reciever_acc_no)
                    if receiver is None:
                        messagebox.showerror("Error", "Receiver account number does not exist!")
                        reciever_acc_no = None

            sender_initial_balance = sender.get_balance()
            if self.main_view.bank_system.overdraft_limits[sender_acc_no] != 0: 
                messagebox.showinfo("Note", "The Overdraft limit is not transferrable\n\nYour transfer limit is %s" %sender_initial_balance)
            else:
                messagebox.showinfo("Note", "Your transfer limit is %s" %sender_initial_balance)
                
            amt = None
            while not amt:
                amt = simpledialog.askinteger("Transfer Money", "Enter amount to transfer:")
                if amt is None:
                    return
                if amt <= 0:
                    messagebox.showerror("Error", "Amount should be greater than 0")
                    amt = None
                elif amt > sender.get_balance():
                    messagebox.showerror("Error", "Insufficient balance")
                    amt = None
                    
            self.main_view.bank_system.transferMoney(sender_acc_no, reciever_acc_no, amt)
            last_name = sender.get_last_name()
            final_balance = sender.get_balance()
            messagebox.showinfo("Transfer Status", "Transaction successful \n The Customer %s balance is %s" %(last_name, final_balance))
            self.data_modified = True
        
        elif choice == 2:
            cust_acc = None
            while not cust_acc:
                cust_acc = simpledialog.askstring("Customer Operations", "Enter customer account number:")
                if cust_acc is None:
                    return
                if cust_acc == "":
                    messagebox.showerror("Error", "Customer account number should not be empty!")
                    cust_acc = None
                elif not cust_acc.isdigit():
                    messagebox.showerror("Error", "Account number must be numeric!")
                    cust_acc = None
                else:
                    receiver = self.main_view.bank_system.search_customers_by_account_no(cust_acc)
                    if receiver is None:
                        messagebox.showerror("Error", "Customer account number does not exist!")
                        cust_acc = None
                        
            customer_obj = self.main_view.bank_system.search_customers_by_account_no(cust_acc)
            
            self.main_view.show_page_1(Page4, customer_obj)
            
        elif choice == 3:
            if admin.has_full_admin_right() == True or admin.has_full_admin_right() == "True":
                customer_account = None
                while not customer_account:
                    customer_account = simpledialog.askstring("Delete Account", "Enter account number to be deleted:")
                    if customer_account is None:
                        return
                    if customer_account == "":
                        messagebox.showerror("Error", "Customer account number is required to delete!")
                        customer_account = None
                    elif not customer_account.isdigit():
                        messagebox.showerror("Error", "Account number must be numeric!")
                        customer_account = None
                    else:
                        found_acc = self.main_view.bank_system.search_customers_by_account_no(customer_account)
                        if found_acc is None:
                            messagebox.showerror("Error", "Customer account number not found")
                            customer_account = None
                for i in self.main_view.bank_system.accounts_list:
                    acc = i.get_account_no()
                    if(acc == customer_account):
                        self.main_view.bank_system.accounts_list.remove(i)
                        messagebox.showinfo("Delete Status",  "The Customer account %s is successfully deleted" %customer_account)
                        self.data_modified = True
                        break
            else:
                messagebox.showwarning("Rights Status", "\nThe admin %s don't have full rights to delete the customer" %admin.get_last_name())
                
        elif choice == 4:
            if self.main_view.bank_system.accounts_list:
                count = 0
                customer_details = []
                for idx, i in enumerate(self.main_view.bank_system.accounts_list, start=1):
                    acc_no = i.get_account_no()
                    customer_account = self.main_view.bank_system.search_customers_by_account_no(acc_no)
                    if customer_account != None:
                        per_detail = f"{idx}.{customer_account.print_details()}"
                        customer_details.append(per_detail)
                    count += 1
                show_details = "\n".join(customer_details)
                
                top = tk.Toplevel(self)
                top.title("Customer Details")

                text_box = tk.Text(top, wrap="word", height=15, width=50)
                text_box.insert(tk.END, show_details)
                text_box.config(state=tk.DISABLED)
                text_box.pack(side="left", fill="both", expand=True)

                scrollbar = tk.Scrollbar(top, command=text_box.yview)
                scrollbar.pack(side="right", fill="y")
                text_box.config(yscrollcommand=scrollbar.set)

                top.mainloop()
            else:
                messagebox.showinfo("Customer Details", "No customer records available!")
            
        elif choice == 5:
            def check_name(input):
                while True:
                    name = simpledialog.askstring("Update Admin Name", input)
                    if name is None:
                        return None
                    if name.isalpha():
                        return name
                    else:
                        messagebox.showerror("Invalid Input", "Please enter a valid name containing only alphabets.")
                        
            fname = check_name("Enter new first name:")
            if fname is None:
                return None
            
            lname = check_name("Enter new last name:")
            if lname is None:
                return None
            
            admin.update_first_name(fname)
            admin.update_last_name(lname)
            messagebox.showinfo("Success", "Admin name updated successfully.")
            self.refresh(admin)
            self.data_modified = True
            
        elif choice == 6:
            def check_address(input):
                while True:
                    value = simpledialog.askstring("Update Admin Address", input)
                    if value is None:
                        return None
                    if value:
                        return value
                    else:
                        messagebox.showerror("Invalid Input", f"{input} cannot be empty. Please try again.")

            address = []        
    
            house_number = check_address("Enter house number:")
            if house_number is None:
                return
            
            address.append(house_number)

            street_name = check_address("Enter street name:")
            if street_name is None:
                return
            
            address.append(street_name)

            city_name = check_address("Enter city name:")
            if city_name is None:
                return
            
            address.append(city_name)

            post_code = check_address("Enter post code:")
            if post_code is None:
                return
            
            address.append(post_code)
            
            admin.update_address(address)
            messagebox.showinfo("Success", "Admin address updated successfully.")
            self.data_modified = True
            
        elif choice == 7:
            if self.main_view.bank_system.admins_list:
                count = 0
                admin_details = []
                for idx, i in enumerate(self.main_view.bank_system.admins_list, start=1):
                    username = i.get_username()
                    admin_account = self.main_view.bank_system.search_admins_by_name(username)
                    if admin_account != None:
                        per_detail = f"{idx}.{admin_account.print_details()}"
                        admin_details.append(per_detail)
                    count+=1
                show_details = "\n".join(admin_details)
                
                top = tk.Toplevel(self)
                top.title("Admin Details")

                text_box = tk.Text(top, wrap="word", height=15, width=50)
                text_box.insert(tk.END, show_details)
                text_box.config(state=tk.DISABLED)
                text_box.pack(side="left", fill="both", expand=True)

                scrollbar = tk.Scrollbar(top, command=text_box.yview)
                scrollbar.pack(side="right", fill="y")
                text_box.config(yscrollcommand=scrollbar.set)

                top.mainloop()
                
            else:
                messagebox.showinfo("Admin Details", "No admin records available!")
            
        elif choice == 8:
            try:
                report = self.main_view.bank_system.management_report()
                
                top = tk.Toplevel(self)
                top.title("Management Report")

                text_box = tk.Text(top, wrap="word", height=9, width=85)
                text_box.insert(tk.END, report)
                text_box.config(state=tk.DISABLED)
                text_box.pack(side="left", fill="both", expand=True)

                scrollbar = tk.Scrollbar(top, command=text_box.yview)
                scrollbar.pack(side="right", fill="y")
                text_box.config(yscrollcommand=scrollbar.set)

                top.mainloop()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to generate management report: {e}")

class Page4(Page):
    def __init__(self, parent, main_view):
        Page.__init__(self, parent, main_view)
        self.label = tk.Label(self, text="Welcome Customer")
        self.label.pack(pady=10)
        
        self.options = [
            "Deposit Money",
            "Withdraw money",
            "Check balance",
            "Update customer name",
            "Update customer address",
            "Show customer details",
        ]
        self.selected_option = tk.IntVar(value=1)

        for idx, option in enumerate(self.options, start=1):
            tk.Radiobutton(self, text=option, variable=self.selected_option, value=idx).pack(anchor="w")

        tk.Button(self, text="Execute", command=self.execute_option, bg="sky blue").pack(pady=10)
        tk.Button(self, text="Back", command=self.go_back).pack(pady=10)
        
    def go_back(self):
        self.main_view.pages[Page2].clear_fields()
        self.main_view.show_page(Page3)
        
    def refresh(self, customer_obj):
        if customer_obj:
            self.label.config(text=f"Welcome Customer {customer_obj.get_first_name()} {customer_obj.get_last_name()}")

    def execute_option(self):
        choice = self.selected_option.get()
        customer = self.main_view.customer_obj
        
        if choice == 1:
            if self.main_view.bank_system.overdraft_limits[customer.get_account_no()] != 0:
                od_used = self.main_view.bank_system.overdraft_limits[customer.get_account_no()] - customer.overdraft_limit
                if self.main_view.bank_system.overdraft_limits[customer.get_account_no()] != customer.overdraft_limit: 
                    messagebox.showinfo("Note", "Used overdraft is %s\n\nThe overdraft limit should be maintained.\n\nThe amount %s will be deposited to Overdraft and\nremaining will be deposited into main account"%(od_used, od_used))
            amt = None
            while not amt:
                amt = simpledialog.askinteger("Deposit Amount", "Enter amount: ")
                if amt is None:
                    return
                if amt <= 0:
                    messagebox.showerror("Error", "Amount should be greater than 0")
                    amt = None
                    
            customer.deposit(amt)
            if self.main_view.bank_system.overdraft_limits[customer.get_account_no()] != 0: 
                messagebox.showinfo("Withdraw Success", "Your balance is %s\n\nYour overdraft limit is %s"%(customer.balance, customer.overdraft_limit))
            else:
                messagebox.showinfo("Withdraw Success", "Your balance is %s"%customer.balance)
            self.data_modified = True
        
        elif choice == 2:
            if customer.balance > 0: 
                total_amount = customer.balance + customer.overdraft_limit
            else:
                total_amount = customer.overdraft_limit
            if self.main_view.bank_system.overdraft_limits[customer.get_account_no()] != 0:   
                if total_amount > 0: 
                    messagebox.showinfo("Note", "The Overdraft can be withdrawn\n\nYour withdrawal limit is %s\n(Overdraft limit is included in the withdrawal limit)"%total_amount)
                else:
                    messagebox.showerror("Note", "Your overdraft limit is %s\n\nYour withdrawal limit is %s\n\nInsufficient balance!"%(customer.overdraft_limit, total_amount))
                    return
            else:
                if total_amount > 0: 
                    messagebox.showinfo("Note", "Your withdrawal limit is %s"%total_amount)
                else:
                    messagebox.showerror("Note", "Your withdrawal limit is %s\n\nInsufficient balance!"%total_amount)
                    return
            
            amt = None
            while not amt:
                amt = simpledialog.askinteger("Withdraw Amount", "Enter amount: ")
                if amt is None:
                    return
                if amt <= 0:
                    messagebox.showerror("Error", "Amount should be greater than 0")
                    amt = None
                elif amt > total_amount:
                    messagebox.showerror("Error", "Insufficient balance")
                    amt = None
                    
            customer.withdraw(amt)
            if self.main_view.bank_system.overdraft_limits[customer.get_account_no()] != 0: 
                messagebox.showinfo("Withdraw Success", "Your balance is %s\n\nYour overdraft limit is %s"%(customer.balance, customer.overdraft_limit))
            else:
                messagebox.showinfo("Withdraw Success", "Your balance is %s"%customer.balance)
            self.data_modified = True
        
        elif choice == 3:
            customer.print_balance()
        
        elif choice == 4:            
            def check_name(input):
                while True:
                    name = simpledialog.askstring("Update Customer Name", input)
                    if name is None:
                        return None
                    if name.isalpha():
                        return name
                    else:
                        messagebox.showerror("Invalid Input", "Please enter a valid name containing only alphabets.")
                        
            fname = check_name("Enter new first name:")
            if fname is None:
                return None
            
            lname = check_name("Enter new last name:")
            if lname is None:
                return None
            
            customer.update_first_name(fname)
            customer.update_last_name(lname)
            messagebox.showinfo("Success", "Customer name updated successfully.")
            self.refresh(customer)
            self.data_modified = True
        
        elif choice == 5:
            def check_address(input):
                while True:
                    value = simpledialog.askstring("Update Customer Address", input)
                    if value is None:
                        return None
                    if value:
                        return value
                    else:
                        messagebox.showerror("Invalid Input", f"{input} cannot be empty. Please try again.")

            address = []        
    
            house_number = check_address("Enter house number:")
            if house_number is None:
                return
            
            address.append(house_number)

            street_name = check_address("Enter street name:")
            if street_name is None:
                return
            
            address.append(street_name)

            city_name = check_address("Enter city name:")
            if city_name is None:
                return
            
            address.append(city_name)

            post_code = check_address("Enter post code:")
            if post_code is None:
                return
            
            address.append(post_code)
            
            customer.update_address(address)
            messagebox.showinfo("Success", "Customer address updated successfully.")
            self.data_modified = True
        
        elif choice == 6:
            customer_detail = []
            name = f"{customer.get_first_name()} {customer.get_last_name()}"
            customer_detail.append(customer.print_details())
            show_detail = "\n".join(customer_detail)
            
            top = tk.Toplevel(self)
            top.title(f"{name} Detail")

            text_box = tk.Text(top, wrap="word", height=15, width=50)
            text_box.insert(tk.END, show_detail)
            text_box.config(state=tk.DISABLED)
            text_box.pack(side="left", fill="both", expand=True)

            scrollbar = tk.Scrollbar(top, command=text_box.yview)
            scrollbar.pack(side="right", fill="y")
            text_box.config(yscrollcommand=scrollbar.set)

            top.mainloop()

class BankSystem(object):
    def __init__(self):
        self.accounts_list = []
        self.admins_list = []
        self.overdraft_limits = {}
        #self.load_bank_data()
    
    def load_bank_data(self):
        
        # create customers
        '''account_no = 1234
        customer_1 = CustomerAccount("Adam", "Smith", ["14", "Wilcot Street", "Bath", "B5 5RT"], account_no, 5000.00)
        self.accounts_list.append(customer_1)
        
        account_no+=1
        customer_2 = CustomerAccount("David", "White", ["60", "Holborn Viaduct", "London", "EC1A 2FD"], account_no, 3200.00)    
        self.accounts_list.append(customer_2)

        account_no+=1
        customer_3 = CustomerAccount("Alice", "Churchil", ["5", "Cardigan Street", "Birmingham", "B4 7BD"], account_no, 18000.00)
        self.accounts_list.append(customer_3)

        account_no+=1
        customer_4 = CustomerAccount("Ali", "Abdallah",["44", "Churchill Way West", "Basingstoke", "RG21 6YR"], account_no, 40.00)
        self.accounts_list.append(customer_4)
                
        # create admins
        admin_1 = Admin("Julian", "Padget", ["12", "London Road", "Birmingham", "B95 7TT"], "id1188", "1441", True)
        self.admins_list.append(admin_1)

        admin_2 = Admin("Cathy",  "Newman", ["47", "Mars Street", "Newcastle", "NE12 6TZ"], "id3313", "2442", False)
        self.admins_list.append(admin_2)'''
        
        current_file = Path(__file__).parent.resolve()
        file_1 = current_file / "customers.txt"
        file_2 = current_file / "admins.txt"
        
        try:
            if not str(file_1).endswith('.txt'):
                raise ValueError("Invalid file format. Only '.txt' files are allowed.")

            if not file_1.exists():
                raise FileNotFoundError(f"The file {file_1} does not exist.")

            if file_1.stat().st_size == 0:
                messagebox.showerror("Error Loading File", "The customer data file is empty. Please provide valid data.")

            with file_1.open('r') as customer_file:
                for line in customer_file:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        line = re.sub(r'(?<!\[)".*?"(?!\])', lambda match: match.group(0)[1:-1], line)
                        fields = re.split(r',\s*(?![^[]*\])', line)
                        if len(fields) != 8:
                            raise ValueError(f"Invalid number of fields in line: {line}")

                        fname = fields[0].strip()
                        lname = fields[1].strip()
                        address = ast.literal_eval(fields[2].strip())
                        if not isinstance(address, list) or len(address) != 4:
                            raise ValueError(f"Invalid address format in line: {line}")

                        account_no = fields[3].strip()
                        balance = float(fields[4].strip())
                        account_name = fields[5].strip()
                        interest_rate = float(fields[6].strip())
                        overdraft_limit = float(fields[7].strip())

                        customer = CustomerAccount(
                            fname=fname,
                            lname=lname,
                            address=address,
                            account_no=account_no,
                            balance=balance,
                            account_name=account_name,
                            interest_rate=interest_rate,
                            overdraft_limit=overdraft_limit
                        )
                        self.accounts_list.append(customer)
                        self.overdraft_limits[account_no] = overdraft_limit

                    except Exception:
                        messagebox.showerror("Error Loading Data", f"Invalid data format in line: {line}. Please provide valid data.")
                        return
                    
            messagebox.showinfo("Customer Data Load Status", "Customer Data has been successfully loaded.")

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file {file_1} does not exist.")
            return
        except ValueError as e:
            messagebox.showerror("File Format Error", f"Invalid file format: {e}")
            return
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            return
            
        try:
            if not str(file_2).endswith('.txt'):
                raise ValueError("Invalid file format. Only '.txt' files are allowed.")

            if not file_2.exists():
                raise FileNotFoundError(f"The file {file_2} does not exist.")

            if file_2.stat().st_size == 0:
                messagebox.showerror("Error Loading File", "The Admin data file is empty. Please provide valid data.")

            with file_2.open('r') as admin_file:
                for line in admin_file:
                    line = line.strip().replace('\u00A0', ' ')
                    if not line:
                        continue
                    try:                        
                        line = re.sub(r'(?<!\[)".*?"(?!\])', lambda match: match.group(0)[1:-1], line)
                        fields = re.split(r',\s*(?![^[]*\])', line)
                        if len(fields) != 6:
                            raise ValueError(f"Invalid number of fields in line: {line}")
                            
                        fname = fields[0].strip()
                        lname = fields[1].strip()
                        address = ast.literal_eval(fields[2].strip())
                        if not isinstance(address, list) or len(address) != 4:
                            raise ValueError(f"Invalid address format in line: {line}")
                        user_name = fields[3].strip()
                        password = fields[4].strip()
                        full_rights = fields[5].strip()
                        
                        admin = Admin(
                            fname=fname,
                            lname=lname,
                            address=address,
                            user_name=user_name,
                            password=password,
                            full_rights=full_rights
                        )
                        self.admins_list.append(admin)

                    except Exception:
                        messagebox.showerror("Error Loading Data", f"Invalid data format in line: {line}. Please provide valid data.")
                        return
                    
            messagebox.showinfo("Admin Data Load Status", "Admin Data has been successfully loaded.")

        except FileNotFoundError:
            messagebox.showerror("File Not Found", f"The file {file_2} does not exist.")
            return
        except ValueError as e:
            messagebox.showerror("File Format Error", f"Invalid file format: {e}")
            return
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {e}")
            return
            
    def is_loaded_data(self):
        if self.accounts_list and self.admins_list:
            return True
        return False
    
    def export_customer_data(self):
        current_file = Path(__file__).parent.resolve()
        export_file_path_customers = current_file / "customers.txt"
        with export_file_path_customers.open('w') as file:
            count = 0
            for i in self.accounts_list:
                acc_no = i.get_account_no()
                customer_account = self.search_customers_by_account_no(acc_no)
                if customer_account != None:
                    file.write(customer_account.upload_to_file())
                count += 1
                
        export_file_path_admins = current_file / "admins.txt"
        with export_file_path_admins.open('w') as file:
            count = 0
            for i in self.admins_list:
                user_name = i.get_username()
                admin_account = self.search_admins_by_name(user_name)
                if admin_account != None:
                    file.write(admin_account.upload_to_file())
                count += 1
                
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
                total_od = od_limits - i.get_overdraft_limit()
                total_od_used += total_od
                
        return f"\n Total number of customers in the system: {count}\n\n Sum of all money the customers currently have in their bank account: {total_money}\n\n Total interest rate payable: {total_interest_rate}\n\n Total overdrafts used: {total_od_used}"

    def search_admins_by_name(self, admin_username):
        #STEP A.2
        found_admin = None
        for a in self.admins_list:
            username = a.get_username()
            if username == admin_username:
                found_admin = a
                break
        '''if found_admin == None:
            print("\n The Admin %s does not exist! Try again...\n" %admin_username)'''
            
        return found_admin
    
    def search_admins_password(self, password):
        found_password = None
        for b in self.admins_list:
            userpassword = b.get_password()
            if userpassword == password:
                found_password = b
                break
        '''if found_password == None:
            print("\n The Password %s does not exist! Try again...\n" %password)'''
            
        return found_password
        
    '''def search_customers_by_name(self, customer_lname):
        #STEP A.3
        found_customer = None
        for b in self.accounts_list:
            last_name = b.get_last_name()
            if last_name == customer_lname:
                found_customer = b
                break
        if found_customer == None:
            print("\n The Customer %s does not exist! Try again...\n" %customer_lname)
            
        return found_customer'''
    
    def search_customers_by_account_no(self, account_no):
        found_customer = None
        for c in self.accounts_list:
            acc_no = c.get_account_no()
            if acc_no == account_no:
                found_customer = c
                break
        '''if found_customer == None:
            print("\n The Account Number %s does not exist! Try again...\n" %account_no)'''
            
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


    '''def run_main_options(self):
        loop = 1         
        while loop == 1:
            choice = self.main_menu()
            if choice == 1:
                username = input ("\n Please input admin username: ")
                password = input ("\n Please input admin password: ")
                msg, admin_obj = self.admin_login(username, password)
                print(msg)
                if admin_obj != None:
                    self.run_admin_options(admin_obj)
            elif choice == 2:
                loop = 0
        print ("\n Thank-You for stopping by the bank!")'''


    '''def transferMoney(self, sender_lname, receiver_lname, receiver_account_no, amount):
        #ToDo
        customer_account_sender = self.search_customers_by_name(sender_lname)
        if customer_account_sender != None:
            customer_account_receiver = self.search_customers_by_name(receiver_lname)
            if customer_account_receiver != None:
                customer_account_receiver.deposit(amount)
                print("The transaction is successful")
            customer_account_sender.withdraw(amount)
            print("The customer %s balance : " %sender_lname, customer_account_sender.get_balance())'''
            
    def transferMoney(self, sender_account_no, receiver_account_no, amount):
        #ToDo
        customer_account_sender = self.search_customers_by_account_no(sender_account_no)
        if customer_account_sender != None:
            transferrable_amount = customer_account_sender.get_balance()
            if amount <= transferrable_amount:
                customer_account_receiver = self.search_customers_by_account_no(receiver_account_no)
                if customer_account_receiver != None:
                    customer_account_receiver.deposit(amount)
                customer_account_sender.withdraw(amount)  
                
    def admin_login(self, username, password):
		  #STEP A.1
        '''found_admin = self.search_admins_by_name(username)
        msg = "\n Login failed"
        if found_admin != None:
            if found_admin.get_password() == password:
                msg = "\n Login successful"
        return msg, found_admin'''
        
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
         print ("5) Update admin name")
         print ("6) Update admin address")
         print ("7) Show admin details")
         print ("8) Sign out")
         print (" ")
         option = int(input ("Choose your option: "))
         return option'''


    '''def run_admin_options(self, admin_obj):                                
        loop = 1
        while loop == 1:
            choice = self.admin_menu(admin_obj)
            if choice == 1:
                sender_lname = input("\n Please input sender surname: ")
                amount = float(input("\n Please input the amount to be transferred: "))
                receiver_lname = input("\n Please input receiver surname: ")
                receiver_account_no = input("\n Please input receiver account number: ")
                self.transferMoney(sender_lname, receiver_lname, receiver_account_no, amount)
                    
            elif choice == 2:
                #STEP A.4
                customer_name = input("\nPlease input customer surname : ")
                customer_account = self.search_customers_by_name(customer_name)
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
                customer_name = input("\nPlease input customer surname : ")
                customer_account = self.search_customers_by_name(customer_name)
                if customer_account != None:
                    customer_account.print_details()
            
            elif choice == 5:
                fname = input("\n Enter new admin first name: ")
                admin_obj.update_first_name(fname)
                sname = input("\n Enter new admin last name: ")
                admin_obj.update_last_name(sname)
                print("\n The admin name has been changed")
                
            elif choice == 6:
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
            
            elif choice == 7:
                admin_obj.print_details()
                
            elif choice == 8:
                loop = 0
        print ("\n Exit account operations")'''


    '''def print_all_accounts_details(self):
            # list related operation - move to main.py
            i = 0
            for c in self.accounts_list:
                i+=1
                print('\n %d. ' %i, end = ' ')
                c.print_details()
                print("------------------------")'''

if __name__ == "__main__":
    #app = BankSystem()
    #app.run_main_options()
    root = tk.Tk()
    root.geometry("400x375")
    app = MainView(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
    
'''app = BankSystem()
app.run_main_options()'''

''' ------------------- Already Existing Code Ends --------------------- '''