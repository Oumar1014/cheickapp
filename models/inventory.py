from typing import Dict, List
from datetime import datetime, timedelta
from .motorcycle import Motorcycle
from .stock_movement import StockMovement

class Inventory:
    def __init__(self):
        self.motorcycles: Dict[str, Motorcycle] = {}
        self.movements: List[StockMovement] = []
        self._initialize_inventory()
    
    def _initialize_inventory(self):
        initial_inventory = [
            ("Marques", 55),
            ("Ghana", 40),
            ("Ralo", 13),
            ("Saneli", 1),
            ("M. Diallo", 3),
            ("ARSONIC", 1),
            ("H-EXPRESS", 14),
            ("Royale", 2),
            ("KTM 125", 1),
            ("X-1", 1),
            ("Sanya", 1),
            ("Roche", 0),
            ("KTM 150", 0),
            ("Haojue B40", 0),
            ("Benelli AP-150", 1)
        ]
        
        for name, qty in initial_inventory:
            self.motorcycles[name] = Motorcycle(name, qty)
            if qty > 0:
                self.add_movement(name, datetime.now(), entries=qty)
    
    def get_stock(self) -> List[Motorcycle]:
        """Retourne la liste des motos en stock"""
        return list(self.motorcycles.values())
    
    def get_previous_stock(self, name: str, date: datetime) -> int:
        previous_date = date - timedelta(days=1)
        previous_movements = [m for m in self.movements 
                            if m.motorcycle_name == name and 
                            m.date.date() <= previous_date.date()]
        
        if not previous_movements:
            return 0
            
        total_entries = sum(m.entries for m in previous_movements)
        total_outputs = sum(m.outputs for m in previous_movements)
        return total_entries - total_outputs
    
    def add_movement(self, name: str, date: datetime, entries: int = 0, outputs: int = 0, price: float = 0.0, comment: str = "") -> None:
        if name not in self.motorcycles:
            self.motorcycles[name] = Motorcycle(name)
        movement = StockMovement(name, date, entries, outputs, price, comment)
        self.movements.append(movement)
        
        # Mise à jour de la quantité dans l'objet Motorcycle
        motorcycle = self.motorcycles[name]
        motorcycle.quantity += entries - outputs
        if price > 0:
            motorcycle.price = price
    
    def remove_motorcycle(self, name: str, quantity: int) -> bool:
        """Retire une quantité de motos du stock. Retourne True si succès, False si stock insuffisant"""
        if name in self.motorcycles:
            motorcycle = self.motorcycles[name]
            if motorcycle.quantity >= quantity:
                self.add_movement(name, datetime.now(), outputs=quantity)
                return True
        return False
    
    def get_daily_movements(self, name: str = None) -> List[dict]:
        movements = self.movements
        if name:
            movements = [m for m in movements if m.motorcycle_name == name]
        
        consolidated = {}
        for movement in movements:
            key = movement.motorcycle_name
            if key not in consolidated:
                prev_stock = self.get_previous_stock(key, movement.date)
                consolidated[key] = {
                    'date': movement.date,
                    'motorcycle': key,
                    'prev_stock': prev_stock,
                    'entries': 0,
                    'outputs': 0,
                    'price': movement.price,
                    'balance': 0,
                    'comment': movement.comment
                }
            
            consolidated[key]['entries'] += movement.entries
            consolidated[key]['outputs'] += movement.outputs
            consolidated[key]['balance'] = (consolidated[key]['prev_stock'] + 
                                          consolidated[key]['entries'] - 
                                          consolidated[key]['outputs'])
            if movement.price > 0:
                consolidated[key]['price'] = movement.price
            if movement.comment:
                consolidated[key]['comment'] = movement.comment
        
        result = []
        for data in consolidated.values():
            data['date'] = data['date'].strftime("%Y-%m-%d")
            result.append(data)
        
        return result