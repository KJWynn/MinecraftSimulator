""" 
Trader. Traders generate daily deals of a material and a selling price for the player. 

Supports random generation of a trader with only the trader's name. Deciding the random trader type is done in the Game class itself. 
Traders are differentiated by their names only, so it's possible for traders to generate deals with the same material(and likely different prices)
"""


from __future__ import annotations

from abc import abstractmethod, ABC
from material import Material
from random_gen import RandomGen
from array_list import ArrayList
from avl import AVLTree
from bst import BSTInOrderIterator

# Generated with https://www.namegenerator.co/real-names/english-name-generator
TRADER_NAMES = [
    "Pierce Hodge",
    "Loren Calhoun",
    "Janie Meyers",
    "Ivey Hudson",
    "Rae Vincent",
    "Bertie Combs",
    "Brooks Mclaughlin",
    "Lea Carpenter",
    "Charlie Kidd",
    "Emil Huffman",
    "Letitia Roach",
    "Roger Mathis",
    "Allie Graham",
    "Stanton Harrell",
    "Bert Shepherd",
    "Orson Hoover",
    "Lyle Randall",
    "Jo Gillespie",
    "Audie Burnett",
    "Curtis Dougherty",
    "Bernard Frost",
    "Jeffie Hensley",
    "Rene Shea",
    "Milo Chaney",
    "Buck Pierce",
    "Drew Flynn",
    "Ruby Cameron",
    "Collie Flowers",
    "Waldo Morgan",
    "Winston York",
    "Dollie Dickson",
    "Etha Morse",
    "Dana Rowland",
    "Eda Ryan",
    "Audrey Cobb",
    "Madison Fitzpatrick",
    "Gardner Pearson",
    "Effie Sheppard",
    "Katherine Mercer",
    "Dorsey Hansen",
    "Taylor Blackburn",
    "Mable Hodge",
    "Winnie French",
    "Troy Bartlett",
    "Maye Cummings",
    "Charley Hayes",
    "Berta White",
    "Ivey Mclean",
    "Joanna Ford",
    "Florence Cooley",
    "Vivian Stephens",
    "Callie Barron",
    "Tina Middleton",
    "Linda Glenn",
    "Loren Mcdaniel",
    "Ruby Goodman",
    "Ray Dodson",
    "Jo Bass",
    "Cora Kramer",
    "Taylor Schultz",
]

class Trader(ABC):
    """
        Abstract Trader class. Traders buys materials from players, only one material at a time, and this material changes day by day. 
        The material selected depends on which of the 3 implementations(Random, Range, Hard)

        Attributes:
        * name: Used to differentiate between traders
        * inventory: the materials that the trader can buy
        * current_material: the material the trader currently wants from the player
        * current_price: the price the trader offers to buy the current material 

    """
    def __init__(self, name: str) -> None:
        """
            Initialises attributes

            :param: the name of the Trader

            :pre: None

            :return: None   

            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        self.name = name
        self.inventory = ArrayList(10) # arbitrary value of 10 given
        self.current_material = None
        self.current_price = None

    @classmethod 
    def random_trader(cls) -> RandomTrader | RangeTrader | HardTrader:
        """
            Returns a RandomTrader or a RangeTrader or a HardTrader with a random name

            :param: None

            :pre: None

            :return: An object of RandomTrader or RangeTrader or HardTrader
            
            :complexity: Best = Worst O(N), where N is the size of the inventor
        """
        random_name = RandomGen.random_choice(TRADER_NAMES)
        random_type = RandomGen.random_choice([RandomTrader, RangeTrader, HardTrader])
        if random_type == RandomTrader:
            return RandomTrader(random_name)
        elif random_type == RangeTrader:
            return RangeTrader(random_name)
        elif random_type == HardTrader:
            return HardTrader(random_name)

    @abstractmethod
    def generate_deal(self):
        pass
    
    def set_all_materials(self, mats: list[Material]) -> None:
        """
            Sets the inventory of the trader with the list of Materials given

            :param: mats - A list of Material objects

            :pre: None

            :return: None

            :complexity: O(N), where N is the size of the list of Materials
        """
        self.inventory.clear()
        for mat in mats:
            self.inventory.append(mat)
    
    def add_material(self, mat: Material) -> None:
        """
            Adds a Material into the inventory

            :param: mats - A list of Material objects

            :pre: None

            :return: None

            :complexity: O(N), where N is the size of <mats>, the list of Materials 
        """
        self.inventory.append(mat)
    
    def is_currently_selling(self) -> bool:
        """
            Returns True if the Trader has an active deal

            :param: None

            :pre: None

            :return: boolean

            :complexity: Best = Worst O(1)
        """
        return not self.current_material is None

    def current_deal(self) -> tuple[Material, float]:
        """
            Returns tuple representing current deal.

            :param: None

            :pre: None

            :return: tuple representing current deal if there's a deal going on

            :complexity: Best = Worst O(1)
        """
        if self.is_currently_selling():
            return (self.current_material, self.current_price)
        else:
            raise ValueError("No deal currently")

    def stop_deal(self) -> None:
        """
            Sets material and price to None to stop any active deals

            :param: None

            :pre: None

            :return: None

            :complexity: Best = Worst O(1)
        
        """
        self.current_material = None
        self.current_price = None
    
    def __str__(self) -> str:
        """
            Returns string representation of trader which includes trader type, trader name and details of active deal

            :param: None

            :pre: None

            :return: String

            :complexity: Best = Worst O(1)
        """
        return f"<{self.__class__.__name__}: {self.name} buying [{self.current_material}] for {self.current_price}💰>"

    def __eq__(self, other: Trader) -> bool:
        """
            Returns True if Traders are equal. Traders are equal if they have the same name

            :param: other - An object of Trader

            :pre: None

            :return: boolean

            :complexity: Best = Worst O(1)
        """
        return self.name == other.name 

    def random_price(self) -> float:
        """
            Returns a randomly generated price the trader will pay the player for one unit of Material.

            :param: None

            :pre: None

            :return: float, a ramdom price 

            :complexity: Best = Worst O(1)
        """
        return round(2 + 8 * RandomGen.random_float(), 2)

    def get_sorted_tree(self) -> AVLTree:
        '''
            Helper method that returns an AVLTree sorted based on material's mining rate

            :return: AVLTree that is sorted based on material's mining rate

            :complexity: Best = Worst = O(N * log N) where N is the number of materials in the inventory
        '''
        total_mats = len(self.inventory)
        sorted_tree = AVLTree()

        # Insert to AVLTree
        for x in range(total_mats): # O(N)
            sorted_tree[self.inventory[x].mining_rate] = self.inventory[x] # O(log N)
        
        return sorted_tree
    

class RandomTrader(Trader):
    """When generating a deal, a random material is selected from their inventory, and a random buy price is selected."""

    def __init__(self, name: str) -> None:
        """
            Initialises attributes

            :param: name - The name of the RandomTrader

            :pre: None

            :return: None

            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        Trader.__init__(self, name)

    def generate_deal(self) -> None:
        """
            Generate the deal: Random material from inventory with random price

            :param: None

            :pre: None

            :return: None

            :complexity: Best = Worst O(1)
        """

        self.current_material = RandomGen.random_choice(self.inventory)
        self.current_price = self.random_price() # random price

    @classmethod
    def random_trader(cls) -> RandomTrader:
        """
            Returns a RandomTrader

            :param: None

            :pre: None

            :return: An object of RandomTrader
            
            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RandomTrader(random_name)


class RangeTrader(Trader):
    """Generates ith to jth materials from their inventory in descending mining rate and randomly chooses one material from this"""

    def __init__(self, name: str) -> None:
        """
            Initialises attributes.

            :param: name - The name of the RangeTrader 

            :pre: None

            :return: None

            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        Trader.__init__(self, name)
        self.sorted_tree = None
        
    def generate_deal(self) -> None:
        """
            Generate the deal: Generate list of ith to jth easiest to mine Materials from inventory, and randomly choose a Material.
                               Random price.

            :param: None

            :pre: None

            :return: None

            :complexity: Best = Worst O(N * Log N + j-i*log(H)), where N is number of materials in inventory and H is the height of the tree
        """
        total_mats = len(self.inventory)
        if total_mats > 1:
            i = RandomGen.randint(0, total_mats-1) # The first number, i, is selected from 0 to the number of available materials - 1
            j = RandomGen.randint(i, total_mats-1) # The second number, j, is selected from i to the number of available materials - 1
            
            # generates a list of all materials which lie between the ith easiest to mine and the jth easiest to mine
            self.sorted_tree = self.get_sorted_tree() # O(N * log N)
            material_list = self.materials_between(i,j) # O(j-i*log(H))

            # choose a Material randomly from this list
            self.current_material = RandomGen.random_choice(material_list)
        else:
            self.current_material = self.inventory[0]
        
        # a random buy price is selected
        self.current_price = self.random_price()


    def materials_between(self, i: int, j: int) -> list[Material]:
        """
            Helper Method that returns a list containing the materials which are somewhere between the ith and jth easiest to mine, inclusive

            Since this is a helper method we will be checking if this method is called from generate_deals function
            If it is not called from generate_deals function, we will generate call function get_sorted_tree()

            :param arg1: i - the starting index 

            :param arg2: j - the ending index

            :pre: None

            :return: List which contains objects of Material

            :complexity: Best Case = O(j-i*log(H))
                         Worst Case = O(N * log N + j-i*log(H)), where N is number of materials in inventory and H is the height of the tree
        """
        # Check whether current method is called from generate_deals function if not this means it's not sorted yet
        if self.sorted_tree == None:
            self.sorted_tree = self.get_sorted_tree() # O(N * log N)
        
        materials_list = self.sorted_tree.range_between(i, j) # O(j-i*log(H))
        self.sorted_tree = None 
        return materials_list


    @classmethod
    def random_trader(cls) -> RangeTrader:
        """
            Returns a RangeTrader

            :param: None

            :pre: None

            :return: An object of RangeTrader
            
            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        random_name = RandomGen.random_choice(TRADER_NAMES)
        return RangeTrader(random_name)


class HardTrader(Trader):
    """Always gets hardest to mine material from their inventory"""

    def __init__(self, name: str) -> None:
        """
            Initialises attributes.

            :param: name - The name of the Hard Trader

            :pre: None

            :return: None

            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        Trader.__init__(self, name)
        self.sorted_tree = None

    def generate_deal(self) -> None:
        """
            Generate the deal: Get the hardest to mine Material from inventory. Random price.

            :param: None

            :pre: None

            :return: None

            :complexity: Best = Worst O(N * log N + N), where N is number of materials in inventory
        """
        self.sorted_tree = self.get_sorted_tree() # O(N * log N)
        self.current_material = self.sorted_tree.get_maximal(self.sorted_tree.root).item # O(log N)
        self.inventory.remove(self.current_material) # O(N), shuffling required
        self.current_price = self.random_price() # a random buy price is selected

    @classmethod
    def random_trader(cls) -> HardTrader:
        """
            Returns a HardTrader

            :param: None

            :pre: None

            :return: An object of HardTrader class
            
            :complexity: Best = Worst O(N), where N is the size of the inventory
        """
        random_name = RandomGen.random_choice(TRADER_NAMES)
        return HardTrader(random_name)








    






