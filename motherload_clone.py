#WASD
#TAB = Inventory
#SPACE to restart after you have won or lost
from pygame import gfxdraw
from pygame import *
from math import *
from random import *

tilesize=75
surfacex=14
surfacey=11
screenw=5
screenh=20
sizex=surfacex*screenw
sizey=surfacey*screenh
screenWidth = surfacex*tilesize
screenHeight = surfacey*tilesize