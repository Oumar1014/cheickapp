from tkinter import ttk
import tkinter as tk

def apply_modern_style():
    style = ttk.Style()
    
    # Configuration générale
    style.configure('.',
        font=('Helvetica', 10),
        background='#f0f0f0')
    
    # Style de l'en-tête
    style.configure('Header.TFrame',
        background='#ffffff')
    
    style.configure('Header.TLabelframe',
        padding=10,
        relief='solid',
        borderwidth=1)
    
    style.configure('HeaderTitle.TLabel',
        font=('Helvetica', 16, 'bold'),
        foreground='#2c3e50',
        background='#f8f9fa')
    
    style.configure('HeaderInfo.TLabel',
        font=('Helvetica', 12),
        foreground='#2c3e50',
        background='#f8f9fa')
    
    # Style du pied de page
    style.configure('Footer.TFrame',
        background='#f8f9fa')
    
    style.configure('Footer.TLabel',
        font=('Helvetica', 8),
        foreground='#6c757d',
        background='#f8f9fa')
    
    # Style des boutons
    style.configure('Modern.TButton',
        padding=(15, 8),
        font=('Helvetica', 10, 'bold'),
        background='#e9ecef',
        foreground='black')
    
    style.map('Modern.TButton',
        background=[('active', '#dee2e6'), ('disabled', '#f8f9fa')],
        foreground=[('disabled', '#6c757d')])
    
    # Style des labels
    style.configure('Modern.TLabel',
        padding=5,
        font=('Helvetica', 10))
    
    # Style des entrées
    style.configure('Modern.TEntry',
        padding=8,
        font=('Helvetica', 10))
    
    # Style des combobox
    style.configure('Modern.TCombobox',
        padding=8,
        font=('Helvetica', 10))
    
    # Style du Treeview
    style.configure('Modern.Treeview',
        background='white',
        fieldbackground='white',
        font=('Helvetica', 10),
        rowheight=30)
    
    style.configure('Modern.Treeview.Heading',
        font=('Helvetica', 10, 'bold'),
        padding=8,
        background='#f8f9fa',
        foreground='black')
    
    # Style des frames
    style.configure('Modern.TLabelframe',
        padding=15,
        relief='solid',
        borderwidth=1,
        background='white')
    
    style.configure('Modern.TLabelframe.Label',
        font=('Helvetica', 11, 'bold'),
        foreground='black',
        background='white')