from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import json
from app import db

class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with transactions
    transactions = db.relationship('Transaction', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Set encrypted password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password"""
        return check_password_hash(self.password_hash, password)
    
    def get_balance(self):
        """Get user's current balance"""
        total_income = sum(t.amount for t in self.transactions if t.transaction_type == 'income')
        total_expense = sum(t.amount for t in self.transactions if t.transaction_type == 'expense')
        return total_income - total_expense
    
    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    """Category model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    color = db.Column(db.String(7), default='#007bff')  # Color for charts
    
    # Relationship with transactions
    transactions = db.relationship('Transaction', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Transaction(db.Model):
    """Transaction model (income/expense)"""
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    transaction_type = db.Column(db.String(10), nullable=False)  # 'income' or 'expense'
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type}: {self.amount}>'

# Function to create default categories
def create_default_categories():
    """Create default categories"""
    default_categories = [
        {'name': 'Food', 'description': 'Groceries and dining', 'color': '#28a745'},
        {'name': 'Transportation', 'description': 'Transport expenses', 'color': '#007bff'},
        {'name': 'Housing', 'description': 'Rent, utilities', 'color': '#dc3545'},
        {'name': 'Healthcare', 'description': 'Medical, medicine', 'color': '#fd7e14'},
        {'name': 'Entertainment', 'description': 'Leisure, movies, restaurants', 'color': '#6f42c1'},
        {'name': 'Education', 'description': 'Courses, books', 'color': '#20c997'},
        {'name': 'Clothing', 'description': 'Clothing purchases', 'color': '#e83e8c'},
        {'name': 'Salary', 'description': 'Main income', 'color': '#28a745'},
        {'name': 'Freelance', 'description': 'Additional income', 'color': '#17a2b8'},
        {'name': 'Other', 'description': 'Other expenses', 'color': '#6c757d'},
    ]
    
    for cat_data in default_categories:
        if not Category.query.filter_by(name=cat_data['name']).first():
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()


# 🤖 AI-Powered Budget Assistant Models
class BudgetGoal(db.Model):
    """Budget goals for categories"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    period = db.Column(db.String(20), default='monthly')  # monthly, weekly, yearly
    current_spent = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='budget_goals')
    category = db.relationship('Category', backref='budget_goals')
    
    def progress_percentage(self):
        """Calculate progress percentage"""
        if self.target_amount == 0:
            return 0
        return min(100, (self.current_spent / self.target_amount) * 100)
    
    def remaining_amount(self):
        """Calculate remaining budget"""
        return max(0, self.target_amount - self.current_spent)
    
    def is_over_budget(self):
        """Check if over budget"""
        return self.current_spent > self.target_amount
    
    def days_remaining(self):
        """Get days remaining in period"""
        if self.end_date:
            return max(0, (self.end_date - datetime.utcnow()).days)
        return 0


class SmartRecommendation(db.Model):
    """AI-powered recommendations"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recommendation_type = db.Column(db.String(50), nullable=False)  # 'budget', 'category', 'savings'
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    impact_score = db.Column(db.Float, default=0.0)  # 0-100
    is_read = db.Column(db.Boolean, default=False)
    is_applied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='recommendations')


class SpendingPattern(db.Model):
    """ML-based spending patterns analysis"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    pattern_type = db.Column(db.String(50))  # 'weekly', 'monthly', 'seasonal'
    average_amount = db.Column(db.Float)
    predicted_next = db.Column(db.Float)
    confidence_score = db.Column(db.Float)  # 0-1
    trend = db.Column(db.String(20))  # 'increasing', 'decreasing', 'stable'
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='spending_patterns')
    category = db.relationship('Category', backref='spending_patterns')


# 📱 PWA & Notifications Models
class UserNotification(db.Model):
    """Smart notifications system"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # 'budget_alert', 'goal_achieved', 'recommendation'
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    is_read = db.Column(db.Boolean, default=False)
    is_push_sent = db.Column(db.Boolean, default=False)
    action_url = db.Column(db.String(200))  # URL for action button
    action_text = db.Column(db.String(50))  # Text for action button
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    read_at = db.Column(db.DateTime)
    
    # Relationships
    user = db.relationship('User', backref='notifications')


class ReceiptScan(db.Model):
    """Receipt scanning results (mock AI)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200))
    detected_amount = db.Column(db.Float)
    detected_merchant = db.Column(db.String(200))
    suggested_category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    confidence_score = db.Column(db.Float)  # 0-1
    raw_text = db.Column(db.Text)  # OCR text
    is_processed = db.Column(db.Boolean, default=False)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction.id'))  # If converted to transaction
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='receipt_scans')
    suggested_category = db.relationship('Category', backref='receipt_suggestions')
    transaction = db.relationship('Transaction', backref='receipt_scan')


# 📊 Custom Dashboard Models
class DashboardWidget(db.Model):
    """Custom dashboard widgets"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    widget_type = db.Column(db.String(50), nullable=False)  # 'balance', 'spending_chart', 'goals', 'recommendations'
    title = db.Column(db.String(200))
    position_x = db.Column(db.Integer, default=0)
    position_y = db.Column(db.Integer, default=0)
    width = db.Column(db.Integer, default=4)  # Grid columns (1-12)
    height = db.Column(db.Integer, default=3)  # Grid rows
    config = db.Column(db.Text)  # JSON config for widget
    is_visible = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='dashboard_widgets')
    
    def get_config(self):
        """Parse JSON config"""
        try:
            return json.loads(self.config) if self.config else {}
        except:
            return {}
    
    def set_config(self, config_dict):
        """Set JSON config"""
        self.config = json.dumps(config_dict)


class Achievement(db.Model):
    """Gamification achievements"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Font Awesome icon
    badge_color = db.Column(db.String(7), default='#ffd700')
    condition_type = db.Column(db.String(50))  # 'transaction_count', 'savings_goal', 'streak'
    condition_value = db.Column(db.Float)
    points = db.Column(db.Integer, default=10)
    is_active = db.Column(db.Boolean, default=True)


class UserAchievement(db.Model):
    """User earned achievements"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    achievement_id = db.Column(db.Integer, db.ForeignKey('achievement.id'), nullable=False)
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.Column(db.Float, default=100.0)  # Percentage towards achievement
    
    # Relationships
    user = db.relationship('User', backref='user_achievements')
    achievement = db.relationship('Achievement', backref='user_achievements')


# Utility Functions for AI Features
def analyze_spending_patterns(user_id):
    """Analyze user spending patterns with mock ML"""
    from sqlalchemy import func
    
    # Get user transactions
    transactions = Transaction.query.filter_by(user_id=user_id, transaction_type='expense').all()
    
    if not transactions:
        return []
    
    # Group by category and analyze
    patterns = []
    for category in Category.query.all():
        cat_transactions = [t for t in transactions if t.category_id == category.id]
        
        if len(cat_transactions) >= 3:  # Need minimum data
            amounts = [t.amount for t in cat_transactions]
            avg_amount = sum(amounts) / len(amounts)
            
            # Simple trend analysis (mock ML)
            recent_amounts = amounts[-3:]
            older_amounts = amounts[:-3] if len(amounts) > 3 else amounts[:1]
            
            recent_avg = sum(recent_amounts) / len(recent_amounts)
            older_avg = sum(older_amounts) / len(older_amounts)
            
            if recent_avg > older_avg * 1.1:
                trend = 'increasing'
            elif recent_avg < older_avg * 0.9:
                trend = 'decreasing'
            else:
                trend = 'stable'
            
            # Calculate prediction (simple moving average)
            predicted_next = recent_avg
            confidence = min(0.9, len(cat_transactions) / 10)  # More data = higher confidence
            
            patterns.append({
                'category_id': category.id,
                'category_name': category.name,
                'average_amount': avg_amount,
                'predicted_next': predicted_next,
                'trend': trend,
                'confidence_score': confidence
            })
    
    return patterns


def generate_smart_recommendations(user_id):
    """Generate AI-powered recommendations"""
    patterns = analyze_spending_patterns(user_id)
    recommendations = []
    
    user = User.query.get(user_id)
    if not user:
        return recommendations
    
    # Budget recommendations
    for pattern in patterns:
        if pattern['trend'] == 'increasing' and pattern['confidence_score'] > 0.5:
            recommendations.append({
                'type': 'budget',
                'title': f"Consider setting a budget for {pattern['category_name']}",
                'description': f"Your {pattern['category_name']} spending is increasing. Average: ${pattern['average_amount']:.2f}",
                'priority': 'medium',
                'impact_score': pattern['confidence_score'] * 70
            })
    
    # Savings recommendations
    balance = user.get_balance()
    if balance > 1000:
        recommendations.append({
            'type': 'savings',
            'title': "Great job! Consider setting up a savings goal",
            'description': f"With ${balance:.2f} balance, you could save 20% monthly",
            'priority': 'low',
            'impact_score': 60
        })
    
    return recommendations
