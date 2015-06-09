from pygame import *
from math import *
from random import *
#####################################
screen=display.set_mode((1000,800)) #
running=True                        #
cx,cy=400,300                       #
#####################################
changex=0
changey=0
accelerationy=1
accelerationx=0.5
gravity=.6
character=Surface((52,102))                                                                           
character.blit(image.load('rectangle.png'),(1,1))
def characterMove(cx,cy,changex,changey,accelerationx,accelerationy,gravity):
    if keys[K_w]:
        changey-=accelerationy
    elif keys[K_s]:
        changey+=accelerationy
    if keys[K_a]:
        changex-=accelerationx
    elif keys[K_d]:
        changex+=accelerationx
    changey+=gravity
    if changex>1:
        changex=changex/1.02
    elif changex<-1:
        changex=changex/1.02
    cx+=changex
    cy+=changey
    return cx,cy,changex,changey
        
while running:
    screen.fill((0,0,0))
    clock=time.Clock()
    clock.tick(60)
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys=key.get_pressed()
    cx,cy,changex,changey=characterMove(cx,cy,changex,changey,accelerationx,accelerationy,gravity)
    characterimage=transform.rotate(character,-changex*2)
    screen.blit(characterimage,(cx,cy))
    display.flip()
quit()
