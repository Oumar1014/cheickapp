class Motorcycle:
    def __init__(self, name: str, quantity: int = 0, price: float = 0.0):
        self.name = name
        self.quantity = quantity
        self.price = price
        
    def __str__(self):
        return f"{self.name} - Quantity: {self.quantity} - Price: {self.price}"