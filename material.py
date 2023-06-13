""" 
Materials in caves are mined my players. They are also involved in trades between the player and the trader.

Materials have a name and a mining rate. Supports random generation of a material. Defines a unique material as having both a unique
name and a unique mining rate.
"""


from __future__ import annotations
from random_gen import RandomGen

# Material names taken from https://minecraft-archive.fandom.com/wiki/Items
RANDOM_MATERIAL_NAMES = [
    "Arrow",
    "Axe",
    "Bow",
    "Bucket",
    "Carrot on a Stick",
    "Clock",
    "Compass",
    "Crossbow",
    "Exploration Map",
    "Fire Charge",
    "Fishing Rod",
    "Flint and Steel",
    "Glass Bottle",
    "Dragon's Breath",
    "Hoe",
    "Lead",
    "Map",
    "Pickaxe",
    "Shears",
    "Shield",
    "Shovel",
    "Sword",
    "Saddle",
    "Spyglass",
    "Totem of Undying",
    "Blaze Powder",
    "Blaze Rod",
    "Bone",
    "Bone meal",
    "Book",
    "Book and Quill",
    "Enchanted Book",
    "Bowl",
    "Brick",
    "Clay",
    "Coal",
    "Charcoal",
    "Cocoa Beans",
    "Copper Ingot",
    "Diamond",
    "Dyes",
    "Ender Pearl",
    "Eye of Ender",
    "Feather",
    "Spider Eye",
    "Fermented Spider Eye",
    "Flint",
    "Ghast Tear",
    "Glistering Melon",
    "Glowstone Dust",
    "Gold Ingot",
    "Gold Nugget",
    "Gunpowder",
    "Ink Sac",
    "Iron Ingot",
    "Iron Nugget",
    "Lapis Lazuli",
    "Leather",
    "Magma Cream",
    "Music Disc",
    "Name Tag",
    "Nether Bricks",
    "Paper",
    "Popped Chorus Fruit",
    "Prismarine Crystal",
    "Prismarine Shard",
    "Rabbit's Foot",
    "Rabbit Hide",
    "Redstone",
    "Seeds",
    "Beetroot Seeds",
    "Nether Wart Seeds",
    "Pumpkin Seeds",
    "Wheat Seeds",
    "Slimeball",
    "Snowball",
    "Spawn Egg",
    "Stick",
    "String",
    "Wheat",
    "Netherite Ingot",
]

class Material:
    """
        Found in caves. Mined by players. Players trade them for emeralds from Traders.

        Attributes:
        * name: Used to identify the material
        * mining Rate: Specifies how many hunger points are needed to mine a single unit of the material (can be a fractional number)
        * found_in: Specifies the caves the material can be found in
        * ratio: the ratio of emeralds earned from mining it(profit) to hunger points required to mine it(cost)
    """
    
    def __init__(self, name: str, mining_rate: float) -> None:
        """
            Initialises attributes

            :param arg1: name - The name of the Material

            :param arg2: mining_rate - The mining rate of the Material

            :pre: None
            
            :return: None

            :complexity: Best=Worst O(1)
        """
        self.name = name
        self.mining_rate = mining_rate # number of hunger points needed to mine one material
        self.found_in = [] # list of caves the material can be found in
        self.ratio = None # ratio of profit to cost
    
    def __str__(self) -> str:
        """
            Returns material name and its mining rate

            :param: None

            :pre: None

            :return: String which contains the detail of the object

            :complexity: Best=Worst O(1)
        """
        return f"{self.name}: {round(self.mining_rate, 2)}🍗/💎"

    def __eq__(self, other: Material) -> bool:
        """
            Returns True if Materials are equal. Two Materials are different if and only if they have distinct names and distinct 
            mining rates.

            :param: other - An object of Material

            :pre: None

            :return: boolean returns True if Materials are equal.

            :complexity: Best=Worst O(1)
        """
        same_name = (self.name == other.name)
        same_mining_rate = (self.mining_rate == other.mining_rate) 
        return (same_name or same_mining_rate) # returns False only when both attributes are different
           

    @classmethod
    def random_material(cls) -> Material:
        """
            Generates and returns a random material

            :param: None

            :pre: None

            :return: Material object which is randomised
            
            :complexity: Best=Worst O(1)
        """
        random_name = RandomGen.random_choice(RANDOM_MATERIAL_NAMES) # gets random name from list of random names provided
        random_mining_rate = RandomGen.random_float() * RandomGen.randint(10, 20) # arbitrary generation of mining rate
        return Material(random_name, random_mining_rate)

if __name__ == "__main__":
    print(Material("Coal", 4.5))

