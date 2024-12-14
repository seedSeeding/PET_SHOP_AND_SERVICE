class Offer:
    def __init__(self,_id,name,price):
        self.id = _id
        self.name = name
        self.price = price
    def full_text(self):
        return f"{self.name} - P{self.price}"
