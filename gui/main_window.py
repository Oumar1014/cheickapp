import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager
from gui.inventory_frame import InventoryFrame
from gui.sales_frame import SalesFrame
from gui.reports_frame import ReportsFrame

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.db_path = 'inventory.db'
        
        # Header frame avec style moderne
        header_frame = ttk.Frame(master, style='Header.TFrame')
        header_frame.pack(fill='x', padx=10, pady=5)
        
        # Company info avec style moderne
        company_frame = ttk.LabelFrame(header_frame, style='Header.TLabelframe')
        company_frame.pack(fill='x')
        
        # Titre principal
        title_label = ttk.Label(
            company_frame,
            text="GESTION DES MOTOS",
            style='HeaderTitle.TLabel'
        )
        title_label.pack(pady=(10, 5))
        
        # Info de contact
        contact_label = ttk.Label(
            company_frame,
            text="NOUHOU BAMMA TOURE\nVendeur des motos\nTél : +223 77873789 / 90434307 / 83211674\nAdresse : 5eme Quartier GAO Rep.Du Mali",
            style='HeaderInfo.TLabel',
            justify='center'
        )
        contact_label.pack(pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=True, fill='both', padx=5, pady=5)
        
        # Create frames with database path
        self.inventory_frame = InventoryFrame(self.notebook, self.db_path)
        self.sales_frame = SalesFrame(self.notebook, self.db_path)
        self.reports_frame = ReportsFrame(self.notebook, self.db_path)
        
        # Add frames to notebook
        self.notebook.add(self.inventory_frame, text='Inventaire')
        self.notebook.add(self.sales_frame, text='Ventes')
        self.notebook.add(self.reports_frame, text='Rapports')