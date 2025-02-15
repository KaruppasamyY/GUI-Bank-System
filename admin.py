class Admin:
    
    def __init__(self, fname, lname, address, user_name, password, full_rights):
        self.fname = fname
        self.lname = lname
        self.address = address
        self.user_name = user_name
        self.password = password
        self.full_admin_rights = full_rights
    
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
    
    def set_username(self, uname):
        self.user_name = uname
        
    def get_username(self):
        return self.user_name
        
    def get_address(self):
        return self.address      
    
    def update_password(self, password):
        self.password = password
    
    def get_password(self):
        return self.password
    
    def set_full_admin_right(self, admin_right):
        self.full_admin_rights = admin_right

    def has_full_admin_right(self):
        return self.full_admin_rights
    
    def print_details(self):
        '''print("First name: %s" %self.fname)
        print("Last name: %s" %self.lname)
        print("Address : %s" %self.address[0])
        print("          %s" %self.address[1])
        print("          %s" %self.address[2])
        print("          %s" %self.address[3])
        print(" ")'''
        
        ret_str = "\n  First name: %s" %self.fname
        ret_str += "\n  Last name: %s" %self.lname
        ret_str += "\n  Address : %s" %self.address[0]
        ret_str += "\n            %s" %self.address[1]
        ret_str += "\n            %s" %self.address[2]
        ret_str += "\n            %s" %self.address[3]
        ret_str += ""
        return ret_str
    
    def upload_to_file(self):
        ret_str = f'"{self.fname}", '
        ret_str += f'"{self.lname}", '
        ret_str += f'{self.address}, '
        ret_str += f'"{self.user_name}", '
        ret_str += f'"{self.password}", '
        ret_str += f"{self.full_admin_rights}\n"
        return ret_str