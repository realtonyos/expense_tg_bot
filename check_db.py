import sqlite3

# Подключение к базе
conn = sqlite3.connect('expenses.db')
cursor = conn.cursor()

# Показать все таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Таблицы в базе:")
for table in tables:
    print(f"  - {table[0]}")

# Показать структуру каждой таблицы
for table in tables:
    print(f"\nСтруктура таблицы '{table[0]}':")
    cursor.execute(f"PRAGMA table_info({table[0]});")
    columns = cursor.fetchall()
    for col in columns:
        print(f"  {col[1]} ({col[2]})")

# Показать данные из users
print("\nПользователи:")
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
for user in users:
    print(f"  ID: {user[0]}, Имя: {user[2]}, Лимит: {user[3]}")

# Показать данные из expenses
print("\nРасходы:")
cursor.execute("SELECT * FROM expenses;")
expenses = cursor.fetchall()
for exp in expenses:
    print(f"  ID: {exp[0]}, User: {exp[1]}, Сумма: {exp[2]}, Категория: {exp[3]}")

conn.close()