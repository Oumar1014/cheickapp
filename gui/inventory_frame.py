import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from database.inventory_manager import InventoryManager

class InventoryFrame(ttk.Frame):
    def __init__(self, parent, db_path):
        super().__init__(parent)
        self.inventory_manager = InventoryManager(db_path)
        
        # Create treeview
        columns = ('Date', 'Marques', 'Stock Précédent', 'Entrées', 'Sorties', 'Prix', 'Quantité Finale', 'Commentaire')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', style='Modern.Treeview')
        
        # Configure columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Form frame
        self.create_form_frame()
        
        # Initial load
        self.refresh_inventory()
    
    def create_form_frame(self):
        """Crée le formulaire d'ajout/modification"""
        form_frame = ttk.LabelFrame(self, text="Ajouter/Modifier Stock", style='Modern.TLabelframe')
        form_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Form fields
        fields_frame = ttk.Frame(form_frame)
        fields_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Date
        ttk.Label(fields_frame, text="Date:").grid(row=0, column=0, padx=5, pady=5)
        self.date_entry = DateEntry(fields_frame, width=12, background='darkblue',
                                  foreground='white', borderwidth=2)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        
        # Nom
        ttk.Label(fields_frame, text="Nom:").grid(row=0, column=2, padx=5, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.name_var).grid(row=0, column=3, padx=5, pady=5)
        
        # Entrées
        ttk.Label(fields_frame, text="Entrées:").grid(row=0, column=4, padx=5, pady=5)
        self.entries_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.entries_var).grid(row=0, column=5, padx=5, pady=5)
        
        # Prix
        ttk.Label(fields_frame, text="Prix:").grid(row=0, column=6, padx=5, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.price_var).grid(row=0, column=7, padx=5, pady=5)
        
        # Commentaire
        ttk.Label(fields_frame, text="Commentaire:").grid(row=1, column=0, padx=5, pady=5)
        self.comment_var = tk.StringVar()
        ttk.Entry(fields_frame, textvariable=self.comment_var).grid(row=1, column=1, columnspan=7, sticky='ew', padx=5, pady=5)
        
        # Buttons
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Enregistrer", command=self.save_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Ajouter", command=self.add_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Modifier", command=self.modify_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Supprimer", command=self.delete_stock).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Rafraîchir", command=self.refresh_inventory).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Nettoyer Base", command=self.clear_database).pack(side=tk.RIGHT, padx=5)
    
    def refresh_inventory(self):
        """Rafraîchit l'affichage de l'inventaire"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            inventory = self.inventory_manager.get_inventory()
            for item in inventory:
                # Convertir le dictionnaire en liste de valeurs dans le bon ordre
                values = [
                    item.get('date', ''),
                    item.get('motorcycle', ''),
                    item.get('prev_stock', 0),
                    item.get('entries', 0),
                    item.get('outputs', 0),
                    f"{item.get('price', 0.0):.2f}",
                    item.get('balance', 0),
                    item.get('comment', '')
                ]
                self.tree.insert('', 'end', values=values)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors du rafraîchissement: {str(e)}")
    
    def save_stock(self):
        """Enregistre les modifications dans la base de données"""
        try:
            name = self.name_var.get()
            entries = int(self.entries_var.get() or 0)
            price = float(self.price_var.get() or 0)
            comment = self.comment_var.get()
            
            if not name:
                messagebox.showerror("Erreur", "Le nom est obligatoire!")
                return
            
            if self.inventory_manager.save_motorcycle(name, entries, price, comment):
                self.clear_form()
                self.refresh_inventory()
                messagebox.showinfo("Succès", "Stock enregistré avec succès!")
            else:
                messagebox.showerror("Erreur", "Erreur lors de l'enregistrement!")
        except ValueError:
            messagebox.showerror("Erreur", "Valeurs invalides!")
    
    def add_stock(self):
        """Ajoute un nouveau stock"""
        self.save_stock()
    
    def modify_stock(self):
        """Modifie le stock sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à modifier")
            return
        
        item = self.tree.item(selection[0])
        values = item['values']
        
        self.name_var.set(values[1])  # Marques
        self.entries_var.set(values[3])  # Entrées
        self.price_var.set(values[5])  # Prix
        self.comment_var.set(values[7])  # Commentaire
    
    def delete_stock(self):
        """Supprime le stock sélectionné"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à supprimer")
            return
        
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment supprimer cet élément?"):
            item = self.tree.item(selection[0])
            name = item['values'][1]
            if self.inventory_manager.delete_motorcycle(name):
                self.refresh_inventory()
                messagebox.showinfo("Succès", "Stock supprimé avec succès!")
            else:
                messagebox.showerror("Erreur", "Erreur lors de la suppression!")
    
    def clear_form(self):
        """Nettoie le formulaire"""
        self.name_var.set('')
        self.entries_var.set('')
        self.price_var.set('')
        self.comment_var.set('')
    
    def clear_database(self):
        """Nettoie la base de données"""
        if messagebox.askyesno("Confirmation", "Voulez-vous vraiment nettoyer la base de données? Cette action est irréversible!"):
            if self.inventory_manager.clear_database():
                self.refresh_inventory()
                messagebox.showinfo("Succès", "Base de données nettoyée avec succès!")
            else:
                messagebox.showerror("Erreur", "Erreur lors du nettoyage de la base de données!")