import random

class game_map_generation():
    #generates bin tree and attaches property to each node
    class Node():
        def __init__(self,data,node_type,parent = None):
            self.data = int(data)
            self.child_left = None
            self.child_right = None
            self.node_type = node_type
            self.parent = parent
            
    def __init__(self):
        self.MAX_DEPTH = 5
        self.root = None 
        self.boss_spawned = False

    def generate_map(self):
        if self.MAX_DEPTH<1 : return None
        self.root = self.generate_node(1,1)
        return self.root

    def generate_node(self, curr_depth, node_data, parent = None):
        if curr_depth > self.MAX_DEPTH : return None
        
        node = self.Node(node_data, self.choose_node_type(curr_depth), parent)
        node_data_left = node_data*2
        node_data_right = 1 + node_data*2

        node.child_left = self.generate_node(curr_depth + 1, node_data_left, node)
        node.child_right = self.generate_node(curr_depth + 1, node_data_right, node)
        return node

    def choose_node_type(self, curr_depth):
        node_type_list = (
    ['basic_enemy' for _ in range(15)] +
    ['elite_enemy' for _ in range(5)] +
    ['reward' for _ in range(5)] +
    ['nothing' for _ in range(14)] +
    (['boss'] if self.boss_spawned and curr_depth == self.MAX_DEPTH else ['nothing'])
                            )
        node_type = random.choice(node_type_list)
        return node_type

class traverse_tree():
    def __init__(self):
        bin_tree_root = game_map_generation().generate_map()
        self.root = bin_tree_root

    def go_left(self):
        self.root = self.root.child_left

    def go_right(self):
        self.root = self.root.child_right

    def go_back(self):
        self.root = self.root.parent

    def choose_travel_destination(self):
        while True:
            left_door = 'wall' if self.root.child_left==None else self.root.child_left.node_type
            right_door = 'wall' if self.root.child_right==None else self.root.child_right.node_type
            print(f'you are in room {self.root.data}, it is a {self.root.node_type} room')
            print(f'in front of you are {left_door} room and {right_door} room')
    
            destination_choice = input('L : R : B : Q\n')
        
            if destination_choice == 'L' and self.root.child_left != None:
                self.root.node_type = "nothing"
                self.go_left()

            elif destination_choice == 'R' and self.root.child_right != None:
                self.root.node_type = "nothing"
                self.go_right()
        
            elif destination_choice == 'B' and self.root.parent != None:
                self.go_back()

            elif destination_choice == 'Q':
                print('goodbye\n')
                exit()
        
            else:
                print('cannot go there\n')
        
        

tree = traverse_tree()
tree.choose_travel_destination()
