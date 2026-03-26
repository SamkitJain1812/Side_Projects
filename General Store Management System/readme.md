# 🛒 Kirana Ki Dukan — General Store Management System

> A full-stack store management dashboard for small Indian kirana/general stores.  
> Built with a Haryanvi desi aesthetic — phulkari patterns, saffron-turmeric palette, earthen textures.

![Python](https://img.shields.io/badge/Python-3.8+-E8520A?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-1C0F05?style=flat-square&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-00758F?style=flat-square&logo=mysql&logoColor=white)
![HTML](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-F0B429?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-4E6B3A?style=flat-square)

---

## 📸 Features

- **📦 Stock Management** — Add, edit, delete products. Search by name or company. Expiry & low-stock badges.
- **🧾 Bill Generator** — Create GST-included receipts with live preview and print support.
- **📈 Sales Log** — Auto-records every bill. Shows total revenue.
- **🛍️ Purchase Records** — Log incoming goods from suppliers.
- **🏠 Dashboard** — Live stats (items, bills, revenue, purchases) + recent stock overview.
- **🔴 Live DB Status** — Pulsing indicator shows MySQL connection status in real time.

---

## 🗂️ Project Structure

```
kirana-ki-dukan/
├── app.py              # Flask backend — REST API + MySQL connection
├── index.html          # Frontend dashboard (single-file HTML/CSS/JS)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## ⚙️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Frontend   | HTML5, CSS3 (Flexbox), Vanilla JS |
| Backend    | Python 3, Flask                   |
| Database   | MySQL 8                           |
| Fonts      | Abril Fatface, Mukta, JetBrains Mono (Google Fonts) |
| API Style  | REST (JSON)                       |

---

## 🚀 Getting Started

### Prerequisites

Make sure these are installed on your machine:

- [Python 3.8+](https://www.python.org/downloads/)
- [MySQL 8.0+](https://dev.mysql.com/downloads/)
- [Git](https://git-scm.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/kirana-ki-dukan.git
cd kirana-ki-dukan
```

---

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install flask flask-cors mysql-connector-python
```

---

### 3. Configure MySQL Password

Open `app.py` and find this block near the top:

```python
DB_CONFIG = {
    "host":   "localhost",
    "user":   "root",
    "passwd": "your_password_here",   # <-- change this
    "database": "Kirana_Store"
}
```

Replace `your_password_here` with your actual MySQL root password and save the file.

> **Note:** The app will automatically create the `Kirana_Store` database and all required tables on first run. You don't need to create anything manually in MySQL.

---

### 4. Make Sure MySQL is Running

**Windows:**
```bash
net start mysql
```

**macOS (Homebrew):**
```bash
brew services start mysql
```

**Linux:**
```bash
sudo systemctl start mysql
```

---

### 5. Start the Flask Server

```bash
python app.py
```

You should see:

```
✔ Database initialised.
🚀 Kirana Ki Dukan running at http://localhost:5000
```

---

### 6. Open in Browser

```
http://localhost:5000
```

The dashboard will load. Check the top-right corner — it should show **🟢 MySQL Connected**.

---

## 🗃️ Database Schema

The following tables are auto-created in the `Kirana_Store` database:

```sql
-- Product inventory
CREATE TABLE stock (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    p_name   VARCHAR(50),
    company  VARCHAR(50),
    expiry   VARCHAR(20),
    qty      INT,
    price    INT
);

-- Sales / bill records
CREATE TABLE sales (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    product  VARCHAR(50),
    qty      INT,
    price    INT,
    gst      INT,
    total    FLOAT,
    created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Purchase / incoming goods
CREATE TABLE purchase (
    id       INT AUTO_INCREMENT PRIMARY KEY,
    product  VARCHAR(50),
    qty      INT,
    cost     INT,
    created  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
---

## 🛠️ Common Issues

| Problem | Fix |
|---|---|
| `pip` not recognized | Install Python and check **Add to PATH** during setup |
| `Access denied for user 'root'` | Wrong MySQL password in `app.py` |
| `MySQL Connected` not showing | MySQL service is not running — start it first |
| Port 5000 already in use | Change `port=5000` to `port=5001` in `app.py`, then open `http://localhost:5001` |
| Page loads but data is empty | Don't close the terminal running `python app.py` |

---

## 📄 License

GNU General Public License — free to use, modify, and distribute.
