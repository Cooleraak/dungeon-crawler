class enemy_tiers():
	def __init__(self):
		self.basic_enemy_list = ('anaconda','crab','cow','crow','demon_small','goblin')
		self.elite_enemy_list = ('bear','demon_big','skeleton','angel','spider')
		self.boss_enemy_list = ('ouroboros','dragon','ophanim','devil')

class enemy_action_properties():
	def __init__(self):
		self.enemy_actions = {
			'anaconda':['teeth'],
			'crab':['claws'],
			'cow':('teeth','weight'),
			'crow':['claws'],
			'demon_small':('claws','teeth','fire'),
			'goblin':('teeth','claws'),
			'bear':('teeth','claws','weight'),
			'demon_big':('claws','fire_big'),
			'skeleton':['punch'],
			'angel':['fire'],
			'spider':['teeth'],
			'ouroboros':['teeth'],
			'dragon':('teeth','claws','fire_big','weight'),
			'ophanim':('weight','fire_big'),
			'devil':('claws','fire_big'),
			}

		self.enemy_passive_actions = {
			'anaconda':['poison'],
			'crow':['elusive'],
			'skeleton':['regenerative'],
			'angel':('regenerative','elusive'),
			'spider':('poison','elusive'),
			'ouroboros':('regenerative','poison'),
			'ophanim':['elusive'],
			'devil':['summoner_devil'],
			}

class enemy_stat_properties():
	def __init__(self):
		# 'enemy_name' : (hp, dmg_multiplier),
		self.enemy_stats = {
			'anaconda':[1000, 5],
			'crab':[500, 6],
			'cow':[1500, 3],
			'crow':[300, 6],
			'demon_small':[700, 6],
			'goblin':[700, 5],
			'bear':[1500, 8],
			'demon_big':[1200, 9],
			'skeleton':[700, 9],
			'angel':[800, 8],
			'spider':[900, 8],
			'ouroboros':[5000, 11],
			'dragon':[5000, 11],
			'ophanim':[3000, 12],
			'devil':[3000, 12],
			}

class enemy_attacks():
	def __init__(self): 
		# 'move' : (dmg_raw)
		self.attacks_and_skills = {
			'claws':11,
			'teeth':12,
			'fire':13,
			'weight':14,
			'punch':10,
			'fire_big':15,
		#misc
			'summoner_devil':3,
			
		# 'passive' : potency
			'regenerative':3,
			'elusive':2,
			'poison':1,
			}