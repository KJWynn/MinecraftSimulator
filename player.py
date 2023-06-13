""" 
Player. Players have access to all the elements in the game. They use emeralds to purchase food to get hunger bars, visit caves to mine materials based
on the hunger points they have. Players sell the materials mined to traders in exchange for emeralds. They make the optimal choices to
maximize their emerald balance at the end of each day.

Supports random generation of a player. Duplicate players are allowed.
"""

from __future__ import annotations
from typing import List

from cave import Cave
from constants import EPSILON
from hash_table import LinearProbeTable
from material import Material
from node import AVLTreeNode
from random_gen import RandomGen
from sorted_list import ListItem
from trader import Trader, RandomTrader
from food import Food
from avl import AVLTree
from hash_table import LinearProbeTable
from array_sorted_list import ArraySortedList
from heap import *


# List taken from https://minecraft.fandom.com/wiki/Mob
PLAYER_NAMES = [
    "Steve",
    "Alex",
    "ɘᴎiɿdoɿɘH",
    "Allay",
    "Axolotl",
    "Bat",
    "Cat",
    "Chicken",
    "Cod",
    "Cow",
    "Donkey",
    "Fox",
    "Frog",
    "Glow Squid",
    "Horse",
    "Mooshroom",
    "Mule",
    "Ocelot",
    "Parrot",
    "Pig",
    "Pufferfish",
    "Rabbit",
    "Salmon",
    "Sheep",
    "Skeleton Horse",
    "Snow Golem",
    "Squid",
    "Strider",
    "Tadpole",
    "Tropical Fish",
    "Turtle",
    "Villager",
    "Wandering Trader",
    "Bee",
    "Cave Spider",
    "Dolphin",
    "Enderman",
    "Goat",
    "Iron Golem",
    "Llama",
    "Panda",
    "Piglin",
    "Polar Bear",
    "Spider",
    "Trader Llama",
    "Wolf",
    "Zombified Piglin",
    "Blaze",
    "Chicken Jockey",
    "Creeper",
    "Drowned",
    "Elder Guardian",
    "Endermite",
    "Evoker",
    "Ghast",
    "Guardian",
    "Hoglin",
    "Husk",
    "Magma Cube",
    "Phantom",
    "Piglin Brute",
    "Pillager",
    "Ravager",
    "Shulker",
    "Silverfish",
    "Skeleton",
    "Skeleton Horseman",
    "Slime",
    "Spider Jockey",
    "Stray",
    "Vex",
    "Vindicator",
    "Warden",
    "Witch",
    "Wither Skeleton",
    "Zoglin",
    "Zombie",
    "Zombie Villager",
    "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
]

class Player():
    """
        Has access to the materials, caves, and traders. Players buy food, mine from caves, and sell materials to traders in 
        exchange of emeralds.
    
        Attributes:
        * name: Player's name
        * balance: Emeralds the player has
        * hunger_points: Required for player to mine materials.
        * traders_list: The traders the player sells materials to in exchange for emeralds.
        * foods_list: Choices of food offered to player to buy.
        * materials_list: The materials from the caves that can be mined by the player.
        * caves_list: The caves the player can visit to mine materials.
    """

    # Constants for random generation of player's starting emeralds
    DEFAULT_EMERALDS = 50

    MIN_EMERALDS = 14
    MAX_EMERALDS = 40

    def __init__(self, name, emeralds=None) -> None:
        """
            Initialises attributes.
            
            :param arg1: name - the name of the player

            :param arg2: emeralds - the number of emralds the player has (default = None)

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.name = name
        self.balance = self.DEFAULT_EMERALDS if emeralds is None else emeralds
        self.hunger_points = 0
        self.traders_list = []
        self.foods_list = []
        self.materials_list = []
        self.caves_list = []

    def set_traders(self, traders_list: list[Trader]) -> None:
        """
            Gives player access to traders

            :param: the list of object Trader

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.traders_list = traders_list

    def set_foods(self, foods_list: list[Food]) -> None:
        """
            Gives player access to foods

            :param: A list of Food object

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.foods_list = foods_list

    @classmethod
    def random_player(self) -> Player:
        """
            Generates and returns a random player

            :param: None

            :pre: None

            :return: An object of Player 
            
            :complexity: Best/Worst O(1)
        """
        random_name = RandomGen.random_choice(PLAYER_NAMES)
        random_emeralds = RandomGen.randint(self.MIN_EMERALDS, self.MAX_EMERALDS)
        return Player(random_name, random_emeralds)

    def set_materials(self, materials_list: list[Material]) -> None:
        """
            Gives player access to materials

            :param: A list of Material object

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.materials_list = materials_list

    def set_caves(self, caves_list: list[Cave]) -> None:
        """
            Gives player access to caves

            :param: A list of Cave object

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.caves_list = caves_list

    def get_materials (self) -> List:
        """
            Returns the list of materials.

            :param: None

            :pre: None

            :return: A list of Material object

            :complexity: Best/Worst O(1)
        """
        return self.materials_list

    def select_food_and_caves(self) -> tuple[Food | None, float, list[tuple[Cave, float]]]:
            """
                The choices the player make to achieve the highest balance of emeralds possible in a single day

                Setups:
                * For each unique material to be mined, keep track of its quantity and the caves it can be found in.
                Approach: LinearProbeTable with material name as key and value is tuple of (total_minable_quantity, Material)

                * Get best selling prices
                Approach: LinearProbeTable(key = material_name, value = Trader)
                Loop through the generated traders, map their current deal's material name to the trader instance. If a trader offers 
                same material but with higher selling price, update the trader instance in the hash table.

                Simulate for each food type bought:
                If player cannot afford food, do nothing. Otherwise, simulate buying food, decreasing emerald balance and increasing hunger bars.
                    * For each material, compute the ratio (profit obtained by mining  / hunger_points needed to mine) where the quantity 
                    is total_minable_quantity(from the available caves)
                    * Store these ratios in MaxHeap. Use LinearProbeTable to map these ratios to the material name.
                    * While player still has hunger points, visit as many caves as possible. If all caves visited, exit loop early
                        Get max ratio using get_max() from ratio_heap. 
                        Search for material name based on ratio. 
                        Search for Material based on material name
                        Get cave(s) to be visited based on Material.found_in
                        Mine from those caves 
                    * if balance < original balance, Player does nothing. Else mine accordingly

                :param: None

                :pre: None

                :return: tuple - (the food which the player will buy, the emerald latest balance, A list of caves that player visits)

                :complexity: Best = Worst = O(C + T + F + [FM + F(log C)] ),
                             where M, T, F and C represent the number of materials, traders, foods and caves respectively.
            """
            # materials_table has material name as key and the data is a [tuple[quantity, Material]], where quantity is how much of it
            # can be mined from all the caves containing it, and material is the material
            materials_table = LinearProbeTable(len(self.materials_list), -1)
            for current_cave in self.caves_list: #! O(C)
                if current_cave.material.name not in materials_table:
                    materials_table.insert(current_cave.material.name, (current_cave.quantity, Material(current_cave.material.name, current_cave.material.mining_rate)))
                else:
                    # if there is an existing cave in the table with the same material, update the quantity and the caves
                    existing_quantity = materials_table[current_cave.material.name][0] # get existing quantity of material from table
                    existing_material = materials_table[current_cave.material.name][1]
                    materials_table.insert(current_cave.material.name, (existing_quantity + current_cave.quantity, existing_material )) # update by adding current quantity to existing quantity
                materials_table[current_cave.material.name][1].found_in.append(current_cave) # add cave to found_in

            # Setup the potential selling prices. Players only find traders who are willing to buy the mined materials.
            trader_deals = LinearProbeTable(len(self.traders_list), -1) # hash table with current material as key and trader as data
            for trader in self.traders_list: #! O(T)
                material = trader.current_material.name # get trader's current material name as key
                if material in trader_deals: # if there is an existing trader in the table selling the same material
                    price = trader_deals[material].current_price # get the existing trader's price

                    # if current trader's price is higher than in the table, replace existing trader with current trader
                    if trader.current_price > price:
                        trader_deals.insert(material, trader)
                else:
                    trader_deals.insert(material, trader) # otherwise it is a new insert


            # repeat for each food type bought
            caves_for_each_food = []
            for food in self.foods_list: #! O(F)
                visited_caves = []
                balance = self.balance         # emeralds
                if balance >= food.price:       # only enter if can purchase food
                    balance -= food.price
                    # print(f"{food.name} BOUGHT. Current emeralds: {self.balance} - {food.price} = {balance}")
                    hunger_points = food.hunger_bars
                else:
                    # print("Player cannot buy food and has no hunger points to mine anything")
                    return (None, self.balance, [])
                    # break

                # get ratios for each material and put into MaxHeap
                ratios_heap = MaxHeap(len(materials_table)) #! O(M), M <= C
                if len(materials_table) < 3:
                    material_dict = LinearProbeTable(3)
                else:
                    material_dict = LinearProbeTable(len(materials_table))
                for material_name in materials_table.keys(): # for each material that can be mined from caves
                    try:
                        trader = trader_deals[material_name]
                    except KeyError:
                        print("This material is not part of trader's deals and should not be mined")
                    else:
                        material = materials_table[material_name][1]
                        quantity = materials_table[material_name][0]
                        # cost
                        mining_rate = material.mining_rate
                        hunger_points_required = quantity * mining_rate
                        # profit
                        selling_price = trader_deals[material_name].current_price
                        profit = quantity * selling_price
                        # assign ratio
                        material.ratio = profit / hunger_points_required
                        ratios_heap.add(material.ratio) # O(log M)
                        material_dict[str(material.ratio)] = material_name # map the ratio to the material name ,O(1) for hash table
 
                # The sum of the iterations in the for loop will equal O(C)
                while hunger_points > 0 and ratios_heap.length > 0: # will visit as many caves as possible until hunger points depleted 
                    max_ratio = ratios_heap.get_max() #! O(log C) 
                    mat_name = material_dict[str(max_ratio)]
                    mat_chosen = materials_table[mat_name] # tuple of (quantity, Material)

                    for cave in mat_chosen[1].found_in: 
                        mining_rate = mat_chosen[1].mining_rate
                        price = trader_deals[mat_name].current_price
                        potential_cost = cave.quantity * mining_rate
                        potential_profit = cave.quantity * price

                        if hunger_points >= potential_cost:
                            balance += potential_profit
                            hunger_points -= potential_cost
                            # print("mining all:")
                            # print(f"Player visited {cave.name} and mined {cave.quantity} {cave.material}, getting {potential_profit}" +\
                            #     f" with total profit of {balance} and now has {hunger_points} hunger points left")
                            cave.is_visited = True
                            visited_caves.append((cave, cave.quantity))
                        else:
                            minable_quantity = hunger_points / mining_rate
                            profit = minable_quantity * price
                            balance += profit
                            hunger_points = 0
                            cave.is_visited = True
                            # print(f"Player visited {cave.name} and mined {cave.quantity} {cave.material}, getting {profit}" +\
                            # f" with total profit of {balance} and now has {hunger_points} hunger points left")
                            visited_caves.append((cave, minable_quantity))
                            break
                
                # after visiting the caves check if it was better to not visit any caves at all
                if balance < self.balance:
                    food = None
                    balance = self.balance
                    for cave, quantity in visited_caves:
                        cave.is_visited = False
                    visited_caves = []

                caves_for_each_food.append((food, visited_caves, balance))

            max_balance = 0
            max_idx = 0
            for i in range(len(caves_for_each_food)): #! O(F)
                if caves_for_each_food[i][2] > max_balance:
                    max_idx = i
                    max_balance = caves_for_each_food[i][2]
            best_choice = caves_for_each_food[max_idx] # (food, visited_caves, balance)
            best_food = best_choice[0]
            best_journey = best_choice[1] # list of traversed caves
            best_balance = best_choice[2]

            return (best_food, best_balance, best_journey)


    def __str__(self) -> str:
        """
            Returns string representation of the player which includes player name, emerald balance and hunger points.
        
            :complexity: Best/Worst O(1)
        """
        return f"{self.name} has {self.balance}💰 and {self.hunger_points}🍗"

if __name__ == "__main__":
    print(Player("Steve"))
    print(Player("Alex", emeralds=1000))

    # RandomGen.set_seed(16)
    
    # gold = Material("Gold Nugget", 27.24)
    # netherite = Material("Netherite Ingot", 20.95)
    # fishing_rod = Material("Fishing Rod", 26.93)
    # ender_pearl = Material("Ender Pearl", 13.91)
    # prismarine = Material("Prismarine Crystal", 11.48)

    # materials = [
    #     gold,
    #     netherite,
    #     fishing_rod,
    #     ender_pearl,
    #     prismarine,
    # ]

    # caves = [
    #     Cave("Boulderfall Cave", prismarine, 10),
    #     Cave("Castle Karstaag Ruins", netherite, 4),
    #     Cave("Glacial Cave", gold, 3),
    #     Cave("Orotheim", fishing_rod, 6),
    #     Cave("Red Eagle Redoubt", fishing_rod, 3),
    # ]


    # # waldo = RandomTrader("Waldo Morgan")
    # # waldo.add_material(fishing_rod)     # Now selling for 7.57
    # # orson = RandomTrader("Orson Hoover")
    # # orson.add_material(gold)            # Now selling for 4.87
    # # lea = RandomTrader("Lea Carpenter")
    # # lea.add_material(prismarine)        # Now selling for 5.65
    # # ruby = RandomTrader("Ruby Goodman")
    # # ruby.add_material(netherite)        # Now selling for 8.54
    # # mable = RandomTrader("Mable Hodge")
    # # mable.add_material(gold)            # Now selling for 6.7

    # # traders = [
    # #     waldo,
    # #     orson,
    # #     lea,
    # #     ruby,
    # #     mable,
    # # ]

    # # for trader in traders:
    # #     trader.generate_deal()

    # # Test the worked example given in spec sheet
    # waldo = RandomTrader("Waldo Morgan")
    # waldo.current_material = fishing_rod
    # waldo.current_price = 7.44
    # orson = RandomTrader("Orson Hoover")
    # orson.current_material = gold           
    # orson.current_price = 7.7
    # lea = RandomTrader("Lea Carpenter")
    # lea.current_material =prismarine     
    # lea.current_price = 7.63
    # ruby = RandomTrader("Ruby Goodman")
    # ruby.current_material = netherite     
    # ruby.current_price = 9.78
    # mable = RandomTrader("Mable Hodge")
    # mable.current_material = gold       
    # mable.current_price = 5.48
    
    # traders = [
    #     waldo,
    #     orson,
    #     lea,
    #     ruby,
    #     mable,
    # ]
        

    # g = game.SoloGame()
    # g.initialise_with_data(materials, caves, traders, ["Jackson"], [50])

    # # Avoid simulate_day - This regenerates trader deals and foods.
    # foods = [
    #     Food("Cabbage Seeds", 106, 30),
    #     Food("Fried Rice", 129, 24),
    #     Food("Cooked Chicken Cuts", 424, 19),
    # ]

    # g.player.set_foods(foods)
    # food, balance, caves = g.player.select_food_and_caves()

    # RandomGen.set_seed(16)
        
    # gold = Material("Gold Nugget", 27.24)
    # netherite = Material("Netherite Ingot", 20.95)
    # fishing_rod = Material("Fishing Rod", 26.93)
    # ender_pearl = Material("Ender Pearl", 13.91)
    # prismarine = Material("Prismarine Crystal", 11.48)

    # materials = [
    #     gold,
    #     netherite,
    #     fishing_rod,
    #     ender_pearl,
    #     prismarine,
    # ]

    # caves = [
    #     Cave("Boulderfall Cave", prismarine, 10),
    #     Cave("Castle Karstaag Ruins", netherite, 4),
    #     Cave("Glacial Cave", gold, 3),
    #     Cave("Orotheim", fishing_rod, 6),
    #     Cave("Red Eagle Redoubt", fishing_rod, 3),
    # ]

    # waldo = RandomTrader("Waldo Morgan")
    # waldo.add_material(fishing_rod)     # Now selling for 7.57
    # orson = RandomTrader("Orson Hoover")
    # orson.add_material(gold)            # Now selling for 4.87
    # lea = RandomTrader("Lea Carpenter")
    # lea.add_material(prismarine)        # Now selling for 5.65
    # ruby = RandomTrader("Ruby Goodman")
    # ruby.add_material(netherite)        # Now selling for 8.54
    # mable = RandomTrader("Mable Hodge")
    # mable.add_material(gold)            # Now selling for 6.7
    
    # traders = [
    #     waldo,
    #     orson,
    #     lea,
    #     ruby,
    #     mable,
    # ]
    
    # for trader in traders:
    #     trader.generate_deal()

    # for trader in traders:
    #     trader.generate_deal()

    # waldo.current_material = materials[4]
    # waldo.current_price = 100
    # print(waldo.current_material)
    # print(waldo.current_price)
    # foods = [
    #     Food("Cabbage Seeds", 106, 30),
    #     Food("Fried Rice", 129, 24),
    #     Food("Cooked Chicken Cuts", 424, 19),
    # ]

    
    # p1 = Player("yes")
    # p1.set_traders(traders)
    # p1.set_caves(caves)
    # p1.set_foods(foods)
    # p1.set_materials(materials)
    # p1.select_food_and_caves()


    # Test the worked example given in spec sheet
    # waldo = RandomTrader("Waldo Morgan")
    # waldo.current_material = fishing_rod
    # waldo.current_price = 7.44
    # orson = RandomTrader("Orson Hoover")
    # orson.current_material = gold           
    # orson.current_price = 7.7
    # lea = RandomTrader("Lea Carpenter")
    # lea.current_material =prismarine     
    # lea.current_price = 7.63
    # ruby = RandomTrader("Ruby Goodman")
    # ruby.current_material = netherite     
    # ruby.current_price = 9.78
    # mable = RandomTrader("Mable Hodge")
    # mable.current_material = gold       
    # mable.current_price = 5.48
    
    # traders = [
    #     waldo,
    #     orson,
    #     lea,
    #     ruby,
    #     mable,
    # ]
        

    # g = game.SoloGame()
    # g.initialise_with_data(materials, caves, traders, ["Jackson"], [50])

    # # Avoid simulate_day - This regenerates trader deals and foods.
    # foods = [
    #     Food("Cabbage Seeds", 106, 30),
    #     Food("Fried Rice", 129, 24),
    #     Food("Cooked Chicken Cuts", 424, 19),
    # ]

    # g.player.set_foods(foods)
    # food, balance, caves = g.player.select_food_and_caves()


    # assert balance >= (185.01974749350165 - pow(10, -4))

    # RandomGen.set_seed(1234)
    # g = game.SoloGame()
    # g.initialise_game()
    # # Spend some time in minecraft
    # # Note that this will crash if you generate a HardTrader with less than 3 materials.
    # for _ in range(3):
    #     g.simulate_day()
    #     g.finish_day()
    # g.player.set_foods(foods)
    # food, balance, caves = g.player.select_food_and_caves()
    # g.verify_output_and_update_quantities(food, balance, caves)
    # print([(cave.name,mined) for (cave,mined) in caves])
