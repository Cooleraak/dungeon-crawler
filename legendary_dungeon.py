from game_assets.enemy_assets import *
from game_assets.game_logic import *
from game_assets.map_contents_gen import *
from game_assets.map_layout_gen import *
from game_assets.player import *
import pygame


class button():
        def __init__(self, x, y, text, width = 75, height = 30):
            self.font = pygame.font.Font(None, 20)
            self.rect = pygame.Rect(x, y, width, height)
            self.text = text
            self.color = 'black'
            self.text_color = 'white'

        def draw(self, surface):
            # Draw the button
            pygame.draw.rect(surface, self.color, self.rect)
            # Render and position the text
            text_surface = self.font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

        def is_clicked(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

class game():
    def __init__(self, start, player):
        if start:
            goal = exploration_logic().set_completion_goal()
            print(f'your goal is: {goal}')
            tree = game_map_generation(goal[0])
            tree.generate_map()

            pygame.init()

            width, height = 800,800
            self.screen = pygame.display.set_mode((width, height))
            pygame.display.set_caption('dungeon crawler')
            background_image = pygame.image.load('game_assets/visual_assets/basic_room_sprite.png')

            # Scale the image to fit the window size
            self.background_image = pygame.transform.scale(background_image, (width, height))

            self.player = player
            self.tree = tree
            self.root = self.tree.root
            self.combat_buttons = [button(0, 770, 'ATK'), button(76, 770,'SPELL'), button(152, 770,'ITEM'), button(223, 770,'QUIT')]
            self.exploration_buttons = [button(0, 770,'QUIT'), button(240, 200, f'{self.root.child_left.node_type}'), button(410, 190, f'{self.root.child_left.node_type}'),button(300, 350, 'back')]
            self.exploration_on_screen_load()
            pygame.quit()
        
    def encounter_on_screen_load(self, player_char):
        combat = True
        while combat:
            running = True
            while running:

                curr_buttons = self.combat_buttons 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        running = False
    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            for butt in curr_buttons:
                                if butt.is_clicked(mouse_pos):
                                    print(f'Button {butt.text} clicked!')
                                    if butt.text == 'QUIT':
                                        save_data(player_char)
                                        exit()

                                    elif butt.text == 'ATK':
                                        move = player_char.actions[0]
                                        running = False
                                    elif butt.text == 'SPELL':
                                        move = player_char.actions[1]
                                        running = False
                                    elif butt.text[0:3] == 'ITEM':
                                        encounter_logic(player_char, self.root.contents[0]).make_move(player_char, 'item', False)
                                        player_char.inventory -= 1

                #bg image load
                self.screen.blit(self.background_image, (0, 0))
                for butt in curr_buttons:
                    butt.draw(self.screen)
                # Update the display
                #enemy_image = pygame.image.load("game_assets\visual_assets\goblin_sprite.png").convert_alpha() 
                enemy_image = pygame.image.load('game_assets/visual_assets/spider_sprite.png').convert_alpha()
                enemy_image = pygame.transform.scale(enemy_image, (300, 300))
                self.screen.blit(enemy_image, (280, 300))
                pygame.display.flip()
            battle = encounter_logic(player_char, self.root.contents[0]).start_battle(move)
            player_char = battle[2]
            self.root.contents[0] = battle[1]
            combat = battle[0]

    def exploration_on_screen_load(self):
        player_char = self.player
        while True:
            left = self.root.child_left.node_type if self.root.child_left != None else "wall"
            right = self.root.child_right.node_type if self.root.child_right != None else "wall"
            self.exploration_buttons = [button(0, 770,'QUIT'), button(240, 200, f'{left}' ), button(410, 190, f'{right}'),button(300, 350, 'back')]
            curr_buttons = self.exploration_buttons
            running = True
            destination = None
            while running:

                #bg image load
                self.screen.blit(self.background_image, (0, 0))
    
                for butt in curr_buttons:
                    butt.draw(self.screen)
                # Update the display
                pygame.display.flip()
                #checks if any event happened
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        running = False
    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = event.pos
                            for butt in curr_buttons:
                                if butt.is_clicked(mouse_pos):
                                    print(f'Button {butt.text} clicked!')
                                    if butt.text == 'QUIT':
                                        save_data(player_char)
                                        exit()

                                    elif butt.text == f'{left}':
                                        child_left = self.root.child_left
                                        if child_left != None:
                                            self.root = child_left
                                        running = False

                                    elif butt.text == f'{right}':
                                        child_right = self.root.child_right
                                        if child_right != None:
                                            self.root = child_right
                                        running = False

                                    elif butt.text == 'back':
                                        parent = self.root.parent
                                        if parent == None:
                                            self.root = self.root
                                        else:
                                            self.root = parent
                                        running = False

            if self.root.node_type not in ['nothing', 'reward', 'entrance', 'already explored']:
                self.root.contents[0]=room_setup(self.root).enemy_generation()
                self.root.contents[1]=room_setup(self.root).loot_generation()
                #print(f'''You have encountered a wild {self.traversal.root.contents[0].name}.\n Prepare for battle!''')
                self.encounter_on_screen_load(player_char)
            
                exploration_logic().combat_end(self.root, player_char)

                self.tree.enemy_count -= 1
                if self.root.node_type == 'boss':
                    self.enemy_count = -1
            self.tree.explored_room_count += 1
            if self.root.data != 1: 
                self.root.node_type = "already explored"
            exploration_logic(player_char.hp).check_for_EOE(self.tree, player_char)