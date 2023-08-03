import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""
walls_left=[]
walls_right=[]
turrets_left=[]
turrets_right=[]
left_anchor_turret=[[10,8],[11,7]]
right_anchor_turret = [[17,7],[18,8]]
supports=[[13, 4], [14, 4], [13, 3], [14, 3]]


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.
        self.strategy_plant_matter(game_state)
        ##self.starter_strategy(game_state)

        game_state.submit_turn()


    """
    : All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """
    

        #game_state.attempt_upgrade(wall_locations
 
    
    def strategy_plant_matter(self,game_state):
        if game_state.turn_number<2:
            self.put_interceptor(game_state)
        elif game_state.turn_number<15:
            self.spawn_demolishers(game_state)
        else:
            self.spawn_scouts(game_state)
        self.build_funnel(game_state)


    def strategy_one(self,game_state):
        if game_state.turn_number <=1:
            self.build_start(game_state)
        if game_state.turn_number <=4:
            self.build_reactive_defense1(game_state)
        if game_state.turn_number >4 and game_state.turn_number <8:
            self.funnel_walls(game_state)
        if game_state.turn_number >5 and game_state.turn_number <15:
            if len(walls_left)+len(turrets_left)==len(walls_right)+len(turrets_right):
                self.upgrade_turret_left(game_state)
                self.upgrade_turret_right(game_state)
            elif len(walls_left)+len(turrets_left)>len(walls_right)+len(turrets_right):
                self.upgrade_turret_left
            else:
                self.upgrade_turret_right
        if game_state.turn_number <=20:
            self.build_one_support(game_state)
        if game_state.turn_number>5 and game_state.turn_number <=20:
            self.upgrade_one_support(game_state)
        
        if game_state.turn_number <2:
            self.two_interceptor(self,game_state)
        else:  
            scouts_util = self.scout_utility(game_state)
            destroyer_util = self.destroyer_utility(game_state)
            if scouts_util[1]>1 or destroyer_util[1]>1:
                if scouts_util[1] < destroyer_util[1]:
                    game_state.attempt_spawn(DEMOLISHER,destroyer_util[0],1000)
                else:
                    game_state.attempt_spawn(SCOUT,scouts_util[0],1000)


        
    def two_interceptor(self,game_state):
        count =0
        interceptors=[[20,6],[7,6]]
        for location in self.scored_on_locations:
            if game_state.attempt_spawn(INTERCEPTOR,location,1)==1:
                count+=1
            if count==2:
                return
        for location in interceptors:
            if game_state.attempt_spawn(INTERCEPTOR,location,1)==1:
                count+=1
            if count==2:
                return
    
    def build_start(self,game_state):
        walls = [[0, 13], [2, 13], [25, 13], [27, 13], [3, 12], [6, 12], [21, 12], [25, 12], [7, 11], [20, 11], [8, 10], [19, 10]]
        turrets = [[1, 12], [26, 12], [2, 11], [25, 11], [10, 8], [17, 8], [11, 7], [16, 7]]
        game_state.attempt_spawn(WALL,walls)
        game_state.attempt_spawn(TURRET,turrets)

    def funnel_walls(self,game_state):
        leftwalls = [[4,11],[5,10],[6,9],[7,8],[8,7]]
        rightwalls = [[23,11],[22,10],[21,9],[20,8],[19,7]]
        leftturrets = [[5,9],[6,8],[7,7],[8,6]]
        rightturrets=[[22,9],[21,8],[20,7],[19,6]]

        if len(walls_left)+len(turrets_left)==len(walls_right)+len(turrets_right):
            for location in leftturrets:
                if game_state.attempt_spawn(TURRET,location)==1:
                    turrets_left.append(location)
            for location in rightturrets:
                if game_state.attempt_spawn(TURRET,location)==1:
                    turrets_right.append(location)
            for location in leftwalls:
                if game_state.attempt_spawn(WALL,location)==1:
                    walls_left.append(location)
            for location in rightwalls:
                if game_state.attempt_spawn(WALL,location)==1:
                    walls_right.append(location)
        elif len(walls_left)+len(turrets_left)>len(walls_right)+len(turrets_right):
            for location in leftturrets:
                if game_state.attempt_spawn(TURRET,location)==1:
                    turrets_left.append(location)
            for location in leftwalls:
                if game_state.attempt_spawn(WALL,location)==1:
                    walls_left.append(location)
        else:
            for location in rightturrets:
                if game_state.attempt_spawn(TURRET,location)==1:
                    turrets_right.append(location)
            for location in rightwalls:
                if game_state.attempt_spawn(WALL,location)==1:
                    walls_right.append(location)
    
    def build_reactive_defense1(self,game_state):
        for location in self.scored_on_locations:
            start= [location[0],location[1]+1]
            #game_state.attempt_spawn(TURRET,[location[0],location[1]+1])
            spawned = game_state.attempt_spawn(TURRET,start)
            game_state.attempt_upgrade(start)
            if location[0]+location[1]==13:
                if spawned==1:
                    turrets_left.append(start)
                right = [location[0]+1,location[1]]
                spawned = game_state.attempt_spawn(TURRET,[location[0]+1,location[1]])
                if spawned==1:
                    turrets_left.append(right)
                game_state.attempt_upgrade([location[0]+1,location[1]])
                game_state.attempt_spawn(WALL,[right[0],right[1]+2])
                game_state.attempt_spawn(WALL,[right[0]+1,right[1]+1])
            else:
                if spawned==1: turrets_right.append(start)
                left = [location[0]-1,location[1]]
                spawned = game_state.attempt_spawn(TURRET,left)
                if spawned==1:
                    turrets_right.append(left)
                game_state.attempt_upgrade(left)
                spawned = game_state.attempt_spawn(WALL,[left[0]-1,left[1]+1])
                if spawned ==1:
                    walls_right.append([left[0]-1,left[1]+1])
                spawned = game_state.attempt_spawn(WALL,[left[0],left[1]+2])
                if spawned==1:
                    walls_right.append([left[0],left[1]+2])
    
    def destroyer_utility(self,game_state):
        location_options = [[10, 3], [17, 3], [11, 2], [16, 2], [12, 1], [15, 1]]
        count = game_state.get_resources(0)[1]//3
        life_per_unit = len(supports)*3+5
        life_dummy = life_per_unit
        damages=[]
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                life_dummy-=len(game_state.get_attackers(path_location,0))*gamelib.GameUnit(TURRET,game_state.config).damage_i
                if life_dummy<=0:
                    life_dummy=life_per_unit
                    count-=1
                damage+=len(game_state.get_attackers(path_location,0))*gamelib.GameUnit(DEMOLISHER,game_state.config).damage_f*count+(count*1.5*gamelib.GameUnit(DEMOLISHER,game_state.config)*len(game_state.get_attackers(path_location,0)))
                if count==0:
                    break
            damage+=count*34.5
            damages.append(damage)

        return [location_options[damages.index(max(damages))],(max(damages)/(count*3))/34]
    
    def scout_utility(self,game_state):
        location_options = [[10, 3], [17, 3], [11, 2], [16, 2], [12, 1], [15, 1]]
        count = game_state.get_resources(0)[1]
        life_per_unit = len(supports)*3+15
        life_dummy = life_per_unit
        damages = []
        for location in location_options:
            damage = 0
            path = game_state.find_path_to_edge(location)
            for path_location in path:
                life_dummy -=len(game_state.get_attackers(path_location,0))*gamelib.GameUnit(TURRET,game_state.config).damage_i
                if life_dummy <=0:
                    life_dummy = life_per_unit
                    count-=1
                damage+=count*(len(game_state.get_attackers(path_location,0))+(0.75*len(game_state.get_attackers(path_location,0))))
            damage+=count*69
            damages.append(damage)
        return [location_options[damages.index(max(damages))],damage/(37.5*game_state.get_resources(0)[1])]

    def upgrade_turret_left(self,game_state):
        for location in turrets_left:
            if game_state.attempt_upgrade(location)==1:
                break
    def upgrade_turret_right(self,game_state):
        for location in turrets_right:
            if game_state.attempt_upgrade(location)==1:
                break
    def build_one_support(self,game_state):
        locations =[[13, 4], [14, 4], [13, 3], [14, 3]]
        count = 0
        for location in locations:
            if game_state.attempt_spawn(SUPPORT,location,1)==1:
                break
    def upgrade_one_support(self,game_state):
        for location in supports:
            if game_state.attempt_upgrade(location)==1:
                break
    
    def least_damage_spawn_location(self, game_state):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        location_options = [[10, 3], [17, 3], [11, 2], [16, 2], [12, 1], [15, 1]]
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy turrets that can attack each location and multiply by turret damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(TURRET, game_state.config).damage_i
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return [location_options[damages.index(min(damages))],min(damages)]

    def put_interceptor(self,game_state):
        game_state.attempt_spawn(INTERCEPTOR,[[7,6]],2)


    #1700 Rated algorithm
    def build_setup(self,game_state):
        wall_locations=[[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [4, 12], [5, 12], [6, 12], [11, 12], [12, 12], [15, 12], [16, 12], [21, 12], [22, 12], [23, 12], [7, 10], [8, 10], [9, 10], [18, 10], [19, 10], [20, 10]]
        #second_walls = [[3, 13], [24, 13], [3, 12], [24, 12], [6, 11], [7, 11], [20, 11], [21, 11]]
        second_turrets = [[2, 12], [25, 12], [7, 9], [20, 9]]
        turret_locations=[[1, 12], [26, 12], [5, 11], [12, 11], [15, 11], [22, 11], [8, 9], [19, 9]]
        third_turrets = [[3, 11], [24, 11], [9, 9], [18, 9]]
        second_walls = [[3, 13], [24, 13], [3, 12], [7, 12], [10, 12], [17, 12], [20, 12], [24, 12], [7, 11], [9, 11], [10, 11], [17, 11], [18, 11], [20, 11]]
        game_state.attempt_spawn(WALL,wall_locations)
        game_state.attempt_spawn(TURRET,turret_locations)
        game_state.attempt_spawn(WALL,second_walls)
        game_state.attempt_spawn(TURRET,second_turrets)
        self.spawn_supports(game_state)
        game_state.attempt_spawn(TURRET,third_turrets)
        game_state.attempt_upgrade(turret_locations)
        game_state.attempt_upgrade(wall_locations)
        game_state.attempt_upgrade(second_turrets)
        game_state.attempt_upgrade(third_turrets)
        
    

    def spawn_demolishers(self,game_state):
        location = [[14,0]]
        corners = [[0,13],[27,13]]
        if game_state.turn_number%3==2:
            game_state.attempt_spawn(DEMOLISHER,location,1000)
    
    def spawn_scouts(self,game_state):
        location=[[7,6]]
        if game_state.turn_number%3==2:
            game_state.attempt_spawn(SCOUT,location,1000)
        
    
    def build_defenses1(self,game_state):
        wall_locations=[[0, 13], [1, 13], [2, 13], [25, 13], [26, 13], [27, 13], [4, 12], [5, 12], [6, 12], [11, 12], [12, 12], [13, 12], [14, 12], [15, 12], [16, 12], [21, 12], [22, 12], [23, 12], [7, 10], [8, 10], [9, 10], [18, 10], [19, 10], [20, 10]]
        second_walls = [[3, 13], [24, 13], [3, 12], [24, 12], [6, 11], [7, 11], [20, 11], [21, 11]]
        turret_locations=[[1, 12], [26, 12], [5, 11], [12, 11], [15, 11], [22, 11], [8, 9], [19, 9]]
        game_state.attempt_spawn(WALL,wall_locations)
        game_state.attempt_spawn(TURRET,turret_locations)
        game_state.attempt_upgrade(wall_locations)

    def spawn_supports(self,game_state):
        support_locations=[[11, 9], [13, 9], [15, 9], [11, 8], [13, 8], [15, 8], [12, 6], [13, 6], [14, 6], [13, 5]]
        game_state.attempt_spawn(SUPPORT,support_locations)

    
                
                


    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build turret one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(TURRET, build_location)

    def stall_with_interceptors(self, game_state):
        """
        Send out interceptors at random locations to defend our base from enemy moving units.
        """
        # We can spawn moving units on our edges so a list of all our edge locations
        friendly_edges = game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_LEFT) + game_state.game_map.get_edge_locations(game_state.game_map.BOTTOM_RIGHT)
        
        # Remove locations that are blocked by our own structures 
        # since we can't deploy units there.
        deploy_locations = self.filter_blocked_locations(friendly_edges, game_state)
        
        # While we have remaining MP to spend lets send out interceptors randomly.
        while game_state.get_resource(MP) >= game_state.type_cost(INTERCEPTOR)[MP] and len(deploy_locations) > 0:
            # Choose a random deploy location.
            deploy_index = random.randint(0, len(deploy_locations) - 1)
            deploy_location = deploy_locations[deploy_index]
            
            game_state.attempt_spawn(INTERCEPTOR, deploy_location)
            """
            We don't have to remove the location since multiple mobile 
            units can occupy the same space.
            """

    def demolisher_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our demolisher can attack from long range.
        """
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [WALL, TURRET, SUPPORT]
        cheapest_unit = WALL
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost[game_state.MP] < gamelib.GameUnit(cheapest_unit, game_state.config).cost[game_state.MP]:
                cheapest_unit = unit

        # Now let's build out a line of stationary units. This will prevent our demolisher from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])

        # Now spawn demolishers next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(DEMOLISHER, [24, 10], 1000)

    

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
