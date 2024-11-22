import random
from copy import deepcopy
from game_assets.enemy_assets import *
from game_assets.player import *
from game_assets.map_contents_gen import *

#add boss encounter scenario -> multiple enemy turns, enhanced attacks/passives

class exploration_logic():
    def __init__(self,player_hp = None):
        self.goal = self.set_completion_goal()
        self.player_hp = player_hp
    def set_completion_goal(self):
        possible_goals = {
            'exploration' : False,
            'execution' : False,
            'boss_hunt' : False,
            }
        goal = random.choice(list(possible_goals.keys()))
        return [goal, possible_goals[goal]]

    def progress_tracker(self):
        pass

    def check_for_EOE(self):
        if self.player_hp <= 0:
            print('you lose')
            exit()
        if self.goal[1] == True:
            self.save()
            exit()

    def combat_end(self,node,player):
        chest = room_setup(node).loot_generation().chest_loot

        print(f'you found {chest}')
        for i in chest:
            player.inventory[i]+=1


class encounter_logic(): 
    def __init__(self,player_char, enemy_char):
        self.MAX_DEPTH = 2
        self.player_original = player_char
        self.enemy_original = enemy_char
        self.player_final = deepcopy(player_char)
        self.enemy_final = deepcopy(enemy_char)
        self.player_copy = deepcopy(player_char)
        self.enemy_copy = deepcopy(enemy_char)
    
    def start_battle(self):
        print('player HP:',self.player_original.hp,'; enemy HP:', self.enemy_final.hp)
        while True:  
            player_move = input(f'Choose action: {self.player_copy.actions}\n')
            if player_move!='item':
                self.make_move(self.player_copy, player_move, False)    
            if self.check_for_EOC(False)==True: break
            
            best_move = self.best_move()
            print(self.enemy_original.name,' used ', best_move)
            self.make_move(self.enemy_copy, best_move, False)
            print(f'you:{self.player_final.hp} HP, enemy: {self.enemy_final.hp} HP\n')
            
            if self.check_for_EOC(False) == True: break
        print('you won!')
    
    def calculalte_dmg(self, actor, move):
        poison_dmg = enemy_attacks().attacks_and_skills['poison'] if 'poison' in actor.passives else 0
        dmg_multiplier = actor.dmg_multiplier
        move_dmg = enemy_attacks().attacks_and_skills[move]
        return (move_dmg+poison_dmg) * dmg_multiplier

    def make_move(self,actor, move, is_testing):
        curr_player= deepcopy(self.player_copy) if is_testing else self.player_final
        curr_enemy = deepcopy(self.enemy_copy) if is_testing else self.enemy_final    
       
        moveset = enemy_attacks().attacks_and_skills
        #passive start of turn regeneration
        actor.hp += moveset['regenerative'] if 'regenerative' in actor.passives else 0

        defender = curr_player if actor==curr_enemy else curr_enemy

        #passive dmg reduction if elusive
        elusive_reduction = random.randint(2,10) if 'elusive' in defender.passives else 0
        
        defender.hp -= self.calculalte_dmg(actor,move) - (elusive_reduction*moveset['elusive'])
        
        #returns both characters after acting in case of passive or timer changes
        return curr_player, curr_enemy
        
    def best_move(self):
        enemy_copy = deepcopy(self.enemy_final)
        max_score = -float('inf')
        best_move = None
        for move in enemy_copy.actions:
            self.player_copy, self.enemy_copy = self.make_move(enemy_copy,move, True)
            score = self.minimax(self.MAX_DEPTH, False)
            self.player_copy, self.enemy_copy = self.player_final, self.enemy_final
            if score > max_score:
                max_score = score
                best_move = move
        return best_move

    def minimax(self, curr_depth, enemy_turn):
        score = self.score_calculator()
        if self.check_for_EOC(True)==True: 
            return score*100
        if curr_depth == 0:
            return score
        
        enemy_copy = deepcopy(self.enemy_copy)
        player_copy = deepcopy(self.player_copy)
        if enemy_turn:
            max_score = -float('inf')
            for move in enemy_copy.actions:
                self.player_copy, self.enemy_copy = self.make_move(enemy_copy,move, True)
                score = self.minimax(curr_depth -1, False)
                self.player_copy,self.enemy_copy = player_copy, enemy_copy
                if score > max_score:
                    max_score = score
            return max_score
                
        else:
            min_score = float('inf')
            for move in player_copy.actions:
                self.player_copy,self.enemy_copy = self.make_move(player_copy, move, True)
                score = self.minimax(curr_depth -1, True)
                self.player_copy,self.enemy_copy = player_copy, enemy_copy
                if score < min_score:
                    min_score = score
            return min_score
                       
    def score_calculator(self):
        #calculates minimax score based on hp percentage difference
        player_hp_percentage = 100*self.player_copy.hp//self.player_original.hp
        enemy_hp_percentage = 100*self.enemy_copy.hp//self.enemy_original.hp
        return player_hp_percentage-enemy_hp_percentage

    def check_for_EOC(self, is_testing):
        #checks for EndOfCombat
        if is_testing: curr_player, curr_enemy = self.player_copy, self.enemy_copy
        else: curr_player, curr_enemy = self.player_final, self.enemy_final
        if curr_player.hp<1: 
            print('you lose')
            exit()
        elif curr_enemy.hp<1:
            curr_player.hp = self.player_original.hp
            return True
        else: return False

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
            self.root.contents[0]=room_setup(self.root).enemy_generation()
            self.root.contents[1]=room_setup(self.root).loot_generation()
            print(f'''You have encountered a wild {self.root.contents[0].name}.\n Prepare for battle!''')
            player_char = player()
            encounter_logic(player_char, self.root.contents[0]).start_battle()
            exploration_logic().combat_end(self.root, player_char)

        

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
        