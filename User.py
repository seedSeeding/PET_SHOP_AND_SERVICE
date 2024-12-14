class User:
    def __init__(self,_id, username=None, password=None, fullname=None, contact=None, email=None, sex=None, location=None):
        self.id = _id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.contact = contact
        self.email = email
        self.sex = sex
        self.location = location
    def check_details(self):
        return self.fullname and self.contact and self.email and self.sex