CREATE_USERS_TABLE = '''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        daily_limit REAL DEFAULT 0,
        currency TEXT DEFAULT 'RUB',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
'''

CREATE_EXPENSES_TABLE = '''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
'''


def create_tables(connection):
    cursor = connection.cursor()
    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_EXPENSES_TABLE)
    connection.commit()
