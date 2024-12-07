# -*- coding: utf-8 -*-
"""
Created on Sat Nov 23 14:53:07 2024

@author: KS
"""


class CustomerAccount:
    def __init__(self, fname, lname, address, account_no, balance, account_name, interest_rate, overdraft_limit):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.account_no = account_no
        self.balance = float(balance)
        self.account_name = account_name
        self.interest_rate = interest_rate
        self.overdraft_limit = overdraft_limit
    
    def update_first_name(self, fname):
        self.fname = fname
    
    def update_last_name(self, lname):
        self.lname = lname
                
    def get_first_name(self):
        return self.fname
    
    def get_last_name(self):
        return self.lname
        
    def update_address(self, addr):
        self.address = addr
        
    def get_address(self):
        return self.address
    
    def get_account_name(self):
        return self.account_name
    
    def get_interest_rate(self):
        return self.interest_rate
    
    def get_overdraft_limit(self):
        return self.overdraft_limit
    
    def update_interest_rate(self, interest_rate):
        self.interest_rate = interest_rate
        
    def update_overdraft_limit(self, overdraft_limit):
        self.overdraft_limit = overdraft_limit
    
    def deposit(self, amount):
        if self.balance < 0:
            while self.balance != 0:
                self.balance += 1
                amount -= 1
                self.overdraft_limit += 1
            while self.balance == 0 and amount != 0:
                self.balance += amount
            print("\n The overdraft balance is %s" %self.overdraft_limit)
        else:
            self.balance+=amount
            print("\n The overdraft balance is %s" %self.overdraft_limit)
        
    def withdraw(self, amount):
        #ToDo
        main_balance = 0
        od_balance = 0
        withdrawable_amount = self.get_balance() + self.get_overdraft_limit()
        if amount <= withdrawable_amount and amount <= self.get_balance():
            self.balance -= amount
        elif amount <= withdrawable_amount and amount >= self.get_balance():
            while self.get_balance() != 0:
                self.balance -= 1
                amount -= 1
                main_balance += 1
            while amount != 0:
                self.overdraft_limit -= 1
                self.balance -= 1
                amount -= 1
                od_balance += 1
            print("\n The overdraft balance is %s" %self.overdraft_limit)
        else:
            print("\n Insufficient balance\n")
            print("\n The overdraft balance is %s" %self.overdraft_limit)
        
    def print_balance(self):
        print("\n The account balance is %.2f" %self.balance)
        
    def get_balance(self):
        return self.balance
    
    def get_account_no(self):
        return self.account_no
    
    def account_menu(self):
        print ("\n Your Transaction Options Are:")
        print ("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print ("1) Deposit money")
        print ("2) Withdraw money")
        print ("3) Check balance")
        print ("4) Update customer name")
        print ("5) Update customer address")
        print ("6) Show customer details")
        print ("7) Back")
        print (" ")
        option = int(input ("Choose your option: "))
        return option
    
    def print_details(self):
        #STEP A.4.3
        print("\nFirst name: %s" %self.fname)
        print("Last name: %s" %self.lname)
        print("Account No: %s" %self.account_no)
        print("Address : %s" %self.address[0])
        print("          %s" %self.address[1])
        print("          %s" %self.address[2])
        print("          %s" %self.address[3])
        print("Account name: %s" %self.account_name)
        print("Interest rate: %s" %self.interest_rate)
        print("Overdraft limit: %s" %self.overdraft_limit)
        
    def run_account_options(self):
        loop = 1
        while loop == 1:
            choice = self.account_menu()
            if choice == 1:
                #STEP A.4.1
                amount = float(input("\n Please enter amount to be deposited: "))
                self.deposit(amount)
                self.print_balance()
                
            elif choice == 2:
                #ToDo
                amount = float(input("\n Please enter amount to withdraw: "))
                self.withdraw(amount)
                self.print_balance()
            
            elif choice == 3:
                #STEP A.4.4
                self.print_balance()
                
            elif choice == 4:
                #STEP A.4.2
                fname = input("\n Enter new customer first name: ")
                self.update_first_name(fname)
                sname = input("\n Enter new customer last name: ")
                self.update_last_name(sname)
                
            elif choice == 5:
                #ToDo
                self.addr = []
                print("\nPlease provide the address details to be updated")
                house_number = input("\nPlease enter the house number: ")
                self.addr.append(house_number)
                street_name = input("\nPlease enter the street name: ")
                self.addr.append(street_name)
                city_name = input("\nPlease enter the name of the city: ")
                self.addr.append(city_name)
                post_code = input("\nPlease enter the post code: ")
                self.addr.append(post_code)
                
                self.update_address(self.addr)
                print("\nThe Address has been updated successfully as per your request")
            
            elif choice == 6:
                self.print_details()
                
            elif choice == 7:
                loop = 0
        print ("\n Exit account operations")
        
    def upload_to_file(self):
        ret_str = f"{self.fname}, "
        ret_str += f"{self.lname}, "
        ret_str += f"{self.address}, "
        ret_str += f"{self.account_no}, "
        ret_str += "{:.2f}, ".format(self.balance)
        ret_str += f"{self.account_name}, "
        ret_str += f"{self.interest_rate}, "
        ret_str += "{:.2f}\n".format(self.overdraft_limit)
        return ret_str