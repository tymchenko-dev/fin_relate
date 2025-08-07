# 🚀 Deployment Guide

## Environment Setup

The application supports multiple environments:
- `development` - Local development with SQLite
- `production` - Production deployment with PostgreSQL
- `testing` - Testing environment

## 📦 Quick Deployment

### Render Deployment (Recommended)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - The `render.yaml` file will automatically configure:
     - Web service with Python environment
     - PostgreSQL database
     - Environment variables

3. **Environment Variables**
   - `FLASK_ENV=production` (auto-set)
   - `SECRET_KEY` (auto-generated)
   - `DATABASE_URL` (auto-connected to PostgreSQL)

### Railway Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy**
   ```bash
   railway login
   railway init
   railway up
   ```

3. **Set Environment Variables**
   ```bash
   railway variables set FLASK_ENV=production
   railway variables set SECRET_KEY=$(python -c "import secrets; print(secrets.token_hex(16))")
   ```

### Manual Deployment (Any Platform)

1. **Set Environment Variables**
   - `FLASK_ENV=production`
   - `SECRET_KEY=<your-secret-key>`
   - `DATABASE_URL=<your-database-url>`

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   gunicorn run:app
   ```

## 🔧 Local Development

1. **Setup Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Application**
   ```bash
   python run.py
   ```

## 🗄️ Database Configuration

### Development (SQLite)
```
DATABASE_URL=sqlite:///expense_tracker.db
```

### Production (PostgreSQL)
```
DATABASE_URL=postgresql://username:password@hostname:port/database_name
```

## 🔐 Security Notes

- Always generate a strong `SECRET_KEY` for production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Use a production-grade database (PostgreSQL recommended)

## 📊 Features Included

✅ **User Management**
- Registration, login, logout
- Secure password hashing

✅ **Expense Tracking**
- Add, edit, delete transactions
- Categories management (CRUD)
- Income and expense tracking

✅ **Analytics & Reports**
- Dashboard with charts
- Extended reports (weekly, monthly, quarterly, yearly)
- Expense analytics by category

✅ **Data Export**
- CSV export with filters
- Custom date ranges
- Category filtering

✅ **User Experience**
- Dark/light theme toggle
- System theme detection
- Responsive design (mobile-friendly)
- Bootstrap 5.3.0 UI

✅ **Production Ready**
- Multi-environment configuration
- PostgreSQL support
- Gunicorn WSGI server
- Render/Railway deployment configs
