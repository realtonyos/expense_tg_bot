import sqlite3
from .models import create_tables


# Подключение к БД
def get_connection():
    return sqlite3.connect('expenses.db')


# ===== USERS =====
def get_or_create_user(user_id, username, first_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Проверяем существование
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        # Создаем нового
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name) 
            VALUES (?, ?, ?)
        ''', (user_id, username, first_name))
        conn.commit()

    conn.close()
    return user_id


def update_user_settings(user_id, daily_limit=None, currency=None):
    conn = get_connection()
    cursor = conn.cursor()

    updates = []
    params = []

    if daily_limit is not None:
        updates.append('daily_limit = ?')
        params.append(daily_limit)
    if currency is not None:
        updates.append('currency = ?')
        params.append(currency)

    if updates:
        params.append(user_id)
        cursor.execute(f'''
            UPDATE users SET {', '.join(updates)} 
            WHERE user_id = ?
        ''', params)
        conn.commit()

    conn.close()


def get_user_settings(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT user_id, username, daily_limit, currency 
        FROM users WHERE user_id = ?
    ''', (user_id,))

    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            'user_id': user[0],
            'username': user[1],
            'daily_limit': user[2],
            'currency': user[3]
        }
    return None


# ===== EXPENSES =====
def add_expense(user_id, amount, category, description=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO expenses (user_id, amount, category, description)
        VALUES (?, ?, ?, ?)
    ''', (user_id, amount, category, description))

    expense_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return expense_id


def get_today_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT amount, category, description 
        FROM expenses 
        WHERE user_id = ? AND date = DATE('now')
        ORDER BY id DESC
    ''', (user_id,))

    expenses = cursor.fetchall()
    conn.close()

    return [
        {'amount': e[0], 'category': e[1], 'description': e[2]}
        for e in expenses
    ]


def get_month_expenses(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            SUM(amount) as total,
            category,
            COUNT(*) as count
        FROM expenses 
        WHERE user_id = ? 
          AND strftime('%Y-%m', date) = strftime('%Y-%m', 'now')
        GROUP BY category
        ORDER BY total DESC
    ''', (user_id,))

    stats = cursor.fetchall()
    conn.close()

    return [
        {'category': s[1], 'total': s[0], 'count': s[2]}
        for s in stats
    ]


# ===== INIT =====
def init_database():
    conn = get_connection()
    create_tables(conn)  # из models.py
    conn.close()
