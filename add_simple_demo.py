#!/usr/bin/env python3
"""
Add demo data without authentication
Creates realistic demo transactions for portfolio display
"""

import os
import sys
from datetime import datetime, timedelta

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, Transaction

def add_simple_demo_data():
    """Add demo transactions directly to database"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get categories
            categories = Category.query.all()
            if not categories:
                print("No categories found. Please run init_db.py first.")
                return False
            
            # Clear existing transactions
            Transaction.query.delete()
            db.session.commit()
            
            print("Adding demo transactions...")
            
            # Simple demo transactions (no user_id needed for demo)
            demo_data = [
                # Food & Dining
                {'category': 'Food & Dining', 'amount': 25.50, 'description': 'Starbucks Coffee', 'type': 'expense', 'days_ago': 2},
                {'category': 'Food & Dining', 'amount': 45.80, 'description': 'Restaurant Dinner', 'type': 'expense', 'days_ago': 5},
                {'category': 'Food & Dining', 'amount': 67.90, 'description': 'Grocery Shopping', 'type': 'expense', 'days_ago': 8},
                {'category': 'Food & Dining', 'amount': 18.75, 'description': 'Pizza Delivery', 'type': 'expense', 'days_ago': 12},
                
                # Transportation
                {'category': 'Transportation', 'amount': 45.00, 'description': 'Gas Station', 'type': 'expense', 'days_ago': 3},
                {'category': 'Transportation', 'amount': 12.50, 'description': 'Metro Card', 'type': 'expense', 'days_ago': 7},
                {'category': 'Transportation', 'amount': 28.75, 'description': 'Uber Ride', 'type': 'expense', 'days_ago': 14},
                
                # Shopping
                {'category': 'Shopping', 'amount': 156.80, 'description': 'Amazon Purchase', 'type': 'expense', 'days_ago': 4},
                {'category': 'Shopping', 'amount': 89.90, 'description': 'Target Shopping', 'type': 'expense', 'days_ago': 10},
                {'category': 'Shopping', 'amount': 234.50, 'description': 'Electronics Store', 'type': 'expense', 'days_ago': 18},
                
                # Entertainment  
                {'category': 'Entertainment', 'amount': 15.99, 'description': 'Netflix Subscription', 'type': 'expense', 'days_ago': 1},
                {'category': 'Entertainment', 'amount': 35.00, 'description': 'Movie Tickets', 'type': 'expense', 'days_ago': 9},
                {'category': 'Entertainment', 'amount': 75.40, 'description': 'Concert Tickets', 'type': 'expense', 'days_ago': 20},
                
                # Income
                {'category': 'Income', 'amount': 2500.00, 'description': 'Monthly Salary', 'type': 'income', 'days_ago': 1},
                {'category': 'Income', 'amount': 450.00, 'description': 'Freelance Project', 'type': 'income', 'days_ago': 15},
                {'category': 'Income', 'amount': 1200.00, 'description': 'Bonus Payment', 'type': 'income', 'days_ago': 25},
                
                # Bills
                {'category': 'Bills & Utilities', 'amount': 89.50, 'description': 'Electric Bill', 'type': 'expense', 'days_ago': 6},
                {'category': 'Bills & Utilities', 'amount': 156.80, 'description': 'Internet Bill', 'type': 'expense', 'days_ago': 11},
                {'category': 'Bills & Utilities', 'amount': 234.60, 'description': 'Insurance Payment', 'type': 'expense', 'days_ago': 22},
            ]
            
            # Create category map
            cat_map = {}
            for cat in categories:
                cat_map[cat.name] = cat.id
            
            # Add transactions
            added_count = 0
            for data in demo_data:
                # Find matching category
                category_id = None
                for cat_name, cat_id in cat_map.items():
                    if data['category'] in cat_name or cat_name in data['category']:
                        category_id = cat_id
                        break
                
                if category_id:
                    transaction_date = datetime.now() - timedelta(days=data['days_ago'])
                    
                    # Create transaction with minimal required fields
                    transaction = Transaction(
                        category_id=category_id,
                        amount=data['amount'],
                        description=data['description'],
                        transaction_type=data['type'],
                        date=transaction_date
                    )
                    
                    db.session.add(transaction)
                    added_count += 1
            
            db.session.commit()
            
            print(f"✓ Successfully added {added_count} demo transactions!")
            print("\nDemo data includes:")
            print("- Monthly salary and freelance income")
            print("- Regular food and dining expenses")
            print("- Transportation costs")
            print("- Shopping and entertainment")
            print("- Utility bills and subscriptions")
            print("\nYour portfolio now has realistic financial data!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    add_simple_demo_data()
