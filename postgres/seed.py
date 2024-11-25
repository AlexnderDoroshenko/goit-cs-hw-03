from faker import Faker
from os import environ as env

import psycopg2


# Ініціалізація Faker
fake = Faker()
# Підключення до PostgreSQL
conn = psycopg2.connect(
    dbname=env.get('POSTGRES_DB') or "hw03",
    user=env.get('POSTGRES_USER') or "postgres",
    password=env.get('POSTGRES_PASSWORD') or "567234",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Функція для створення випадкових користувачів


def create_users(num_users):
    for _ in range(num_users):
        fullname = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# Функція для створення статусів


def create_statuses():
    statuses = ['new', 'in progress', 'completed']
    for status in statuses:
        cursor.execute("INSERT INTO status (name) VALUES (%s)", (status,))

# Функція для створення завдань


def create_tasks(num_tasks):
    for _ in range(num_tasks):
        title = fake.sentence(nb_words=6)
        description = fake.text()
        status_id = fake.random_int(min=1, max=3)
        user_id = fake.random_int(min=1, max=10)
        cursor.execute(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            (title, description, status_id, user_id)
        )


# Запуск функцій
create_statuses()
create_users(10)  # Створити 10 користувачів
create_tasks(20)  # Створити 20 завдань

# Збереження змін та закриття підключення
conn.commit()
cursor.close()
conn.close()

print("Database has been seeded with random data.")
