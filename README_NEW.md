# 💰 Expense Tracker - AI-Powered Portfolio Project

A modern, full-featured expense tracking application with AI-powered insights, built with Flask and designed for portfolio demonstration.

## 🌟 Live Demo
- **Live App:** [Coming Soon - Railway Deployment]
- **Demo Credentials:** `demo_user` / `demo123`

## ✨ Key Features

### 🏠 Core Functionality
- **Smart Dashboard** - Real-time financial overview
- **Transaction Management** - Add, edit, delete expenses/income
- **Category Management** - Custom categories with color coding
- **Export/Import** - CSV export with custom filters

### 🤖 AI-Powered Features  
- **Smart Insights** - AI-generated financial recommendations
- **Budget Goals** - Intelligent budget tracking and alerts
- **Receipt Scanner** - Camera integration for expense capture
- **Achievement System** - Gamified savings goals

### 📱 Modern UX/UI
- **Responsive Design** - Works on desktop, tablet, mobile
- **Progressive Web App** - Offline functionality
- **Interactive Charts** - Real-time data visualization
- **Loading States** - Smooth user experience

### 🔒 Professional Features
- **User Authentication** - Secure login system
- **Data Security** - CSRF protection, secure sessions
- **Error Handling** - Professional error pages
- **Production Ready** - Configured for cloud deployment

## 🛠️ Technology Stack

**Backend:**
- Python 3.9+
- Flask (Web framework)
- SQLAlchemy (Database ORM)
- Flask-Login (Authentication)
- WTForms (Form handling)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5 (UI framework)
- Chart.js (Data visualization)
- FontAwesome (Icons)

**Database:**
- SQLite (Development)
- PostgreSQL (Production ready)

**Deployment:**
- Railway/Heroku ready
- Gunicorn WSGI server
- Environment-based configuration

## 🚀 Quick Start

### Local Development

1. **Clone the repository:**
```bash
git clone <your-repo-url>
cd expense_tracker
```

2. **Set up virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Create demo data:**
```bash
python create_demo_data.py
```

5. **Run the application:**
```bash
# For local access only:
python run.py

# For network access (mobile testing):
HOST=0.0.0.0 PORT=5000 python run.py
```

6. **Access the application:**
- Local: `http://127.0.0.1:5000`
- Network: `http://your-ip:5000`
- macOS: `http://your-hostname.local:5000`

### Demo Data
- **Username:** `demo_user`
- **Password:** `demo123`
- Pre-loaded with 40+ realistic transactions, categories, and achievements

## 📊 Project Highlights

This project demonstrates:

- **Full-Stack Development** - Complete CRUD operations
- **Database Design** - Normalized schema with relationships
- **User Experience** - Intuitive interface design
- **Modern Web Standards** - PWA, responsive design
- **AI Integration** - Smart recommendations system
- **Production Deployment** - Cloud-ready architecture
- **Testing & QA** - Error handling and edge cases

## 🎯 Portfolio Value

**For Employers/Clients, this showcases:**
- Clean, maintainable code structure
- Modern development practices
- User-centered design thinking
- Problem-solving capabilities
- Full project lifecycle management
- Professional deployment practices

## 🔧 Configuration

Environment variables:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
```

## 📱 Mobile Support

Fully responsive design tested on:
- iPhone/iPad (Safari)
- Android devices (Chrome)
- Desktop browsers (Chrome, Firefox, Safari)

## 🌐 Deployment

Ready for deployment on:
- Railway
- Heroku  
- Render
- DigitalOcean App Platform
- AWS/GCP/Azure

## 📈 Future Enhancements

- [ ] Real-time notifications
- [ ] Multi-currency support  
- [ ] Advanced analytics dashboard
- [ ] API for mobile app integration
- [ ] Machine learning expense categorization

## 👨‍💻 About

This project was built as a portfolio piece to demonstrate modern web development skills and serves as a practical tool for personal finance management.

**Contact:** [Your Contact Information]
**Portfolio:** [Your Portfolio URL]
**LinkedIn:** [Your LinkedIn URL]
