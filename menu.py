import pygame
from legendary_dungeon import *

class menu():
    #startup menu
    def __init__(self):
        pygame.init()
        font = pygame.font.Font(None, 20)
        width, height = 800,800
        screen = pygame.display.set_mode((width, height))

        pygame.display.set_caption('dungeon crawler menu')
        buttons = [button(100,200,'NEW_GAME'), button(350,200,'LOAD'),  button(600,200,'QUIT')]
        running = True
        while True:
            while running:
                for butt in buttons:
                    butt.draw(screen)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT: 
                        running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        for butt in buttons:
                            if butt.is_clicked(mouse_pos):
                                print(f'Button {butt.text} clicked!')
                                if butt.text == 'QUIT':
                                    pygame.quit()
                                    exit()

                            if butt.is_clicked(mouse_pos):
                                print(f'Button {butt.text} clicked!')
                                if butt.text == 'NEW_GAME':
                                    player = construct_player_data().construct(False)
                                    game(True, player)
                
                            if butt.is_clicked(mouse_pos):
                                print(f'Button {butt.text} clicked!')
                                if butt.text == 'LOAD':
                                    player = construct_player_data().construct(True)
                                    game(True, player)
        
menu()