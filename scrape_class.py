import requests
from bs4 import BeautifulSoup
import pandas as pd 
import numpy as np
import re

headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36"}

class AllRecipes():
    """ This class will output the recipe details. Recipes have the
    following properties:

    Attributes:
        url: The url of the recipe on website.

    Methods:
        Ingredients: Recipe ingredients.
        Cooking time: What it says on the tin.
        Serves: How many people the recipe serves.
    """
    def __init__(self, url):
        self.url = url 
        self.soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    
    def recipe_name(self):
        """ Locates the recipe title """
        # Some of the urls are not recipe urls so to avoid errors we use try/except 
        try:
            return self.soup.find('title').text.strip()
          # return self.soup.select('ht.hidden-xs')[0].text.strip()
        except: 
            return np.nan

    def serves(self):
        """ Locates the number of people the meal serves """
        try:
            # Updated to correctly find the servings based on the provided HTML structure
            servings_div = self.soup.find('div', string='Servings:').find_next_sibling('div')
            return servings_div.text.strip()
        except:
            return np.nan

    def cooking_time(self):
        """ Locates the total cooking time """
        try:
            # Updated to correctly find the total cooking time based on the provided HTML structure
            total_time_div = self.soup.find('div', string='Total Time:').find_next_sibling('div')
            return total_time_div.text.strip()
        except:
            return np.nan

    def ingredients(self):
        """ Creating a list containing the ingredients of the recipe """
        try:
            ingredients = []
            # Updated selector to match the provided HTML structure
            for li in self.soup.select('.mntl-structured-ingredients__list-item'):
                # Extracting quantity, unit, and name based on their specific data attributes
                quantity = li.find('span', {'data-ingredient-quantity': 'true'}).text.strip()
                unit = li.find('span', {'data-ingredient-unit': 'true'}).text.strip()
                name = li.find('span', {'data-ingredient-name': 'true'}).text.strip()

                # Constructing the ingredient string
                ingredient = f"{quantity} {unit} {name}"
                # Cleaning up the ingredient string to remove any excess spaces, especially for ingredients without a unit
                ingredient_cleaned = ' '.join(ingredient.split())
                ingredients.append(ingredient_cleaned)
            return ingredients
        except:
            return np.nan



