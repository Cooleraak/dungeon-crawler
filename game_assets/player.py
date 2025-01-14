class player():
    type = 'PLAYER'
    def __init__(self, level = 1, moveset = ['punch', 'punch'], passives = ['poison'], item = 3, curr_xp = 0):
        self.level = level
        self.name = "player"
        self.hp = 550*level
        self.max_hp = 550*level
        self.dmg_multiplier = 7*level
        self.mp = 100
        self.actions = ['pass'] + moveset 
        self.passives = passives
        self.inventory = 5
        self.curr_xp = curr_xp
        self.curr_max_xp = 100*level

    def update_xp(self):
        self.curr_xp += 20
        if self.curr_xp >= self.curr_max_xp:
            self.level += 1 if self.level<6 else 0
            self.curr_xp = 0
            self.curr_max_xp = 120*self.level
            if self.level <= 6:
                self.actions =  construct_player_data().curr_moveset(self.level)
                self.passives = construct_player_data().curr_passives(self.level)


class save_data():
    #save player data into a file
    def __init__(self, player):
        with open('game_assets\save.txt','w') as file:
            file.write(f'{player.level} {player.inventory} {player.curr_xp}')
            file.close()


class load_data():
    #loads player data from file
    def __init__(self):
        self.data = None
        with open('game_assets\save.txt','r') as file:
            self.data = file.read().strip().split(' ')
            file.close()

    def get_level(self):
        return int(self.data[0])

    def get_item(self):
        return self.data[1]

    def get_xp(self):
        return self.data[2]


class construct_player_data():
    #inputs player data from load and recovers progress
    def __init__(self):
        self.data = None
        self.player = None
        self.moveset = {1 :'punch',
                        2:'claws',
                        3:'teeth',
                        4:'fire',
                        5:'weight',
                        6:'fire_big'}

        self.passives = {1:'poison',
                         6:'elusive'}

    def construct(self, load):
        if load:
            self.data = load_data()
            level = self.curr_level()
            self.player =  player(level, self.curr_moveset(), self.curr_passives(level), self.curr_item(), self.curr_xp())
        else: 
            self.player =  player()
        return self.player

    def curr_level(self):
        return self.data.get_level()

    def curr_moveset(self, level = None):
        if level ==None:
            level = self.curr_level()
        moveset = [self.moveset[level-1 if level>1 else 1],
                   self.moveset[level] ]
        return moveset

    def curr_passives(self, level):
        if level ==None:
            level = self.curr_level()
        if level < 3: 
            return ['poison']
        elif level < 6: 
            return ['poison','elusive']
        else: 
            return ['poison','elusive',':) nothing'] #got rid of regen on player because pots are available

    def curr_item(self):
        return int(self.data.get_item())

    def curr_xp(self):
        return int(self.data.get_xp())