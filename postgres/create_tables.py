import psycopg2
from os import environ as env

# Параметри підключення до PostgreSQL
conn = psycopg2.connect(
    dbname=env.get('POSTGRES_DB') or "hw03",
    user=env.get('POSTGRES_USER') or "postgres",
    password=env.get('POSTGRES_PASSWORD') or "567234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# SQL запит для створення таблиць
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL CHECK (name IN ('new', 'in progress', 'completed'))
);
"""

create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

# Виконання запитів для створення таблиць
cur.execute(create_users_table)
cur.execute(create_status_table)
cur.execute(create_tasks_table)

# Збереження змін і закриття з'єднання
conn.commit()
cur.close()
conn.close()

print("Таблиці успішно створено!")
