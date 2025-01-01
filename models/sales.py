from datetime import datetime
from typing import List

class Sale:
    def __init__(self, motorcycle_name: str, quantity: int, price: float, 
                 client_name: str = "", client_address: str = "", client_phone: str = ""):
        self.motorcycle_name = motorcycle_name
        self.quantity = quantity
        self.price = price
        self.date = datetime.now()
        self.client_name = client_name
        self.client_address = client_address
        self.client_phone = client_phone
        
class SalesManager:
    def __init__(self):
        self.sales: List[Sale] = []
    
    def record_sale(self, motorcycle_name: str, quantity: int, price: float,
                   client_name: str, client_address: str, client_phone: str) -> None:
        sale = Sale(motorcycle_name, quantity, price, client_name, client_address, client_phone)
        self.sales.append(sale)
    
    def get_sales_report(self) -> List[dict]:
        return [
            {
                "date": sale.date.strftime("%Y-%m-%d %H:%M"),
                "motorcycle": sale.motorcycle_name,
                "quantity": sale.quantity,
                "price": sale.price,
                "total": sale.quantity * sale.price,
                "client": sale.client_name
            }
            for sale in self.sales
        ]