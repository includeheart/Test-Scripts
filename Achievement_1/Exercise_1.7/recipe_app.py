from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_db")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = 'final_recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))
    def __repr__(self):
        return f"<Recipe(id={self.id}, name={self.name}, difficulty={self.difficulty})>"
    def __str__(self):
        return f"Recipe: {self.name}, Difficulty: {self.difficulty}"
    def calculate_difficulty(self):
        items = self.return_ingredients_as_list()
        num_ingredients = len(items)
        if self.cooking_time < 10:
            if num_ingredients < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if num_ingredients < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"
    def return_ingredients_as_list(self):
        if not self.ingredients:
            return []
        return [i.strip() for i in self.ingredients.split(',') if i.strip()]

Base.metadata.create_all(engine)

# I was assisted by ChatGPT to help me implement the following validation logic
def _validate_and_normalize_recipe_inputs(name, ingredients, cooking_time):
    """Validate inputs and return normalized (name, ingredients_csv, cooking_time_int).

    - name: required, str, trimmed, max 50 chars
    - ingredients: str or iterable of strings; normalized to a comma-separated string of
      unique, trimmed items; total length <= 255
    - cooking_time: int-convertible, >= 0
    """
    # Name
    if name is None:
        raise ValueError("name is required")
    name_clean = str(name).strip()
    if not name_clean:
        raise ValueError("name cannot be empty")
    if len(name_clean) > 50:
        raise ValueError("name must be at most 50 characters")

    # Ingredients -> list of unique, trimmed strings preserving order
    items = []
    if ingredients is None:
        items = []
    elif isinstance(ingredients, str):
        items = [i.strip() for i in ingredients.split(',') if i.strip()]
    else:
        try:
            for itm in ingredients:
                s = ("" if itm is None else str(itm)).strip()
                if s and s not in items:
                    items.append(s)
        except TypeError:
            # Not iterable; coerce to single-item list
            s = str(ingredients).strip()
            if s:
                items = [s]
    if not items:
        raise ValueError("ingredients must contain at least one item")

    ingredients_csv = ",".join(items)
    if len(ingredients_csv) > 255:
        raise ValueError("ingredients are too long; please shorten to fit 255 characters")

    # Cooking time
    try:
        cooking_time_int = int(cooking_time)
    except (TypeError, ValueError):
        raise ValueError("cooking_time must be an integer")
    if cooking_time_int < 0:
        raise ValueError("cooking_time must be 0 or greater")

    return name_clean, ingredients_csv, cooking_time_int

def create_recipe(name, ingredients, cooking_time):
    # Validate and normalize inputs before persisting
    name, ingredients, cooking_time = _validate_and_normalize_recipe_inputs(name, ingredients, cooking_time)
    recipe = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
    recipe.calculate_difficulty()
    session.add(recipe)
    session.commit()
    return recipe

# --- Query helpers ---
def search_recipes(ingredient_substring: str):
    term = (ingredient_substring or "").strip()
    if not term:
        return []
    # Case-insensitive search by lowering both sides (works across backends)
    return (
        session.query(Recipe)
        .filter(func.lower(Recipe.ingredients).like(f"%{term.lower()}%"))
        .all()
    )

def update_recipe(recipe_id: int, name, ingredients, cooking_time):
    obj = session.get(Recipe, recipe_id)
    if not obj:
        return None

    # Treat blank/None inputs as "keep existing"
    merged_name = obj.name if name is None or str(name).strip() == "" else name
    merged_ingredients = obj.ingredients if ingredients is None or str(ingredients).strip() == "" else ingredients
    merged_cooking_time = obj.cooking_time if cooking_time is None or str(cooking_time).strip() == "" else cooking_time

    # Validate normalized values
    name_v, ingredients_v, cooking_time_v = _validate_and_normalize_recipe_inputs(
        merged_name, merged_ingredients, merged_cooking_time
    )

    obj.name = name_v
    obj.ingredients = ingredients_v
    obj.cooking_time = cooking_time_v
    obj.calculate_difficulty()
    session.commit()
    return obj

def delete_recipe(recipe_id: int) -> bool:
    obj = session.get(Recipe, recipe_id)
    if not obj:
        return False
    session.delete(obj)
    session.commit()
    return True

def view_all_recipes():
    return session.query(Recipe).all()

while True:
    print("1. Create Recipe")
    print("2. Search Recipe by Ingredient")
    print("3. Update Recipe")
    print("4. Delete Recipe")
    print("5. View All Recipes")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        try:
            name = input("Enter recipe name: ")
            ingredients = input("Enter ingredients (comma-separated): ")
            cooking_time = input("Enter cooking time (in minutes): ")
            recipe = create_recipe(name, ingredients, cooking_time)
            print(f"Created: {recipe} (id={recipe.id})")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == '2':
        term = input("Enter ingredient to search: ")
        results = search_recipes(term)
        if not results:
            print("No recipes found.")
        else:
            for r in results:
                print(f"[{r.id}] {r.name} | {r.difficulty} | {r.ingredients}")

    elif choice == '3':
        try:
            recipe_id = int(input("Enter recipe ID to update: "))
            name = input("Enter new recipe name (Press Enter to Skip): ")
            ingredients = input("Enter new ingredients (comma-separated, Press Enter to Skip): ")
            cooking_time = input("Enter new cooking time (in minutes, Press Enter to Skip): ")
            updated = update_recipe(recipe_id, name, ingredients, cooking_time)
            if not updated:
                print("Recipe not found.")
            else:
                print(f"Updated: {updated}")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == '4':
        try:
            recipe_id = int(input("Enter recipe ID to delete: "))
            ok = delete_recipe(recipe_id)
            print("Deleted." if ok else "Recipe not found.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == '5':
        recipes = view_all_recipes()
        if not recipes:
            print("No recipes found.")
        else:
            for r in recipes:
                print(f"[{r.id}] {r.name} | {r.difficulty} | {r.ingredients}")

    elif choice == '6':
        break

    else:
        print("Invalid choice. Please try again.")
