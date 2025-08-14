# FinRelate

![Dashboard Screenshot](screen/FinRelate%20-%20Smart%20Finance%20Management.png)
![Welcome Screenshot](screen/Contact%20-%20FinRelate.png)

FinRelate is a modern, AI-powered personal finance management platform that helps you track expenses, manage budgets, analyze your financial data, and achieve your financial goals with ease. The project is currently under active development and will continue to be updated with new features and improvements.

## Features

- **Smart Analytics**: Get detailed insights into your spending patterns with interactive charts and reports.
- **Expense Tracking**: Add, edit, and delete transactions. Categorize your expenses and income for better management.
- **Budget Goals**: Set and monitor budget goals for different categories.
- **Achievements & Gamification**: Earn achievements for financial milestones and healthy habits.
- **AI Recommendations**: Receive smart, AI-driven financial tips and insights.
- **Data Export**: Export your transactions to CSV or Excel for further analysis.
- **Receipt Scanner**: Scan receipts and automatically extract transaction data (mock AI demo).
- **User Management**: Secure registration, login, and logout with password hashing.
- **Dark/Light Theme**: Toggle between dark and light modes, with system preference detection.
- **Mobile Friendly**: Responsive design for all devices.
- **Production Ready**: Multi-environment configuration, PostgreSQL support, and deployment configs for Render/Railway.

## Screenshots

### Dashboard
![Dashboard](screen/FinRelate%20-%20Smart%20Finance%20Management.png)

### Welcome Page
![Welcome](screen/Screenshot%202025-08-14%20at%202.22.46%E2%80%AFPM.png)

### Contact Page
![Contact](screen/Contact%20-%20FinRelate.png)

### Analytics
![Analytics](screen/Screenshot%202025-08-14%20at%202.22.58%E2%80%AFPM.png)

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/finrelate.git
   cd finrelate
   ```
2. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Create demo data**
   ```bash
   python create_demo_data.py
   ```
4. **Run the application**
   ```bash
   python run.py
   ```
5. **Open in your browser**
   - http://127.0.0.1:5002

**Demo login:**
- Username: `demo_user`
- Password: `demo123`

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for full deployment instructions (Render, Railway, manual, etc).

## Roadmap
- [x] Core expense tracking and analytics
- [x] Budget goals and achievements
- [x] AI-powered recommendations (demo)
- [x] Data export (CSV/Excel)
- [x] Responsive UI and theming
- [ ] Advanced AI insights
- [ ] Multi-user collaboration
- [ ] More integrations and automation

## Status

> **Note:** This project is a work in progress and will be updated regularly. Contributions and feedback are welcome!

## License

MIT License
