import pickle

file_name = input("Enter the filename to search for recipes (without extension): ") + ".bin"
with open(file_name, "rb") as my_file:
    data = pickle.load(my_file)
recipes = data["recipes"]
ingredients = data["ingredients"]
print("Available Recipes:")
for recipe in recipes:
    print(f"- {recipe}")