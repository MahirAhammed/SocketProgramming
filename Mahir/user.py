class user:
    def __init__(self, username, password, ip_num, udp_addr, status):
        self.username = username
        self.password = password
        self.ip_num = ip_num
        self.status = status
        self.udp_addr = udp_addr
    
    def get_username(self):
        return self.username
    
    def get_password(self):
        return self.password
    
    def get_ip_num(self):
        return self.ip_num
    
    def get_status(self):
        return self.status
    
    def get_udp_addr(self):
        return self.udp_addr
    
    def set_udp_addr(self,udp_addr):
        self.udp_addr = udp_addr
        
    def set_status(self, status):
        self.status = status
    
    def set_ip_num(self, ip_num):
        self.ip_num = ip_num
    
