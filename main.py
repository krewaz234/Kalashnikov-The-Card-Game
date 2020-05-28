import pygame
from pygame.sprite import Sprite
import socket
import time
import threading

class LogoSprite(Sprite):
    def __init__(self, logodir):
        self.image = pygame.image.load(logodir).convert_alpha()

class Card(Sprite):
    def __init__(self, rank, suit):
        image_dir = "cardsprites/" + str(rank) + "_" + str(suit) + ".png"
        self.rank = rank
        self.suit = suit
        self.image = pygame.image.load(image_dir).convert_alpha()
        self.pos_x = 0
        self.pos_y = 0

FPS = 144
CARD_W = 318
CARD_H = 450
respond = "" #respond to the last made request to database
pygame.init()
fullscreen_mode = "ON"
sound_mode = "ON"
dark_mode = "ON"
cursor_light_dir = "cursor_light.png"
cursor_dark_dir = "cursor_dark.png"
cursor_pointer_dark_dir = "cursor_pointer.png"
cursor_pointer_light_dir = "cursor_pointer_light.png"

options_file = open("options.txt", 'r')
for line in options_file:
    param = line[:line.find('=')]
    value = line[line.find('=') + 1:-1]
    if param == "FULLSCREEN":
        fullscreen_mode = value
    if param == "SOUND":
        sound_mode = value
options_file.close()

win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
win_info = pygame.display.Info()
FULLSCREEN_W = win_info.current_w
FULLSCREEN_H = win_info.current_h
if fullscreen_mode == "OFF":
    win = pygame.display.set_mode((1280, 720))
win_info = pygame.display.Info()

cursor_dark             = pygame.image.load(cursor_dark_dir).convert_alpha()
cursor_light            = pygame.image.load(cursor_light_dir).convert_alpha()
cursor_pointer_dark     = pygame.image.load(cursor_pointer_dark_dir).convert_alpha()
cursor_pointer_light    = pygame.image.load(cursor_pointer_light_dir).convert_alpha()

cursor_dark = pygame.transform.scale(cursor_dark, (cursor_dark.get_width() // 5, cursor_dark.get_height() // 5))
cursor_light = pygame.transform.scale(cursor_light, (cursor_light.get_width() // 5, cursor_light.get_height() // 5))
cursor_pointer_dark = pygame.transform.scale(cursor_pointer_dark, (cursor_pointer_dark.get_width() // 4, cursor_pointer_dark.get_height() // 4))
cursor_pointer_light = pygame.transform.scale(cursor_pointer_light, (cursor_pointer_light.get_width() // 5, cursor_pointer_light.get_height() // 5))

pygame.mouse.set_visible(False)

current_cursor = cursor_dark

pygame.display.set_caption("Kalashnikov the Card Game")

clock = pygame.time.Clock()
win_bgcolor = (255, 255, 204)
text_color = (30, 30, 30)

#dark theme
win_bgcolor, text_color = text_color, win_bgcolor

card = Card("queen", "hearts")
logo = LogoSprite("logo_dark_theme.png")

def draw_cursor(cur):
    win.blit(cur, pygame.mouse.get_pos())

def send_request(req):
    global respond
    SERVER_IP = '192.168.50.19'
    REQ_SERVER_PORT = 1024
    sock = socket.socket()
    try:
        sock.connect((SERVER_IP, REQ_SERVER_PORT))
    except ConnectionRefusedError:
        respond = "ERROR"
        print("Theres an error")
        return
        
    sock.send(bytes(req, encoding='utf-8'))
    try:
        respond = sock.recv(1024)
    except Exception:
        respond = "ERROR"
        return
    sock.close()
    respond = str(respond)[2:-1]

def pr():
    for i in range(5):
        print(i)
        time.sleep(.5)

def main_menu():
    time.sleep(.3)
    global win
    global current_cursor
    pr1 = threading.Thread(target=pr)
    pr1.start()
    while True:
        click = False
        if dark_mode == "ON":
            current_cursor = cursor_dark
        else:
            current_cursor = cursor_light
        win.fill(win_bgcolor)

        win.blit(logo.image, (win_info.current_w // 2 - logo.image.get_width() // 2, 50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    click = True

        #START BUTTON
        font = pygame.font.Font("Bevan.ttf", 56)
        textsprite = font.render("Start!", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 - 100, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                select_search()
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 - 100))
        ###########################################################################################################

        #OPTIONS BUTTON
        textsprite = font.render("Options", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                options()
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2))
        ##############################################################################################################

        #QUIT BUTTON
        textsprite = font.render("Quit", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 + 100, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                pr1.join()
                return
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 + 100))
        ################################################################################################################

        draw_cursor(current_cursor)
        pygame.display.update()
        clock.tick(FPS)
    pr1.join()

def select_search():
    time.sleep(.3)
    global win
    font = pygame.font.Font("Bevan.ttf", 56)

    while True:
        win.fill(win_bgcolor)
        if dark_mode == "ON":
            current_cursor = cursor_dark
        else:
            current_cursor = cursor_light
        click = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        textsprite = font.render("Find a game", 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, 50))
        #FIND A RANDOM GAME
        textsprite = font.render("Find a random player", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 - 100, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                random_player_search()
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2 - 100))
        ###############################################################################################################
        
        #PLAY WITH FRIEND
        textsprite = font.render("Play with comrade", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                play_with_friend()
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h // 2))
        ###############################################################################################################
        #BACK BUTTON
        textsprite = font.render("Back", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                return
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200))
        ###############################################################################################################
        draw_cursor(current_cursor)
        pygame.display.update()
        clock.tick(FPS)

def random_player_search():
    pass

def play_with_friend():
    time.sleep(.3)
    font = pygame.font.Font("Bevan.ttf", 56)
    while True:
        win.fill(win_bgcolor)
        if dark_mode == "ON":
            current_cursor = cursor_dark
        else:
            current_cursor = cursor_light

        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True
        
        #PLAY WITH FRIEND
        textsprite = font.render("Play with comrade", 1, text_color)
        win.blit(textsprite, (((win_info.current_w - textsprite.get_width()) // 2, 50)))
        ###########################################################################################################

        margin_from_center_x = 300
        #HOST THE GAME BUTTON
        textsprite = font.render("Host the game", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2 - margin_from_center_x, win_info.current_h // 2, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                host_the_game()
    
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 - margin_from_center_x, win_info.current_h // 2))
        ####################################################################################################################
        
        #JOIN THE GAME BUTTON
        textsprite = font.render("Join the game", 1, text_color)
        textsprite_rect = pygame.Rect((win_info.current_w - textsprite.get_width()) // 2 + margin_from_center_x, win_info.current_h // 2, textsprite.get_width(), textsprite.get_height())
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                join_the_game()
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 + margin_from_center_x, win_info.current_h // 2))
        ###############################################################################################################

        #BACK BUTTON
        textsprite = font.render("Back", 1, (text_color))
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 300, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                return

        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 300))
        ###################################################################################################################

        draw_cursor(current_cursor)
        pygame.display.update()
        clock.tick(FPS)

def host_the_game():
    time.sleep(.3)
    global respond
    netThread = threading.Thread(target=send_request, args=("CREATE",))
    netThread.start()
    font = pygame.font.Font("Bevan.ttf", 56)
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if respond != "ERROR" and respond != "":
                        send_request("DELETE " + respond)
                    respond = ""
                    netThread.join()
                    return
            if event.type == pygame.QUIT:
                netThread.join()
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        win.fill(win_bgcolor)

        if dark_mode == "ON":
            current_cursor = cursor_dark
        else:
            current_cursor = cursor_light

        if respond == "":
            draw_cursor(current_cursor)
            pygame.display.update()
            clock.tick(FPS)
            continue

        if respond == "ERROR":
            textsprite = font.render("An error occured. Try again later", 1, text_color)
            win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, (win_info.current_h - textsprite.get_height()) // 2))
            draw_cursor(current_cursor)
            pygame.display.update()
            clock.tick(FPS)
            continue

        #LOBBY ID TEXT
        textsprite = font.render("Lobby ID: " + respond, 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, (win_info.current_h - textsprite.get_height()) // 2 + 75//2))
        #################################################################################################################################

        textsprite = font.render("Waiting for your friend to join...", 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, (win_info.current_h - textsprite.get_height()) // 2 - 75//2))

        #BACK BUTTON
        textsprite = font.render("Back", 1, (text_color))
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                send_request("DELETE " + respond)
                netThread.join()
                respond = ""
                return
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200))
        ###########################################################################################################################################

        draw_cursor(current_cursor)
        pygame.display.update()
        clock.tick(FPS)


def join_the_game():
    pass

def options():
    time.sleep(.3)
    global win
    global win_info
    global fullscreen_mode
    global sound_mode
    global logo
    global dark_mode
    global text_color
    global win_bgcolor
    global current_cursor
    font = pygame.font.Font("Bevan.ttf", 56)
    while True:
        click = False
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        win.fill(win_bgcolor)
        if dark_mode == "ON":
            current_cursor = cursor_dark
        else:
            current_cursor = cursor_light
        
        #WE ARE IN OPTIONS
        textsprite = font.render("Options", 1, text_color)
        win.blit(textsprite, (((win_info.current_w - textsprite.get_width()) // 2, 50)))
        ####################################

        #WINDOW MODE LABEL
        textsprite = font.render("Fullscreen mode:", 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 - 250, win_info.current_h // 2 - 200))
        ####################################################################################################################

        #ON/OFF SWITCH
        textsprite = font.render(fullscreen_mode, 1, text_color)
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2 - 200, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                lfile = []
                f = open("options.txt", "r")
                for line in f:
                    lfile.append(line[:-1])
                if fullscreen_mode == "ON":
                    lfile[0] = "FULLSCREEN=OFF"
                    fullscreen_mode = "OFF"
                    win = pygame.display.set_mode((1280, 720))
                    win_info = pygame.display.Info()
                else:
                    lfile[0] = "FULLSCREEN=ON"
                    fullscreen_mode = "ON"
                    win = pygame.display.set_mode((FULLSCREEN_W, FULLSCREEN_H), pygame.FULLSCREEN)
                    win_info = pygame.display.Info()
                f.close()
                f = open("options.txt", "w")
                for i in lfile:
                    f.write(i + '\n')
                f.close()

        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2 - 200))
        ####################################################################################################################
        
        #SOUND ON/OFF LABEL
        textsprite = font.render("Sounds:", 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 - 250, win_info.current_h // 2 - 100, textsprite.get_width(), textsprite.get_height()))
        ###################################################################################################################
        
        #ON/OFF SWITCH
        textsprite = font.render(sound_mode, 1, text_color)
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2 - 100, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                lfile = []
                f = open("options.txt", "r")
                for line in f:
                    lfile.append(line[:-1])
                if sound_mode == "ON":
                    lfile[1] = "SOUND=OFF"
                    sound_mode = "OFF"
                else:
                    lfile[1] = "SOUND=ON"
                    sound_mode = "ON"
                f.close()
                f = open("options.txt", "w")
                for i in lfile:
                    f.write(i + '\n')
                f.close()

        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2 - 100))
        ####################################################################################################################


        #DARK THEME SWITCH
        textsprite = font.render("Dark theme:", 1, text_color)
        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 - 250, win_info.current_h // 2))
        ####################################################################################################################

        #ON/OFF SWITCH
        textsprite = font.render(dark_mode, 1, text_color)
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                if dark_mode == "ON":
                    dark_mode = "OFF"
                    logo = LogoSprite("logo.png")
                    text_color, win_bgcolor = win_bgcolor, text_color
                    current_cursor = cursor_light
                    
                else:
                    dark_mode = "ON"
                    logo = LogoSprite("logo_dark_theme.png")
                    text_color, win_bgcolor = win_bgcolor, text_color
                    current_cursor = cursor_dark

        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2 + 250, win_info.current_h // 2))
        ##################################################################################################################

        #BACK BUTTON
        textsprite = font.render("Back", 1, (text_color))
        textsprite_rect = pygame.Rect(((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200, textsprite.get_width(), textsprite.get_height()))
        if textsprite_rect.collidepoint(pygame.mouse.get_pos()):
            button_bgcolor = (win_bgcolor[0] - 30, win_bgcolor[1] - 30, win_bgcolor[2] - 30)
            pygame.draw.rect(win, button_bgcolor, textsprite_rect)
            if current_cursor == cursor_dark:
                current_cursor = cursor_pointer_dark
            else:
                current_cursor = cursor_pointer_light
            if click:
                return

        win.blit(textsprite, ((win_info.current_w - textsprite.get_width()) // 2, win_info.current_h - 200))
        ###################################################################################################################

        draw_cursor(current_cursor)
        pygame.display.update()
        clock.tick(FPS)

main_menu()
pygame.quit()

# while run:

#     win.fill(win_bgcolor)
#     if current_menu == "main_menu":
#         win.blit(logo.image, (win_info.current_w // 2 - 492 // 2, 50))
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     if pygame.mouse.get_pressed()[0]:
#         card.pos = pygame.mouse.get_pos()
#         card.pos_x = pygame.mouse.get_pos()[0] - CARD_W // 2
#         card.pos_y = pygame.mouse.get_pos()[1] - CARD_H // 2
#     win.blit(card.image, (card.pos_x, card.pos_y))
# pygame.quit()
