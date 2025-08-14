# 🔗 Share the app via link

## Quick way with ngrok (RECOMMENDED)

### 1. Register on ngrok (one time)
1. Go to https://ngrok.com
2. Register for free
3. In the dashboard, find your authtoken
4. Run the command:
```bash
./ngrok config add-authtoken YOUR_TOKEN_HERE
```

### 2. Start the application
Your app should already be running at http://127.0.0.1:5002

### 3. Create a public link
In a new terminal, run:
```bash
./ngrok http 5002
```

### 4. Get the link
After starting ngrok, it will show something like:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:5002
```

**You can send this link https://abc123.ngrok.io to your friend!**

---

## Alternative methods

### Railway.app (Permanent solution)
- The app will always be available
- Free plan: $5/month credits
- Commands are already prepared in the project

### Localtunnel (Alternative to ngrok)
```bash
npm install -g localtunnel
lt --port 5002
```

---

## What your friend will get
✅ Full-featured application  
✅ Demo data with 40+ transactions  
✅ All features: charts, export, AI recommendations  
✅ Mobile version  
✅ Ready test account: demo_user / demo123  

## ngrok limitations
⚠️ Free version:
- The link works only while ngrok is running
- Random URL each time
- Traffic limit

For a permanent solution, use Railway.app
