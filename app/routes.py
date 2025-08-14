from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
import csv
import io
import json
import random
import base64
from app import db
from app.models import (User, Transaction, Category, create_default_categories,
                       BudgetGoal, SmartRecommendation, SpendingPattern, UserNotification,
                       ReceiptScan, DashboardWidget, Achievement, UserAchievement,
                       analyze_spending_patterns, generate_smart_recommendations)
from app.forms import LoginForm, RegisterForm, TransactionForm, CategoryForm

 # Create blueprints
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Main routes
@main.route('/terms')
def terms():
    return render_template('terms.html')
@main.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')
@main.route('/contact')
def contact():
    return render_template('contact.html')
@main.route('/')
def index():
    """Home page"""
    response = make_response(render_template('finrelate_home.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@main.route('/export_pdf')
@login_required
def export_pdf():
    import io
    from flask import send_file
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    file_stream = io.BytesIO()
    c = canvas.Canvas(file_stream, pagesize=letter)
    width, height = letter
    c.setFont('Helvetica', 12)
    y = height - 40
    c.drawString(40, y, 'Transactions Report')
    y -= 30
    c.drawString(40, y, 'ID   Date   Category   Amount   Description')
    y -= 20
    for t in transactions:
        line = f"{t.id}   {t.date}   {t.category.name if t.category else ''}   {t.amount}   {t.description}"
        c.drawString(40, y, line)
        y -= 18
        if y < 40:
            c.showPage()
            y = height - 40
    c.save()
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name='transactions.pdf', mimetype='application/pdf')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@main.route('/disable-sw')
def disable_service_worker():
    """Disable service worker page"""
    html_content = '''
<!DOCTYPE html>
<html>
<head>
    <title>Disable Service Worker</title>
    <style>
        body { background: #f8f9fa; }
        .btn { margin-top: 2em; }
    </style>
</head>
<body>
    <h1>Disable Service Worker</h1>
    <button class="btn" onclick="disableServiceWorker()">Disable Service Worker</button>
    <script>
    function disableServiceWorker() {
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.getRegistrations().then(function(registrations) {
                for(let registration of registrations) {
                    registration.unregister();
                }
                alert('Service Worker disabled!');
            });
        }
    }
    </script>
</body>
</html>
'''
    response = make_response(html_content)
    response.headers['Content-Type'] = 'text/html'
    return response

@main.route('/dashboard')
@login_required
def dashboard():
    """Dashboard - main user page"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # Get last 10 transactions
        recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
                                             .order_by(Transaction.date.desc())\
                                             .limit(10).all()
        
        # Get all transactions for calculations
        all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in all_transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in all_transactions if t.transaction_type == 'expense')
        balance = current_user.get_balance()
        
        # Get form for adding transaction
        form = TransactionForm()
        categories = Category.query.all()
        form.category_id.choices = [(c.id, c.name) for c in categories]
        
        # Calculate analytics data for modal
        now = datetime.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Monthly data
        monthly_transactions = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= current_month_start
        ).all()
        
        monthly_income = sum(t.amount for t in monthly_transactions if t.transaction_type == 'income')
        monthly_expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense')
        
        # Transaction trends
        transaction_count = len(all_transactions)
        days_with_data = max(1, (now - min([t.date for t in all_transactions] + [now])).days + 1) if all_transactions else 1
        avg_transaction = round(transaction_count / days_with_data, 1) if transaction_count > 0 else 0
        
        # Categories data
        categories_data = []
        if all_transactions:
            from collections import defaultdict
            category_totals = defaultdict(lambda: {'total': 0, 'count': 0, 'name': 'Unknown'})
            
            for transaction in all_transactions:
                if transaction.transaction_type == 'expense':
                    cat_name = transaction.category.name if transaction.category else 'Other'
                    category_totals[cat_name]['total'] += transaction.amount
                    category_totals[cat_name]['count'] += 1
                    category_totals[cat_name]['name'] = cat_name
            
            # Convert to list and sort by total
            categories_data = sorted([
                {'name': data['name'], 'total': data['total'], 'count': data['count']}
                for data in category_totals.values()
            ], key=lambda x: x['total'], reverse=True)
        
        # Quick insights
        savings_rate = round(((monthly_income - monthly_expenses) / monthly_income * 100), 1) if monthly_income > 0 else 0
        daily_average = monthly_expenses / max(1, now.day) if monthly_expenses > 0 else 0
        balance_trend = 0  # Could be calculated based on historical data
        
        # Debug output
        print(f"DEBUG: monthly_income={monthly_income}, monthly_expenses={monthly_expenses}")
        print(f"DEBUG: transaction_count={transaction_count}, avg_transaction={avg_transaction}")
        print(f"DEBUG: categories_data={categories_data[:2] if categories_data else 'None'}")
        
        # Use fixed dashboard template (no Chart.js issues)
        return render_template('dashboard_fixed.html', 
                             transactions=recent_transactions, 
                             balance=balance, 
                             form=form,
                             total_income=total_income,
                             total_expenses=total_expenses,
                             categories=categories,
                             monthly_income=monthly_income,
                             monthly_expenses=monthly_expenses,
                             transaction_count=transaction_count,
                             avg_transaction=avg_transaction,
                             categories_data=categories_data,
                             savings_rate=savings_rate,
                             daily_average=daily_average,
                             balance_trend=balance_trend)
    except Exception as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        # Fallback to simple dashboard if there's an error
        return render_template('dashboard_simple.html', 
                             transactions=[], 
                             balance=0, 
                             form=None,
                             total_income=0,
                             total_expenses=0,
                             categories=[])

@main.route('/analytics')
@login_required
def analytics():
    """Financial Analytics page"""
    try:
        from datetime import datetime, timedelta
        from sqlalchemy import func
        
        # Get all transactions for calculations
        all_transactions = Transaction.query.filter_by(user_id=current_user.id).all()
        
        # Calculate totals
        total_income = sum(t.amount for t in all_transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in all_transactions if t.transaction_type == 'expense')
        balance = current_user.get_balance()
        
        # Calculate analytics data
        now = datetime.now()
        current_month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Monthly data
        monthly_transactions = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.date >= current_month_start
        ).all()
        
        monthly_income = sum(t.amount for t in monthly_transactions if t.transaction_type == 'income')
        monthly_expenses = sum(t.amount for t in monthly_transactions if t.transaction_type == 'expense')
        
        # Transaction trends
        transaction_count = len(all_transactions)
        days_with_data = max(1, (now - min([t.date for t in all_transactions] + [now])).days + 1) if all_transactions else 1
        avg_transaction = round(transaction_count / days_with_data, 1) if transaction_count > 0 else 0
        
        # Categories data
        categories_data = []
        if all_transactions:
            from collections import defaultdict
            category_totals = defaultdict(lambda: {'total': 0, 'count': 0, 'name': 'Unknown'})
            
            for transaction in all_transactions:
                if transaction.transaction_type == 'expense':
                    cat_name = transaction.category.name if transaction.category else 'Other'
                    category_totals[cat_name]['total'] += transaction.amount
                    category_totals[cat_name]['count'] += 1
                    category_totals[cat_name]['name'] = cat_name
            
            # Convert to list and sort by total
            categories_data = sorted([
                {'name': data['name'], 'total': data['total'], 'count': data['count']}
                for data in category_totals.values()
            ], key=lambda x: x['total'], reverse=True)
        
        # Quick insights
        savings_rate = round(((monthly_income - monthly_expenses) / monthly_income * 100), 1) if monthly_income > 0 else 0
        daily_average = monthly_expenses / max(1, now.day) if monthly_expenses > 0 else 0
        balance_trend = 0  # Could be calculated based on historical data
        
        return render_template('analytics.html', 
                             balance=balance,
                             total_income=total_income,
                             total_expenses=total_expenses,
                             monthly_income=monthly_income,
                             monthly_expenses=monthly_expenses,
                             transaction_count=transaction_count,
                             avg_transaction=avg_transaction,
                             categories_data=categories_data,
                             savings_rate=savings_rate,
                             daily_average=daily_average,
                             balance_trend=balance_trend)
    except Exception as e:
        flash(f'Error loading analytics: {str(e)}', 'error')
        return redirect(url_for('main.dashboard'))

@main.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    """Add new transaction"""
    form = TransactionForm()
    categories = Category.query.all()
    form.category_id.choices = [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            description=form.description.data,
            transaction_type=form.transaction_type.data,
            date=form.date.data,
            user_id=current_user.id,
            category_id=form.category_id.data
        )
        db.session.add(transaction)
        db.session.commit()
        flash('Transaction successfully added!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('main.dashboard'))

@main.route('/delete_transaction/<int:transaction_id>')
@login_required
def delete_transaction(transaction_id):
    """Delete transaction"""
    transaction = Transaction.query.get_or_404(transaction_id)
    
    # Check that transaction belongs to current user
    if transaction.user_id != current_user.id:
        flash('You do not have permission to delete this transaction', 'error')
        return redirect(url_for('main.dashboard'))
    
    db.session.delete(transaction)
    db.session.commit()
    flash('Transaction deleted', 'success')
    return redirect(url_for('main.dashboard'))

@main.route('/stats')
@login_required
def stats():
    """Statistics page"""
    # Get data for charts
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    # Category statistics
    category_stats = {}
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            category_name = transaction.category.name
            if category_name not in category_stats:
                category_stats[category_name] = {
                    'amount': 0, 
                    'color': transaction.category.color
                }
            category_stats[category_name]['amount'] += transaction.amount
    
    # Monthly statistics (last 6 months)
    monthly_stats = []
    for i in range(6):
        month_start = datetime.now().replace(day=1) - timedelta(days=i*30)
        month_end = month_start + timedelta(days=30)
        
        month_income = sum(t.amount for t in transactions 
                          if t.transaction_type == 'income' 
                          and month_start <= t.date <= month_end)
        month_expense = sum(t.amount for t in transactions 
                           if t.transaction_type == 'expense' 
                           and month_start <= t.date <= month_end)
        
        monthly_stats.append({
            'month': month_start.strftime('%m/%Y'),
            'income': month_income,
            'expense': month_expense,
            'balance': month_income - month_expense
        })
    
    monthly_stats.reverse()  # Show from old to new
    
    return render_template('stats.html', 
                         category_stats=category_stats,
                         monthly_stats=monthly_stats)

@main.route('/transactions')
@login_required
def transactions():
    """Transactions page with all user transactions"""
    # Get all transactions for the user
    transactions = Transaction.query.filter_by(user_id=current_user.id)\
                                  .order_by(Transaction.date.desc())\
                                  .all()
    
    # Get categories for the filter dropdown
    categories = Category.query.all()
    
    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
    balance = total_income - total_expenses
    
    return render_template('transactions.html',
                         transactions=transactions,
                         categories=categories,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         balance=balance)

@main.route('/settings')
@login_required
def settings():
    """User settings page"""
    categories = Category.query.all()
    return render_template('settings.html', categories=categories)

@main.route('/reports')
@login_required
def reports():
    """Extended reports page"""
    period = request.args.get('period', 'month')  # week, month, quarter, year
    
    # Get transactions for the user
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    # Calculate periods based on selection
    if period == 'week':
        periods_data = get_weekly_stats(transactions)
    elif period == 'quarter':
        periods_data = get_quarterly_stats(transactions)
    elif period == 'year':
        periods_data = get_yearly_stats(transactions)
    else:  # month
        periods_data = get_monthly_stats_extended(transactions)
    
    return render_template('reports.html', 
                         periods_data=periods_data,
                         current_period=period)

def get_weekly_stats(transactions):
    """Get weekly statistics for last 12 weeks"""
    weekly_stats = []
    for i in range(12):
        week_start = datetime.now() - timedelta(weeks=i+1)
        week_end = week_start + timedelta(days=7)
        
        week_income = sum(t.amount for t in transactions 
                         if t.transaction_type == 'income' 
                         and week_start <= t.date <= week_end)
        week_expense = sum(t.amount for t in transactions 
                          if t.transaction_type == 'expense' 
                          and week_start <= t.date <= week_end)
        
        weekly_stats.append({
            'period': f"Week {week_start.strftime('%d.%m')} - {week_end.strftime('%d.%m')}",
            'income': week_income,
            'expense': week_expense,
            'balance': week_income - week_expense
        })
    
    return list(reversed(weekly_stats))

def get_monthly_stats_extended(transactions):
    """Get monthly statistics for last 12 months"""
    monthly_stats = []
    for i in range(12):
        month_start = (datetime.now().replace(day=1) - timedelta(days=i*30)).replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1) - timedelta(days=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1) - timedelta(days=1)
        
        month_income = sum(t.amount for t in transactions 
                          if t.transaction_type == 'income' 
                          and month_start <= t.date <= month_end)
        month_expense = sum(t.amount for t in transactions 
                           if t.transaction_type == 'expense' 
                           and month_start <= t.date <= month_end)
        
        monthly_stats.append({
            'period': month_start.strftime('%B %Y'),
            'income': month_income,
            'expense': month_expense,
            'balance': month_income - month_expense
        })
    
    return list(reversed(monthly_stats))

def get_quarterly_stats(transactions):
    """Get quarterly statistics for last 8 quarters"""
    quarterly_stats = []
    for i in range(8):
        # Calculate quarter start
        current_quarter = ((datetime.now().month - 1) // 3) + 1
        quarter_year = datetime.now().year
        quarters_back = i
        
        while quarters_back > 0:
            current_quarter -= 1
            if current_quarter < 1:
                current_quarter = 4
                quarter_year -= 1
            quarters_back -= 1
        
        # Quarter start and end dates
        quarter_start = datetime(quarter_year, (current_quarter - 1) * 3 + 1, 1)
        if current_quarter == 4:
            quarter_end = datetime(quarter_year + 1, 1, 1) - timedelta(days=1)
        else:
            quarter_end = datetime(quarter_year, current_quarter * 3 + 1, 1) - timedelta(days=1)
        
        quarter_income = sum(t.amount for t in transactions 
                            if t.transaction_type == 'income' 
                            and quarter_start <= t.date <= quarter_end)
        quarter_expense = sum(t.amount for t in transactions 
                             if t.transaction_type == 'expense' 
                             and quarter_start <= t.date <= quarter_end)
        
        quarterly_stats.append({
            'period': f"Q{current_quarter} {quarter_year}",
            'income': quarter_income,
            'expense': quarter_expense,
            'balance': quarter_income - quarter_expense
        })
    
    return list(reversed(quarterly_stats))

def get_yearly_stats(transactions):
    """Get yearly statistics for last 5 years"""
    yearly_stats = []
    current_year = datetime.now().year
    
    for i in range(5):
        year = current_year - i
        year_start = datetime(year, 1, 1)
        year_end = datetime(year, 12, 31)
        
        year_income = sum(t.amount for t in transactions 
                         if t.transaction_type == 'income' 
                         and year_start <= t.date <= year_end)
        year_expense = sum(t.amount for t in transactions 
                          if t.transaction_type == 'expense' 
                          and year_start <= t.date <= year_end)
        
        yearly_stats.append({
            'period': str(year),
            'income': year_income,
            'expense': year_expense,
            'balance': year_income - year_expense
        })
    
    return list(reversed(yearly_stats))

@main.route('/export')
@login_required
def export_transactions():
    """Export transactions to CSV"""
    # Get filter parameters
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    transaction_type = request.args.get('type')  # income, expense, or all
    category_id = request.args.get('category')
    
    # Base query
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    # Apply filters
    if start_date:
        try:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            query = query.filter(Transaction.date >= start_date_obj)
        except ValueError:
            flash('Invalid start date format', 'error')
            return redirect(url_for('main.dashboard'))
    
    if end_date:
        try:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            query = query.filter(Transaction.date <= end_date_obj)
        except ValueError:
            flash('Invalid end date format', 'error')
            return redirect(url_for('main.dashboard'))
    
    if transaction_type and transaction_type != 'all':
        query = query.filter(Transaction.transaction_type == transaction_type)
    
    if category_id and category_id != 'all':
        try:
            query = query.filter(Transaction.category_id == int(category_id))
        except ValueError:
            flash('Invalid category', 'error')
            return redirect(url_for('main.dashboard'))
    
    # Get transactions
    transactions = query.order_by(Transaction.date.desc()).all()
    
    # Create CSV content
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Date', 'Type', 'Category', 'Description', 'Amount', 'Balance After'
    ])
    
    # Calculate running balance
    running_balance = 0
    for transaction in reversed(transactions):  # Start from oldest
        if transaction.transaction_type == 'income':
            running_balance += transaction.amount
        else:
            running_balance -= transaction.amount
    
    # Write data rows
    current_balance = running_balance
    for transaction in transactions:  # Now from newest
        # Adjust balance backwards
        if transaction.transaction_type == 'income':
            current_balance -= transaction.amount
        else:
            current_balance += transaction.amount
        
        # Calculate balance after this transaction
        balance_after = current_balance + (transaction.amount if transaction.transaction_type == 'income' else -transaction.amount)
        
        writer.writerow([
            transaction.date.strftime('%Y-%m-%d %H:%M'),
            transaction.transaction_type.title(),
            transaction.category.name,
            transaction.description or '',
            f"${transaction.amount:.2f}",
            f"${balance_after:.2f}"
        ])
        
        current_balance = balance_after
    
    # Create response
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    
    # Generate filename
    filename = f"transactions_{current_user.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    
    return response

@main.route('/categories')
@login_required
def categories():
    """Categories management page"""
    categories = Category.query.all()
    return render_template('categories.html', categories=categories)

@main.route('/export_excel')
@login_required
def export_excel():
    import io
    from flask import send_file
    from openpyxl import Workbook

    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    wb = Workbook()
    ws = wb.active
    ws.title = "Transactions"
    ws.append(['ID', 'Date', 'Category', 'Amount', 'Description'])

    for t in transactions:
        ws.append([
            t.id,
            t.date.strftime('%Y-%m-%d %H:%M'),
            t.category.name if t.category else '',
            t.amount,
            t.description
        ])

    file_stream = io.BytesIO()
    wb.save(file_stream)
    file_stream.seek(0)
    return send_file(file_stream, as_attachment=True, download_name='transactions.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@main.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """Add new category"""
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            description=form.description.data,
            color=form.color.data
        )
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('main.categories'))
    
    return render_template('edit_category.html', form=form, action='Add')

@main.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    """Edit existing category"""
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        category.description = form.description.data
        category.color = form.color.data
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('main.categories'))
    
    return render_template('edit_category.html', form=form, category=category, action='Edit')

@main.route('/categories/delete/<int:category_id>')
@login_required
def delete_category(category_id):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    
    # Check if category has transactions
    transaction_count = Transaction.query.filter_by(category_id=category_id).count()
    if transaction_count > 0:
        flash(f'Cannot delete category "{category.name}" because it has {transaction_count} transactions. Move or delete those transactions first.', 'error')
        return redirect(url_for('main.categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('main.categories'))

# Authentication routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    """Login"""
    # Always allow access to login page, even if authenticated
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user"""
    # Always allow access to register page
    form = RegisterForm()
    if form.validate_on_submit():
        # Check that user with this username or email doesn't exist
        existing_user = User.query.filter(
            (User.username == form.username.data) | 
            (User.email == form.email.data)
        ).first()
        
        if existing_user:
            flash('User with this username or email already exists', 'error')
        else:
            # Create new user
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            
            db.session.add(user)
            db.session.commit()
            
            # Create default categories on first registration
            if User.query.count() == 1:
                create_default_categories()
            
            flash('Registration successful!', 'success')
            return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    """Logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

# API routes for chart data
@main.route('/api/chart_data')
@login_required
def chart_data():
    """API for chart data"""
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()
    
    # Data for expense pie chart by categories
    category_data = {}
    for transaction in transactions:
        if transaction.transaction_type == 'expense':
            category_name = transaction.category.name
            if category_name not in category_data:
                category_data[category_name] = {
                    'amount': 0,
                    'color': transaction.category.color
                }
            category_data[category_name]['amount'] += transaction.amount
    
    return jsonify({
        'categories': category_data
    })


# 🤖 AI-Powered Budget Assistant Routes
@main.route('/budget-goals')
@login_required
def budget_goals():
    """Budget goals management"""
    goals = BudgetGoal.query.filter_by(user_id=current_user.id, is_active=True).all()
    categories = Category.query.all()
    
    # Update current spent for each goal
    for goal in goals:
        # Calculate current spending in period
        start_date = goal.start_date
        end_date = goal.end_date or datetime.utcnow()
        
        current_spent = db.session.query(db.func.sum(Transaction.amount))\
            .filter(Transaction.user_id == current_user.id,
                   Transaction.category_id == goal.category_id,
                   Transaction.transaction_type == 'expense',
                   Transaction.date >= start_date,
                   Transaction.date <= end_date)\
            .scalar() or 0
        
        goal.current_spent = current_spent
        db.session.commit()
    
    return render_template('budget_goals.html', goals=goals, categories=categories)


@main.route('/add-budget-goal', methods=['POST'])
@login_required
def add_budget_goal():
    """Add new budget goal"""
    category_id = request.form.get('category_id')
    target_amount = float(request.form.get('target_amount', 0))
    period = request.form.get('period', 'monthly')
    
    # Calculate end date based on period
    start_date = datetime.utcnow()
    if period == 'weekly':
        end_date = start_date + timedelta(weeks=1)
    elif period == 'yearly':
        end_date = start_date + timedelta(days=365)
    else:  # monthly
        end_date = start_date + timedelta(days=30)
    
    goal = BudgetGoal(
        user_id=current_user.id,
        category_id=category_id,
        target_amount=target_amount,
        period=period,
        start_date=start_date,
        end_date=end_date
    )
    
    db.session.add(goal)
    db.session.commit()
    
    flash(f'Budget goal created successfully!', 'success')
    return redirect(url_for('main.budget_goals'))


@main.route('/smart-insights')
@login_required
def smart_insights():
    """AI-powered financial insights"""
    # Generate fresh recommendations
    recommendations_data = generate_smart_recommendations(current_user.id)
    
    # Clear old recommendations
    SmartRecommendation.query.filter_by(user_id=current_user.id).delete()
    
    # Add new recommendations to database
    for rec_data in recommendations_data:
        recommendation = SmartRecommendation(
            user_id=current_user.id,
            recommendation_type=rec_data['type'],
            title=rec_data['title'],
            description=rec_data['description'],
            priority=rec_data['priority'],
            impact_score=rec_data['impact_score']
        )
        db.session.add(recommendation)
    
    db.session.commit()
    
    # Get spending patterns
    patterns = analyze_spending_patterns(current_user.id)
    
    # Get recommendations from database
    recommendations = SmartRecommendation.query.filter_by(user_id=current_user.id)\
                                               .order_by(SmartRecommendation.impact_score.desc()).all()
    
    return render_template('smart_insights.html', 
                         recommendations=recommendations, 
                         patterns=patterns)


# 📱 PWA & Notifications Routes
@main.route('/notifications')
@login_required
def notifications():
    """User notifications center"""
    notifications = UserNotification.query.filter_by(user_id=current_user.id)\
                                          .order_by(UserNotification.created_at.desc()).all()
    
    # Mark as read
    unread_notifications = [n for n in notifications if not n.is_read]
    for notification in unread_notifications:
        notification.is_read = True
        notification.read_at = datetime.utcnow()
    
    db.session.commit()
    
    return render_template('notifications.html', notifications=notifications)


@main.route('/receipt-scanner')
@login_required
def receipt_scanner():
    """Receipt scanner interface"""
    recent_scans = ReceiptScan.query.filter_by(user_id=current_user.id)\
                                   .order_by(ReceiptScan.created_at.desc())\
                                   .limit(10).all()
    
    return render_template('receipt_scanner.html', recent_scans=recent_scans)


@main.route('/scan-receipt', methods=['POST'])
@login_required
def scan_receipt():
    """Process receipt scan (mock AI)"""
    # Mock AI processing
    mock_merchants = ["Target", "Walmart", "Starbucks", "McDonald's", "Gas Station", "Grocery Store"]
    mock_amounts = [15.99, 32.45, 8.75, 125.00, 67.20, 23.15]
    
    # Simulate AI detection
    detected_amount = random.choice(mock_amounts)
    detected_merchant = random.choice(mock_merchants)
    confidence = random.uniform(0.75, 0.95)
    
    # Suggest category based on merchant (mock AI)
    category_suggestions = {
        "Starbucks": "Food",
        "McDonald's": "Food", 
        "Gas Station": "Transportation",
        "Grocery Store": "Food",
        "Target": "Other",
        "Walmart": "Other"
    }
    
    suggested_category_name = category_suggestions.get(detected_merchant, "Other")
    suggested_category = Category.query.filter_by(name=suggested_category_name).first()
    
    # Save scan result
    scan = ReceiptScan(
        user_id=current_user.id,
        filename=f"receipt_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.jpg",
        detected_amount=detected_amount,
        detected_merchant=detected_merchant,
        suggested_category_id=suggested_category.id if suggested_category else None,
        confidence_score=confidence,
        raw_text=f"Receipt from {detected_merchant}\nTotal: ${detected_amount:.2f}"
    )
    
    db.session.add(scan)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'amount': detected_amount,
        'merchant': detected_merchant,
        'category': suggested_category_name,
        'confidence': confidence,
        'scan_id': scan.id
    })


@main.route('/convert-receipt/<int:scan_id>')
@login_required
def convert_receipt_to_transaction(scan_id):
    """Convert receipt scan to transaction"""
    scan = ReceiptScan.query.get_or_404(scan_id)
    
    if scan.user_id != current_user.id:
        flash('Access denied', 'error')
        return redirect(url_for('main.receipt_scanner'))
    
    # Create transaction from scan
    transaction = Transaction(
        amount=scan.detected_amount,
        description=f"Receipt: {scan.detected_merchant}",
        transaction_type='expense',
        date=datetime.utcnow(),
        user_id=current_user.id,
        category_id=scan.suggested_category_id or 1
    )
    
    db.session.add(transaction)
    scan.transaction_id = transaction.id
    scan.is_processed = True
    db.session.commit()
    
    flash(f'Receipt converted to transaction: ${scan.detected_amount:.2f}', 'success')
    return redirect(url_for('main.dashboard'))


# 📊 Custom Dashboard Routes
@main.route('/custom-dashboard')
@login_required
def custom_dashboard():
    """Custom dashboard with widgets"""
    widgets = DashboardWidget.query.filter_by(user_id=current_user.id, is_visible=True)\
                                  .order_by(DashboardWidget.position_y, DashboardWidget.position_x).all()
    
    # If no widgets, create default ones
    if not widgets:
        default_widgets = [
            {'type': 'balance', 'title': 'Current Balance', 'position_x': 0, 'position_y': 0, 'width': 4, 'height': 2},
            {'type': 'spending_chart', 'title': 'Monthly Spending', 'position_x': 4, 'position_y': 0, 'width': 4, 'height': 3},
            {'type': 'goals', 'title': 'Budget Goals', 'position_x': 8, 'position_y': 0, 'width': 4, 'height': 3},
            {'type': 'recommendations', 'title': 'Smart Tips', 'position_x': 0, 'position_y': 2, 'width': 4, 'height': 2},
        ]
        
        for widget_data in default_widgets:
            widget = DashboardWidget(
                user_id=current_user.id,
                widget_type=widget_data['type'],
                title=widget_data['title'],
                position_x=widget_data['position_x'],
                position_y=widget_data['position_y'],
                width=widget_data['width'],
                height=widget_data['height']
            )
            db.session.add(widget)
        
        db.session.commit()
        widgets = DashboardWidget.query.filter_by(user_id=current_user.id, is_visible=True).all()
    
    return render_template('custom_dashboard.html', widgets=widgets)


@main.route('/widget-data/<widget_type>')
@login_required
def widget_data(widget_type):
    """Get data for specific widget type"""
    if widget_type == 'balance':
        return jsonify({
            'balance': current_user.get_balance(),
            'currency': 'USD'
        })
    
    elif widget_type == 'spending_chart':
        # Get last 30 days spending by category
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        transactions = Transaction.query.filter(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == 'expense',
            Transaction.date >= thirty_days_ago
        ).all()
        
        category_data = {}
        for transaction in transactions:
            cat_name = transaction.category.name
            if cat_name not in category_data:
                category_data[cat_name] = {
                    'amount': 0,
                    'color': transaction.category.color
                }
            category_data[cat_name]['amount'] += transaction.amount
        
        return jsonify(category_data)
    
    elif widget_type == 'goals':
        goals = BudgetGoal.query.filter_by(user_id=current_user.id, is_active=True).limit(5).all()
        goals_data = []
        for goal in goals:
            goals_data.append({
                'category': goal.category.name,
                'target': goal.target_amount,
                'current': goal.current_spent,
                'progress': goal.progress_percentage(),
                'over_budget': goal.is_over_budget()
            })
        
        return jsonify(goals_data)
    
    elif widget_type == 'recommendations':
        recommendations = SmartRecommendation.query.filter_by(user_id=current_user.id)\
                                                   .order_by(SmartRecommendation.impact_score.desc())\
                                                   .limit(3).all()
        rec_data = []
        for rec in recommendations:
            rec_data.append({
                'title': rec.title,
                'description': rec.description,
                'priority': rec.priority,
                'impact_score': rec.impact_score
            })
        
        return jsonify(rec_data)
    
    return jsonify({'error': 'Unknown widget type'})


# 🎮 Gamification Routes
@main.route('/achievements')
@login_required
def achievements():
    """User achievements page"""
    user_achievements = UserAchievement.query.filter_by(user_id=current_user.id).all()
    all_achievements = Achievement.query.filter_by(is_active=True).all()
    
    earned_achievement_ids = [ua.achievement_id for ua in user_achievements]
    available_achievements = [a for a in all_achievements if a.id not in earned_achievement_ids]
    
    return render_template('achievements.html', 
                         user_achievements=user_achievements,
                         available_achievements=available_achievements)


# 📊 Advanced Analytics API
@main.route('/api/spending-trends')
@login_required
def api_spending_trends():
    """Advanced spending trends API"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    transactions = Transaction.query.filter(
        Transaction.user_id == current_user.id,
        Transaction.date >= start_date
    ).order_by(Transaction.date).all()
    
    # Group by day
    daily_data = {}
    for transaction in transactions:
        date_key = transaction.date.strftime('%Y-%m-%d')
        if date_key not in daily_data:
            daily_data[date_key] = {'income': 0, 'expense': 0}
        
        if transaction.transaction_type == 'income':
            daily_data[date_key]['income'] += transaction.amount
        else:
            daily_data[date_key]['expense'] += transaction.amount
    
    return jsonify(daily_data)


@main.route('/api/predictions')
@login_required
def api_predictions():
    """AI predictions API"""
    patterns = analyze_spending_patterns(current_user.id)
    
    # Generate monthly prediction
    total_predicted = sum(p['predicted_next'] for p in patterns)
    
    # Generate insights
    insights = []
    for pattern in patterns:
        if pattern['trend'] == 'increasing':
            insights.append(f"⚠️ {pattern['category_name']} spending is trending up")
        elif pattern['trend'] == 'decreasing':
            insights.append(f"📉 Great! {pattern['category_name']} spending is decreasing")
    
    return jsonify({
        'monthly_prediction': total_predicted,
        'confidence': sum(p['confidence_score'] for p in patterns) / len(patterns) if patterns else 0,
        'insights': insights,
        'patterns': patterns
    })


# 🔄 Real-time Updates API
@main.route('/api/live-balance')
@login_required
def api_live_balance():
    """Live balance updates"""
    return jsonify({
        'balance': current_user.get_balance(),
        'timestamp': datetime.utcnow().isoformat()
    })


# PWA Service Worker
@main.route('/sw.js')
def service_worker():
    """Service Worker for PWA"""
    sw_content = """
const CACHE_NAME = 'finrelate-cache-v1';
const urlsToCache = [
    '/',
    '/static/style.css',
    '/static/finrelate.css',
    '/dashboard',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    return self.clients.claim();
});

self.addEventListener('fetch', function(event) {
    // Don't intercept requests to avoid redirect issues
    return;
});

// Push notifications
self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : 'New FinRelate notification',
        icon: '/static/icon-192x192.png',
        badge: '/static/badge-72x72.png',
        tag: 'finrelate',
        requireInteraction: true
    };

    event.waitUntil(
        self.registration.showNotification('FinRelate', options)
    );
});
"""
    response = make_response(sw_content)
    response.headers['Content-Type'] = 'application/javascript'
    return response


# PWA Manifest
@main.route('/manifest.json')
def manifest():
    """PWA Manifest"""
    manifest_data = {
        "name": "Expense Tracker",
        "short_name": "ExpenseApp",
        "description": "AI-powered personal finance management",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#007bff",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>💰</text></svg>",
                "sizes": "192x192",
                "type": "image/svg+xml"
            }
        ]
    }
    response = make_response(json.dumps(manifest_data))
    response.headers['Content-Type'] = 'application/json'
    return response
