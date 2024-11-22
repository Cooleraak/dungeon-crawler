#ADD INVENTORY FOR PLAYER

class player():
    def __init__(self):
        data = construct_player_data()
        level, moveset, passives = data.curr_level(), data.curr_moveset(), data.curr_passives() 

        self.name = "player"
        self.hp = 100*level
        self.dmg_multiplier = 2*level
        self.actions = moveset
        self.passives = passives
        self.inventory = {'050potion':0,
                          '100potion':0,
                          '500potion':0,
            }
        self.curr_xp = 0
        self.curr_max_xp = 100*level


class save_data():
    def __init__(self, player):
        pass #save player data into file

class load_data():
    def __init__(self):
        pass #open file and read data

class construct_player_data():
    def __init__(self):
        #inputs player data from load and recovers progress
        self.level = self.curr_level()
        self.moveset = {1 :'punch',
                        2:'claws',
                        3:'teeth',
                        4:'fire',
                        5:'weight',
                        6:'fire_big'}

        self.passives = {1:'poison',
                         3:'regenerative',
                         6:'elusive',}

    def curr_level(self):
        try:
            with open('game_assets\save.txt','r') as file:
                return int(file.read(1))
        except: return 1
                
    def curr_moveset(self):
        moveset = [self.moveset[self.level-1 if self.level>1 else 1],
                   self.moveset[self.level] ]
        return moveset

    def curr_passives(self):
        if self.level <3: return ['poison']
        elif self.level <6: return ['poison','regenerative']
        else: return ['poison','regenerative','elusive']