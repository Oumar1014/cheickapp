from datetime import datetime

class StockMovement:
    def __init__(self, motorcycle_name: str, date: datetime, entries: int = 0, 
                 outputs: int = 0, price: float = 0.0, comment: str = ""):
        self.motorcycle_name = motorcycle_name
        self.date = date if isinstance(date, datetime) else datetime.now()
        self.entries = entries
        self.outputs = outputs
        self.price = price
        self.comment = comment

    def get_balance(self) -> int:
        return self.entries - self.outputs