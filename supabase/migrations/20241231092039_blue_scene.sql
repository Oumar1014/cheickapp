/*
  # Initial database schema

  1. Tables
    - motorcycles: Stock des motos
    - sales: Enregistrement des ventes
    - inventory_movements: Mouvements de stock

  2. Indexes
    - idx_sales_date: Pour les recherches par date
    - idx_movements_date: Pour les recherches par date
*/

CREATE TABLE IF NOT EXISTS motorcycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    quantity INTEGER DEFAULT 0,
    price REAL DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    motorcycle_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    client_name TEXT NOT NULL,
    client_address TEXT,
    client_phone TEXT,
    sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (motorcycle_id) REFERENCES motorcycles(id)
);

CREATE TABLE IF NOT EXISTS inventory_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    motorcycle_id INTEGER NOT NULL,
    entries INTEGER DEFAULT 0,
    outputs INTEGER DEFAULT 0,
    price REAL DEFAULT 0.0,
    comment TEXT,
    movement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (motorcycle_id) REFERENCES motorcycles(id)
);

CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_movements_date ON inventory_movements(movement_date);