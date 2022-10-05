import pygame, sys
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("Assets/Image/background.png")
LOGO = pygame.image.load("Assets/Image/logo.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("Assets/font.ttf", size)

def play():
    pass
        
def how_to_play():
    HOW_TO_PLAY_IM = pygame.image.load("Assets/Image/howto.png")
    OPTIONS_BACK = Button(image=None, pos=(90, 60), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

    while True:
        SCREEN.blit(HOW_TO_PLAY_IM, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

    
def about():
    ABOUT_IM = pygame.image.load("Assets/Image/credit.png")
    OPTIONS_BACK = Button(image=None, pos=(90, 60), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")
    
    while True:
        SCREEN.blit(ABOUT_IM, (0, 0))
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(LOGO, (184, 20))

        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(332, 400), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOW_TO_PLAY_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(947, 400), 
                            text_input="HOW TO PLAY", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        ABOUT_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(332, 550), 
                            text_input="ABOUT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Image/rect.png"), pos=(947, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, HOW_TO_PLAY_BUTTON, ABOUT_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if HOW_TO_PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    how_to_play()
                if ABOUT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    about()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()