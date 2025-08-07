# 🤖 AI-Powered Expense Tracker

A cutting-edge personal finance management application built with Flask, featuring AI-powered insights, PWA capabilities, and advanced analytics.

## 🌟 Features

### Core Functionality
- **💰 Transaction Management**: Add, edit, and categorize income and expenses
- **📊 Dashboard**: Real-time financial overview with interactive charts
- **🏷️ Categories**: Customizable expense categories with color coding
- **📈 Statistics**: Detailed financial analytics and trends

### 🤖 AI-Powered Features
- **Smart Budget Assistant**: Machine learning predictions for spending patterns
- **Intelligent Recommendations**: AI-driven financial advice based on your habits
- **Automatic Categorization**: Smart categorization of transactions
- **Spending Pattern Analysis**: AI insights into your financial behavior
- **Predictive Analytics**: Forecast future expenses and savings

### 📱 Progressive Web App (PWA)
- **Offline Support**: Full functionality without internet connection
- **Camera Receipt Scanning**: Scan and process receipts with AI
- **Push Notifications**: Smart alerts and reminders
- **Mobile-First Design**: Responsive design optimized for all devices
- **App Installation**: Install directly from browser to home screen

### 📊 Advanced Dashboard
- **Custom Widgets**: Drag-and-drop dashboard customization
- **Real-time Charts**: Interactive visualizations with Chart.js
- **Financial Insights**: AI-powered spending analysis
- **Budget Goals**: Set and track financial objectives
- **Achievement System**: Gamified financial milestones

### 🎯 Smart Features
- **Budget Goals**: AI-assisted budget planning and tracking
- **Smart Notifications**: Contextual alerts based on spending patterns
- **Achievement System**: Gamification with rewards and milestones
- **Export Reports**: Generate detailed financial reports
- **Data Visualization**: Advanced charts and graphs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Flask
- SQLAlchemy

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense_tracker
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python init_db.py
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

6. **Access the app**
   Open your browser and go to `http://localhost:5002`

7. **Create demo data (Optional)**
   - Register a new user account
   - Use the application to add some transactions
   - Or manually add demo transactions for portfolio showcase

### Demo Account Setup
For portfolio demonstration, create an account and add sample transactions:
- Monthly salary: $2500-3000
- Regular expenses: food, transportation, shopping
- Recurring bills: utilities, subscriptions
- Entertainment: movies, dining out

## 📱 PWA Installation

### Desktop (Chrome/Edge)
1. Visit the app in your browser
2. Click the install icon in the address bar
3. Follow the installation prompts

### Mobile (iOS/Android)
1. Open the app in Safari/Chrome
2. Tap "Add to Home Screen" from the share menu
3. The app will be installed as a native-like app

## 🤖 AI Features Setup

### Mock AI (Default)
The application comes with mock AI functions that simulate:
- Spending pattern analysis
- Smart recommendations
- Predictive insights
- Receipt processing

### Real AI Integration (Optional)
To enable real AI features, you can integrate:

1. **OpenAI GPT** for natural language processing
2. **TensorFlow/PyTorch** for custom ML models
3. **Google Vision API** for receipt scanning
4. **Custom algorithms** for financial analysis

## 🎯 Usage Guide

### Getting Started
1. **Register** a new account or login
2. **Add transactions** manually or scan receipts
3. **Set budget goals** for different categories
4. **Explore AI insights** for personalized recommendations

### Dashboard Navigation
- **📊 Dashboard**: Main financial overview
- **💰 Transactions**: Add and manage transactions
- **📈 Statistics**: Detailed analytics
- **🎯 Budget Goals**: Set and track financial objectives
- **🤖 AI Insights**: Smart recommendations and patterns
- **📷 Receipt Scanner**: Camera-based receipt processing
- **🏆 Achievements**: Track your financial milestones
- **⚙️ Settings**: Customize categories and preferences

### AI Features
- **Smart Insights**: Get AI-powered spending analysis
- **Budget Assistant**: Receive personalized budget recommendations
- **Pattern Recognition**: Discover spending patterns and trends
- **Predictive Analytics**: Forecast future financial scenarios

## 🏗️ Architecture

### Backend
- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **WTForms**: Form handling and validation

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Chart.js**: Interactive data visualizations
- **Font Awesome**: Icon library
- **PWA**: Service worker for offline functionality

### Database Schema
- **Users**: User accounts and authentication
- **Categories**: Expense/income categories
- **Transactions**: Financial transactions
- **Budget Goals**: AI-assisted budget planning
- **Achievements**: Gamification system
- **Smart Recommendations**: AI insights storage
- **Receipt Scans**: Processed receipt data

### AI/ML Components
- **Pattern Analysis**: Spending behavior analysis
- **Recommendation Engine**: Personalized financial advice
- **Prediction Models**: Future spending forecasts
- **Natural Language Processing**: Receipt text extraction

## 🔧 Development

### Project Structure
```
expense_tracker/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── routes.py            # URL routes and views
│   ├── forms.py             # WTForms definitions
│   ├── static/              # CSS, JS, images
│   └── templates/           # Jinja2 templates
├── instance/                # Instance-specific config
├── config.py               # Configuration settings
├── run.py                  # Application entry point
├── init_db.py              # Database initialization
└── requirements.txt        # Python dependencies
```

### Adding New Features
1. **Models**: Add new database models in `app/models.py`
2. **Routes**: Create new routes in `app/routes.py`
3. **Templates**: Add HTML templates in `app/templates/`
4. **Static Files**: Add CSS/JS in `app/static/`

### Database Migrations
```bash
# Initialize database
python init_db.py

# Reset database (WARNING: deletes all data)
python init_db.py --reset
```

## 🌐 API Endpoints

### Main Routes
- `GET /` - Landing page
- `GET /dashboard` - Main dashboard
- `GET /transactions` - Transaction management
- `GET /statistics` - Financial analytics

### AI Features
- `GET /smart-insights` - AI recommendations
- `GET /budget-goals` - Budget management
- `POST /api/ai/analyze` - Spending analysis
- `POST /api/ai/recommend` - Get recommendations

### PWA Endpoints
- `GET /service-worker.js` - Service worker
- `GET /manifest.json` - PWA manifest
- `GET /offline` - Offline page

## 🎨 Customization

### Themes
- Modify CSS variables in `app/static/css/`
- Customize Bootstrap theme
- Add custom color schemes

### AI Models
- Replace mock functions with real ML models
- Integrate external AI services
- Train custom models on user data

### Dashboard Widgets
- Create new widget types
- Customize existing widgets
- Add real-time data updates

## 🚀 Deployment

### Local Development
```bash
python run.py
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app

# Using Docker (create Dockerfile)
docker build -t expense-tracker .
docker run -p 5000:5000 expense-tracker
```

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///expense_tracker.db
FLASK_ENV=production
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- 📧 Email: support@expense-tracker.com
- 💬 Discord: [Join our community]
- 📚 Documentation: [Full docs]
- 🐛 Bug Reports: [GitHub Issues]

## 🔮 Roadmap

### Upcoming Features
- [ ] Real-time collaboration
- [ ] Bank account integration
- [ ] Advanced ML models
- [ ] Multi-currency support
- [ ] Investment tracking
- [ ] Tax report generation
- [ ] Voice command interface
- [ ] Blockchain integration

### AI Enhancements
- [ ] Advanced pattern recognition
- [ ] Predictive cashflow modeling
- [ ] Automated bill detection
- [ ] Smart savings recommendations
- [ ] Financial goal optimization

---

Built with ❤️ using Flask, AI, and modern web technologies.
