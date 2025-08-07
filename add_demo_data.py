#!/usr/bin/env python3
"""
Simple demo data script for Expense Tracker
Adds realistic transactions directly to database using SQLAlchemy
"""

import os
import sys
from datetime import datetime, timedelta
import random

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Category, Transaction

def add_demo_transactions():
    """Add realistic demo transactions to existing user"""
    app = create_app()
    
    with app.app_context():
        try:
            # Get existing categories
            categories = Category.query.all()
            if not categories:
                print("No categories found. Please run init_db.py first.")
                return False
            
            # Remove existing demo transactions if any
            Transaction.query.filter(Transaction.description.like('%DEMO%')).delete()
            db.session.commit()
            
            # Create realistic demo transactions
            demo_transactions = []
            
            # Food & Dining transactions
            food_category = next((cat for cat in categories if 'Food' in cat.name), categories[0])
            food_transactions = [
                (25.50, 'Starbucks Coffee - DEMO', 'expense', 2),
                (45.80, 'Local Restaurant Dinner - DEMO', 'expense', 5),
                (12.30, 'McDonald\'s Lunch - DEMO', 'expense', 8),
                (67.90, 'Grocery Shopping - DEMO', 'expense', 12),
                (18.75, 'Pizza Delivery - DEMO', 'expense', 15),
                (89.40, 'Fine Dining Restaurant - DEMO', 'expense', 20),
                (8.50, 'Gas Station Snacks - DEMO', 'expense', 25),
                (34.20, 'Thai Food Takeout - DEMO', 'expense', 28)
            ]
            
            # Transportation transactions
            transport_category = next((cat for cat in categories if 'Transport' in cat.name), categories[1])
            transport_transactions = [
                (45.00, 'Gas Station Fill-up - DEMO', 'expense', 3),
                (12.50, 'Metro Card Purchase - DEMO', 'expense', 7),
                (28.75, 'Uber Ride Downtown - DEMO', 'expense', 14),
                (95.00, 'Car Maintenance - DEMO', 'expense', 22),
                (3.50, 'Bus Fare - DEMO', 'expense', 26)
            ]
            
            # Shopping transactions
            shopping_category = next((cat for cat in categories if 'Shopping' in cat.name), categories[2])
            shopping_transactions = [
                (156.80, 'Amazon Online Purchase - DEMO', 'expense', 4),
                (89.90, 'Target Shopping - DEMO', 'expense', 10),
                (234.50, 'Electronics Store - DEMO', 'expense', 18),
                (45.20, 'Pharmacy Items - DEMO', 'expense', 24)
            ]
            
            # Entertainment transactions
            entertainment_category = next((cat for cat in categories if 'Entertainment' in cat.name), categories[3])
            entertainment_transactions = [
                (15.99, 'Netflix Subscription - DEMO', 'expense', 1),
                (35.00, 'Movie Theater Tickets - DEMO', 'expense', 9),
                (12.99, 'Spotify Premium - DEMO', 'expense', 16),
                (75.40, 'Concert Tickets - DEMO', 'expense', 23)
            ]
            
            # Income transactions
            income_category = next((cat for cat in categories if 'Income' in cat.name), categories[-2])
            income_transactions = [
                (2500.00, 'Monthly Salary - DEMO', 'income', 1),
                (2500.00, 'Monthly Salary - DEMO', 'income', 31),
                (450.00, 'Freelance Project - DEMO', 'income', 15),
                (1200.00, 'Bonus Payment - DEMO', 'income', 20)
            ]
            
            # Bills & Utilities transactions
            bills_category = next((cat for cat in categories if 'Bills' in cat.name), categories[4])
            bills_transactions = [
                (89.50, 'Electric Bill - DEMO', 'expense', 6),
                (156.80, 'Internet & Cable - DEMO', 'expense', 11),
                (78.90, 'Phone Bill - DEMO', 'expense', 17),
                (234.60, 'Insurance Payment - DEMO', 'expense', 27)
            ]
            
            # Combine all transactions
            all_demo_data = [
                (food_category, food_transactions),
                (transport_category, transport_transactions),
                (shopping_category, shopping_transactions),
                (entertainment_category, entertainment_transactions),
                (income_category, income_transactions),
                (bills_category, bills_transactions)
            ]
            
            # Create transaction objects
            for category, transactions in all_demo_data:
                for amount, description, transaction_type, days_ago in transactions:
                    transaction_date = datetime.now() - timedelta(days=days_ago)
                    
                    transaction = Transaction(
                        category_id=category.id,
                        amount=amount,
                        description=description,
                        transaction_type=transaction_type,
                        date=transaction_date
                    )
                    demo_transactions.append(transaction)
            
            # Add all transactions to database
            for transaction in demo_transactions:
                db.session.add(transaction)
            
            db.session.commit()
            
            print(f"✓ Successfully added {len(demo_transactions)} demo transactions!")
            print("\nDemo transactions include:")
            print("- Food & dining expenses")
            print("- Transportation costs")
            print("- Shopping purchases")
            print("- Entertainment subscriptions")
            print("- Monthly salary income")
            print("- Utility bills")
            print("\nYour expense tracker now has realistic data for demonstration!")
            
            return True
            
        except Exception as e:
            print(f"❌ Error adding demo transactions: {e}")
            db.session.rollback()
            return False

if __name__ == '__main__':
    add_demo_transactions()
