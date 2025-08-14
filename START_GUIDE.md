# 🚀 How to Run Expense Tracker for Demo

## After turning on your Mac:

### 1️⃣ Open Terminal
- Press `Cmd + Space` and type "Terminal"
- Or find Terminal in Applications → Utilities

### 2️⃣ Go to the project folder
```bash
cd /Users/jameskenway/Downloads/Tim/Portfolio/expense_tracker
```

### 3️⃣ Start the application
```bash
python3 run.py
```

**Expected result:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5002
```

### 4️⃣ In a new terminal window, start ngrok
Open a **second terminal** (`Cmd + T`) and run:

```bash
cd /Users/jameskenway/Downloads/Tim/Portfolio/expense_tracker
./ngrok http 5002
```

**Expected result:**
```
Forwarding    https://XXXXX.ngrok-free.app -> http://localhost:5002
```

### 5️⃣ Get the link for your friend
Copy the link like `https://XXXXX.ngrok-free.app`

---

## 📱 Login details (send to your friend):

**Link:** https://XXXXX.ngrok-free.app  
**Login:** `demo_user`  
**Password:** `demo123`

---

## 🔧 If something went wrong:

### Python not found:
```bash
 # Try:
python3 run.py
# или
python run.py
```

### ngrok not found:
```bash
 # If ngrok doesn't work, download again:
curl -o ngrok.zip https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip
unzip ngrok.zip
chmod +x ngrok
```

### ngrok token reset:
```bash
./ngrok config add-authtoken 30xhECVbBbkelpzn0g15Sa6c9Fj_d8f3CUXx3iUxnXxRxyJJ
```

---

## ⭐ Quick start (one command):

Create an auto-start script:

```bash
 # In terminal:
echo '#!/bin/bash
cd /Users/jameskenway/Downloads/Tim/Portfolio/expense_tracker
python3 run.py &
sleep 3
./ngrok http 5002' > start_demo.sh

chmod +x start_demo.sh
```

Now to start, just run:
```bash
./start_demo.sh
```

---

## 🎯 What your friend will see:
✅ Full application with demo data  
✅ 40+ transactions, charts, reports  
✅ AI recommendations and achievements system  
✅ Export to CSV available  
✅ Mobile version works  

## ⏰ Important:
- The link works while your Mac is running
- Each time you restart ngrok, the link changes
- To stop: `Ctrl+C` in both terminals
