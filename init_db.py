#!/usr/bin/env python3
"""
Database initialization script for Expense Tracker with AI features
Creates all tables and sets up default data
"""

import os
import sys
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, Transaction, BudgetGoal, Achievement

def init_database():
    """Initialize the database with tables and default data"""
    app = create_app()
    
    with app.app_context():
        try:
            # Create all tables
            print("Creating database tables...")
            db.create_all()
            print("✓ Tables created successfully")
            
            # Create default categories if they don't exist
            if Category.query.count() == 0:
                print("Creating default categories...")
                default_categories = [
                    {'name': 'Food & Dining', 'description': 'Restaurants, groceries, takeout', 'color': '#ff6b6b'},
                    {'name': 'Transportation', 'description': 'Gas, public transport, parking', 'color': '#4ecdc4'},
                    {'name': 'Shopping', 'description': 'Clothing, electronics, general purchases', 'color': '#45b7d1'},
                    {'name': 'Entertainment', 'description': 'Movies, games, subscriptions', 'color': '#96ceb4'},
                    {'name': 'Bills & Utilities', 'description': 'Electricity, water, internet, phone', 'color': '#ffeaa7'},
                    {'name': 'Healthcare', 'description': 'Medical expenses, pharmacy, insurance', 'color': '#dda0dd'},
                    {'name': 'Income', 'description': 'Salary, freelance, other income', 'color': '#98d8c8'},
                    {'name': 'Savings', 'description': 'Emergency fund, investments', 'color': '#a8e6cf'},
                ]
                
                for cat_data in default_categories:
                    category = Category(**cat_data)
                    db.session.add(category)
                
                db.session.commit()
                print("✓ Default categories created")
            
            # Create default achievements if they don't exist
            if Achievement.query.count() == 0:
                print("Creating default achievements...")
                default_achievements = [
                    {
                        'name': 'First Steps',
                        'description': 'Add your first transaction',
                        'icon': 'baby',
                        'badge_color': '#28a745',
                        'points': 10,
                        'condition_type': 'transaction_count',
                        'condition_value': 1
                    },
                    {
                        'name': 'Getting Started',
                        'description': 'Add 10 transactions',
                        'icon': 'seedling',
                        'badge_color': '#20c997',
                        'points': 25,
                        'condition_type': 'transaction_count',
                        'condition_value': 10
                    },
                    {
                        'name': 'Transaction Master',
                        'description': 'Add 100 transactions',
                        'icon': 'chart-line',
                        'badge_color': '#17a2b8',
                        'points': 100,
                        'condition_type': 'transaction_count',
                        'condition_value': 100
                    },
                    {
                        'name': 'Budget Planner',
                        'description': 'Create your first budget goal',
                        'icon': 'bullseye',
                        'badge_color': '#6f42c1',
                        'points': 20,
                        'condition_type': 'budget_goals_count',
                        'condition_value': 1
                    },
                    {
                        'name': 'Budget Master',
                        'description': 'Stay within budget for 30 days',
                        'icon': 'crown',
                        'badge_color': '#ffc107',
                        'points': 50,
                        'condition_type': 'budget_success_days',
                        'condition_value': 30
                    },
                    {
                        'name': 'Savings Champion',
                        'description': 'Save $1000 in a single month',
                        'icon': 'piggy-bank',
                        'badge_color': '#28a745',
                        'points': 100,
                        'condition_type': 'monthly_savings',
                        'condition_value': 1000
                    },
                    {
                        'name': 'Category Explorer',
                        'description': 'Use all default categories',
                        'icon': 'tags',
                        'badge_color': '#fd7e14',
                        'points': 30,
                        'condition_type': 'categories_used',
                        'condition_value': 8
                    },
                    {
                        'name': 'AI Enthusiast',
                        'description': 'Use AI recommendations 10 times',
                        'icon': 'robot',
                        'badge_color': '#6f42c1',
                        'points': 75,
                        'condition_type': 'ai_recommendations_used',
                        'condition_value': 10
                    },
                    {
                        'name': 'Receipt Scanner Pro',
                        'description': 'Scan 25 receipts',
                        'icon': 'camera',
                        'badge_color': '#fd7e14',
                        'points': 60,
                        'condition_type': 'receipts_scanned',
                        'condition_value': 25
                    },
                    {
                        'name': 'Consistency King',
                        'description': 'Log transactions for 30 consecutive days',
                        'icon': 'calendar-check',
                        'badge_color': '#20c997',
                        'points': 80,
                        'condition_type': 'consecutive_days',
                        'condition_value': 30
                    },
                    {
                        'name': 'Power User',
                        'description': 'Use all major features of the app',
                        'icon': 'star',
                        'badge_color': '#ffc107',
                        'points': 150,
                        'condition_type': 'features_used',
                        'condition_value': 5
                    },
                    {
                        'name': 'Financial Guru',
                        'description': 'Maintain positive balance for 90 days',
                        'icon': 'gem',
                        'badge_color': '#6f42c1',
                        'points': 200,
                        'condition_type': 'positive_balance_days',
                        'condition_value': 90
                    }
                ]
                
                for achievement_data in default_achievements:
                    achievement = Achievement(**achievement_data)
                    db.session.add(achievement)
                
                db.session.commit()
                print("✓ Default achievements created")
            
            print("\n🎉 Database initialization completed successfully!")
            print("\nNext steps:")
            print("1. Run the application: python run.py")
            print("2. Register a new user account")
            print("3. Start tracking your expenses!")
            
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            db.session.rollback()
            return False
    
    return True

def reset_database():
    """Reset the database (WARNING: This will delete all data!)"""
    app = create_app()
    
    with app.app_context():
        try:
            print("⚠️  WARNING: This will delete all existing data!")
            confirm = input("Are you sure you want to reset the database? (type 'yes' to confirm): ")
            
            if confirm.lower() == 'yes':
                print("Dropping all tables...")
                db.drop_all()
                print("✓ Tables dropped")
                
                print("Recreating tables...")
                init_database()
                return True
            else:
                print("Database reset cancelled.")
                return False
                
        except Exception as e:
            print(f"❌ Error resetting database: {e}")
            return False

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Database management for Expense Tracker')
    parser.add_argument('--reset', action='store_true', help='Reset the database (WARNING: deletes all data)')
    
    args = parser.parse_args()
    
    if args.reset:
        reset_database()
    else:
        init_database()
