import random
from copy import deepcopy
from game_assets.enemy_assets import *
from game_assets.player import *
from game_assets.map_contents_gen import *

#add boss encounter scenario -> multiple enemy turns, enhanced attacks/passives

class exploration_logic():
    #general functions for exploration
    def __init__(self, player_hp = None):
        self.goal = self.set_completion_goal()
        self.player_hp = player_hp
        

    def set_completion_goal(self):
        possible_goals = {
            'explore' : False,
            'execute' : False,
            'boss' : False,
            }
        goal = random.choice(list(possible_goals.keys()))
        return [goal, possible_goals[goal]]

    def progress_tracker(self):
        pass

    def check_for_EOE(self, tree, player):
        if self.player_hp <= 0:
            print('you lose')
            exit()

        self.goal[1] = self.update_exploration_status(tree)
        if self.goal[1] == True:
            print('goal complete!')
            save_data(player)
            exit()

    def update_exploration_status(self, tree):
        if self.goal == 'explore':
            if (100*tree.explored_room_count//tree.total_room_count) >= 85:
                return True
        elif self.goal == 'execute':
            if tree.enemy_count == 0:
                return True
        else:
            if tree.enemy_count == -1:
                return True
        return False

    def combat_end(self,node,player):
        chest = room_setup(node).loot_generation().chest_loot
        player.inventory += chest
        player.curr_xp += 20
        player.update_xp()


class encounter_logic(): 
    #general functions for battle
    def __init__(self,player_char, enemy_char):
        self.MAX_DEPTH = 2
        self.player_original = player_char
        self.enemy_original = enemy_char
        self.player_final = deepcopy(player_char)
        self.enemy_final = deepcopy(enemy_char)
        self.player_copy = deepcopy(player_char)
        self.enemy_copy = deepcopy(enemy_char)
    
    def start_battle(self, player_move): 
        print(self.enemy_final.mp)
        #player_move = input(f'MP: {self.player_copy.mp}\nChoose action: {self.player_copy.actions}\n')
        if player_move!='item':
            self.make_move(self.player_final, player_move, False)    
        if self.check_for_EOC(False):
            return [False, self.enemy_final, self.player_final]
            
        if self.enemy_original.name in enemy_tiers().boss_enemy_list:
            best_move = self.best_move(True)
            print(self.enemy_original.name,' used ', best_move)
            self.make_move(self.enemy_copy, best_move, False)
            print(f'you:{self.player_final.hp} HP, enemy: {self.enemy_final.hp} HP\n')

        best_move = self.best_move(False)
        print(self.enemy_original.name,' used ', best_move)
        self.make_move(self.enemy_copy, best_move, False)
        print(f'you:{self.player_final.hp} HP, enemy: {self.enemy_final.hp} HP\n')
            
        if self.check_for_EOC(False):
            return [False, self.enemy_final, self.player_final]
        return [True, self.enemy_final, self.player_final]
    
    def calculalte_dmg(self, actor, move):
        if actor.mp < 0: 
            if actor == self.enemy_final or actor == self.player_final:
                print(f'{actor.type}: insufficient mana, nothing happened')
            return False

        poison_dmg = enemy_attacks().attacks_and_skills['poison'] if 'poison' in actor.passives else 0
        dmg_multiplier = actor.dmg_multiplier
        move_dmg = enemy_attacks().attacks_and_skills[move]
        return (move_dmg+poison_dmg) * dmg_multiplier

    def make_move(self,actor, move, is_testing):
        #makes move for game simulation and for real move
        curr_player= deepcopy(self.player_copy) if is_testing else self.player_final
        curr_enemy = deepcopy(self.enemy_copy) if is_testing else self.enemy_final    
        
        defender = curr_player if actor==self.enemy_copy else curr_enemy

        actor.mp += 2*actor.dmg_multiplier
        if actor.mp > 5*actor.dmg_multiplier:
            actor.mp = 5*actor.dmg_multiplier

        if move == 'item':
            if actor.inventory != 0:
                actor.hp += 25*actor.dmg_multiplier
                return curr_player, curr_enemy 
            print('insufficient item')
            return curr_player, curr_enemy
        if move == 'pass':
            return curr_player, curr_enemy
        mp_cost = 10*(actor.actions.index(move)+1)
        actor.mp -= mp_cost

        moveset = enemy_attacks().attacks_and_skills
        #passive start of turn regeneration
        actor.hp += moveset['regenerative'] if 'regenerative' in actor.passives else 0
        
        #passive dmg reduction if elusive
        elusive_reduction = random.randint(2,10) if 'elusive' in defender.passives else 0

        damage = self.calculalte_dmg(actor,move)
        if damage == False:
            actor.mp += mp_cost
            return curr_player, curr_enemy
        defender.hp -= damage - (elusive_reduction*moveset['elusive'])
        
        #returns both characters after acting in case of passive or timer changes
        return curr_player, curr_enemy
        
    def best_move(self, first_action_of_round):
        #finds theorethical best move for computer
        enemy_copy = deepcopy(self.enemy_final)
        max_score = -float('inf')
        best_move = None
        for move in enemy_copy.actions:
            self.player_copy, self.enemy_copy = self.make_move(enemy_copy,move, True)
            score = self.minimax(self.MAX_DEPTH, False, first_action_of_round)
            self.player_copy, self.enemy_copy = self.player_final, self.enemy_final
            if score > max_score:
                max_score = score
                best_move = move
        return best_move

    def minimax(self, curr_depth, enemy_turn, first_action_of_round):
        #simulate fight
        score = self.score_calculator()
        if self.check_for_EOC(True) == True: 
            return score*100000
        if curr_depth == 0:
            return score
        
        enemy_copy = deepcopy(self.enemy_copy)
        player_copy = deepcopy(self.player_copy)

        if enemy_copy.name in enemy_tiers().boss_enemy_list:
            enemy_turn = True if first_action_of_round == True else False
        first_action_of_round = False if first_action_of_round == True else True

        if enemy_turn:
            max_score = -float('inf')
            for move in enemy_copy.actions:
                self.player_copy, self.enemy_copy = self.make_move(enemy_copy,move, True)
                score = self.minimax(curr_depth -1, False, first_action_of_round)
                self.player_copy,self.enemy_copy = player_copy, enemy_copy
                if score > max_score:
                    max_score = score
            return max_score
                
        else:
            min_score = float('inf')
            for move in player_copy.actions:
                self.player_copy,self.enemy_copy = self.make_move(player_copy, move, True)
                score = self.minimax(curr_depth -1, True, True)
                self.player_copy,self.enemy_copy = player_copy, enemy_copy
                if score < min_score:
                    min_score = score
            return min_score
                       
    def score_calculator(self):
        #calculates minimax score based on resource percentage difference
        player_hp_percentage = 100*self.player_copy.hp/self.player_original.hp
        enemy_hp_percentage = 100*self.enemy_copy.hp/self.enemy_original.hp

        player_mp_percentage = 100*self.player_copy.mp/self.player_original.mp
        if self.enemy_original.mp == 0:
            self.enemy_original.mp = 1
        enemy_mp_percentage = 100*self.enemy_copy.mp/self.enemy_original.mp
        
        return (player_hp_percentage - enemy_hp_percentage + 
                player_mp_percentage - enemy_mp_percentage )

    def check_for_EOC(self, is_testing):
        #checks for EndOfCombat
        if is_testing: curr_player, curr_enemy = self.player_copy, self.enemy_copy
        else: curr_player, curr_enemy = self.player_final, self.enemy_final
        if curr_player.hp<1 and curr_player == self.player_final: 
            print('you lose')
            exit()
        elif curr_enemy.hp < 1:
            return True
        elif curr_player == self.player_copy and curr_player.hp < 1:
            return True
        return False