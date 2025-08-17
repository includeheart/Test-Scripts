recipes_list = []
ingredients_list = []
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
    # Print each recipe's details inside the loop
    print(f"Recipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {difficulty}")
    print()  # Add blank line between recipes
# Print all ingredients at the end (outside the loop)
ingredients_list.sort()
print(f"Ingredients from all recipes: {', '.join(ingredients_list)}")