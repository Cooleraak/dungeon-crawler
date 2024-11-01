class enemy_action_properties():
	def __init__(self):
		self.basic_enemy_action_properties = {
			'anaconda':('teeth','poison'),
			'crab':('claws'),
			'cow':('teeth','weigth'),
			'crow':('claws'),
			'demon_small':('claws','teeth','fire'),
			'goblin':('teeth','claws'),
			}

		self.elite_enemy_action_properties = {
			'bear':('teeth','claws','weigth'),
			'demon_big':('claws','fire_big'),
			'skeleton':('regenerative','punch'),
			'angel':('regenerative','elusive','fire'),
			'spider':('poison','teeth','elusive'),
			}

		self.boss_enemy_action_properties = {
			'ouroboros':('regenerative','teeth','poison'),
			'dragon':('teeth','claws','fire_big','weight'),
			'ophanim':('elusive','weight','fire_big'),
			'devil':('claws','fire_big','summoner_devil'),
			}

class enemy_stat_properties():
	def __init__(self):
		self.basic_enemy_action_properties = {
			'anaconda':(100, 5),
			'crab':(50, 10),
			'cow':(150, 3),
			'crow':(30, 10),
			'demon_small':(70, 10),
			'goblin':(70, 5),
			}

		self.elite_enemy_action_properties = {
			'bear':(150, 15),
			'demon_big':(120, 20),
			'skeleton':(70, 20),
			'angel':(80, 15),
			'spider':(90, 15),
			}

		self.boss_enemy_action_properties = {
			'ouroboros':(500, 30),
			'dragon':(500, 30),
			'ophanim':(300, 40),
			'devil':(300, 40),
			}

class enemy_attacks():
	def __init__(self):
		self.basic_attacks = {
			'claws':(),
			'teeth':(),
			'weight':(),
			}

		self.basic_skills = {
			'fire':(),
			'poison':(),
			}

		self.elite_skills = {
			'fire_big':(),
			'summoner_devil':(),
			}

		self.passive_skills = {			
			'regenerative':(),
			'elusive':(),
			}