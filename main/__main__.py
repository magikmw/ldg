#! /usr/bin/env python2
# -*- coding: utf-8 -*-

"""Small laz0r dodging game."""

#Copyright (c) 2012, Michał Walczak
#All rights reserved.

#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#
#Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.

#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
#ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
#LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
#CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
#GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
#OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

################################
# LOGGER INITIALIZATION        #
################################

import logging

# create a logger
logg = logging.getLogger('Main')
logg.setLevel(logging.DEBUG)

# create a handler and set level
logg_ch = logging.StreamHandler()
logg_fh = logging.FileHandler('ldg.log', mode='a', encoding=None, delay=False)
logg_ch.setLevel(logging.INFO)
logg_fh.setLevel(logging.DEBUG)

# crate a formatter and add it to the handler
# [HH:MM:SS AM][LEVEL] Message string
logg_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%I:%M:%S')
logg_ch.setFormatter(logg_formatter)
logg_fh.setFormatter(logg_formatter)

# add ch to logger
logg.addHandler(logg_ch) #console handler at level INFO
logg.addHandler(logg_fh) #file handler at level DEBUG for more detail

# ready to go!
# logging convention:
# logg.debug('') for variable passing
# logg.info('') for standard initialization messages
# logg.warn('') for known errors and caught exceptions
# logg.error('') for something that shouldn't happen
# logg.critical('') for breakage errors

logg.info('Logging initialized.')

################################
# MODULE IMPORT                #
################################

logg.info('Module import initialized.')
import libtcodpy as libtcod #libtcod import, and rename
logg.debug('libTCOD initialized')

logg.info('All modules imported succesfully.')

################################
# CONSTANTS                    #
################################

logg.info('Constants initialization.')

#tile
WINDOW_TITLE = 'LDG'
GAME_TITLE = 'Laz0r Dodging Game'
VERSION = '0.2'

#DEBUG

#FPS maximum
LIMIT_FPS = 20

#console size
SCREEN_WIDTH = 18
SCREEN_HEIGHT = 64

#on-screen map size within above
MAP_WIDTH = 18
MAP_HEIGHT = 60

#info panel size
PANEL_HEIGHT = 2

#Colors
color_ground_f = libtcod.white
color_ground_b = libtcod.grey * 0.3
color_wall_f = libtcod.light_blue * libtcod.silver * 1.5
color_wall_b = libtcod.grey * 0.3
color_player = libtcod.green
color_player_dead = libtcod.white
color_cannons = libtcod.yellow * libtcod.red * 1.5
color_point = libtcod.gold
color_laser_1 = libtcod.red
color_laser_2 = libtcod.blue
color_laser_3 = libtcod.green
color_menu_text = libtcod.lighter_grey * 1.5
color_menu_highlight_b = libtcod.darker_grey

logg.info('Constants initialization finished.')

################################
# CLASSES                      #
################################

logg.info('Classes initialization.')

class Gamestate():
    """The main state class"""
    def __init__(self):
        
        logg.info('Main loop initialization.')

        logg.debug('Font size set to 8')
        libtcod.console_set_custom_font('main/terminal8x8_gs_ro.png',
            libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GRAYSCALE)

        logg.debug('Main console initialization.')
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
            WINDOW_TITLE + ' v.' + VERSION, False,
                renderer = libtcod.RENDERER_SDL)
        logg.debug('Setting the FPS limit.')
        libtcod.sys_set_fps(LIMIT_FPS)
        logg.debug('Drawing console initialization.')
        self.con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
        #bottom panel console
        logg.debug('Panels console initialization.')
        self.top_panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)
        self.bottom_panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

        logg.debug('Gamestate variables initialization')
        self.entities=[]
        self.player = None
        self.gamestate = ""
        self.player_action = None
        self.map = None
        self.random = libtcod.random_new()
        self.score = 0
        self.gamemode = ''

    def main_menu(self):
        """THE main menu, no other."""
        LIMIT_FPS = 20
        libtcod.sys_set_fps(LIMIT_FPS)

        img = libtcod.image_load('main/lazor.png')

        while not libtcod.console_is_window_closed():
            #show the background image, at twice the regular console resolution
            libtcod.image_blit_2x(img, 0, 0, 0)

            #show the game's title, and credits
            libtcod.console_set_default_foreground(0, color_menu_text)
            libtcod.console_print_ex(0, SCREEN_WIDTH/2, 1, libtcod.BKGND_NONE, libtcod.CENTER, 'Laz0r Dodging Game')
            libtcod.console_print_ex(0, SCREEN_WIDTH/2, 2, libtcod.BKGND_NONE, libtcod.CENTER, 'by magikmw')

            #show options and wait for the player's choice
            choice = menu('Choose an option:\n', ['Real-Time', 'Turn-Based', 'Help', 'Quit.'], 18, -10)

            if choice == 0: #new game
                self.new_game('RT')
            if choice == 1:
                self.new_game('TB')
            if choice == 2:
                #TODO help screen funcion call here
                pass
            if choice == 3: #quit
                break

            #libtcod.console_flush() #clear the console before redraw (fixes blacking out issue?)

        #self.new_game('RT')

    def new_game(self, gamemode):
        """Reset variables and go!"""
        self.entities=[]
        if libtcod.random_get_int(Game.random, 0, 1) == 1:
            x = SCREEN_WIDTH/2
        else:
            x = SCREEN_WIDTH/2 - 1
        self.player = Entity(x, 57, "Player", "@", color_player, False, False)
        self.entities.append(self.player)
        make_map()
        self.score = 0
        self.gamemode = gamemode
        if Game.gamemode == 'RT':
            LIMIT_FPS = 10
        else:
            LIMIT_FPS = 20
        libtcod.sys_set_fps(LIMIT_FPS)
        self.gamestate = "playing"
        self.play_game()

    def play_game(self):
        """Where's the game @."""
        #Start main loop
        while not libtcod.console_is_window_closed():

            self.player_action = None

            render_all() #render stuff
            libtcod.console_flush() #refresh the console

            #erase before move
            for ent in self.entities:
                ent.clear()

            #import keys handling
            self.player_action = handle_keys()
            if self.player_action == None:
                self.player_action = 'didnt-take-turn'
            if self.player_action == 'exit': #if pressing a key returns 'exit' - close the window
                break

            #'AI' takes turns
            if self.gamestate == 'playing' and self.player_action != 'didnt-take-turn' or Game.gamemode == 'RT':
                for ent in self.entities:
                    if ent.ai:
                        ent.ai.take_turn()
                        if ent.killer and ent.x == self.player.x and ent.y == self.player.y:
                            player_death()
                        elif ent.point and ent.x == self.player.x and ent.y == self.player.y:
                            self.score += 1
                            ent.clear()
                            Game.entities.remove(ent)
                spawn_points()

logg.debug('Gamestate initialized.')

class Tile(object):
    """A tile for the map, passable by default."""
    def __init__(self, blocked=False,):
        self.blocked = blocked

logg.debug('Tile initialized.')

class Entity(object):
    """Any and all entities in the game."""
    def __init__(self, x, y, name, char, color, blocks=False, killer=False, point=False, ai=False):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.blocks = blocks
        self.killer = killer
        self.point = point
        
        self.ai = ai
        if self.ai: #let AI component know who owns it
            self.ai.owner = self

    def move(self, dx, dy):
        #logg.debug('move() called, %s, %s', dx, dy)
        #moving by given amount
        if not is_blocked(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy

    def draw(self):
        #if visible to the player, or explored and always visible
        #logg.debug('Method draw() called by %s, pos x: %s, y: %s', self.name, str(self.x), str(self.y))
        libtcod.console_set_default_foreground(Game.con, self.color)
        libtcod.console_put_char(Game.con, self.x, self.y, self.char, libtcod.BKGND_NONE)
        
    def clear(self):
        #clear the sign
        #logg.debug('Method clear() called by %s, pos x: %s, y: %s', self.name, str(self.x), str(self.y))
        libtcod.console_put_char_ex(Game.con, self.x, self.y, ' ', color_ground_f, color_ground_b)

    def send_to_back(self):
        #logg.debug('send_to_back() called')
        #make this obcject drawn first so it appears beneath everything else
        Game.entities.remove(self)
        Game.entities.insert(0, self)    

logg.debug('Entity initialized.')

class Cannon(object):
    """The 'AI' for cannons"""
    def __init__(self):
        pass

    def take_turn(self):
        if Game.gamemode == 'RT':
            power = libtcod.random_get_int(Game.random, 0, 20)
            color_laser = color_laser_1
        else:
            d100 = libtcod.random_get_int(Game.random, 0, 100)
            if d100 < 10:
                power = 3
                color_laser = color_laser_3
            elif d100 < 10+10:
                power = 2
                color_laser = color_laser_2
            elif d100 < 10+10+30:
                power = libtcod.random_get_int(Game.random, 0, 1)
                color_laser = color_laser_1
            else:
                power = 0

        if power > 0 and power <= 3:
            can = self.owner
            ai_component = Lazor(power)
            laser = Entity(can.x, can.y+1, "laser", '|', color_laser, False, True, ai=ai_component)
            Game.entities.append(laser)

class Lazor(object):
    """The lazor 'AI'."""
    def __init__(self, power):
        self.power = power
        self.tick = 4

    def take_turn(self):
        if self.tick == -1:
            self.tick = 2
        laz = self.owner
        if laz.y + self.power > MAP_HEIGHT-2:
            Game.entities.remove(laz)
        elif self.tick == 0:
            laz.move(0,self.power)

        self.tick -= 1

class Point(object):
    """The 'AI' for the point thingies"""
    def __init__(self, timer):
        self.timer = timer

    def take_turn(self):
        self.timer = self.timer - 1
        if self.timer == 0:
            Game.entities.remove(self.owner)

logg.info('Classes initialization finished.')

################################
# FUNCTIONS                    #
################################

logg.info('Functions initialization.')

def render_all():
    """The main rendering function."""
    for y in range(MAP_HEIGHT):
        for x in range(MAP_WIDTH):
            wall = Game.map[x][y].blocked
            #TODO create FOV fall-off
            if wall:
                libtcod.console_put_char_ex(Game.con, x, y, '#', color_wall_f, color_wall_b)
            else:
                libtcod.console_put_char_ex(Game.con, x, y, ' ', color_ground_f, color_ground_b)

    #draw all objects in the list, except the player that is drawn AFTER everything else
    for ent in Game.entities:
        if ent != Game.player:
            ent.draw()
    Game.player.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(Game.con, 0, 0, SCREEN_WIDTH, MAP_HEIGHT, 0, 0, 2)

    libtcod.console_print_ex(Game.top_panel, SCREEN_WIDTH/2, 0, libtcod.BKGND_NONE, libtcod.CENTER, GAME_TITLE)
    libtcod.console_print_ex(Game.top_panel, SCREEN_WIDTH/2, 1, libtcod.BKGND_NONE, libtcod.CENTER, 'v.' + VERSION + ' by magikmw')

    libtcod.console_blit(Game.top_panel, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

    libtcod.console_print_ex(Game.bottom_panel, SCREEN_WIDTH/2, 0, libtcod.BKGND_NONE, libtcod.CENTER, "Stage 14")
    libtcod.console_print_ex(Game.bottom_panel, 0, 1, libtcod.BKGND_NONE, libtcod.LEFT, "Magikmw: " + str(Game.score) + 'pts')

    libtcod.console_blit(Game.bottom_panel, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, MAP_HEIGHT+2)

def make_map():
    #logg.debug('make_map() called')

    #fill map with "blocked" tiles
    Game.map = [[ Tile()
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

    for y in range(MAP_HEIGHT):
        Game.map[0][y].blocked = True
        Game.map[17][y].blocked = True

    for x in range(MAP_WIDTH):
        Game.map[x][0].blocked = True
        Game.map[x][59].blocked = True

    for z in range(16):
        ai_component = Cannon()
        lazor = Entity(z+1, 1, "laz0r", '^', color_cannons, True, True, ai=ai_component)
        Game.entities.append(lazor)

def handle_keys():
    key = libtcod.Key()

    libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, libtcod.Mouse())
    key_char = chr(key.c)

    if key.vk is not 0:
        logg.debug('Key pressed: key_char[%s], key.vk[%s].', key_char, key.vk)

    #toggle fullscreen
    if key.vk == libtcod.KEY_F11:
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
    #exit game
    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'

    #if the game is playing
    if Game.gamestate == 'playing':
        #movement keys
        #numpad, arrows, vim
        if key.vk == libtcod.KEY_KP8 or key.vk == libtcod.KEY_UP or key_char == 'k':
            Game.player.move(0, -1)
            return True

        elif key.vk == libtcod.KEY_KP2 or key.vk == libtcod.KEY_DOWN or key_char == 'j':
            Game.player.move(0, 1)
            return True

        elif key.vk == libtcod.KEY_KP4 or key.vk == libtcod.KEY_LEFT or key_char == 'h':
            Game.player.move(-1, 0)
            return True

        elif key.vk == libtcod.KEY_KP6 or key.vk == libtcod.KEY_RIGHT or key_char == 'l':
            Game.player.move(1, 0)
            return True

        elif key.vk == libtcod.KEY_KP5 or key.vk == libtcod.KEY_SPACE or key_char == '.': #KP_5, SPACE, . - wait a turn
            Game.player.move(0, 0)
            return True

        else:
            #test for other keys

            if key_char == 'P':
                #screenshot, because I can
                libtcod.sys_save_screenshot()

            if key.vk == libtcod.KEY_F1:
                help_screen()

            return 'didnt-take-turn' #This makes sure that monsters don't take turn if player did not.

logg.debug('handle_keys()')

def spawn_points():
    if libtcod.random_get_int(Game.random, 0, 1) == 1:
        x = libtcod.random_get_int(Game.random, 1, 16)
        y = libtcod.random_get_int(Game.random, 2, 55)
        #t = libtcod.random_get_int(Game.random, 20, 60)
        t = 60

        ai_component = Point(t)
        point = Entity(x, y, 'point', '*', color_point, False, False, True, ai=ai_component)
        Game.entities.append(point)
        point.send_to_back()

logg.debug('spawn_points()')

def player_death():
    Game.player.char = '%'
    Game.player.color = color_player_dead
    Game.gamestate = 'death'

logg.debug('player_death()')

#function that checks if the tile is blocked
def is_blocked(x, y):
    #check map tile first
    try:
        #XXX Hack for windows, seems the libtcod.dll is broken and throws up y in range of couple million
        if Game.map[x][y].blocked:
            return True
    except IndexError:
        logg.warn('is_blocked() catched an IndexError with values x: %s and y: %s', str(x), str(y))
        return True

    #than check for blocking objects
    for ent in Game.entities:
        if ent.blocks and ent.x == x and ent.y == y:
            return True

    return False

logg.debug('is_blocked()')

def menu(header, options, width, offset=0):
    """Generic menu function"""
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options.')

    #calculate total height for the header (auto-wraped), and one line per option
    header_height = libtcod.console_get_height_rect(Game.con, 0, 0, width, SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    highlight = ord('a')

    while True:
        #creates an off-screen console that represents the menu's window
        window = libtcod.console_new(width, height)

        #print the header with auto-wrap
        libtcod.console_set_default_foreground(window, color_menu_text)
        libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)
        libtcod.console_set_default_background(window, color_menu_highlight_b)

        #print the menu's options
        y = header_height
        letter_index = ord('a')
        for option_text in options:
            text = '(' + chr(letter_index) + ') ' + option_text
            if not highlight == letter_index:
                libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
            else:
                libtcod.console_print_ex(window, 0, y, libtcod.BKGND_SET, libtcod.LEFT, text)
            y += 1
            letter_index +=1

        #blit "window" contents to the root console
        x = SCREEN_WIDTH/2 - width/2
        y = SCREEN_HEIGHT/2 - height/2 + offset
        libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)

        #present the console, and wait for a key-press
        libtcod.console_flush()

        mouse = libtcod.Mouse()
        key = libtcod.Key()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        mouse_move = abs(mouse.dy) + abs(mouse.dx)

        if mouse_move > 2:
            if header_height != 0 and mouse.cy > y and mouse.cy < y+height:
                highlight = ord('a') + mouse.cy - y - header_height
            else:
                highlight = ord('a') + mouse.cy - y

            if highlight < ord('a'):
                highlight = ord('a')
            elif highlight > letter_index - 1:
                highlight = letter_index -1


        if mouse.lbutton_pressed:
            index = highlight - ord('a')
            if index >= 0 and index < len(options): return index

        if chr(key.c) == "P":
            libtcod.sys_save_screenshot()

        if key.vk == libtcod.KEY_F11:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        if key.vk == libtcod.KEY_ESCAPE:
            #XXX WTF I do with that.
            pass

        if key.vk == libtcod.KEY_ENTER or key.vk == libtcod.KEY_KPENTER or key.vk == libtcod.KEY_SPACE:
            index = highlight - ord('a')
            if index >= 0 and index < len(options): return index

        if key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2 or chr(key.c) == 'k':
            if not highlight == letter_index -1:
                highlight += 1

        elif key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8 or chr(key.c) == 'j':
            if not highlight == ord('a'):
                highlight -= 1

        #convert ASCII code to an index; if it corresponds to an option - return that
        index = key.c - ord('a')
        if index >= 0 and index < len(options): return index

    print(index)
    return index

logg.debug('menu()')    
    
def help_screen():
    print "This is the halp screen."

logg.info('Functions initialization finished.')

################################
# Initialization               #
################################

logg.info('Main loop initialization.')

Game = Gamestate()

logg.info('Invoking main_menu()')
Game.main_menu()

logg.info('Program terminated properly. Have a nice day.')
#End of the line.