import random
from game_assets.enemy_assets import *
from game_assets.game_logic import *
from game_assets.map_contents_gen import *
from game_assets.player import *

 #REMAKE TO DYNAMIC CREATION -> only create next set of children after entering their parent

class game_map_generation():
    #generates bin tree and attaches property to each node
    class Node():
        type = 'ROOM'
        def __init__(self,data,node_type,parent = None):
            self.data = data
            self.child_left = None
            self.child_right = None
            self.node_type = node_type
            self.parent = parent
            self.contents = ['enemy','loot']
             
    def __init__(self, goal=None):
        self.MAX_DEPTH = 5
        self.root = None 
        self.exploration_goal = goal
        self.boss_spawned = False
        self.enemy_count = 0
        self.total_room_count = 0
        self.explored_room_count = 0

    def generate_map(self):
        #initiates generation and returns first node
        if self.MAX_DEPTH<1 : return None
        self.root = self.generate_node(1,1)
        return self.root

    def generate_node(self, curr_depth, node_data, parent = None):
        if curr_depth > self.MAX_DEPTH : 
            return None

        node_type = self.choose_node_type(curr_depth)
        if node_type == 'wall': 
            return None
        self.total_room_count += 1
        node = self.Node(node_data, node_type, parent)
        node_data_left = node_data*2
        node_data_right = 1 + node_data*2

        node.child_left = self.generate_node(curr_depth + 1, node_data_left, node)
        node.child_right = self.generate_node(curr_depth + 1, node_data_right, node)
        return node

    def choose_node_type(self, curr_depth):
        #attaches room type to room based on chance
        if curr_depth == 1: 
            return 'entrance'
        if self.boss_spawned:
            return 'wall'
        if curr_depth == self.MAX_DEPTH and self.exploration_goal == 'boss' and not self.boss_spawned: 
            self.boss_spawned = True
            return 'boss'
        
        #creates artificial room rarity
        node_type_list = (
    ['basic_enemy' for _ in range(15)] +
    ['elite_enemy' for _ in range(5)] +
    ['reward' for _ in range(5)] +
    ['nothing' for _ in range(14)] +
    ['wall' for _ in range(3 if (curr_depth>3 and self.exploration_goal!='boss') else 0)]
                            )
        node_type = random.choice(node_type_list)
        if node_type in ['basic_enemy', 'elite_enemy']: 
            self.enemy_count += 1
        
        return node_type