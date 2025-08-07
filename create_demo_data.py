#!/usr/bin/env python3
"""
Demo Data Generator for Expense Tracker Portfolio

Creates realistic demo data for portfolio demonstration:
- Demo user with authentication
- Sample expenses across categories
- Budget goals and achievements
- AI recommendations
- Recent activity for dashboard
"""

import os
import sys
from datetime import datetime, timedelta
import random
from decimal import Decimal

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from run import create_app
from app import db
from app.models import (
    User, Transaction, Category, BudgetGoal, Achievement, 
    UserAchievement, SmartRecommendation, ReceiptScan
)
from werkzeug.security import generate_password_hash


def create_demo_user():
    """Create a demo user for portfolio presentation"""
    demo_user = User(
        username='demo_user',
        email='demo@expensetracker.com',
        password_hash=generate_password_hash('demo123', method='pbkdf2:sha256'),
        created_at=datetime.utcnow() - timedelta(days=30)
    )
    db.session.add(demo_user)
    db.session.commit()
    return demo_user


def create_categories():
    """Create expense categories"""
    categories_data = [
        ('Food & Dining', 'Monthly food and dining expenses', '#28a745'),
        ('Transportation', 'Transport and travel costs', '#007bff'),
        ('Shopping', 'Shopping and retail purchases', '#dc3545'),
        ('Entertainment', 'Entertainment and leisure', '#ffc107'),
        ('Bills & Utilities', 'Monthly bills and utilities', '#6f42c1'),
        ('Healthcare', 'Medical and health expenses', '#fd7e14'),
        ('Education', 'Learning and education costs', '#20c997'),
        ('Travel', 'Travel and vacation expenses', '#17a2b8'),
        ('Personal Care', 'Personal care and beauty', '#e83e8c'),
        ('Home & Garden', 'Home improvement and garden', '#6c757d')
    ]
    
    categories = []
    for name, description, color in categories_data:
        category = Category(
            name=name,
            description=description,
            color=color
        )
        db.session.add(category)
        categories.append(category)
    
    db.session.commit()
    return categories


def create_expenses(user, categories):
    """Create realistic expense data for the last 3 months"""
    expenses_data = [
        # Food & Dining
        ('Starbucks Coffee', 'Food & Dining', 4.95, 'Coffee and pastry'),
        ('Whole Foods Market', 'Food & Dining', 67.43, 'Weekly groceries'),
        ('Pizza Palace', 'Food & Dining', 24.99, 'Friday dinner'),
        ('Local Deli', 'Food & Dining', 12.50, 'Lunch sandwich'),
        ('Fine Dining Restaurant', 'Food & Dining', 89.99, 'Anniversary dinner'),
        
        # Transportation
        ('Metro Card', 'Transportation', 25.00, 'Monthly transit pass'),
        ('Uber Ride', 'Transportation', 15.75, 'Airport pickup'),
        ('Gas Station', 'Transportation', 45.20, 'Fuel fillup'),
        ('Parking Meter', 'Transportation', 3.50, 'Downtown parking'),
        ('Car Wash', 'Transportation', 12.00, 'Vehicle maintenance'),
        
        # Shopping
        ('Amazon Purchase', 'Shopping', 156.78, 'Electronics and books'),
        ('Target', 'Shopping', 43.21, 'Household items'),
        ('Clothing Store', 'Shopping', 89.95, 'Winter jacket'),
        ('Online Marketplace', 'Shopping', 32.49, 'Phone accessories'),
        
        # Entertainment
        ('Netflix Subscription', 'Entertainment', 15.99, 'Monthly streaming'),
        ('Movie Theater', 'Entertainment', 28.50, 'Weekend movie'),
        ('Concert Tickets', 'Entertainment', 75.00, 'Live music event'),
        ('Gaming Store', 'Entertainment', 49.99, 'Video game purchase'),
        
        # Bills & Utilities
        ('Electric Company', 'Bills & Utilities', 89.34, 'Monthly electricity'),
        ('Internet Provider', 'Bills & Utilities', 69.99, 'High-speed internet'),
        ('Phone Bill', 'Bills & Utilities', 45.00, 'Mobile service'),
        ('Water Utility', 'Bills & Utilities', 34.56, 'Monthly water bill'),
        
        # Healthcare
        ('Pharmacy', 'Healthcare', 23.45, 'Prescription medication'),
        ('Dental Checkup', 'Healthcare', 150.00, 'Routine cleaning'),
        ('Gym Membership', 'Healthcare', 39.99, 'Monthly fitness'),
        
        # Education
        ('Online Course', 'Education', 99.99, 'Professional development'),
        ('Bookstore', 'Education', 45.67, 'Technical books'),
        
        # Travel
        ('Hotel Booking', 'Travel', 120.00, 'Business trip'),
        ('Flight Tickets', 'Travel', 345.99, 'Vacation travel'),
        
        # Personal Care
        ('Hair Salon', 'Personal Care', 65.00, 'Haircut and styling'),
        ('Spa Treatment', 'Personal Care', 85.00, 'Relaxation day'),
        
        # Home & Garden
        ('Hardware Store', 'Home & Garden', 76.43, 'Home improvement'),
        ('Garden Center', 'Home & Garden', 28.99, 'Plants and soil')
    ]
    
    category_map = {cat.name: cat for cat in categories}
    
    expenses = []
    start_date = datetime.utcnow() - timedelta(days=90)
    
    for i, (description, category_name, amount, notes) in enumerate(expenses_data):
        # Distribute expenses over the last 90 days
        days_offset = random.randint(0, 89)
        expense_date = start_date + timedelta(days=days_offset)
        
        expense = Transaction(
            user_id=user.id,
            category_id=category_map[category_name].id,
            amount=float(amount),
            description=description,
            transaction_type='expense',
            date=expense_date,
            created_at=expense_date
        )
        db.session.add(expense)
        expenses.append(expense)
        
        # Add some additional random expenses
        if i % 5 == 0:
            random_amount = round(random.uniform(5.0, 150.0), 2)
            random_expense = Transaction(
                user_id=user.id,
                category_id=random.choice(categories).id,
                amount=random_amount,
                description=f"Random expense #{i//5 + 1}",
                transaction_type='expense',
                date=expense_date + timedelta(hours=random.randint(1, 23)),
                created_at=expense_date + timedelta(hours=random.randint(1, 23))
            )
            db.session.add(random_expense)
            expenses.append(random_expense)
    
    db.session.commit()
    return expenses


def create_budget_goals(user, categories):
    """Create budget goals for different categories"""
    budget_data = [
        ('Food & Dining', 500.00),
        ('Transportation', 200.00),
        ('Entertainment', 150.00),
        ('Shopping', 300.00),
        ('Bills & Utilities', 250.00)
    ]
    
    category_map = {cat.name: cat for cat in categories}
    goals = []
    
    for category_name, budget_amount in budget_data:
        goal = BudgetGoal(
            user_id=user.id,
            category_id=category_map[category_name].id,
            target_amount=budget_amount,
            current_spent=0.0,
            period='monthly',
            start_date=datetime.utcnow().replace(day=1),
            end_date=datetime.utcnow().replace(month=datetime.utcnow().month+1, day=1) - timedelta(days=1)
        )
        db.session.add(goal)
        goals.append(goal)
    
    db.session.commit()
    return goals


def create_achievements():
    """Create achievement templates"""
    achievements_data = [
        ('First Expense', 'Record your first expense', 'fas fa-star', '#ffd700'),
        ('Budget Saver', 'Stay under budget for a month', 'fas fa-piggy-bank', '#28a745'),
        ('Expense Tracker', 'Log 50 expenses', 'fas fa-chart-line', '#17a2b8'),
        ('Monthly Reporter', 'View monthly report', 'fas fa-calendar-check', '#ffc107'),
        ('Goal Setter', 'Create your first budget goal', 'fas fa-target', '#dc3545'),
        ('Consistent Logger', 'Log expenses for 7 days straight', 'fas fa-fire', '#6c757d'),
        ('Big Spender Alert', 'Log an expense over $100', 'fas fa-exclamation-triangle', '#fd7e14'),
        ('Category Master', 'Use all expense categories', 'fas fa-th-large', '#6f42c1'),
        ('Receipt Scanner', 'Upload your first receipt', 'fas fa-camera', '#20c997'),
        ('Smart Saver', 'Follow an AI recommendation', 'fas fa-robot', '#007bff')
    ]
    
    achievements = []
    for name, description, icon, badge_color in achievements_data:
        achievement = Achievement(
            name=name,
            description=description,
            icon=icon,
            badge_color=badge_color,
            points=10
        )
        db.session.add(achievement)
        achievements.append(achievement)
    
    db.session.commit()
    return achievements


def create_user_achievements(user, achievements):
    """Award some achievements to the demo user"""
    awarded_achievements = random.sample(achievements, k=min(5, len(achievements)))
    
    for achievement in awarded_achievements:
        user_achievement = UserAchievement(
            user_id=user.id,
            achievement_id=achievement.id,
            earned_at=datetime.utcnow() - timedelta(days=random.randint(1, 20))
        )
        db.session.add(user_achievement)
    
    db.session.commit()


def create_smart_recommendations(user):
    """Create AI-powered recommendations"""
    recommendations_data = [
        ('Budget Alert', 'You\'re 85% through your food budget this month. Consider cooking at home more often.', 'warning', 'budget'),
        ('Savings Opportunity', 'You could save $50/month by switching to a cheaper phone plan based on your usage.', 'info', 'savings'),
        ('Spending Pattern', 'Your weekend spending is 40% higher than weekdays. Plan weekend activities with a budget.', 'primary', 'category'),
        ('Subscription Review', 'You have 3 entertainment subscriptions. Consider consolidating to save money.', 'warning', 'budget'),
        ('Achievement Unlock', 'You\'re close to the "Consistent Logger" achievement! Log 2 more daily expenses.', 'success', 'category')
    ]
    
    for title, description, priority, rec_type in recommendations_data:
        recommendation = SmartRecommendation(
            user_id=user.id,
            title=title,
            description=description,
            priority=priority,
            recommendation_type=rec_type,
            is_read=random.choice([True, False])
        )
        db.session.add(recommendation)
    
    db.session.commit()


def main():
    """Main function to create all demo data"""
    print("🚀 Creating demo data for Expense Tracker portfolio...")
    
    app = create_app()
    
    with app.app_context():
        # Drop and recreate all tables
        print("📊 Setting up database...")
        db.drop_all()
        db.create_all()
        
        # Create demo user
        print("👤 Creating demo user...")
        user = create_demo_user()
        
        # Create categories
        print("📂 Creating expense categories...")
        categories = create_categories()
        
        # Create expenses
        print("💰 Creating sample expenses...")
        expenses = create_expenses(user, categories)
        
        # Create budget goals
        print("🎯 Creating budget goals...")
        goals = create_budget_goals(user, categories)
        
        # Create achievements
        print("🏆 Creating achievements...")
        achievements = create_achievements()
        
        # Award achievements to user
        print("⭐ Awarding achievements...")
        create_user_achievements(user, achievements)
        
        # Create AI recommendations
        print("🤖 Creating smart recommendations...")
        create_smart_recommendations(user)
        
        print("\n✅ Demo data created successfully!")
        print(f"📈 Created {len(expenses)} expenses")
        print(f"📂 Created {len(categories)} categories")
        print(f"🎯 Created {len(goals)} budget goals")
        print(f"🏆 Created {len(achievements)} achievements")
        print("\n🎭 Demo Login Credentials:")
        print("   Username: demo_user")
        print("   Email: demo@expensetracker.com")
        print("   Password: demo123")
        print("\n🎪 Your portfolio demo is ready!")


if __name__ == '__main__':
    main()
