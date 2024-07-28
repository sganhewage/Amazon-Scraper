import datetime

class Order:
    def __init__(self, order_placed: datetime.date, order_delivered: datetime.date, 
                 total: float, total_before_tax: float, item_name: str, 
                 status: str, seller: str, payment_method: str, url: str,
                 order_number: str, shipping_address: str):
        self.order_placed = order_placed
        self.order_delivered = order_delivered
        self.total = total
        self.total_before_tax = total_before_tax
        self.item_name = item_name
        self.status = status
        self.seller = seller
        self.payment_method = payment_method
        self.url = url
        self.order_number = order_number
        self.shipping_address = shipping_address
