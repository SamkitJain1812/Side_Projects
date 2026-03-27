from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__, static_folder='.')
CORS(app)

# ── DB CONFIG — change password here ──
DB_CONFIG = {
    "host":   "localhost",
    "user":   "root",
    "passwd": "your_dbms_password",   # <-- put your MySQL password
    "database": "Kirana_Store"
}

def get_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

def init_db():
    """Create database and tables if they don't exist."""
    cfg = DB_CONFIG.copy()
    cfg.pop("database")
    conn = mysql.connector.connect(**cfg)
    cur  = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS Kirana_Store")
    cur.execute("USE Kirana_Store")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS stock (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            p_name   VARCHAR(50),
            company  VARCHAR(50),
            expiry   VARCHAR(20),
            qty      INT,
            price    INT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            product  VARCHAR(50),
            qty      INT,
            price    INT,
            gst      INT,
            total    FLOAT,
            created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS purchase (
            id       INT AUTO_INCREMENT PRIMARY KEY,
            product  VARCHAR(50),
            qty      INT,
            cost     INT,
            created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    print("✔ Database initialised.")

# ════════════════════════════════════════
#  STOCK
# ════════════════════════════════════════

@app.route('/api/stock', methods=['GET'])
def get_stock():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM stock ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/stock', methods=['POST'])
def add_stock():
    d = request.json
    conn = get_db(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO stock (p_name, company, expiry, qty, price) VALUES (%s,%s,%s,%s,%s)",
        (d['p_name'], d['company'], d['expiry'], d['qty'], d['price'])
    )
    conn.commit(); conn.close()
    return jsonify({"status": "ok", "message": "Item added"})

@app.route('/api/stock/<int:item_id>', methods=['PUT'])
def update_stock(item_id):
    d = request.json
    conn = get_db(); cur = conn.cursor()
    cur.execute(
        "UPDATE stock SET p_name=%s, company=%s, expiry=%s, qty=%s, price=%s WHERE id=%s",
        (d['p_name'], d['company'], d['expiry'], d['qty'], d['price'], item_id)
    )
    conn.commit(); conn.close()
    return jsonify({"status": "ok", "message": "Item updated"})

@app.route('/api/stock/<int:item_id>', methods=['DELETE'])
def delete_stock(item_id):
    conn = get_db(); cur = conn.cursor()
    cur.execute("DELETE FROM stock WHERE id=%s", (item_id,))
    conn.commit(); conn.close()
    return jsonify({"status": "ok", "message": "Item deleted"})

# ════════════════════════════════════════
#  SALES
# ════════════════════════════════════════

@app.route('/api/sales', methods=['GET'])
def get_sales():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM sales ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/sales', methods=['POST'])
def add_sale():
    d = request.json
    qty   = int(d['qty'])
    price = int(d['price'])
    gst   = int(d.get('gst', 0))
    total = price * qty * (1 + gst / 100)
    conn = get_db(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO sales (product, qty, price, gst, total) VALUES (%s,%s,%s,%s,%s)",
        (d['product'], qty, price, gst, round(total, 2))
    )
    conn.commit(); conn.close()
    return jsonify({"status": "ok", "total": round(total, 2)})

# ════════════════════════════════════════
#  PURCHASE
# ════════════════════════════════════════

@app.route('/api/purchase', methods=['GET'])
def get_purchase():
    conn = get_db(); cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM purchase ORDER BY id DESC")
    rows = cur.fetchall()
    conn.close()
    return jsonify(rows)

@app.route('/api/purchase', methods=['POST'])
def add_purchase():
    d = request.json
    conn = get_db(); cur = conn.cursor()
    cur.execute(
        "INSERT INTO purchase (product, qty, cost) VALUES (%s,%s,%s)",
        (d['product'], d['qty'], d['cost'])
    )
    conn.commit(); conn.close()
    return jsonify({"status": "ok"})

# ════════════════════════════════════════
#  DASHBOARD STATS
# ════════════════════════════════════════

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db(); cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM stock")
    items = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM sales")
    bills = cur.fetchone()[0]
    cur.execute("SELECT COALESCE(SUM(total),0) FROM sales")
    revenue = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM purchase")
    purchases = cur.fetchone()[0]
    conn.close()
    return jsonify({"items": items, "bills": bills, "revenue": round(revenue,2), "purchases": purchases})

# ════════════════════════════════════════
#  SERVE FRONTEND
# ════════════════════════════════════════

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    init_db()
    print("🚀 Kirana Ki Dukan running at http://localhost:5000")
    app.run(debug=True, port=5000)
