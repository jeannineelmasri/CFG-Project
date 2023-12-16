import requests

def recipe_search(ingredient, dietary_preference):
    app_id = 'b2cf0a94'
    app_key = 'a9382b2133d69110fffaa3a5de6452a3'
    url = 'https://api.edamam.com/search'
    params = {
        'q': ingredient,
        'app_id': app_id,
        'app_key': app_key,
    }
    if dietary_preference:
        params['health'] = dietary_preference
    result = requests.get(url, params=params)
    data = result.json()

    if 'hits' in data and isinstance(data['hits'], list):
        return data['hits']
    else:
        print("No recipes found for the given ingredient and dietary preference.")
        return []

def save_to_txt(ingredient, dietary_preference, recipes):
    filename = "Recipes.txt"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"\nRecipes for {ingredient} with dietary preferences: {', '.join(dietary_preference)}:\n")
        for result in recipes:
            recipe = result['recipe']
            file.write(f"Recipe: {recipe['label']}\n")
            file.write(f"URI: {recipe['uri']}\n")

            # Extract and save the ingredients to the shopping list
            file.write("Ingredients:\n")
            for ingredient_info in recipe['ingredientLines']:
                file.write(f"- {ingredient_info}\n")

            file.write("\n")
def run():
    #prompts user to enter ingredient and stores it into ingredient variable
    ingredient = input('Enter an ingredient: ')
    # Ask the user for dietary preferences or allergies
    dietary_preference = input('Enter any dietary preferences or allergies (comma-separated): ')
    # Convert the input string to a list
    if dietary_preference:
        health_labels = dietary_preference.split(',')
    else:
        health_labels = None

    results = recipe_search(ingredient, dietary_preference=health_labels)
    # Display the dietary preferences
    print(f"Dietary Preferences: {dietary_preference}\n")
    # Display the recipes and create a shopping list for each search result
    for result in results:
        recipe = result['recipe']
        print(f"Recipe: {recipe['label']}")
        print(f"URI: {recipe['uri']}")
        # Display the ingredients
        print("Ingredients:")
        for ingredient_info in recipe['ingredientLines']:
            print(f"- {ingredient_info}")
        print()

    # Save the recipes and shopping list to a text file (erasing existing content)
    save_to_txt(ingredient, health_labels, results)
    print(f"Recipes and shopping list saved to Recipes.txt")


if __name__ == "__main__":
    run()
