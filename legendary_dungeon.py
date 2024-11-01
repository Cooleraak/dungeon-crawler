import random

class player_char():
    
    def __init__(self):
        #itemID's: hp-hitpoint;
        self.inventory = {
            'hp' : 100,
            }

    def display_stats(self): 
        print(f"HP {self.inventory['hp']} : MP {self.inventory['mp']} : POT {self.inventory['pt']}")
        pass

    def change_item_count(self, item, add, value):  #item->str; #add->bool; #value->int; 
        pass

class enemy_char():
    def __init__(self):
        self.inventory = {
            'hp' : 100,
            }

class chest():
    def __init__(self):
        self.contents_preview = []    

    def generate_loot(self):
        loot = ['','','']
        loot_amount = len(self.contents_preview)
        if loot_amount<3: self.reset_available_loot()
        for i in range(3):
            rand_loot_index = random.randint(0,loot_amount)
            loot[i] = self.contents_preview[rand_loot_index]
            self.contents_preview.pop(random.randint(0,loot_amount))
        return loot

    def reset_available_loot(self): #not rewrite to increase the odds of rare items
        rarity = {'common':5, 'rare' : 3, 'epic' : 1}
        self.contents_preview+=['10hp' for _ in range(rarity['common'])] + [
                                '3mp' for _ in range(rarity['common'])] + [
                                '50hp' for _ in range(rarity['rare'])] + [
                                'pt' for _ in range(rarity['epic'])]

class game_logic():
    def __init__(self):
        pass

    def transfer_loot(self, trans_from, trans_to): #trans_to can be None, meaning trans_from is losing sth 
        pass

    def check_for_EOC(self): #EOC == end of combat
        return False

    def check_for_EOE(self): #EOF == End Of Exploration
        return False

class map(): #traversible binary tree

    class parent():
        def __init__(self, node_id = None):
            self.node_id = node_id
            self.child_left = None
            self.child_right = None
    
    def __init__(self):
        self.node = self.parent(1)

    def map_gen(self):
        pass

    def doors(self):
        pass