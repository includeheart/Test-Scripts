import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password',
)

cursor = conn.cursor()

cursor.execute('CREATE DATABASE IF NOT EXISTS task_db')

cursor.execute('USE task_db')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)    
    )
''')

def create_recipe(name, ingredients, cooking_time, difficulty):
    cursor.execute('''
        INSERT INTO recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
    ''', (name, ingredients, cooking_time, difficulty))
    conn.commit()

def search_recipe(ingredient):
    cursor.execute('''
        SELECT * FROM recipes
        WHERE ingredients LIKE %s
    ''', ('%' + ingredient + '%',))
    return cursor.fetchall()

def update_recipe(recipe_id, name, ingredients, cooking_time, difficulty):
    cursor.execute('''
        UPDATE recipes
        SET name = %s, ingredients = %s, cooking_time = %s, difficulty = %s
        WHERE id = %s
    ''', (name, ingredients, cooking_time, difficulty, recipe_id))
    conn.commit()

def delete_recipe(recipe_id):
    cursor.execute('''
        DELETE FROM recipes
        WHERE id = %s
    ''', (recipe_id,))
    conn.commit()

def calculate_difficulty(ingredients_str: str, cooking_time: int) -> str:
    """Calculate difficulty based on cooking_time and number of ingredients.

    Rules:
    - cooking_time < 10 and num_ingredients < 4 => Easy
    - cooking_time < 10 and num_ingredients >= 4 => Medium
    - cooking_time >= 10 and num_ingredients < 4 => Intermediate
    - cooking_time >= 10 and num_ingredients >= 4 => Hard
    """
    items = [i.strip() for i in (ingredients_str or "").split(',') if i.strip()]
    num_ingredients = len(items)

    if cooking_time < 10:
        return "Easy" if num_ingredients < 4 else "Medium"
    else:
        return "Intermediate" if num_ingredients < 4 else "Hard"

while True:
    print("1. Create Recipe")
    print("2. Search Recipe")
    print("3. Update Recipe")
    print("4. Delete Recipe")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        name = input("Enter recipe name: ")
        ingredients = input("Enter ingredients: ")
        cooking_time = int(input("Enter cooking time (in minutes): "))
        difficulty = calculate_difficulty(ingredients, cooking_time)
        create_recipe(name, ingredients, cooking_time, difficulty)

    elif choice == '2':
        ingredient = input("Enter ingredient to search: ")
        recipes = search_recipe(ingredient)
        for recipe in recipes:
            print(recipe)

    elif choice == '3':
        recipe_id = int(input("Enter recipe ID to update: "))
        name = input("Enter new recipe name: ")
        ingredients = input("Enter new ingredients: ")
        cooking_time = int(input("Enter new cooking time (in minutes): "))
        difficulty = calculate_difficulty(ingredients, cooking_time)
        update_recipe(recipe_id, name, ingredients, cooking_time, difficulty)

    elif choice == '4':
        recipe_id = int(input("Enter recipe ID to delete: "))
        delete_recipe(recipe_id)

    elif choice == '5':
        break

    else:
        print("Invalid choice. Please try again.")

conn.commit()
cursor.close()
conn.close()