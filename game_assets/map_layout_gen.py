import random
from game_assets.enemy_assets import *
from game_assets.game_logic import *
from game_assets.map_contents_gen import *
from game_assets.player import *


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
            self.contents = ['enemy','loot', 'door']
             
    def __init__(self, goal=None):
        if goal == 'explore':
            self.MAX_DEPTH = random.randint(5,6)
        elif goal == 'execute':
            self.MAX_DEPTH = random.randint(4,6)
        else:
            self.MAX_DEPTH = 4
        self.root = None 
        self.exploration_goal = goal
        self.boss_spawned = False
        self.enemy_count = 0
        self.total_room_count = 0
        self.explored_room_count = 0
        self.portal_generated = False

    def generate_map(self):
        #initiates generation and returns first node
        if self.MAX_DEPTH<1 : return None
        self.root = self.generate_node(1,1)
        if self.portal_generated == True:
            self.generate_portal_route()
        return self.root

    def generate_node(self, curr_depth, node_data, parent = None):
        if curr_depth > self.MAX_DEPTH : 
            return None

        node_type = self.choose_node_type(curr_depth)
        if node_type == 'wall': 
            return None
        
        node = self.Node(node_data, node_type, parent)
        node.contents[2] = self.choose_door_type(node_type)
        if node_type == 'portal':
            node.child_left = None
            node.child_right = None
            return node

        node_data_left = node_data*2
        node_data_right = 1 + node_data*2

        node.child_left = self.generate_node(curr_depth + 1, node_data_left, node)
        node.child_right = self.generate_node(curr_depth + 1, node_data_right, node)
        self.total_room_count += 1
        if node_type in ['basic_enemy', 'elite_enemy']: 
            self.enemy_count += 1
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
        if node_type == 'wall' and self.portal_generated==False: 
            node_type = random.choice(['wall' for _ in range(9)]+['portal'])
            self.portal_generated = True
        return node_type

    def choose_door_type(self, node_type):
        door_types = (['trap' for _ in range(4)] +
                      ['nothing' for _ in range(9)])
        return random.choice(door_types)

    def generate_portal_route(self):
        stack = [self.root]
        portal = None
        reward = None
        while len(stack)>0:
            curr = stack.pop()
            left = curr.child_left
            right = curr.child_right
            if left != None:
                stack.append(left)
                if left.node_type == 'portal':
                    portal = [curr, 'left']

            if right != None:
                stack.append(right)
                if right.node_type == 'portal':
                    portal = [curr, 'right']

            if portal != None:
                break

        if portal == None:
            return

        stack = [self.root]
        while len(stack)>0:
            curr = stack.pop()
            if curr.node_type == 'reward':
                reward = curr
                reward.contents[2] = 'portal'
                break
            
            left = curr.child_left
            right = curr.child_right
            if left != None:
                stack.append(left)
            if right != None:
                stack.append(right)
            
        if portal[1] == 'left':
            portal[0].child_left = None
            portal[0].child_left = reward
        else:
            portal[0].child_right = None
            portal[0].child_right = reward