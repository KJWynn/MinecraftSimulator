""" 
Implements the general Game class as well as the two specific game modes SoloGame and MultiplayerGame. The game starts with initialization
of game elements(materials, caves, traders) then the player(s). Then each day is simulated, with traders generating a deal, players selecting 
food to buy and caves to visit and trading with the traders. At the end of the day, the caves' quantities of materials are updated. 

For multiplayer mode, players can only purchase the single offered food (if possible) and can only mine from one cave.
"""

from __future__ import annotations
from genericpath import samefile
from heap import MaxHeap

from player import Player
from trader import *
from material import Material
from cave import Cave
from food import Food
from random_gen import RandomGen
from aset import ASet
from hash_table import LinearProbeTable
from player import Player
from avl import AVLTree

from constants import EPSILON
from avl import AVLTree
from hash_table import LinearProbeTable

class Game:
    """
        Initializes the game objects that the player interacts with. These can either be randomly generated or manually set.

        Attributes:
        * materials: Once generated, used for generating traders and caves.
        * caves: The caves available for the player to visit. Determines the materials the player can mine.
        * traders: Players trade the mined materials for emeralds with them.
    
    """
    # Constants for random generation
    MIN_MATERIALS = 5
    MAX_MATERIALS = 10

    MIN_CAVES = 5
    MAX_CAVES = 10

    MIN_TRADERS = 4
    MAX_TRADERS = 8

    MIN_FOOD = 2
    MAX_FOOD = 5

    def __init__(self) -> None:
        """
            Initialises attributes.
            
            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.materials = []
        self.caves = []
        self.traders = []
        self.trader_deals = None

    def initialise_game(self) -> None:
        """
            Initialise all game objects: Materials, Caves, Traders randomly.
            
            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(A), where A is the largest value among M, C and T, which are the number of materials, caves and traders respectively.
        """
        N_MATERIALS = RandomGen.randint(self.MIN_MATERIALS, self.MAX_MATERIALS)
        self.generate_random_materials(N_MATERIALS)
        # print("Materials:\n\t", end="")
        # print("\n\t".join(map(str, self.get_materials()))) # O(M), where M is number of materials
        N_CAVES = RandomGen.randint(self.MIN_CAVES, self.MAX_CAVES)
        self.generate_random_caves(N_CAVES)
        # print("Caves:\n\t", end="")
        # print("\n\t".join(map(str, self.get_caves()))) # O(C), where C is number of caves
        N_TRADERS = RandomGen.randint(self.MIN_TRADERS, self.MAX_TRADERS)
        self.generate_random_traders(N_TRADERS)
        # print("Traders:\n\t", end="")
        # print("\n\t".join(map(str, self.get_traders()))) # O(T), where T is number of traders

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader]) -> None:
        """
            Manually initialise game objects with arguments given.
                        
            :param arg1: materials - A list of Material objects

            :param arg2: caves - A list of Cave objects

            :param arg3: traders - A list of Trader objects

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        self.set_materials(materials)
        self.set_caves(caves)
        self.set_traders(traders)

    def set_materials(self, mats: list[Material]) -> None:
        """
            Sets the materials for Trader and Cave generation.
                                    
            :param: materials - A list of Material objects

            :pre: None

            :return: None
        
            :complexity: Best/Worst O(1)
        """
        self.materials = mats

    def set_caves(self, caves: list[Cave]) -> None:
        """
            Sets the caves.
                                    
            :param: caves - A list of Cave objects

            :pre: None

            :return: None
        
            :complexity: Best/Worst O(1)
        """
        self.caves = caves

    def set_traders(self, traders: list[Trader]) -> None:
        """
            Sets the traders
                                                
            :param: traders - A list of Trader objects

            :pre: None

            :return: None
        
            :complexity: Best/Worst O(1)
        """
        self.traders = traders

    def get_materials(self) -> list[Material]:
        """
            Returns the generated materials        

            :param: None

            :pre: None

            :return: list - A list of Material objects

            :complexity: Best/Worst O(1)        
        """
        return self.materials

    def get_caves(self) -> list[Cave]:
        """
            Returns the generated caves

            :param: None

            :pre: None

            :return: list - A list of Cave objects

            :complexity: Best/Worst O(1)        
        """
        return self.caves

    def get_traders(self) -> list[Trader]:
        """
            Returns the generated traders

            :param: None

            :pre: None

            :return: list - A list of Trader objects

            :complexity: Best/Worst O(1)        
        """
        return self.traders

    def generate_random_materials(self, amount) -> None:
        """
            Generates <amount> random materials using Material.random_material
            Generated materials must all have different names and different mining_rates. (Defined in __eq__ of Material)
            (You may have to call Material.random_material more than <amount> times.)

            :param: amount - the amount of materials I wish to ramdonly generate

            :pre: None

            :return: None

            :complexity: Best O(N^2), where N is the amount of Materialto be randomly generated
                         Worst O(infinity), when set of unique objects never becomes full
        """
        self.generate_random(Material, amount)

    def generate_random_caves(self, amount) -> None:
        """
            Generates <amount> random caves using Cave.random_cave
            Generated caves must all have different names. (Defined in __eq__ of Cave)
            (You may have to call Cave.random_cave more than <amount> times.)

            :param: amount - the amount of caves I wish to ramdonly generate

            :pre: Assumes <Game>.self.materials is not empty, i.e. <Game>.generate_random_materials() has been called

            :return: None

            :complexity: Best O(N^2), where N is the amount of Cave to be randomly generated
                         Worst O(infinity), when set of unique objects never becomes full
        """
        self.generate_random(Cave, amount)

    def generate_random_traders(self, amount) -> None:
        """
            Generates <amount> random traders by selecting a random trader class
            and then calling <TraderClass>.random_trader()
            and then calling set_all_materials with some subset of the already generated materials.
            Generated traders must all have different names
            (You may have to call <TraderClass>.random_trader() more than <amount> times.)
            
            :param: amount - the amount of traders I wish to ramdonly generate

            :pre: Assumes <Game>.self.materials is not empty, i.e. <Game>.generate_random_materials() has been called

            :return: None

            :complexity: Best O(N^A), where N is the amount of Trader to be randomly generated, A is the larger value between N and M, 
                         where M is the number of materials
                         Worst O(infinity), when set of unique objects never becomes full
        """
        self.generate_random(Trader, amount) # generates the traders first, O(N^2)
        
        # Give each trader randomized inventory
        materials = self.get_materials()
        for trader in self.traders: # O(N), where N is the number of traders
        
            # Get random_subset: shuffle materials, then get its ith to jth materials inclusive
            RandomGen.random_shuffle(materials) # O(M), where M is the number of materials
            i = RandomGen.randint(1, len(materials)-1)
            j = RandomGen.randint(i, len(materials)-1)
            random_subset = materials[i:j+1]
            trader.set_all_materials(random_subset)

    def generate_random(self, elem_type: Material | Cave | Trader, amount: int) -> None:
        """
            Generates <amount> materials or caves or traders depending on the <elem_type> argument. Sets these attributes for the Game instance.
        
            :param arg1: elem_type - the type of objec I wish to generate

            :param arg2: amount - the amount I wish to generate

            :pre: None

            :return: None

            :complexity: Best O(N^2), where N is the amount of either Material or Cave or Trader to be randomly generated
                         Worst O(infinity), when set of unique objects never becomes full
        """
      
        hash_table = LinearProbeTable(amount, amount) 
        rand_elem = None
        temp = [] # to store generated objects 

        # Select appropriate random callable to generate material/cave/trader and the correspondng setter
        if elem_type == Material:
            mining_rate_tracker = []
            rand_elem = lambda: Material.random_material() # callable which returns a material
           
            # Fill the set with <amount> elements by calling rand_elem. May need to call more than <amount> times
            # Best case if <amount>, N = 4: O(1) + O(N-3) + O(N-2) + O(N-1) + O(N) --> O(N^2)
            while len(hash_table) < amount: # Best case executes <amount> times, worst case executes infinite times(unlikely)
                material = rand_elem()
                if material.name not in hash_table and material.mining_rate not in mining_rate_tracker:
                    hash_table.insert(material.name, material) # Best O(1), Worst O(N), where N is the number of elements currently in the set
                    mining_rate_tracker.append(material.mining_rate)
                
            # Set materials, O(<amount>)
            for i in range(len(hash_table.table)):
                if hash_table.table[i] != None:
                    temp.append(hash_table.table[i][1])
            self.set_materials(temp)
        
        elif elem_type == Cave:
            rand_elem = lambda: Cave.random_cave(self.materials) # callable which returns a cave
            
            # Fill the set with <amount> elements by calling rand_elem. May need to call more than <amount> times
            while len(hash_table) < amount: # Best case executes <amount> times, worst case executes infinite times(unlikely)
                cave = rand_elem()
                if cave.name not in hash_table:
                    hash_table.insert(cave.name, cave)
            
            # Set caves, O(<amount>)
            for i in range(len(hash_table.table)):
                if hash_table.table[i] != None:
                    temp.append(hash_table.table[i][1])
            self.set_caves(temp)
        
        elif elem_type == Trader:
            while len(hash_table) < amount: # Best case executes <amount> times, worst case executes infinite times(unlikely)
                rand_name = Trader.random_trader().name # Select random name
                rand_type = RandomGen.random_choice([RandomTrader, RangeTrader, HardTrader]) # Select trader type
                trader = rand_type(rand_name) # callable which returns a trader, O(M), where M is the size of the inventory
                if trader.name not in hash_table:
                    hash_table.insert(trader.name, trader)
            
            # Set traders, O(<amount>)
            for i in range(len(hash_table.table)):
                if hash_table.table[i] != None:
                    # print(hash_table.table[i])
                    temp.append(hash_table.table[i][1])
            self.set_traders(temp)

        
    def finish_day(self) -> None:
        """
            DO NOT CHANGE
            Affects test results.
            Either remove or add materials to each cave at the end of each day, then round off the quantity to two decimal places
            
            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(N), where N is the number of caves
        """
        for cave in self.get_caves():
            if cave.quantity > 0 and RandomGen.random_chance(0.2): # Chance to remove some quantity if there is still some material left
                cave.remove_quantity(RandomGen.random_float() * cave.quantity)
            else: # Add some quantity if the cave's material is depleted
                cave.add_quantity(round(RandomGen.random_float() * 10, 2))
            cave.quantity = round(cave.quantity, 2)

    def generate_trader_deals_table(self) -> None:
        """
            Setup the trader deals for the day, updates material with higher traded price if material already exist in the hash table.
            
            :param: None

            :pre: None

            :return: None
            
            :complexity: Best/Worst O(T), where T is the number of traders
        """
        # setup trader_deals(best prices) for the day
        self.trader_deals = LinearProbeTable(len(self.traders), -1) # hash table with current material as key and trader as data
        for trader in self.traders: # O(T)
            material = trader.current_material.name # get current trader's material name as key
            if material in self.trader_deals: # if there is an existing trader in the table selling the same material, O(1) search
                price = self.trader_deals[material].current_price # get the existing trader's price, O(1) access

                # if current trader's price is higher than in the table, replace existing trader with current trader
                if trader.current_price > price:
                    self.trader_deals.insert(material, trader) # Assumed O(1)
            else:
                self.trader_deals.insert(material, trader) # otherwise it is a new insert, assumed O(1)

class SoloGame(Game):
    """
        Single player implementation of Game class which adds a player who has access and interaction with game objects day by day.
        Player can be initialized randomly or manually.

        Attributes:
        * Inherits from Game class
        * player: Player instance
    """

    def initialise_game(self) -> None:
        """
            Initialise all game objects: Materials, Caves, Traders, Player randomly.

            :param: None

            :pre: None

            :return: None
        
            :complexity: O(A), where A is the largest value among M, C and T, which are the number of materials, caves and traders respectively.
        """
        super().initialise_game()
        self.player = Player.random_player()
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]) -> None:
        """
            Manually initializes attributes.
                        
            :param arg1: materials - A list of Material objects

            :param arg2: caves - A list of Cave objects

            :param arg3: traders - A list of Trader objects

            :param arg4: player_names - A list of String (players' name)

            :param arg5: emerald_info - A list of floating number

            :pre: None

            :return: None

            :complexity: Best/Worst O(1)
        """
        super().initialise_with_data(materials, caves, traders)
        self.player = Player(player_names[0], emeralds=emerald_info[0])
        self.player.set_materials(self.get_materials())
        self.player.set_caves(self.get_caves())
        self.player.set_traders(self.get_traders())

    def simulate_day(self) -> None:
        """
            Simulates a day with the sequence of
            1. Traders each generating a deal
            2. Generate foods offered to player
            3. Player select a food to purchase.
            4. Player visits caves to mine materials then sells the materials to the Trader
            5. Cave quantities updated.
            5. Cave quantities are added/removed.

            :param: None

            :pre: None

            :return: None

            :complexity: Best/Worst O(C+T+F+[FM + F(log C)]), where M, T, F and C represent the number of traders, foods and caves respectively.
        """
        # reset hunger point to 0 for player every day
        self.player.hunger_points = 0

        # 1. Traders make deals
        # Best O(T) if all are RandomTraders, Worst O(T * N (CompK * N)) if all are Range/HardTraders
        for trader in self.get_traders(): # O(T)
            trader.generate_deal() # Best O(1) if RandomTrader, Worst O(N (CompK * N) if Range/HardTrader
        # print("Traders Deals:\n\t", end="")
        # print("\n\t".join(map(str, self.get_traders())))

        # 2. Food is offered
        food_num = RandomGen.randint(self.MIN_FOOD, self.MAX_FOOD) # number of foods
        foods = []
        for _ in range(food_num): # O(F), where F is number of foods
            foods.append(Food.random_food())
        # print("\nFoods:\n\t", end="")
        # print("\n\t".join(map(str, foods)))
        self.player.set_foods(foods)
        
        # 3. Select one food item to purchase
        food, balance, caves = self.player.select_food_and_caves()
        # print(f"selected food and cave : {food}, {balance}, {caves}")
        
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(food, balance, caves)

    def verify_output_and_update_quantities(self, food: Food | None, balance: float, caves: list[tuple[Cave, float]]) -> None:
        """
        Checks inputs:
        a. Caves must be from game initialization, the mined quantities cannot exceed the cave's quantity
        b. Checks that the caves visited are profitable, i.e. have materials that can be sold to traders
        c. Checks that balances are either more than or equal to player's original balances
        d. Check no caves visited, no hunger points and unchanged balance for player if food is not purchased
        e. Check player able to purchase food selected, and only purchase food that are generated during game initialization.
        
        Check player's initial stats(at start of each day):
        a. Hunger points must be zero
        b. Player's emerald balance must be more than zero

        Check player's choices:
        a. Check caves visited yields maximum profit
        b. Check that maximum number of materials are mined for available player hunger
        c. Ensure balance is correct for quantities mined and traded

        Sets caves for the next day. Updates the quantities for players and visited caves. Then sets caves for the next day.

        :param arg1: food (default = None)

        :param arg2: balance - the balance of the player

        :param arg3: cave - A list with tuple(Cave, mine_quantity)
            
        :pre:
        * food is Food object or None type
        * balance is float
        * caves is list object, length of list does not exceed caves generated that day
        * for caves that are not empty, should contain tuple of length 2: (Cave visited (Cave),quantity of material mined (float))

        :return: None

        :complexity: Best/Worst O(C+F+T+[FM + F(log C)]), where M, T, F and C represent the number of traders, foods and caves respectively.

        """
        # check precondition O(C), C is number of caves generated
        try:
            assert food is None or isinstance(food,Food), "Food should be food object or None"
            assert balance is not None and isinstance(balance, float) or isinstance(balance, int), "Balance should be float object"
            assert caves is not None and isinstance(caves,list), "Caves should be list object"
            assert len(caves) == 0 or len(caves) <= len(self.player.caves_list), "Caves list should not exceed length of caves generated"
            if len(caves) > 0:
                assert all(isinstance(details,tuple) and len(details)==2 for details in caves), "Caves list should contain tuple of length 2 (cave, mined quantity)"
                assert all(isinstance(cave, Cave) and (isinstance(mined,float) or isinstance(mined,int)) for cave, mined in caves),\
                    "Caves list should only contain Cave and float object that does not exceed number of caves generated or is an empty list"
        except AssertionError as e:
            raise ValueError(e)

        # setup the trader deals hash table for the day O(T)
        self.generate_trader_deals_table()
        traded_deals = self.trader_deals
        
        # check quantities provided O(C), C is number of caves generated, T is number of traders generated
        try:
            # check all caves visited are generated caves
            assert all(cave in self.get_caves() for (cave,mined) in caves),"Caves visited are invalid, not generated by game"
            # check all mined quantities does not exceed the valid caves quantity
            assert all(mined-EPSILON < cave.get_quantity() for (cave, mined) in caves),"Invalid quantity of mined materials for Cave visited"
            # check all mined materials are bought by traders
            assert all(cave.material.name in traded_deals for (cave,mined) in caves),f"Materials that are not traded are mined."

            player_bal, player_hunger = self.player.balance, self.player.hunger_points
            # check initial player balance and hunger points
            assert player_bal > EPSILON and player_hunger == 0,f"Invalid initial player balance {player_bal} and hunger points {player_hunger}"
            # check balance provided gives profit or remain unchanged
            assert balance > player_bal - EPSILON, f"Selection must ensure no losses. Balance {balance}, Before move {player_bal}"

        except AssertionError as e:
            raise Exception(e)
   

        # get boolean value for if there is any purchasable food O(F), F is number of food generated
        try:
            purchasable_food = any(food.price < player_bal - EPSILON for food in self.player.foods_list)
        except AttributeError:
            purchasable_food = False

        # check checks relevant to food O(F), F is number of food generated
        try:
            # check when no food selected O(1), assuming that we ignore comparison complexities
            if food is None:
                # check player balance unchanged for no purchase made
                assert balance == player_bal, f"Balance {player_bal} should remain unchanged for no food purchased: {balance}"
                # check no hunger points for no food
                assert player_hunger == 0, "Player should have no hunger points for no purchase of food"
                # check no caves visited for no food
                assert len(caves) == 0, "No caves should be visited for no purchase of food"

            # check when food is selected O(F), where F is number of food generated
            else:
                assert purchasable_food, "Player could not purchase any food generated"
                # check food purchased is generated by game
                assert food in self.player.foods_list, "Food purchased should be generated by game"
                # check player can purchase food selected
                assert food.price < player_bal - EPSILON, f"Food price {food.price} exceeded player balance {player_bal}"

        except AssertionError as e:
            raise Exception(e)

        # check maximum profit is generated O(C + T + F + [FM + F(log C)] )
        best_food, best_bal, best_journey = self.player.select_food_and_caves()
        assert best_food == food, f"Best food should be {best_food}, but {food} purchased"
        assert best_journey == caves, f"Best caves to yield max profit are not visited"
        assert best_bal == balance, f"Best balance is {best_bal}, but {balance} obtained"


        # check remaining balance and hunger points O(C), C is number of caves generated
        try:
            if not food is None:
                # setup temporary player hunger as hunger obtained from food bought
                player_hunger += food.hunger_bars
                # decrease emerald balance as a result of buying food
                player_bal -= food.price

                # player travel caves O(C), C is number of caves generated
                for (cave, mined) in caves:
                    # get best deal for current cave material
                    traded_price = self.trader_deals[cave.material.name].current_price
                    # increase balance based on materials mined and traded
                    player_bal += mined * traded_price
                    # deplete player hunger based on materials mined
                    player_hunger -= cave.material.mining_rate * mined

                # ensure remaining hunger points cant mine any more materials O(C), number of caves generated
                if player_hunger > 0:
                    assert not any((cave.material.mining_rate*cave.quantity)//player_hunger > 0 for cave in self.caves if not cave.is_visited), f"More materials can be mined with hunger points {player_hunger}"

            # ensure remaining balance is correct
            assert player_bal == balance, f"Balance of {player_bal} does not match {balance}"
        
        except AssertionError as e:
            raise Exception(e)       

        # prepare caves for next day O(C), C is number of caves generated
        remaining_caves = []
        for i in range(len(self.caves)):
            generated_cave = self.caves[i]
            if generated_cave.is_visited:
                # if the cave was visited, then insert the cave with its updated quantity(could be zero)
                for j in range(len(caves)):
                    if caves[j] is not None and generated_cave.name == caves[j][0].name:
                        assert caves[j][1] <= caves[j][0].quantity, f"Mined quantity {caves[j][1]} must not exceed existing quantity {caves[j][0].quantity}"
                        caves[j][0].quantity -= caves[j][1]
                        remaining_caves.append(caves[j][0]) # caves[i] is the tuple of (cave, mined_quantity), caves[i][0] is the cave with updated quantity
                        break
            else:
                remaining_caves.append(generated_cave)

        # update the attributes of players after it has passed all tests 
        self.player.hunger_points = player_hunger
        self.player.balance = balance
        self.player.food = food
        self.player.set_caves(remaining_caves)

class MultiplayerGame(Game):
    """
        Similar to the Solo Game, with some key differences:
        ● Only 1 food is offered per day - everyone can either buy this or not go mining at all.
        ● Each player can only visit one cave per day
        ● Players go mining in order, so player #1 does all of their mining, followed by player #2, then player #3, and so on.
        
        Attributes:
        * Inherits from Game class
        * players: Player instances
    """
    # Constants for random generation of number of players
    MIN_PLAYERS = 2
    MAX_PLAYERS = 5

    def __init__(self) -> None:
        """
            Initialises attributes, now with list to store players
        
            :complexity: Best/Worst O(1)
        """
        super().__init__()
        self.players = []

    def initialise_game(self) -> None:
        """
            Initialise all game objects: Materials, Caves, Traders, Players randomly.

            :complexity: Best/Worst O(A), where A is the largest value among M, C and T, which are the number of materials, caves and traders respectively.
        """
        super().initialise_game()
        N_PLAYERS = RandomGen.randint(self.MIN_PLAYERS, self.MAX_PLAYERS)
        self.generate_random_players(N_PLAYERS)
        for player in self.players: # O(P), where P is the number of players
            player.set_materials(self.get_materials())
            player.set_caves(self.get_caves())
            player.set_traders(self.get_traders())
        # print("Players:\n\t", end="")
        # print("\n\t".join(map(str, self.players)))

    def generate_random_players(self, amount) -> None:
        """
            Generate <amount> random players. Don't need anything unique, but you can do so if you'd like.
            
            :complexity: Best/Worst O(N), where N is <amount>
        """
        for _ in range(amount):
            self.players.append(Player.random_player())

    def initialise_with_data(self, materials: list[Material], caves: list[Cave], traders: list[Trader], player_names: list[int], emerald_info: list[float]) -> None:
        """
            Manually initialise game objects with arguments given.

                                    
            :param arg1: materials - A list of Material objects

            :param arg2: caves - A list of Cave objects

            :param arg3: traders - A list of Trader objects

            :param arg4: player_names - A list of String (players' name)

            :param arg5: emerald_info - A list of floating number

            :pre: Number of player names matches number of emerald info.

            :return: None

            :complexity: Best: O(1)
                         Worst O(P), where P is the number of players
        """
        if len(player_names) != len(emerald_info):
            raise ValueError("Number of player names does not equal number of emerald info")
        
        super().initialise_with_data(materials, caves, traders)
        for player, emerald in zip(player_names, emerald_info): 
            self.players.append(Player(player, emeralds=emerald))
            self.players[-1].set_materials(self.get_materials())
            self.players[-1].set_caves(self.get_caves())
            self.players[-1].set_traders(self.get_traders())
        # print("Players:\n\t", end="")
        # print("\n\t".join(map(str, self.players)))

    def simulate_day(self) -> None:
        """
            Simulates a day with the sequence of
            1. Traders each generating a deal
            2. Generate one random food offered to players. Then players take turns doing the following:
                * Purchase food if possible
                * Choose one cave to mine materials then sell the materials to the Trader
                * Cave quantity updated
            5. Cave quantities are added/removed.

            :param: None

            :pre: None

            :return: None

            :complexity: Worst O(P + T * (N * Log N + j-i*log(H)) + 2J + (M + T + C + P * log C) + (2F + 2B + 2T + 3C + 4P + (C * (2C + 2M)) + (F * Fc) + (C * log Ph) + (P * (2log Ph)) + (C ^ 2)))
            Best O(P + T + 2J + (M + T + C + P * log C) + (2F + 2B + 6C + 2T + 5P))
            where,
            P is number of players
            T is number of traders
            N is number of materials in inventory
            H is the height of the tree
            J is the complexity for Join method in Python

        """
        # print("########## NEW DAY #############")
        for player in self.players:
            player.hunger_points = 0 # ensure player starts the game with 0 hunger points

        # 1. Traders make deals
        # Best O(T) if all are RandomTraders, Worst O(T * N (CompK * N)) if all are Range/HardTraders
        for trader in self.get_traders(): # O(T)
            trader.generate_deal() # Best O(1) if RandomTrader, Worst O(N * Log N + j-i*log(H)) if Range Trader

        # print("Traders Deals:\n\t", end="")
        # print("\n\t".join(map(str, self.get_traders()))) # O(J)
        # 2. Food is offered
        offered_food = Food.random_food()
        # print(f"\nFoods:\n\t{offered_food}")

        # print("Caves")
        # print("\n\t".join(map(str, self.get_caves())))
        # 3. Each player selects a cave - The game does this instead.
        foods, balances, caves = self.select_for_players(offered_food)
        # 4. Quantites for caves is updated, some more stuff is added.
        self.verify_output_and_update_quantities(foods, balances, caves)

    def select_for_players(self, food: Food) -> tuple[list[Food|None], list[float], list[tuple[Cave, float]|None]]:
        """
            Players take turns to buy food if possible, choose a cave to mine materials, sell the material to Trader. 

            Step 1: Get best selling prices
            Approach: LinearProbeTable(key = material_name, value = Trader)
            Loop through the generated traders, map their current deal's material name to the trader instance. If a trader offers same material 
            but with higher selling price, update the trader instance in the hash table.

            Step 2: Compute profits for each cave that should be mined from, i.e. the cave's materials can be sold to traders
            Approach: MaxHeap to store each cave's profit
                      LinearProbeTable(key = string representing profit, value = List[Cave])
            Loop through generated caves, computing the cave's profit and storing into MaxHeap. Keep track of the cave associated with that
            profit by mapping the profit to the cave. The value of this hash table is a list because it's possible that different caves have same profits,
            so searching for this profit in the hash table yields all the caves with that profit.
            
            Step 3: Players take turns making optimal choices to get maximum emerald balance. Cave quantities must be updated after each player makes move
            Approach: 
            If cannot afford food, player does nothing. Continue to next player
            If on this player's turn the caves have been depleted, player does nothing. Continue to next player
            Otherwise, simulate mining:
            * Player buys food, decreasing emerald balance
            * Player uses get_max()from the profit_heap to get maximum profit on their turn, increasing emerald balance from this profit
            * Player checks if it was worth mining (balance >= original balance)
            
            If it was not worth it, player does nothing. Continue to next player (Changes made during the simulation need to be reverted)
            Otherwise, player mines according to simulation. Continue to next player

            :param: food - An object of Food

            :pre: None

            :return: tuple of list - (foods_bought, players_emerald, caves_visited)
            
            :complexity: Best = Worst O(T + C *(log C) + P *log C), where T is number of traders, C is number of caves, P is number of players
        """
        profit_heap = MaxHeap(len(self.caves)) # O(C)
        profit_caves = LinearProbeTable(len(self.caves)) # O(C)
        
        # setup prices
        self.generate_trader_deals_table()
        trader_deals = self.trader_deals # hash table with current material as key and trader as data
        
        # compute profits for each cave based on number of materials mined, and we only choose caves with materials that can be sold
        for cave in self.caves: # O(C)
            # NOTE: Due to finish_day()'s functionality, it's possible that the cave will have 0.0 materials
            if cave.material.name in trader_deals: # O(1) search
                minable_quantity = food.hunger_bars / cave.material.mining_rate
                cave_quantity = cave.get_quantity()

                # if quantity in cave less than how much a player can mine
                if cave_quantity <= minable_quantity:
                    # mine all in cave
                    cave.mined_quantity = cave_quantity
                    cave.remaining_quantity = 0 # indicates that cave is depleted
                else:
                    # otherwise mine whatever the player can
                    cave.mined_quantity = minable_quantity
                    cave.remaining_quantity = cave_quantity - minable_quantity # there is still some left in cave
                profit = trader_deals[cave.material.name].current_price * cave.mined_quantity # O(1) search
                
                # Hash caves based on its string value of the profit. Each profit string will have its list of caves
                # if it is a unique profit key, then it is new insert
                if str(profit) not in profit_caves:
                    same_profit_caves = []
                    # print(str(profit) in profit_caves, "Unique profit", profit)
                    same_profit_caves.append(cave)
                    profit_caves.insert(str(profit), same_profit_caves)
                # duplicate profit key, so just update caves
                elif str(profit) in profit_caves:
                    # print(str(profit) in profit_caves, "THIS IS THE PROFIT", profit)
                    profit_caves[str(profit)].append(cave)
                profit_heap.add(profit)  # insert profit into profit heap, O(log C)

        caves_visited = []
        players_emerald = []
        foods_bought = []
        for player in self.players: # O(P)
            balance = player.balance
            hunger_points = player.hunger_points
            if balance > food.price: # if player can buy food
                player.foods_list = [food]
                balance -= food.price
                hunger_points += food.hunger_bars
                foods_bought.append(food)
            else:
                foods_bought.append(None)
                caves_visited.append(None)
                players_emerald.append(balance)
                continue

            # no more caves to mine, so this player, along with the rest can skip
            if profit_heap.length == 0:
                # print("All caves have been depleted")
                # print(f"{player.name} did not buy food. Balance : {player.balance}, Food: None\n \tVisited caves: None")
                players_emerald.append(player.balance) 
                player.hunger_points = 0
                foods_bought.pop()
                foods_bought.append(None)
                caves_visited.append(None)
                continue # go to next player

            # this gives the potential profit from mining all of the material in the cave, but it may not actually be the profit 
            # gained by the player since the quantity mined is limited by hunger points
            chosen_cave_profit = profit_heap.get_max() # This method also removes the profit from the heap, O(log C)

            same_profit_caves = profit_caves[str(chosen_cave_profit)] # returns list of caves with same profit - O(1)
            updated_profit = 0
            cave = same_profit_caves.pop() # Get one of the caves with that profit(order should not matter)

            # check if it was better to not visit any caves at all
            balance += chosen_cave_profit
            if balance < player.balance:
                # print(f"{player.name} did not buy food and visit {cave.name}. Balance : {player.balance}, Food: None\n \tVisited caves: None")
                players_emerald.append(player.balance) 
                player.hunger_points = 0
                foods_bought.pop()
                cave.is_visited = False
                same_profit_caves.append(cave)
                foods_bought.append(None)
                caves_visited.append(None)
                profit_heap.add(chosen_cave_profit) # since we removed the profit from the heap, we must reinsert now, O(log C)
                continue # go to next player
            # else:
                # print(f"{player.name} visited {cave.name} because current max profit that is affordable is {chosen_cave_profit} and they mined {cave.mined_quantity} {cave.material} from the available {cave.quantity}")
                # print(f"At this point the length of same_profit_caves is {len(same_profit_caves)}")


            if cave.remaining_quantity != 0:
                # updates for next player
                minable_quantity = food.hunger_bars / cave.material.mining_rate 
                if minable_quantity < cave.remaining_quantity:
                    cave.mined_quantity = minable_quantity
                    cave.remaining_quantity -= minable_quantity
                    updated_profit = minable_quantity * trader_deals[cave.material.name].current_price
                else:
                    cave.mined_quantity = cave.remaining_quantity
                    updated_profit = cave.remaining_quantity * trader_deals[cave.material.name].current_price
                    cave.remaining_quantity = 0
                if str(updated_profit) not in profit_caves:
                    profit_caves.insert(str(updated_profit), [cave]) 
                else:
                    profit_caves[str(updated_profit)].append(cave)
                profit_heap.add(updated_profit)

            
            # update stats
            players_emerald.append(balance)   
            hunger_points -= cave.mined_quantity * cave.material.mining_rate 
            caves_visited.append((cave, cave.mined_quantity))



            
        return (foods_bought, players_emerald, caves_visited)

    def verify_output_and_update_quantities(self, foods: list[Food | None], balances: list[float], caves: list[tuple[Cave, float]|None]) -> None:
        """
            Checks inputs:
            a. Quantities are in line with what the players provided. If there are 20 players the input lists should all have 20 entries. The type of list elements also verified.
            b. Only one type of Food allowed, and Food purchase must be affordable based on a player's balance
            c. Caves must be from game initialization, the mined quantities cannot exceed the cave's quantity
            d. Checks that the caves visited are profitable, i.e. have materials that can be sold to traders
            e. Checks that balances are either more than or equal to player's original balances
            
            Check player's initial stats(at start of each day):
            a. Hunger points must be zero
            b. Player's emerald balance must be more than zero

            Check that players made best possible choices to have maximal emerald balance at the end of the day:
            Players either 
            a) Do nothing: 
                Their corresponding entry in <foods> is None 
                Their corresponding entry in <caves> is None 
                Their entry in <balance> should be their original balance
            b) Choose a cave to mine:
                Their corresponding entry in <foods> is the single food choice offered
                Their corresponding entry in <caves> is the one with highest profit on their turn
                Their entry in <balance> should match the expected balance from buying the food and mining from the chosen cave
            
            Players do nothing when:
            a) The emerald balance after mining from most profitable cave is less than the original balance
            b) The cave for that day have been depleted. (If one player encounters this all subsequent players also follow suit)


            Updates the quantities for players and visited caves. Then sets caves for the next day.

            :param arg1: food (default = None)

            :param arg2: balance - the balance of the player

            :param arg3: cave - A list with tuple(Cave, mine_quantity)

            :pre: None

            :return: None
            
            :complexity: 
            Worst O(2F + 2B + 2T + 3C + 4P + (C * (C + 2M)) + (F * Fc) + (C * log Ph) + (P * log Ph) + (C ^ 2))
            Best O(2F + 2B + 6C + 2T + 5P)
            Where,
            F is the number of elements in foods list
            B is the number of elements in balances list
            C is the number of element in caves list
            P is the number of players
            M is the number of current materials for every traders
            Fc is the number of elements in food_choice list
            Ph is the number of nodes in profit heap
        """
        print("######## VERIFYING ##########")
        # check input parameters
        try:
            # check that length of the three lists in the parameter matches number of players
            assert len(foods) == len(self.players) and len(balances) == len(self.players) and len(caves) == len(self.players), "Each player must have a choice"
            # check foods
            assert isinstance(foods, list) and all((isinstance(food, Food) or food is None) for food in foods), "Foods should be list consisting of Food objects or None"
            # check balances
            assert isinstance(balances, list)  and all(isinstance(balance, float) or isinstance(balance, int) for balance in balances), "Balance should be float or int"
            # check caves
            assert isinstance(caves, list), "Caves should be list object"
            assert all((isinstance(details,tuple) or details is None) for details in caves), "Caves list should contain tuple or None"
            assert all(len(details) == 2 for details in caves if isinstance(details, tuple)), "Caves list tuple should be of length 2: (cave, mined quantity)"
            for details in caves:
                if details is not None:
                    assert isinstance(details[0], Cave), "The tuple's first eleement should be a Cave instance "
                    assert isinstance(details[1], float) or isinstance(details[1], int), "The tuple's second element should be float or int"
        except AssertionError as e:
            raise ValueError(e)

        # setup trader_deals(best prices), profits for each cave available on that day
        self.generate_trader_deals_table()
        trader_deals = self.trader_deals

        # further checks on caves input
        try: 
            for details in caves:
                if details is not None:
                    # check all caves visited are generated caves
                    assert details[0] in self.get_caves(),"Caves visited are invalid, not generated by game"
                    # check all mined quantities does not exceed the valid caves quantity
                    assert details[1]-EPSILON < details[0].get_quantity(),"Invalid quantity of mined materials for Cave visited"
                    # check all mined materials are bought by traders
                    assert details[0].material.name in trader_deals, f"Materials that are not traded are mined."
        except AssertionError as e:
            raise Exception(e)
        
        # further checks on foods
        try:
            food_choice = []
            for food in foods:
                if food is not None:
                    if not food.name in food_choice:
                        food_choice.append(food.name)
            assert len(food_choice) == 1, "Should only have one food type that players can purchase"
            # setup food_choice for future checks
            for food in foods:
                if food is not None:
                    food_choice = food
                    break 
        except AssertionError as e:
            raise Exception(e)

        # check initial player balance and hunger points
        try:
            for i in range(len(self.players)):
                assert self.players[i].balance > EPSILON and self.players[i].hunger_points == 0, f"Invalid initial player balance {self.players[i].balance} and hunger points {self.players[i].hunger_points}"
        except AssertionError as e:
            raise Exception(e)

        # check balances provided gives profit or remain unchanged
        try:
            player_balances = [player.balance for player in self.players]
            for i in range(len(balances)):
                assert balances[i] > player_balances[i] - EPSILON, f"Selection must ensure no losses. Balance after {balances[i]}, Balance Before {player_balances[i]}"
        except AssertionError as e:
            raise Exception(e)

        # for players who bought food check if they could actually afford it
        for i in range(len(self.players)):
            player = self.players[i]
            try:
                if foods[i] is not None:
                    assert food_choice.price < player.balance - EPSILON, f"Food price of {food_choice.price} exceeded {player.name}'s balance"
            except AssertionError as e:
                raise Exception(e)  



        # setup profit for each cave available on that day
        profit_caves = LinearProbeTable(len(self.caves))
        profit_heap = MaxHeap(len(self.caves))
        for cave in self.caves: # O(C)
            if cave.material.name in trader_deals: # linear probe O(1)
                minable_quantity = food_choice.hunger_bars / cave.material.mining_rate
                cave_quantity = cave.get_quantity()

                # if quantity in cave less than how much a player can mine
                if cave_quantity <= minable_quantity:
                    # mine all in cave
                    cave.mined_quantity = cave_quantity
                    cave.remaining_quantity = 0 # indicates that cave is depleted
                else:
                    # otherwise mine whatever the player can
                    cave.mined_quantity = minable_quantity
                    cave.remaining_quantity = cave.quantity - minable_quantity # there is still some material left in cave
                assert cave.mined_quantity <= cave.quantity
                profit = trader_deals[cave.material.name].current_price * cave.mined_quantity
                
                # Hash caves based on its string value of the profit. Each profit string will have its list of caves
                # if it is a unique profit key, then it is new insert
                if str(profit) not in profit_caves:
                    same_profit_caves = []
                    same_profit_caves.append(cave)
                    profit_caves.insert(str(profit), same_profit_caves)
                # duplicate profit key, so just update caves
                elif str(profit) in profit_caves:
                    profit_caves[str(profit)].append(cave)
                profit_heap.add(profit)  # insert profit into profit heap

        # check if player made optimal choices to get best balances
        for i in range(len(self.players)):
            player = self.players[i]
            try:
                # cannot afford food
                if player.balance < food_choice.price:
                    balance = player.balance
                    hunger_points = 0
                    assert foods[i] is None and caves[i] is None and balances[i] == balance, f"{player.name} should do nothing(can't afford food)"
                # can afford food
                else:
                    # if caves are depleted for that day, this player (and any other subsequent players) should do nothing
                    if profit_heap.length == 0: 
                        assert foods[i] is None and caves[i] is None and balances[i] == player.balance, "Player cannot do anything because all caves are depleted"
                        hunger_points = 0
                        continue # directly go to next player

                    # player thinks about whether it is worth it to mine
                    balance = player.balance - food_choice.price # assume player bought food
                    max_profit = profit_heap.get_max() # choose highest profit possible, this will remove the profit from the heap
                    same_profit_caves = profit_caves[str(max_profit)] # get list of caves with that max profit
                    chosen_cave = same_profit_caves.pop() # go to one of those caves, this will remove the cave
                    balance += max_profit # assume that player got profit from that cave

                    # if above attempt resulted in a loss, then player does nothing
                    if balance < player.balance: 
                        assert foods[i] is None and caves[i] is None and balances[i] == player.balance, f"{player.name} should do" + \
                            f"nothing({max_profit} from mining less than cost of {food_choice.price})"
                        hunger_points = 0
                        same_profit_caves.append(chosen_cave) # need to reinsert because we removed it previously
                        profit_heap.add(max_profit) # need to reinsert because we removed it previously
                        continue
                    # if the attempt was profitable (balance > original balance)
                    else:
                        assert foods[i] == food_choice, f"{player.name} should have bought food: {food_choice.name}"
                        assert caves[i][0] == chosen_cave, f"{player.name} should have visited {chosen_cave.name} because {chosen_cave} gives profit of {max_profit}, instead visited {caves[i][0]}"
                        assert balances[i] == balance, f"{player.name}'s balance of {balances[i]} does not match expected {balance} after mining"
                        hunger_points = food_choice.hunger_bars
                        
                        # if chosen_cave has remaining material, recalculate profit and reinsert into hash table and heap
                        if chosen_cave.remaining_quantity != 0:

                            # updates for next player
                            minable_quantity = food_choice.hunger_bars / chosen_cave.material.mining_rate 
                            if minable_quantity < chosen_cave.remaining_quantity:
                                chosen_cave.mined_quantity = minable_quantity
                                chosen_cave.remaining_quantity -= minable_quantity
                                updated_profit = minable_quantity * trader_deals[chosen_cave.material.name].current_price
                            else:
                                chosen_cave.mined_quantity = chosen_cave.remaining_quantity
                                updated_profit = chosen_cave.remaining_quantity * trader_deals[chosen_cave.material.name].current_price
                                chosen_cave.remaining_quantity = 0
                            if str(updated_profit) not in profit_caves:
                                profit_caves.insert(str(updated_profit), [chosen_cave]) 
                            else:
                                profit_caves[str(updated_profit)].append(chosen_cave)
                            profit_heap.add(updated_profit)
            
            except AssertionError as e:
                raise Exception(e)

        # prepare caves for next day
        remaining_caves = []
        for i in range(len(self.caves)): # These are the generated caves that were used to initialize the game. 
            generated_cave = self.caves[i]
            # if the cave was visited, its quantities need to be updated according to what was mined
            if generated_cave.is_visited: 
                for j in range(len(caves)): # caves: List[(cave, mined_quantity)] 
                    if caves[j] is not None and generated_cave.name == caves[j][0].name:
                        assert caves[j][1] <= caves[j][0].quantity, f"Mined quantity {caves[j][1]} must not exceed existing quantity {caves[j][0].quantity}"
                        caves[j][0].quantity -= caves[j][1] # decrement the cave's quantity
                        # reset is_visited
                        caves[j][0].is_visited = False
                        remaining_caves.append(caves[j][0]) 
                        break

            # if the cave was not visited, just add it(no need to modify its quantity)
            else:
                remaining_caves.append(generated_cave)

        # update the attributes of players after it has passed all tests 
        for i in range(len(self.players)):
            self.players[i].hunger_points = hunger_points
            self.players[i].balance = balances[i]
            self.players[i].foods_list = [foods[i]]
            self.players[i].set_caves(remaining_caves)

# if __name__ == "__main__":
#     g = MultiplayerGame()
#     gold = Material("Gold Nugget", 27.24)
#     netherite = Material("Netherite Ingot", 20.95)
#     fishing_rod = Material("Fishing Rod", 26.93)
#     ender_pearl = Material("Ender Pearl", 13.91)
#     prismarine = Material("Prismarine Crystal", 11.48)

#     materials = [
#         gold,
#         netherite,
#         fishing_rod,
#         ender_pearl,
#         prismarine,
#     ]   

#     caves = [
#         Cave("Boulderfall Cave", prismarine, 10),
#         Cave("Castle Karstaag Ruins", netherite, 4),
#         Cave("Glacial Cave", gold, 3),
#         Cave("Orotheim", fishing_rod, 6),
#         Cave("Red Eagle Redoubt", fishing_rod, 3),
#     ]

#     waldo = RandomTrader("Waldo Morgan")
#     waldo.add_material(fishing_rod)
#     waldo.generate_deal()
#     waldo.current_price = 7.44
#     orson = RandomTrader("Orson Hoover")
#     orson.add_material(gold)
#     orson.generate_deal()
#     orson.current_price = 7.70
#     lea = RandomTrader("Lea Carpenter")
#     lea.add_material(prismarine)
#     lea.generate_deal()
#     lea.current_price = 7.63
#     ruby = RandomTrader("Ruby Goodman")
#     ruby.add_material(netherite)
#     ruby.generate_deal()
#     ruby.current_price = 9.78
#     mable = RandomTrader("Mable Hodge")
#     mable.add_material(gold)
#     mable.generate_deal()
#     mable.current_price = 5.48

#     traders = [
#         waldo,
#         orson,
#         lea,
#         ruby,
#         mable,
#     ]
    
    
#     g.initialise_with_data(materials, caves, traders,[1], [0.1])
#     g.players = [Player("Alexey", 50), Player("Jackson", 14), Player("Saksham", 35), Player('Brendon', 44)]
#     g.select_for_players(Food("Cooked Chicken Cuts", 100, 19))


#     PLAYER_NAMES = [
#         "Steve",
#         "Alex",
#         "ɘᴎiɿdoɿɘH",
#         "Allay",
#         "Axolotl",
#         "Bat",
#         "Cat",
#         "Chicken",
#         "Cod",
#         "Cow",
#         "Donkey",
#         "Fox",
#         "Frog",
#         "Glow Squid",
#         "Horse",
#         "Mooshroom",
#         "Mule",
#         "Ocelot",
#         "Parrot",
#         "Pig",
#         "Pufferfish",
#         "Rabbit",
#         "Salmon",
#         "Sheep",
#         "Skeleton Horse",
#         "Snow Golem",
#         "Squid",
#         "Strider",
#         "Tadpole",
#         "Tropical Fish",
#         "Turtle",
#         "Villager",
#         "Wandering Trader",
#         "Bee",
#         "Cave Spider",
#         "Dolphin",
#         "Enderman",
#         "Goat",
#         "Iron Golem",
#         "Llama",
#         "Panda",
#         "Piglin",
#         "Polar Bear",
#         "Spider",
#         "Trader Llama",
#         "Wolf",
#         "Zombified Piglin",
#         "Blaze",
#         "Chicken Jockey",
#         "Creeper",
#         "Drowned",
#         "Elder Guardian",
#         "Endermite",
#         "Evoker",
#         "Ghast",
#         "Guardian",
#         "Hoglin",
#         "Husk",
#         "Magma Cube",
#         "Phantom",
#         "Piglin Brute",
#         "Pillager",
#         "Ravager",
#         "Shulker",
#         "Silverfish",
#         "Skeleton",
#         "Skeleton Horseman",
#         "Slime",
#         "Spider Jockey",
#         "Stray",
#         "Vex",
#         "Vindicator",
#         "Warden",
#         "Witch",
#         "Wither Skeleton",
#         "Zoglin",
#         "Zombie",
#         "Zombie Villager",
#         "H̴͉͙̠̥̹͕͌̋͐e̸̢̧̟͈͍̝̮̹̰͒̀͌̈̆r̶̪̜͙̗̠̱̲̔̊̎͊̑̑̚o̷̧̮̙̗̖̦̠̺̞̾̓͆͛̅̉̽͘͜͝b̸̨̛̟̪̮̹̿́̒́̀͋̂̎̕͜r̸͖͈͚̞͙̯̲̬̗̅̇̑͒͑ͅi̶̜̓̍̀̑n̴͍̻̘͖̥̩͊̅͒̏̾̄͘͝͝ę̶̥̺̙̰̻̹̓̊̂̈́̆́̕͘͝͝"
#     ]

#     RandomGen.set_seed(1234)
#     materials = [
#         Material.random_material()
#         for _ in range(10)
#     ]
#     mat_set = set()
#     mining_set = set()
#     materials = list(filter(lambda x: (x.name not in mat_set and x.mining_rate not in mining_set) and (mat_set.add(x.name) or mining_set.add(x.mining_rate)) is None, materials))
#     caves = [
#         Cave.random_cave(materials)
#         for _ in range(20)
#     ]
#     cave_set = set()
#     caves = list(filter(lambda x: x.name not in cave_set and cave_set.add(x.name) is None, caves))      
#     traders = [
#         RandomGen.random_choice([RangeTrader, RandomTrader]).random_trader()
#         for _ in range(10)
#     ]
#     trade_set = set()
#     traders = list(filter(lambda x: x.name not in trade_set and trade_set.add(x.name) is None, traders))
#     for trader in traders:
#         trader.set_all_materials(materials)
#     players = [
#         RandomGen.random_choice(PLAYER_NAMES)
#         for _ in range(10)
#     ]
#     balances = [
#         RandomGen.randint(20, 100)
#         for _ in range(10)
#     ]
#     RandomGen.set_seed(12345)
#     g = MultiplayerGame()
#     g.initialise_with_data(
#         materials,
#         caves,
#         traders,
#         players,
#         balances,
#     )


#     for trader in g.get_traders(): # O(T)
#         trader.generate_deal() # Best O(1) if RandomTrader, Worst O(N (CompK * N) if Range/HardTrader

#     print("Traders Deals:\n\t", end="")
#     print("\n\t".join(map(str, g.get_traders())))
#     # 2. Food is offered
#     offered_food = Food.random_food()
#     print(f"\nFoods:\n\t{offered_food}")
#     # 3. Each player selects a cave - The game does this instead.
#     foods, balances, caves = g.select_for_players(offered_food)


if __name__ == "__main__":
    RandomGen.set_seed(1234)
    g = SoloGame()
    g.initialise_game()
    # Spend some time in minecraft
    # Note that this will crash if you generate a HardTrader with less than 3 materials.
    for _ in range(3):
        g.simulate_day()
        g.finish_day()