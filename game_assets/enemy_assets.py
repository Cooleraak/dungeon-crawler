class enemy_tiers():
	def __init__(self):
		self.basic_enemy_list = ('anaconda','crab','cow','crow','demon_small','goblin')
		self.elite_enemy_list = ('bear','demon_big','skeleton','angel','spider')
		self.boss_enemy_list = ('ouroboros','dragon','ophanim','devil')

class enemy_action_properties():
	def __init__(self):
		self.enemy_actions = {
			'anaconda':['teeth'], #done
			'crab':['claws'], #done
			'cow':['teeth','weight'],
			'crow':['claws'],
			'demon_small':['claws','teeth','fire'],
			'goblin':['teeth','claws'], #done
			'bear':['teeth','claws','weight'],
			'demon_big':['claws','fire_big'],
			'skeleton':['punch'],
			'angel':['fire'],
			'spider':['teeth'],
			'ouroboros':['teeth'],
			'dragon':['teeth','claws','fire_big','weight'],
			'ophanim':['weight','fire_big'], #done
			'devil':['claws','fire_big'],
			}
		self.enemy_passive_actions = {
			'anaconda':['poison'],
			'crow':['elusive'],
			'skeleton':['regenerative'],
			'angel':['regenerative','elusive'],
			'spider':['poison','elusive'],
			'ouroboros':['regenerative','poison'],
			'ophanim':['elusive'],
			'devil':['summoner_devil'],
			}

class enemy_stat_properties():
	def __init__(self, level):
		# 'enemy_name' : (hp, dmg_multiplier),
		self.enemy_stats = {
			'anaconda':[1500*(level+1)/level, 5*(level)],
			'crab':[1000*(level+1)/level, 6*(level)],
			'cow':[2000*(level+1)/level, 3*(level)],
			'crow':[1500*(level+1)/level, 6*(level)],
			'demon_small':[1700*(level+1)/level, 6*(level)],
			'goblin':[1000*(level+1)/level, 5*(level)],
			'bear':[3000*(level+1)/level, 8*(level)],
			'demon_big':[2500*(level+1)/level, 9*(level)],
			'skeleton':[1500*(level+1)/level, 9*(level)],
			'angel':[1600*(level+1)/level, 8*(level)],
			'spider':[1700*(level+1)/level, 8*(level)],
			'ouroboros':[5000*(level+1)/level, 11*(level)],
			'dragon':[5000*(level+1)/level, 13*(level)],
			'ophanim':[4000*(level+1)/level, 12*(level)],
			'devil':[4000*(level+1)/level, 12*(level)],
			}

class enemy_attacks():
	def __init__(self): 
		# 'move' : (dmg_raw)
		self.attacks_and_skills = {
			'claws':11,
			'teeth':12,
			'fire':13,
			'weight':10,
			'punch':10,
			'fire_big':20,
		#misc
			'summoner_devil':3,
			
		# 'passive' : potency
			'regenerative':15,
			'elusive':2,
			'poison':1,
			}