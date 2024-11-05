import random
import enemy_assets
import game_logic
import map_contents_gen

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

    def generate_map(self): #REMAKE TO DYNAMIC CREATION -> only create next set of children after entering their parent
        if self.MAX_DEPTH<1 : return None
        self.root = self.generate_node(1,1)
        return self.root

    def generate_node(self, curr_depth, node_data, parent = None):
        if curr_depth > self.MAX_DEPTH : return None

        node_type = self.choose_node_type(curr_depth)
        if node_type == 'wall': return None
        
        node = self.Node(node_data, node_type, parent)
        node_data_left = node_data*2
        node_data_right = 1 + node_data*2

        node.child_left = self.generate_node(curr_depth + 1, node_data_left, node)
        node.child_right = self.generate_node(curr_depth + 1, node_data_right, node)
        return node

    def choose_node_type(self, curr_depth):
        if curr_depth == 1: return 'entrance'
        if curr_depth == self.MAX_DEPTH and self.exploration_goal == 'boss': 
            self.boss_spawned = True
            return 'boss'
        #creates artificial room rarity
        node_type_list = (
    ['basic_enemy' for _ in range(15)] +
    ['elite_enemy' for _ in range(5)] +
    ['reward' for _ in range(5)] +
    ['nothing' for _ in range(14)] +
    ['wall' for _ in range(3 if curr_depth>3 else 0)]
                            )
        node_type = random.choice(node_type_list)
        return node_type

class traverse_tree(): #maybe move this to another module
    def __init__(self, bin_tree_root):
        self.root = bin_tree_root
        self.choose_travel_destination()

    def go_left(self):
        self.root = self.root.child_left
        
    def go_right(self):
        self.root = self.root.child_right
        
    def go_back(self):
        self.root = self.root.parent

    def choose_travel_destination(self):
        left_door = 'wall' if self.root.child_left==None else self.root.child_left.node_type
        right_door = 'wall' if self.root.child_right==None else self.root.child_right.node_type
        print(f'you are in room {self.root.data}, it is a {self.root.node_type} room')
        
        if self.root.node_type not in ['nothing', 'reward', 'entrance']:
            self.root.contents[0]=map_contents_gen.room_setup(self.root).enemy_generation()
            enemy = map_contents_gen.room_setup(self.root).enemy_generation()
            print(f'''You have encountered a wild {self.root.contents[0].name}.\n Prepare for battle!''')
            print(enemy.name)
            game_logic.encounter_logic(enemy, self.root.contents[0]).start_battle()
        

        print(f'in front of you are {left_door} room and {right_door} room')
        if self.root.data != 1: self.root.node_type = "nothing"
        
        destination_choice = input('L : R : B : Q\n')
        
        if destination_choice == 'L' and self.root.child_left != None:
            self.go_left()

        elif destination_choice == 'R' and self.root.child_right != None:
            self.go_right()
        
        elif destination_choice == 'B' and self.root.parent != None:
            self.go_back()

        elif destination_choice == 'Q':
            print('goodbye\n')
            exit()
        
        else:
            print('cannot go there\n')