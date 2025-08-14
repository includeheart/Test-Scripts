class Recipe:
    all_ingredients = set()

    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        self.difficulty = None

    # Getters
    def get_name(self):
        return self.name
    def get_ingredients(self):
        return self.ingredients
    def get_cooking_time(self):
        return self.cooking_time
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    def get_ingredients(self):
        return self.ingredients
    
    # Setters
    def set_name(self, name):
        self.name = name
    def set_ingredients(self, ingredients):
        self.ingredients = ingredients
        self.difficulty = None 
        self.update_all_ingredients()
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.difficulty = None 
    def set_difficulty(self, difficulty):
        self.difficulty = difficulty

    
    def add_ingredients(self, *ingredients):
        to_add = [i for i in ingredients if i]
        self.ingredients.extend(to_add)
        self.update_all_ingredients()
        self.difficulty = None
    
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients)
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

    def search_ingredient(self, ingredient):
        ingredient_lower = ingredient.lower()
        return any(ingredient_lower == ingr.lower() for ingr in self.ingredients)
    
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)
    
    def __str__(self):
        return f"Recipe: {self.name}, Ingredients: {self.ingredients}, Cooking Time: {self.cooking_time}, Difficulty: {self.get_difficulty()}"
    
    def recipe_search(data, search_term):
        print(f"Recipes that contain '{search_term}':")
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(f" - {recipe.name}")
    
tea = Recipe("Tea", ["water", "tea leaves"], 5)
coffee = Recipe("Coffee", ["Coffee Powder", "Sugar", "Water"], 5)
cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"], 5)

recipes_list = [tea, coffee, cake, smoothie]

for recipe in recipes_list:
    print(recipe)

for ingredient in ["Water", "Sugar", "Bananas"]:
    Recipe.recipe_search(recipes_list, ingredient)