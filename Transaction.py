from enum import Enum
class CardTransaction:
    def __init__(self,user_id,amount,date,type):
        self.user_id = user_id
        self.amount =amount
        self.date = date
        self.type = type


class TranType(Enum):
    CASH_IN = "CASH IN"
    CASHO_UT = "CASH OUT"