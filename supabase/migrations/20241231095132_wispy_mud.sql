-- Schema for motorcycle inventory management system

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

-- Indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(sale_date);
CREATE INDEX IF NOT EXISTS idx_movements_date ON inventory_movements(movement_date);

-- Insert initial inventory data
INSERT OR IGNORE INTO motorcycles (name, quantity, price) VALUES
    ("Marques", 55, 0),
    ("Ghana", 40, 0),
    ("Ralo", 13, 0),
    ("Saneli", 1, 0),
    ("M. Diallo", 3, 0),
    ("ARSONIC", 1, 0),
    ("H-EXPRESS", 14, 0),
    ("Royale", 2, 0),
    ("KTM 125", 1, 0),
    ("X-1", 1, 0),
    ("Sanya", 1, 0),
    ("Roche", 0, 0),
    ("KTM 150", 0, 0),
    ("Haojue B40", 0, 0),
    ("Benelli AP-150", 1, 0);