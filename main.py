import tkinter as tk
from gui.main_window import MainWindow
from gui.styles import apply_modern_style

def main():
    root = tk.Tk()
    root.title("Gestion de Vente de Motos")
    root.geometry("1024x768")
    
    # Apply modern style
    apply_modern_style()
    
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()