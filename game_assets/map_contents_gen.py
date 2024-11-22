import random
from game_assets.enemy_assets import *

class room_setup():
    def __init__(self, node):
        #add types to enemy, player, chest
        self.chest_contents_preview = []   
        self.room = node
        self.room_tier = self.set_room_tier()

    def enemy_generation(self):
        enemy_list = enemy_tiers()
        if self.room_tier == 1: return self.enemy_char(random.choice(enemy_list.basic_enemy_list))
        elif self.room_tier == 3: return self.enemy_char(random.choice(enemy_list.elite_enemy_list))
        elif self.room_tier == 4: return self.enemy_char(random.choice(enemy_list.boss_enemy_list))
        else: return None

    def loot_generation(self):
        if self.room_tier == 0:
            chest = self.chest(0)

        elif self.room_tier == 1: 
            chest = self.chest(1)

        elif self.room_tier == 2:
            chest = self.chest(2)

        elif self.room_tier == 3: 
            chest = self.chest(3)

        else:
            chest = self.chest(4)

        chest.generate_chest_loot()
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
            self.chest_loot=[]
            self.contents_preview = []
    
        def generate_chest_loot(self):
            loot = ['']*self.chest_tier 
            if len(self.contents_preview)<3: self.reset_available_loot()
            for i in range(self.chest_tier):
                rand_loot_index = random.randint(0,len(self.contents_preview)-1)
                loot[i] = self.contents_preview[rand_loot_index]
                self.contents_preview.pop(rand_loot_index)
            self.chest_loot = loot

        def reset_available_loot(self): 
            #adds items instead of reseting to increase the odds of rare items
            rarity = {'common':10, 'rare' : 4, 'epic' : 1}
            self.contents_preview+=['050potion' for _ in range(rarity['common'])] + [
                                    '100potion' for _ in range(rarity['rare'])] + [
                                    '500potion' for _ in range(rarity['epic'])]

    class enemy_char():
        type = 'ENEMY'
        def __init__(self, enemy_name):
            self.name = enemy_name
            self.hp = enemy_stat_properties().enemy_stats[enemy_name][0]
            self.dmg_multiplier = enemy_stat_properties().enemy_stats[enemy_name][1]
            self.actions = enemy_action_properties().enemy_actions[enemy_name]
            try: self.passives = enemy_action_properties().enemy_passive_actions[enemy_name]
            except: self.passives = []