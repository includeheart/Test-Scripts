import pickle
recipe = {
    "name": "Tea",
    "ingredients": [
        "Tea leaves",
        "Water",
        "Sugar",
    ],
    "cooking_time": "5 minutes",
    "difficulty": "Easy"
}
my_file = open("tea_recipe.bin", "wb")
pickle.dump(recipe, my_file)
my_file.close()