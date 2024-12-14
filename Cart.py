class ProductCart:
    def __init__(self,_id,user_id,product,quantity,date):
        self.id = _id
        self.user_id = user_id
        self.product = product
        self.quantity = quantity
        self.date = date
    def get_price(self):
        parts = self.product.split(' - P')
        if len(parts) == 2:
            try:
                return int(parts[1])
            except ValueError:
                return 0



class ServiceCart:
    def __init__(self,_id,user_id,service,details,date):
        self.id = _id
        self.user_id = user_id
        self.service = service
        self.details = details
        self.date = date

    def get_price(self):
        parts = self.service.split(' - P')
        if len(parts) == 2:
            try:
                return int(parts[1])
            except ValueError:
                return 0

class Cart:
    def __init__(self,service,product):
        self.service = service
        self.product = product