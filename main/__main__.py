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
GAME_TITLE = 'Laz0r Dodging Game'
VERSION = '0.1'

#DEBUG

#FPS maximum
LIMIT_FPS = 20

#console size
SCREEN_WIDTH = 18
SCREEN_HEIGHT = 64

#on-screen map size within above
MAP_WIDTH = 18
MAP_HEIGHT = 62

#info panel size
PANEL_HEIGHT = 2

#Colors
color_ground_f = libtcod.white
color_ground_b = libtcod.black
color_wall_f = libtcod.white
color_wall_b = libtcod.black
color_player = libtcod.light_blue

logg.info('Constants initialization finished.')

################################
# CLASSES                      #
################################

logg.info('Classes initialization.')

class Gamestate():
    """The main state class"""
    def __init__(self):
        
        logg.info('Main loop initialization.')

        logg.debug('Font size set to 10')
        libtcod.console_set_custom_font('main/terminal8x8_gs_ro.png',
            libtcod.FONT_LAYOUT_ASCII_INROW | libtcod.FONT_TYPE_GRAYSCALE)

        logg.debug('Main console initialization.')
        libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT,
            GAME_TITLE + ' v.' + VERSION, False,
                renderer = libtcod.RENDERER_SDL)
        logg.debug('Setting the FPS limit.')
        libtcod.sys_set_fps(LIMIT_FPS)
        logg.debug('Drawing console initialization.')
        self.con = libtcod.console_new(SCREEN_WIDTH, SCREEN_HEIGHT)
        #bottom panel console
        logg.debug('Bottom panel console initialization.')
        self.panel = libtcod.console_new(SCREEN_WIDTH, PANEL_HEIGHT)

        logg.debug('Gamestate variables initialization')
        self.entities=[]
        self.player = None
        self.gamestate = ""
        self.player_action = None
        self.map = [[]]

    def main_menu(self):
        """THE main menu, no other."""
        print "I'm a main menu yay \o/"
        self.new_game()

    def new_game(self):
        """Reset variables and go!"""
        self.entities=[]
        self.player = Entity(5, 5, "Player", "@", color_player, True)
        self.entities.append(self.player)
        make_map()
        self.gamestate = "playing"
        self.play_game()

    def play_game(self):
        """Where's the game @."""

        self.player_action = None
        #Start main loop
        while not libtcod.console_is_window_closed():

            render_all() #render stuff
            libtcod.console_flush() #refresh the console

            #erase before move
            for ent in self.entities:
                ent.clear()


logg.debug('Gamestate initialized.')

class Tile():
    """A tile for the map, passable by default."""
    def __init__(self, blocked=False,):
        self.blocked = blocked

logg.debug('Tile initialized.')

class Entity():
    """Any and all entities in the game."""
    def __init__(self, x, y, name, char, color, blocks=False):
        self.x = x
        self.y = y
        self.name = name
        self.char = char
        self.color = color
        self.blocks = blocks

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
        
    def clear(self):
        #clear the sign
        #logg.debug('Method clear() called by %s, pos x: %s, y: %s', self.name, str(self.x), str(self.y))
        libtcod.console_put_char_ex(Game.con, self.x, self.y, '.', color_ground_f, color_ground_b)

logg.debug('Entity initialized.')

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
                libtcod.console_put_char_ex(Game.con, x, y, '.', color_ground_f, color_ground_b)

    #draw all objects in the list, except the player that is drawn AFTER everything else
    for ent in Game.entities:
        if ent != Game.player:
            ent.draw()
    Game.player.draw()

    #blit the contents of "con" to the root console
    libtcod.console_blit(Game.con, 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 0, 0, 0)

def make_map():
    #logg.debug('make_map() called')

    #fill map with "blocked" tiles
    Game.map = [[ Tile()
        for y in range(MAP_HEIGHT) ]
            for x in range(MAP_WIDTH) ]

#function that checks if the tile is blocked
def is_blocked(x, y):
    #check map tile first
    try:
        #XXX Hack for windows, seems the libtcod.dll is broken and throws up y in range of couple million
        if map[x][y].blocked:
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