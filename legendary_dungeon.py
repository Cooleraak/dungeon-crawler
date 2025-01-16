from game_assets.enemy_assets import *
from game_assets.game_logic import *
from game_assets.map_contents_gen import *
from game_assets.map_layout_gen import *
from game_assets.player import *
import pygame
import random


class button():
    def __init__(self, x, y, text, bg_images=None, width=75, height=30):
        self.x = x
        self.font = pygame.font.Font(None, 20)
        self.rect = pygame.Rect(x, y, width if not bg_images else 150, height if not bg_images else 300)
        self.text = text
        self.text_color = 'white'
        self.bg_images = [pygame.image.load(f'game_assets/visual_assets/{img}_sprite.png').convert_alpha() for img in (bg_images) or []]
        # Scale all images to the button size
        for i in range(len(self.bg_images)):
            self.bg_images[i] = pygame.transform.scale(self.bg_images[i], (150, 300))

    def draw(self, surface):
        # Draw each background layer
        for img in self.bg_images:
            surface.blit(img, self.rect.topleft)

        # Render and position the text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


class game():
    def __init__(self, start, player):
        if start:
            self.logic = exploration_logic()
            self.logic.set_completion_goal()
            print(f'your goal is: {self.logic.goal}')
            tree = game_map_generation(self.logic.goal[0])
            tree.generate_map()

            pygame.init()

            width, height = 800,800
            self.screen = pygame.display.set_mode((width, height))
            self.font = pygame.font.Font(None, 20)
            pygame.display.set_caption('dungeon crawler')
            background_image = pygame.image.load('game_assets/visual_assets/basic_room_sprite.png')

            # Scale the image to fit the window size
            self.background_image = pygame.transform.scale(background_image, (width, height))

            self.player = player
            self.tree = tree
            self.root = self.tree.root
            self.combat_buttons = [button(0, 770, 'ATK'), button(76, 770,'SPELL'), button(152, 770,'ITEM'), button(223, 770,'MANA'), button(299, 770,'QUIT')]
            self.exploration_buttons = [button(0, 770,'QUIT'), button(240, 200, f'{self.root.child_left.node_type}',), button(410, 190, f'{self.root.child_left.node_type}'),button(300, 350, 'back')]
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
                                        exit()

                                    elif butt.text == 'ATK':
                                        move = player_char.actions[1]
                                        running = False
                                    elif butt.text == 'SPELL':
                                        move = player_char.actions[2]
                                        running = False
                                    elif butt.text == 'ITEM':
                                        if player_char.inventory > 0:
                                            player_char = encounter_logic(player_char, self.root.contents[0]).make_move(player_char, 'item')
                                            player_char.inventory -= 1
                                            self.screen.blit(self.font.render(f'HP: {player_char.hp} - ITEM: {player_char.inventory} - MP: {player_char.mp}' , True, 'white'), (0,760))
                                            pygame.display.flip()
                                    elif butt.text == 'MANA':
                                        move = 'pass'
                                        running = False


                #bg image load
                self.screen.blit(self.background_image, (0, 0))
                for butt in curr_buttons:
                    butt.draw(self.screen)

                enemy_stats = self.font.render(f'ENEMY HP: {self.root.contents[0].hp}: ENEMY MP: {self.root.contents[0].mp}' , True, 'white')
                # Update the display
                try:
                    enemy_image = pygame.image.load(f'game_assets/visual_assets/{self.root.contents[0].name}_sprite.png').convert_alpha()
                except:
                    enemy_image = pygame.image.load(f'game_assets/visual_assets/goblin_sprite.png').convert_alpha()
                enemy_image = pygame.transform.scale(enemy_image, (300, 300))
                self.screen.blit(enemy_image, (280, 300))
                self.screen.blit(enemy_stats, (280, 270))
                self.screen.blit(self.font.render(f'HP: {player_char.hp} - ITEM: {player_char.inventory} - MP: {player_char.mp}' , True, 'white'), (0,760))
                pygame.display.flip()
            battle = encounter_logic(player_char, self.root.contents[0]).start_battle(move)
            self.player = battle[2]
            self.root.contents[0] = battle[1]
            combat = battle[0]

    def exploration_on_screen_load(self):
        player_char = self.player
        main_loop = True
        while main_loop:
            self.logic.check_for_EOE(self.tree, player_char)
            if self.root.child_left != None:
                if self.root.child_left.parent == self.root:
                    if self.root.child_left.contents[2]!='nothing':
                        left = [self.root.child_left.node_type, self.root.child_left.contents[2]]
                    else:
                        left = [self.root.child_left.node_type]
                else:
                    if self.root.child_left.contents[2]=='portal':
                        left = [self.root.child_left.node_type, 'portal']
            else: left = ['wall']
            if self.root.child_right != None:
                if self.root.child_right.parent == self.root:
                    if self.root.child_right.contents[2]!='nothing':
                        right = [self.root.child_right.node_type, self.root.child_right.contents[2] ]
                    else:
                        right = [self.root.child_right.node_type]
                else:
                    if self.root.child_right.contents[2]=='portal':
                        right = [self.root.child_right.node_type, 'portal']
            else: right = ['wall']

            self.exploration_buttons = [button(0, 770,'QUIT'), button(210, 100, '', left ), button(380, 90, '', right),button(300, 380, '', ['back'])]
            curr_buttons = self.exploration_buttons
            running = True
            destination = None
            print('----------------------------------')
            print('explored',self.tree.explored_room_count, ':', 'total',self.tree.total_room_count)
            print('needed enemies ',self.tree.enemy_count)
            print('----------------------------------')
            while running:
                #bg image load
                self.screen.blit(self.background_image, (0, 0))
    
                for butt in curr_buttons:
                    butt.draw(self.screen)
                self.screen.blit(self.font.render(f'HP: {self.player.hp} : ITEM: {self.player.inventory}' , True, 'white'), (0,760))
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

                                    elif butt.x == 210:
                                        child_left = self.root.child_left
                                        if child_left != None:
                                            if child_left.contents[2] == 'trap':
                                                player_char.hp -= 100
                                                child_left.contents[2] = 'nothing'
                                            self.root = child_left
                                            self.tree.explored_room_count += 1
                                        running = False

                                    elif butt.x == 380:
                                        child_right = self.root.child_right
                                        if child_right != None:
                                            if child_right.contents[2] == 'trap':
                                                player_char.hp -= 100
                                                child_right.contents[2] = 'nothing'
                                            self.root = child_right
                                            self.tree.explored_room_count += 1
                                        running = False

                                    elif butt.x == 300:
                                        parent = self.root.parent
                                        if parent == None:
                                            self.root = self.root
                                        else:
                                            self.root = parent
                                        running = False
            
            if self.root.node_type not in ['nothing', 'reward', 'entrance', 'already_explored']:
                self.root.contents[0]=room_setup(self.root).enemy_generation()
                self.root.contents[1]=room_setup(self.root).loot_generation()
                
                self.encounter_on_screen_load(player_char)
                self.logic.combat_end(self.root, player_char)
                self.tree.enemy_count -= 1
                if self.root.node_type == 'boss':
                    self.enemy_count = -1
                self.logic.check_for_EOE(self.tree, player_char)
            
            
            if self.root.node_type == 'nothing':
                choices = ['nothing', 'enemy', 'reward']
                choice = random.choice(choices)
                if choice == 'enemy':
                    self.root.contents[0]=room_setup(self.root).enemy_generation()
                    self.encounter_on_screen_load(player_char)
                    self.logic.combat_end(self.root, player_char)

                elif choice == 'reward':
                    self.root.contents[1]=room_setup(self.root).loot_generation()
                    self.logic.combat_end(self.root, player_char)
            if self.root.node_type == 'reward':
                self.root.contents[1]=room_setup(self.root).loot_generation()
                self.logic.combat_end(self.root, player_char)

            if self.root.data != 1: 
                self.root.node_type = "already_explored"
                if self.root.node_type != 'already_explored':
                    self.tree.explored_room_count += 1
            self.logic.check_for_EOE(self.tree, player_char)
<<<<<<< HEAD
            pygame.display.flip()
=======
            pygame.display.flip()
>>>>>>> 399e69fbd8ec1df89cbae4aa9e27215b52a2ae67
