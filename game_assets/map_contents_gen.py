import random
from game_assets.enemy_assets import *
from game_assets.player import load_data as load

class room_setup():
    def __init__(self, node):
        #add tiers, enemy, chest to rooms  
        self.room = node
        self.room_tier = self.set_room_tier()

    def enemy_generation(self):
        enemy_list = enemy_tiers()
        if self.room_tier == 1 or self.room_tier == 0: return self.enemy_char(random.choice(enemy_list.basic_enemy_list))
        elif self.room_tier == 3: return self.enemy_char(random.choice(enemy_list.elite_enemy_list))
        elif self.room_tier == 4: return self.enemy_char(random.choice(enemy_list.boss_enemy_list))

    def loot_generation(self):
        if self.room_tier == 0:
            chest = self.chest(1)

        elif self.room_tier == 1: 
            chest = self.chest(2)

        elif self.room_tier == 2:
            chest = self.chest(3)

        elif self.room_tier == 3: 
            chest = self.chest(4)

        else:
            chest = self.chest(5)
        return chest

    def set_room_tier(self):
        room = self.room.node_type
        if room == 'nothing': return 0
        elif room == 'basic_enemy': return 1
        elif room == 'reward': return 2
        elif room == 'elite_enemy': return 3
        else: return 4


    class chest():
        type = 'CHEST'
        def __init__(self, room_type):
            self.chest_tier = room_type
            self.chest_loot= room_type
            

    class enemy_char():
        type = 'ENEMY'
        def __init__(self, enemy_name):
            stats = enemy_stat_properties(load().get_level())
            actions = enemy_action_properties()
            self.name = enemy_name
            self.hp = stats.enemy_stats[enemy_name][0]
            self.max_hp = self.hp
            self.dmg_multiplier = stats.enemy_stats[enemy_name][1]
            self.mp = 100
            self.actions = ['pass'] + actions.enemy_actions[enemy_name]
            try: self.passives = actions.enemy_passive_actions[enemy_name]
            except: self.passives = []