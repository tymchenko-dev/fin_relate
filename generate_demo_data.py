#!/usr/bin/env python3
"""
Demo data generator for Expense Tracker
Creates realistic sample transactions and user data for portfolio demonstration
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Category, Transaction, BudgetGoal, UserAchievement, Achievement

def create_demo_user():
    """Create a demo user account"""
    demo_user = User(
        username='demo_user',
        email='demo@expense-tracker.com'
    )
    # Use a simpler password hashing for demo
    from werkzeug.security import generate_password_hash
    demo_user.password_hash = generate_password_hash('demo123')
    db.session.add(demo_user)
    db.session.commit()
    return demo_user

def generate_realistic_transactions(user, categories, num_transactions=80):
    """Generate realistic transaction data over the past 3 months"""
    
    # Define realistic transaction patterns
    transaction_patterns = {
        'Food & Dining': {
            'amounts': [8.50, 12.30, 25.80, 45.20, 67.90, 15.75, 89.40, 22.10],
            'frequency': 0.25,  # 25% of all transactions
            'type': 'expense'
        },
        'Transportation': {
            'amounts': [3.50, 45.00, 65.00, 12.50, 95.00, 28.75, 150.00],
            'frequency': 0.15,
            'type': 'expense'
        },
        'Shopping': {
            'amounts': [25.99, 89.90, 156.50, 45.20, 299.99, 78.30, 125.80],
            'frequency': 0.20,
            'type': 'expense'
        },
        'Entertainment': {
            'amounts': [9.99, 15.50, 35.00, 12.99, 49.90, 25.00, 75.40],
            'frequency': 0.12,
            'type': 'expense'
        },
        'Bills & Utilities': {
            'amounts': [89.50, 156.80, 234.60, 78.90, 345.20, 123.45],
            'frequency': 0.08,
            'type': 'expense'
        },
        'Healthcare': {
            'amounts': [25.00, 125.50, 78.30, 234.80, 45.60, 189.90],
            'frequency': 0.05,
            'type': 'expense'
        },
        'Income': {
            'amounts': [2500.00, 3200.00, 2800.00, 450.00, 1200.00],
            'frequency': 0.10,
            'type': 'income'
        },
        'Savings': {
            'amounts': [500.00, 250.00, 750.00, 1000.00, 300.00],
            'frequency': 0.05,
            'type': 'income'
        }
    }
    
    transactions = []
    category_map = {cat.name: cat for cat in categories}
    
    # Generate transactions over the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    for i in range(num_transactions):
        # Pick a random category based on frequency weights
        category_names = list(transaction_patterns.keys())
        weights = [transaction_patterns[name]['frequency'] for name in category_names]
        
        # Weighted random selection
        category_name = random.choices(category_names, weights=weights)[0]
        category = category_map.get(category_name)
        
        if not category:
            continue
            
        pattern = transaction_patterns[category_name]
        
        # Generate random date within the range
        random_days = random.randint(0, 90)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Pick random amount from pattern
        amount = random.choice(pattern['amounts'])
        
        # Add some variation to amounts
        variation = random.uniform(0.8, 1.2)
        amount = round(amount * variation, 2)
        
        # Generate realistic descriptions
        descriptions = {
            'Food & Dining': [
                'Starbucks Coffee', 'McDonald\'s', 'Local Restaurant', 'Grocery Store',
                'Pizza Delivery', 'Subway Lunch', 'Thai Restaurant', 'Gas Station Snacks',
                'Whole Foods', 'Domino\'s Pizza', 'Local Cafe', 'Food Truck'
            ],
            'Transportation': [
                'Gas Station', 'Metro Card', 'Uber Ride', 'Taxi Fare',
                'Parking Fee', 'Bus Pass', 'Car Maintenance', 'Oil Change'
            ],
            'Shopping': [
                'Amazon Purchase', 'Target', 'Best Buy', 'Clothing Store',
                'Online Shopping', 'Pharmacy', 'Home Depot', 'Walmart'
            ],
            'Entertainment': [
                'Netflix Subscription', 'Movie Theater', 'Concert Tickets', 'Spotify',
                'Gaming', 'Books', 'Streaming Service', 'Sports Event'
            ],
            'Bills & Utilities': [
                'Electric Bill', 'Internet Bill', 'Phone Bill', 'Water Bill',
                'Insurance Payment', 'Rent', 'Credit Card Payment'
            ],
            'Healthcare': [
                'Doctor Visit', 'Pharmacy', 'Dental Checkup', 'Eye Exam',
                'Medical Insurance', 'Prescription', 'Health Supplement'
            ],
            'Income': [
                'Salary Deposit', 'Freelance Payment', 'Bonus', 'Side Hustle',
                'Investment Return', 'Gift Money', 'Refund'
            ],
            'Savings': [
                'Emergency Fund', 'Investment Deposit', 'Retirement Savings',
                'Vacation Fund', 'Goal Savings', 'Transfer to Savings'
            ]
        }
        
        description_list = descriptions.get(category_name, ['Transaction'])
        description = random.choice(description_list)
        
        transaction = Transaction(
            user_id=user.id,
            category_id=category.id,
            amount=amount,
            description=description,
            transaction_type=pattern['type'],
            date=transaction_date
        )
        
        transactions.append(transaction)
    
    # Add all transactions to database
    for transaction in transactions:
        db.session.add(transaction)
    
    db.session.commit()
    print(f"✓ Created {len(transactions)} realistic transactions")
    return transactions

def create_demo_budget_goals(user, categories):
    """Create realistic budget goals"""
    expense_categories = [cat for cat in categories if cat.name != 'Income' and cat.name != 'Savings']
    
    budget_goals = [
        {
            'category': next((cat for cat in expense_categories if cat.name == 'Food & Dining'), None),
            'target_amount': 400.00,
            'period': 'monthly',
            'current_amount': 285.60
        },
        {
            'category': next((cat for cat in expense_categories if cat.name == 'Transportation'), None),
            'target_amount': 200.00,
            'period': 'monthly', 
            'current_amount': 156.30
        },
        {
            'category': next((cat for cat in expense_categories if cat.name == 'Entertainment'), None),
            'target_amount': 150.00,
            'period': 'monthly',
            'current_amount': 89.50
        },
        {
            'category': next((cat for cat in expense_categories if cat.name == 'Shopping'), None),
            'target_amount': 300.00,
            'period': 'monthly',
            'current_amount': 245.80
        }
    ]
    
    for goal_data in budget_goals:
        if goal_data['category']:
            goal = BudgetGoal(
                user_id=user.id,
                category_id=goal_data['category'].id,
                target_amount=goal_data['target_amount'],
                period=goal_data['period'],
                current_amount=goal_data['current_amount']
            )
            db.session.add(goal)
    
    db.session.commit()
    print("✓ Created realistic budget goals")

def award_realistic_achievements(user):
    """Award some achievements based on demo data"""
    # Get available achievements
    achievements = Achievement.query.all()
    
    # Award some realistic achievements
    achievements_to_award = [
        'First Steps',
        'Getting Started', 
        'Budget Planner',
        'Category Explorer'
    ]
    
    for achievement_name in achievements_to_award:
        achievement = next((ach for ach in achievements if ach.name == achievement_name), None)
        if achievement:
            user_achievement = UserAchievement(
                user_id=user.id,
                achievement_id=achievement.id,
                earned_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            db.session.add(user_achievement)
    
    db.session.commit()
    print("✓ Awarded realistic achievements")

def generate_demo_data():
    """Main function to generate all demo data"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if demo user already exists
            existing_user = User.query.filter_by(username='demo_user').first()
            if existing_user:
                print("Demo user already exists. Removing old data...")
                # Clean up old demo data
                Transaction.query.filter_by(user_id=existing_user.id).delete()
                BudgetGoal.query.filter_by(user_id=existing_user.id).delete()
                UserAchievement.query.filter_by(user_id=existing_user.id).delete()
                db.session.delete(existing_user)
                db.session.commit()
            
            print("Creating demo user...")
            demo_user = create_demo_user()
            
            print("Loading categories...")
            categories = Category.query.all()
            if not categories:
                print("No categories found. Please run init_db.py first.")
                return False
            
            print("Generating realistic transactions...")
            generate_realistic_transactions(demo_user, categories, 80)
            
            print("Creating budget goals...")
            create_demo_budget_goals(demo_user, categories)
            
            print("Awarding achievements...")
            award_realistic_achievements(demo_user)
            
            print("\n🎉 Demo data generated successfully!")
            print("\nDemo Account Credentials:")
            print("Username: demo_user")
            print("Password: demo123")
            print("\nYour expense tracker now has realistic data for portfolio demonstration!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error generating demo data: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    generate_demo_data()
