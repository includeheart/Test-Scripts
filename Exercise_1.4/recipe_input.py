import pickle

recipes_list = []
ingredients_list = []
data = {"recipes": recipes_list, "ingredients": ingredients_list}

n = int(input("Enter the number of recipes you want to add: "))

def take_recipe(): # Function to take recipe details from user
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time (in minutes): "))
    ingredients = [ingredient.strip() for ingredient in input("Enter the ingredients (separated by commas): ").split(",")]
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }
    return recipe

for i in range(n): # Loop to take multiple recipes
    recipe = take_recipe()
    for ingredient in recipe["ingredients"]:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list: # Loop to determine the difficulty of each recipe
    if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Easy"
    elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
        difficulty = "Medium"
    elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    print(f"Recipe: {recipe['name']}") # Print each recipe's details inside the loop
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {difficulty}")
    print()  # Add blank line between recipes

ingredients_list.sort()  # Print all ingredients at the end (outside the loop)

print(f"Ingredients from all recipes: {', '.join(ingredients_list)}")

filename = input("Enter the filename for saving recipes (without extension): ") + ".bin"
try:
    with open(filename, "wb") as my_file:
        pickle.dump(data, my_file)  # Save the recipes list to a binary file
    print(f"Recipes saved to {filename}")

except OSError as e: # Catches errors in filename
    print(f"Error: Could not save file '{filename}'. {e}")
    print("Please check that the filename is valid and you have write permissions.")
    try: # Attempt to save to a default file if the specified filename fails
        default_filename = "recipes.bin"
        with open(default_filename, "wb") as my_file:
            pickle.dump(data, my_file)
        print(f"Recipes saved to default file: {default_filename}")
    except OSError:
        print("Failed to save recipes to any file.")