import random
from copy import deepcopy
from game_assets.enemy_assets import *
from game_assets.player import *
from game_assets.map_contents_gen import *

class exploration_logic():
    #general functions for exploration
    def __init__(self):
        self.goal = self.set_completion_goal()
        
    def set_completion_goal(self):
        possible_goals = {
            'explore' : False,
            'execute' : False,
            'boss' : False,
            }
        goal = random.choice(list(possible_goals.keys()))
        return [goal, possible_goals[goal]]

    def check_for_EOE(self, tree, player):
        if player.hp <= 0:
            print('you lose')
            exit()

        if self.update_exploration_status(tree) == True:
            print('goal complete!')
            save_data(player)
            exit()

    def update_exploration_status(self, tree):
        if self.goal[0] == 'explore':
            print('goal explore')
            if (100*tree.explored_room_count)//tree.total_room_count >= 85:
                print('goal complete!')
                exit()
                return True
        elif self.goal[0] == 'execute':
            print('goal execute')
            if tree.enemy_count <= 0:
                print('goal complete!')
                exit()
                return True
        else:
            print('goal boss')
            if tree.enemy_count == -1:
                print('goal complete!')
                exit()
                return True
        return False

    def combat_end(self,node,player):
        chest = room_setup(node).loot_generation()
        player.inventory += chest
        player.curr_xp += 20
        player.update_xp()
        player.mp = 100


class encounter_logic():
    def __init__(self, player_char, enemy_char):
        self.player_char = player_char
        self.enemy_char = enemy_char
        self.MAX_MINIMAX_DEPTH = 4 if enemy_char.name in enemy_tiers().boss_enemy_list else 2

    def start_battle(self, player_move):
        self.make_move(self.player_char, player_move)
        
        if self.enemy_char.name in enemy_tiers().boss_enemy_list:
            enemy_move = self.best_move(True)
            self.make_move(self.enemy_char, enemy_move)
            
        enemy_move = self.best_move(False)
        self.make_move(self.enemy_char, enemy_move)
 
        if self.check_for_EOC():
            return [False, self.enemy_char, self.player_char]
        return [True, self.enemy_char, self.player_char]

    def make_move(self, actor, move):
        if actor.type == 'PLAYER':
            defender = self.enemy_char
        else:
            defender = self.player_char

        if move == 'item':
            if actor.inventory > 0:
                if actor.hp == actor.max_hp:
                    pass #to prevent overhealing
                elif actor.hp + 25*actor.dmg_multiplier <= actor.max_hp:
                    actor.hp += 25*actor.dmg_multiplier
                else:
                    actor.hp = actor.max_hp
            return self.player_char

        moveset = enemy_attacks().attacks_and_skills
        #passive start of turn regeneration
        regen_val = moveset['regenerative'] if 'regenerative' in actor.passives else 0
        if actor.hp == actor.max_hp:
            pass #to prevent overhealing
        elif actor.hp + regen_val <= actor.max_hp:
            actor.hp += regen_val
        else:
            actor.hp = actor.max_hp
        #passive dmg reduction if elusive
        elusive_reduction = 3 if 'elusive' in defender.passives else 0

        if move == 'pass':
            actor.mp += 51
        else:            
            mp_cost = 50*(actor.actions.index(move))
            actor.mp -= mp_cost

            damage = self.calculalte_dmg(actor, move)
            if damage == False:
                #punish for insufficient mana; -1 for computer eval
                if actor.type == 'PLAYER':
                    actor.mp = -1
                else:
                    actor.hp -= 99999999   
            else:
                defender.hp -= damage - elusive_reduction*moveset['elusive']
        return self.player_char, self.enemy_char

    def best_move(self, first_action_of_round):
        player_copy = deepcopy(self.player_char)
        enemy_copy = deepcopy(self.enemy_char)
        best_score = -100
        best_move = 'pass'
        for move in self.enemy_char.actions:
            self.make_move(self.enemy_char, move)
            score = self.minimax(self.MAX_MINIMAX_DEPTH, False, first_action_of_round)
            self.player_char.__dict__ = deepcopy(player_copy.__dict__)
            self.enemy_char.__dict__ = deepcopy(enemy_copy.__dict__)
            if score >= best_score:
                best_score = score
                best_move = move
        print(f'used {best_move}')
        return best_move

    def calculalte_dmg(self, actor, move):
        if actor.mp < 0:
            return False
        poison_dmg = enemy_attacks().attacks_and_skills['poison'] if 'poison' in actor.passives else 0
        dmg_multiplier = actor.dmg_multiplier
        move_dmg = enemy_attacks().attacks_and_skills[move]
        return (move_dmg+poison_dmg) * dmg_multiplier

    def minimax(self, curr_depth, enemy_turn, first_action_of_round): 
        #simulate fight
        score = self.calculate_score()
        if self.check_for_EOC():
            return score
        if curr_depth <= 0:
            return score
        #enables bosses to attack twice in a row
        if self.enemy_char.name in enemy_tiers().boss_enemy_list:
            enemy_turn = True if first_action_of_round == True else False
            first_action_of_round = False if first_action_of_round == True else True

        player_copy = deepcopy(self.player_char.__dict__)
        enemy_copy = deepcopy(self.enemy_char.__dict__)

        if enemy_turn:
            max_score = -100
            for move in self.enemy_char.actions:
                self.make_move(self.enemy_char, move)
                score = self.minimax(curr_depth - 1, False, first_action_of_round)
                self.player_char.__dict__, self.enemy_char.__dict__ = player_copy, enemy_copy
                if score >= max_score:
                    max_score = score
            return max_score
        else:
            min_score = 100
            for move in self.player_char.actions:
                self.make_move(self.player_char, move)
                score = self.minimax(curr_depth - 1, True, first_action_of_round)
                self.player_char.__dict__, self.enemy_char.__dict__ = player_copy, enemy_copy
                if score <= min_score:
                    min_score = score
            return min_score

    def calculate_score(self):
        if self.enemy_char.mp < 0:
            mana_var = 0
        else:
            mana_var = 1
        if self.player_char.mp < 0:
            mana_var_player = 0
        else:
            mana_var_player = 1
        if self.player_char.hp < 1:
            return 100
        
        enemy_hp_percent = (self.enemy_char.hp*100)//self.enemy_char.max_hp
        player_hp_percent = (self.player_char.hp*100)//self.player_char.max_hp
        return mana_var*enemy_hp_percent - mana_var_player*player_hp_percent

    def check_for_EOC(self):
        #checks for EndOfCombat
        if self.enemy_char.hp < 1:
            return True
        elif self.player_char.hp < 1:
            return True
        return False