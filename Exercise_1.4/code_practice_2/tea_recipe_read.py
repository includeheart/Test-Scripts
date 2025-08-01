import pickle
with open("Exercise_1.4/code_practice_2/tea_recipe.bin", "rb") as my_file:
    recipe = pickle.load(my_file)
print("Recipe Name:", recipe["name"])
print("Ingredients:", ", ".join(recipe["ingredients"]))
print("Cooking Time:", recipe["cooking_time"])
print("Difficulty:", recipe["difficulty"])