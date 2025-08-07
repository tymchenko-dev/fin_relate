#!/usr/bin/env python3
"""
Production initialization script for Railway/Heroku deployment
This script sets up the database and creates demo data in production
"""

import os
from app import create_app, db
from app.models import User, Category, Transaction, BudgetGoal, Achievement, SmartRecommendation, UserAchievement
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from decimal import Decimal
import random

def init_production_db():
    """Initialize production database with demo data"""
    
    print("🚀 Initializing production database...")
    
    # Create application context
    config_name = os.environ.get('FLASK_ENV', 'production')
    app = create_app(config_name)
    
    with app.app_context():
        # Create all tables
        print("📊 Creating database tables...")
        db.create_all()
        
        # Check if demo user already exists
        if User.query.filter_by(username='demo_user').first():
            print("✅ Demo data already exists!")
            return
        
        # Create demo user
        print("👤 Creating demo user...")
        demo_user = User(
            username='demo_user',
            email='demo@expensetracker.com',
            password_hash=generate_password_hash('demo123')
        )
        db.session.add(demo_user)
        db.session.commit()
        
        # Create categories
        print("📂 Creating categories...")
        categories_data = [
            ('Food & Dining', '#FF6B6B', '🍽️'),
            ('Transportation', '#4ECDC4', '🚗'),
            ('Shopping', '#45B7D1', '🛒'),
            ('Entertainment', '#96CEB4', '🎬'),
            ('Bills & Utilities', '#FECA57', '⚡'),
            ('Healthcare', '#FF9FF3', '🏥'),
            ('Education', '#54A0FF', '📚'),
            ('Travel', '#5F27CD', '✈️'),
            ('Personal Care', '#00D2D3', '💅'),
            ('Income', '#2ED573', '💰')
        ]
        
        categories = []
        for name, color, icon in categories_data:
            category = Category(
                name=name,
                color=color,
                icon=icon,
                user_id=demo_user.id
            )
            categories.append(category)
            db.session.add(category)
        
        db.session.commit()
        
        # Create sample transactions
        print("💰 Creating sample transactions...")
        transaction_templates = [
            # Food & Dining
            ("McDonald's", 12.45, categories[0]),
            ("Starbucks Coffee", 5.80, categories[0]),
            ("Grocery Store", 67.23, categories[0]),
            ("Pizza Delivery", 24.50, categories[0]),
            ("Restaurant Dinner", 45.60, categories[0]),
            
            # Transportation  
            ("Gas Station", 52.00, categories[1]),
            ("Uber Ride", 15.30, categories[1]),
            ("Parking Fee", 8.00, categories[1]),
            ("Bus Pass", 25.00, categories[1]),
            
            # Shopping
            ("Amazon Purchase", 89.99, categories[2]),
            ("Clothing Store", 120.00, categories[2]),
            ("Electronics Store", 299.99, categories[2]),
            
            # Entertainment
            ("Movie Tickets", 28.00, categories[3]),
            ("Netflix Subscription", 15.99, categories[3]),
            ("Concert Tickets", 75.00, categories[3]),
            
            # Bills
            ("Electric Bill", 89.45, categories[4]),
            ("Internet Bill", 59.99, categories[4]),
            ("Phone Bill", 45.00, categories[4]),
            
            # Income
            ("Salary", 3500.00, categories[9]),
            ("Freelance Work", 750.00, categories[9]),
            ("Investment Return", 120.50, categories[9])
        ]
        
        # Create transactions for the last 3 months
        for i in range(40):
            # Random date within last 3 months
            days_ago = random.randint(0, 90)
            transaction_date = datetime.now() - timedelta(days=days_ago)
            
            # Pick random transaction template
            desc, amount, category = random.choice(transaction_templates)
            
            # Determine transaction type
            transaction_type = 'income' if category.name == 'Income' else 'expense'
            
            # Add some randomness to amounts
            if transaction_type == 'expense':
                amount = round(amount * random.uniform(0.7, 1.3), 2)
            
            transaction = Transaction(
                description=f"{desc} #{random.randint(1000, 9999)}",
                amount=Decimal(str(amount)),
                transaction_type=transaction_type,
                category_id=category.id,
                user_id=demo_user.id,
                date_created=transaction_date
            )
            db.session.add(transaction)
        
        # Create budget goals
        print("🎯 Creating budget goals...")
        budget_goals_data = [
            ('Monthly Food Budget', 500.00, categories[0]),
            ('Transportation Limit', 200.00, categories[1]),
            ('Entertainment Fund', 150.00, categories[3]),
            ('Shopping Budget', 300.00, categories[2]),
            ('Monthly Savings', 1000.00, categories[9])
        ]
        
        for goal_name, amount, category in budget_goals_data:
            start_date = datetime.now().replace(day=1)  # First day of current month
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)  # Last day of current month
            
            budget_goal = BudgetGoal(
                name=goal_name,
                amount=Decimal(str(amount)),
                start_date=start_date.date(),
                end_date=end_date.date(),
                category_id=category.id,
                user_id=demo_user.id
            )
            db.session.add(budget_goal)
        
        # Create achievements
        print("🏆 Creating achievements...")
        achievements_data = [
            ('First Transaction', 'Add your first transaction', 10, '🎯'),
            ('Budget Setter', 'Set your first budget goal', 25, '📊'),
            ('Week Tracker', 'Track expenses for 7 days', 50, '📅'),
            ('Month Master', 'Complete a full month of tracking', 100, '🏅'),
            ('Category Creator', 'Create 5 custom categories', 30, '📂'),
            ('Export Expert', 'Export your first report', 20, '📋'),
            ('Budget Keeper', 'Stay within budget for a month', 75, '💪'),
            ('Savings Star', 'Save $1000 in a month', 150, '⭐'),
            ('Consistent Tracker', 'Track for 30 consecutive days', 200, '🔥'),
            ('Financial Guru', 'Reach all budget goals', 500, '👑')
        ]
        
        for name, description, points, icon in achievements_data:
            achievement = Achievement(
                name=name,
                description=description,
                points=points,
                icon=icon
            )
            db.session.add(achievement)
        
        db.session.commit()
        
        # Award some achievements to demo user
        print("⭐ Awarding achievements...")
        achievements = Achievement.query.all()
        awarded_achievements = random.sample(achievements, 4)  # Award 4 random achievements
        
        for achievement in awarded_achievements:
            user_achievement = UserAchievement(
                user_id=demo_user.id,
                achievement_id=achievement.id,
                date_earned=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(user_achievement)
        
        # Create smart recommendations
        print("🤖 Creating smart recommendations...")
        recommendations_data = [
            ("Your food expenses are 23% higher than similar users. Consider meal planning to reduce costs.", "food_spending"),
            ("You've been consistent with tracking! Keep it up to build better financial habits.", "tracking_consistency"),
            ("Try setting up a transportation budget to better manage your commute costs.", "budget_suggestion"),
            ("Great job staying within your entertainment budget this month!", "budget_success"),
            ("Consider using the 50/30/20 rule: 50% needs, 30% wants, 20% savings.", "savings_tip")
        ]
        
        for recommendation_text, rec_type in recommendations_data:
            recommendation = SmartRecommendation(
                user_id=demo_user.id,
                recommendation_text=recommendation_text,
                recommendation_type=rec_type,
                date_created=datetime.now() - timedelta(days=random.randint(1, 7))
            )
            db.session.add(recommendation)
        
        db.session.commit()
        
        print("✅ Production database initialized successfully!")
        print(f"📈 Created:")
        print(f"   - Demo user: demo_user (password: demo123)")
        print(f"   - {len(categories)} categories")
        print(f"   - 40+ sample transactions")
        print(f"   - {len(budget_goals_data)} budget goals")
        print(f"   - {len(achievements_data)} achievements")
        print(f"   - {len(recommendations_data)} AI recommendations")
        print("\n🎪 Your production app is ready for demo!")

if __name__ == '__main__':
    init_production_db()
