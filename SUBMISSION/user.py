class user:
    def __init__(self, username, password, ip_num, sock_num, status):
        self.username = username
        self.password = password
        self.ip_num = ip_num
        self.status = status
        self.sock_num = sock_num
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_ip_num(self):
        return self.ip_num
    
    def get_status(self):
        return self.status
    
    def get_sock_num(self):
        return self.sock_num
    
    def set_sock_num(self,sock_num):
        self.sock_num = sock_num
        
    def set_status(self, status):
        self.status = status
    
    def set_ip_num(self, ip_num):
        self.ip_num = ip_num
    
