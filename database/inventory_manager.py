from datetime import datetime
from .db_manager import DatabaseManager

class InventoryManager:
    def __init__(self, db_path):
        self.db = DatabaseManager(db_path)
    
    def get_inventory(self):
        """Get current inventory with movements"""
        query = """
            SELECT 
                m.name,
                m.quantity,
                m.price,
                COALESCE(im.entries, 0) as entries,
                COALESCE(im.outputs, 0) as outputs,
                COALESCE(im.comment, '') as comment,
                m.created_at
            FROM motorcycles m
            LEFT JOIN inventory_movements im ON m.id = im.motorcycle_id
            ORDER BY m.created_at DESC
        """
        
        try:
            results = self.db.execute_query(query)
            inventory = []
            for row in results:
                inventory.append({
                    'date': row[6],
                    'motorcycle': row[0],
                    'prev_stock': row[1] - (row[3] or 0) + (row[4] or 0),
                    'entries': row[3] or 0,
                    'outputs': row[4] or 0,
                    'price': row[2] or 0.0,
                    'balance': row[1],
                    'comment': row[5]
                })
            return inventory
        except Exception as e:
            print(f"Error getting inventory: {e}")
            return []

    def save_sale(self, motorcycle_name, quantity, price, client_name, client_address, client_phone):
        """Record a sale in database"""
        try:
            # First get motorcycle id
            query = "SELECT id, quantity FROM motorcycles WHERE name = ?"
            results = self.db.execute_query(query, (motorcycle_name,))
            if not results:
                return False
                
            motorcycle_id, current_quantity = results[0]
            
            if current_quantity < quantity:
                return False
                
            # Record sale
            query = """
                INSERT INTO sales (
                    motorcycle_id, quantity, price, 
                    client_name, client_address, client_phone
                ) VALUES (?, ?, ?, ?, ?, ?)
            """
            if not self.db.execute_update(query, (
                motorcycle_id, quantity, price,
                client_name, client_address, client_phone
            )):
                return False
            
            # Update motorcycle quantity
            query = """
                UPDATE motorcycles 
                SET quantity = quantity - ?
                WHERE id = ?
            """
            if not self.db.execute_update(query, (quantity, motorcycle_id)):
                return False
                
            # Record movement
            query = """
                INSERT INTO inventory_movements (
                    motorcycle_id, outputs, price, comment
                ) VALUES (?, ?, ?, ?)
            """
            return self.db.execute_update(query, (
                motorcycle_id, quantity, price,
                f"Vente à {client_name}"
            ))
            
        except Exception as e:
            print(f"Error recording sale: {e}")
            return False
    
    def save_motorcycle(self, name, entries, price, comment=""):
        """Save or update motorcycle in inventory"""
        try:
            # First, update or insert motorcycle
            query = """
                INSERT INTO motorcycles (name, quantity, price)
                VALUES (?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                quantity = quantity + ?,
                price = ?
            """
            if not self.db.execute_update(query, (name, entries, price, entries, price)):
                return False
            
            # Then record the movement
            query = """
                INSERT INTO inventory_movements (
                    motorcycle_id, entries, price, comment
                ) VALUES (
                    (SELECT id FROM motorcycles WHERE name = ?),
                    ?, ?, ?
                )
            """
            return self.db.execute_update(query, (name, entries, price, comment))
        except Exception as e:
            print(f"Error saving motorcycle: {e}")
            return False
    
    def delete_motorcycle(self, name):
        """Delete a motorcycle from inventory"""
        query = "DELETE FROM motorcycles WHERE name = ?"
        return self.db.execute_update(query, (name,))
    
    def clear_database(self):
        """Clear all data from database"""
        try:
            queries = [
                "DELETE FROM inventory_movements",
                "DELETE FROM sales",
                "DELETE FROM motorcycles"
            ]
            for query in queries:
                if not self.db.execute_update(query):
                    return False
            return True
        except Exception as e:
            print(f"Error clearing database: {e}")
            return False

    def get_sales_report(self, date=None):
        """Get sales report for specific date"""
        query = """
            SELECT 
                s.id,
                s.sale_date,
                m.name as motorcycle,
                s.client_name,
                s.quantity,
                s.price,
                (s.quantity * s.price) as total
            FROM sales s
            JOIN motorcycles m ON s.motorcycle_id = m.id
        """
        params = []
        
        if date:
            query += " WHERE DATE(s.sale_date) = DATE(?)"
            params.append(date.strftime('%Y-%m-%d'))
            
        query += " ORDER BY s.sale_date DESC"
        
        try:
            results = self.db.execute_query(query, params)
            return [{
                'id': row[0],
                'date': row[1],
                'motorcycle': row[2],
                'client': row[3],
                'quantity': row[4],
                'price': row[5],
                'total': row[6]
            } for row in results]
        except Exception as e:
            print(f"Error getting sales report: {e}")
            return []