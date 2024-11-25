from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from pprint import pprint

# Підключення до MongoDB (локально або через Atlas)


def connect_to_db():
    try:
        # Якщо ви використовуєте MongoDB Atlas, використовуйте відповідний URI
        client = MongoClient('mongodb://localhost:27017/')
        db = client['cat_database']  # Створюємо/підключаємось до бази даних
        return db['cats']  # Підключаємося до колекції "cats"
    except ConnectionFailure as e:
        print(f"Помилка з підключенням до MongoDB: {e}")
        return None

# 1. Створення нового кота (Create)


def create_cat(collection, name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    try:
        result = collection.insert_one(cat)
        print(f"Додано кота з ID: {result.inserted_id}")
    except PyMongoError as e:
        print(f"Помилка при додаванні кота: {e}")

# 2. Читання всіх котів (Read)


def get_all_cats(collection):
    try:
        cats = collection.find()
        for cat in cats:
            pprint(cat)
    except PyMongoError as e:
        print(f"Помилка при читанні котів: {e}")

# 3. Читання кота за ім'ям (Read)


def get_cat_by_name(collection, name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            pprint(cat)
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except PyMongoError as e:
        print(f"Помилка при пошуку кота: {e}")

# 4. Оновлення віку кота (Update)


def update_cat_age(collection, name, new_age):
    try:
        result = collection.update_one(
            {"name": name}, {"$set": {"age": new_age}})
        if result.matched_count:
            print(f"Вік кота {name} оновлено.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений для оновлення.")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

# 5. Додавання характеристики до списку features кота (Update)


def add_feature_to_cat(collection, name, feature):
    try:
        result = collection.update_one(
            {"name": name},
            # Використовуємо $addToSet, щоб уникнути дублювання
            {"$addToSet": {"features": feature}}
        )
        if result.matched_count:
            print(f"Характеристика '{feature}' додана до кота {name}.")
        else:
            print(f"Кіт з ім'ям {
                  name} не знайдений для додавання характеристики.")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики: {e}")

# 6. Видалення кота за ім'ям (Delete)


def delete_cat_by_name(collection, name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count:
            print(f"Кіт з ім'ям {name} видалений.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений для видалення.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

# 7. Видалення всіх котів (Delete)


def delete_all_cats(collection):
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except PyMongoError as e:
        print(f"Помилка при видаленні всіх котів: {e}")

# Головна функція для тестування


def main():
    collection = connect_to_db()

    if collection is not None:
        # Тест: Додати кілька котів
        create_cat(collection, "Barsik", 3, [
                   "ходить в капці", "дає себе гладити", "рудий"])
        create_cat(collection, "Murzik", 5, [
                   "любить їсти рибу", "довга шерсть"])

        # Тест: Вивести всіх котів
        print("\nВсі коти:")
        get_all_cats(collection)

        # Тест: Вивести інформацію про кота за ім'ям
        print("\nІнформація про кота 'Barsik':")
        get_cat_by_name(collection, "Barsik")

        # Тест: Оновлення віку кота
        update_cat_age(collection, "Barsik", 4)

        # Тест: Додавання нової характеристики
        add_feature_to_cat(collection, "Barsik", "любить грати з м'ячиком")

        # Тест: Видалення кота
        delete_cat_by_name(collection, "Murzik")

        # Тест: Видалення всіх котів
        delete_all_cats(collection)


if __name__ == "__main__":
    main()
