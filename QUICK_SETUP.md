# 🚀 Local Setup for Expense Tracker

## Quick Start

### 1. Download the project
```bash
git clone https://github.com/your-username/expense-tracker-portfolio.git
cd expense-tracker-portfolio
```

### 2. Install Python dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create demo data
```bash
python create_demo_data.py
```

### 4. Run the application
```bash
python run.py
```

### 5. Open in your browser
http://127.0.0.1:5002

### Demo login credentials
- **Username:** demo_user
- **Password:** demo123

---

## 📱 To access from your phone (on the same Wi-Fi network)

```bash
HOST=0.0.0.0 python run.py
```

Then use your computer's IP address: http://192.168.x.x:5002
