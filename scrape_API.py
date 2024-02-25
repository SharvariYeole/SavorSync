import requests
import csv


def get_recipes_by_ingredient(ingredient):
    """Fetch recipes by ingredient from TheMealDB."""
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?i={ingredient}"
    response = requests.get(url)
    if response.status_code == 200 and response.json()['meals'] is not None:
        return response.json()['meals']
    else:
        print("No recipes found or API error occurred.")
        return []


def get_recipes_from_recipe_puppy(ingredients):
    """Fetch recipes by ingredients from Recipe Puppy."""
    url = f"http://www.recipepuppy.com/api/?i={ingredients}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print("API request failed with status code:", response.status_code)
        return []


def write_recipes_to_csv(ingredient):
    recipes = get_recipes_by_ingredient(ingredient)
    with open('AllRecipes_full.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['recipe_urls', 'recipe_name', 'serves', 'cooking_time', 'ingredients'])

        if recipes:
            for recipe in recipes:
                recipe_id = recipe['idMeal']
                recipe_name = recipe['strMeal']
                recipe_urls = f"https://www.themealdb.com/meal/{recipe_id}"  # Assumed URL pattern

                # TheMealDB requires an additional call to get detailed recipe info, including ingredients and cooking time
                # For simplicity, this example uses placeholders
                serves = 'N/A'  # Placeholder, not directly provided by TheMealDB
                cooking_time = 'N/A'  # Placeholder, not directly provided by TheMealDB
                ingredients = 'N/A'  # Placeholder, requires additional API call and parsing

                writer.writerow([recipe_urls, recipe_name, serves, cooking_time, ingredients])
        else:
            print("No recipes found for the ingredient:", ingredient)


# Example usage
write_recipes_to_csv('tomato')
