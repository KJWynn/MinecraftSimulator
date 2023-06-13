""" 
Food. Players purchase them with emeralds to get hunger bars so that they can mine materials.

Food objects have a name, a price and a certain number of hunger points it provides to the player. Supports random generation of a food item. 
"""
from __future__ import annotations

from random_gen import RandomGen

# List of food names from https://github.com/vectorwing/FarmersDelight/tree/1.18.2/src/main/resources/assets/farmersdelight/textures/item
FOOD_NAMES = [
    "Apple Cider",
    "Apple Pie",
    "Apple Pie Slice",
    "Bacon",
    "Bacon And Eggs",
    "Bacon Sandwich",
    "Baked Cod Stew",
    "Barbecue Stick",
    "Beef Patty",
    "Beef Stew",
    "Cabbage",
    "Cabbage Leaf",
    "Cabbage Rolls",
    "Cabbage Seeds",
    "Cake Slice",
    "Chicken Cuts",
    "Chicken Sandwich",
    "Chicken Soup",
    "Chocolate Pie",
    "Chocolate Pie Slice",
    "Cod Slice",
    "Cooked Bacon",
    "Cooked Chicken Cuts",
    "Cooked Cod Slice",
    "Cooked Mutton Chops",
    "Cooked Rice",
    "Cooked Salmon Slice",
    "Dog Food",
    "Dumplings",
    "Egg Sandwich",
    "Fish Stew",
    "Fried Egg",
    "Fried Rice",
    "Fruit Salad",
    "Grilled Salmon",
    "Ham",
    "Hamburger",
    "Honey Cookie",
    "Honey Glazed Ham",
    "Honey Glazed Ham Block",
    "Horse Feed",
    "Hot Cocoa",
    "Melon Juice",
    "Melon Popsicle",
    "Milk Bottle",
    "Minced Beef",
    "Mixed Salad",
    "Mutton Chops",
    "Mutton Wrap",
    "Nether Salad",
    "Noodle Soup",
    "Onion",
    "Pasta With Meatballs",
    "Pasta With Mutton Chop",
    "Pie Crust",
    "Pumpkin Pie Slice",
    "Pumpkin Slice",
    "Pumpkin Soup",
    "Ratatouille",
    "Raw Pasta",
    "Rice",
    "Rice Panicle",
    "Roast Chicken", 
    "Roast Chicken Block",
    "Roasted Mutton Chops",
    "Rotten Tomato",
    "Salmon Slice",
    "Shepherds Pie",
    "Shepherds Pie Block",
    "Smoked Ham",
    "Squid Ink Pasta",
    "Steak And Potatoes",
    "Stuffed Potato",
    "Stuffed Pumpkin",
    "Stuffed Pumpkin Block",
    "Sweet Berry Cheesecake",
    "Sweet Berry Cheesecake Slice",
    "Sweet Berry Cookie",
    "Tomato",
    "Tomato Sauce",
    "Tomato Seeds",
    "Vegetable Noodles",
    "Vegetable Soup",
]

class Food:
    """
        Player's uses emeralds to buy food to replenish hunger bars.

        Attributes:
        * Name: Used to identify the food.
        * Hunger bars: The number of bars of hunger this food will give you when eaten. This can be used to mine materials.
        * Price: The emerald cost of the food. This is fixed.

    """
    
    def __init__(self, name: str, hunger_bars: int, price: int) -> None:
        """
            Initialises attributes

            :param arg1: name of the food (Mutton, Tomato, etc)
            :param arg2: number of hunger bars the food can replenish 
            :param arg3: emarald cost for the food

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.name = name
        self.hunger_bars = hunger_bars
        self.price = price
    
    def __str__(self) -> str:
        """
            Returns string representation which includes food name, emerald cost for food and hunger bars of food
            
            :param: None

            :pre: None

            :return: string representation of food

            :complexity: Best/Worst O(1)
        """

        return f"{self.name} {self.price}💰 for {self.hunger_bars}🍗"

    @classmethod
    def random_food(cls) -> Food:
        """
            Generates and returns a random food

            :param: None

            :pre: None
            
            :return: random food object

            :complexity: Best/Worst O(1)
        """
        random_name = RandomGen.random_choice(FOOD_NAMES) # gets random name from list of random names provided
        random_hunger_bars = RandomGen.randint(10,400) # arbitrary generation of hunger bars awarded
        random_price = RandomGen.randint(10, 20) # arbitrary generation of price of food
        return Food(random_name, random_hunger_bars, random_price)

if __name__ == "__main__":
    print(Food.random_food())

