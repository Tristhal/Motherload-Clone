#WASD
#TAB = Inventory
#SPACE to restart after you have won or lost
from pygame import gfxdraw
from pygame import *
from math import *
import pygame as pygame
from random import *
#import winsound
# Play Windows exit sound.
tilesize=75
surfacex=14
surfacey=11
screenw=5
screenh=40
sizex=surfacex*screenw
sizey=surfacey*screenh
screenWidth = surfacex*tilesize
screenHeight = surfacey*tilesize

####################################################
screen=display.set_mode((screenWidth,screenHeight))#
running=True                                       #
####################################################
init()
mixer.init()
music=choice([mixer.Sound("Music.wav"),mixer.Sound("Music2.wav")])
music.play(10)
music.set_volume(1)
digsounds=[mixer.Sound("untitled1.wav"),mixer.Sound("untitled2.wav"),mixer.Sound("untitled3.wav"),mixer.Sound("untitled4.wav"),mixer.Sound("untitled5.wav")]
burnt=mixer.Sound("Burnt.wav")
dolariumsounds=[mixer.Sound("dolarium1.wav"),mixer.Sound("dolarium2.wav"),mixer.Sound("dolarium3.wav"),mixer.Sound("dolarium4.wav")]
font.init()
Font=font.SysFont('Courier New',20)
smallfont=font.SysFont('Courier New',15)
bigfont=font.SysFont('Courrier New',30)
mousebuttonup=False
class whisp():
    def __init__(self):
        self.changex=0
        self.image=Surface((50,50))
        self.changey=0
        self.posx=100
        self.posy=200
        self.screen=(randint(-5,0),randint(-1,0))
        self.tempscreen=themap.screenmap[self.screen[0]][self.screen[1]].copy()#copy of the sky so it can be replaced each time
        self.movetimer=10
        self.movetimemax=20
        self.randomlist=[i/10 for i in range(-20,20)]
    def refresh(self):#must refreshes the particular surface
        themap.screenmap[self.screen[0]][self.screen[1]].blit(self.tempscreen,(0,0))
    def move(self):
        self.movetimer+=1
        if self.movetimer>self.movetimemax:#random motion - after the move time is up another speed is added
            self.changex+=choice(self.randomlist)
            self.changey+=choice(self.randomlist)
            self.movetimer=0
        self.posx+=self.changex
        self.posy+=self.changey
        if self.posx>screenWidth-20:#to stay in the borders of the screen
            self.changex=-3
        elif self.posx<20:
            self.changex=3
        if self.posy>screenHeight-20:
            self.changey=-3
        elif self.posy<20:
            self.changey=3
        for x in range(0,15,5):#The whisps
            gfxdraw.filled_circle(themap.screenmap[self.screen[0]][self.screen[1]],int(self.posx),int(self.posy),int(x),(255,238,0,50))
def treeDraw(startx,starty,length,branches,variantx,counter,screen):#Recursively draws trees
    variantxoriginal=variantx
    variant=randint(0,50)
    counter+=1
    for i in range(0,branches):
        variantx=variantxoriginal
        if i==2:
            variantx-=variant
            changey=sin(radians(270+variantx))*length
            changex=cos(radians(270+variantx))*length
            endx=startx+changex
            endy=starty+changey
        elif i==1:
            variantx+=variant
            changey=sin(radians(270+variantx))*length
            changex=cos(radians(270+variantx))*length
            endx=startx+changex
            endy=starty+changey
        elif i==0:
            #variantx-=15
            changey=sin(radians(270+variantx))*length
            changex=cos(radians(270+variantx))*length
            endx=startx+changex
            endy=starty+changey
        else:
            variant=randint(-30,30)
            variantx+=variant
            changey=sin(radians(270+variantx))*length
            changex=cos(radians(270+variantx))*length
            endx=startx+changex
            endy=starty+changey
        if length>21 and counter<15:
            for i in range(-150,150):
                draw.aaline(screen,(abs(i),abs(i),abs(i)),((startx+i/100),starty),((endx+i/100),endy))
            treeDraw(endx,endy,length//choice([1.3,1.2,2,1.2,1.4,2,1.5,1.7,2,.9999]),3,variantx,counter+1,screen)
        else:
            for angle in range(0,361,40):
                changey=sin(radians(angle))*min(length,15)+(random()*5-2.5)
                changex=cos(radians(angle))*min(length,15)+(random()*5-2.5)
                endx=startx+changex
                endy=starty+changey
                colour=randint(20,50)
                for i in range(4):
                    draw.aaline(screen,(colour,colour,colour),(startx+i,starty),(endx+i,endy))
            return
    return

class theMap:
    def __init__(self, tilesize, surfacex, surfacey, screenw, screenh):
        self.tilesize=tilesize
        self.surfacex=surfacex
        self.surfacey=surfacey
        self.screenw=screenw
        self.screenh=screenh
        self.sizex=self.surfacex*self.screenw
        self.sizey=self.surfacey*self.screenh
        self.posx=0
        self.posy=0
        self.map=[]
        self.accelerationx=0.5
        self.accelerationy=1
        self.gravity=0.5
        self.changex=0
        self.changey=0
        self.characterx=500
        self.charactery=400
        self.onground=False
        self.onrwall=False
        self.onlwall=False
        self.character=Surface((52,102))
        self.character.blit(image.load('rectangle.jpg'),(1,1))
        self.screenmap=[]
        self.characterRadius=15
        self.digcooldowntime=60
        self.digcooldown=120
        self.lavadamage=40
        self.health=50
        self.maxhealth=100
        self.healthcap=200
        self.energy=100
        self.maxenergy=100
        self.energycap=300
        self.energydrain=.1
        self.dolariumdigger=False
        self.score=0
        self.total=0
        self.queuedMoney=0
        self.won=False
        self.inventory=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        #map populate
        self.resetVariables()
    
    def moveMap(self, keys):
        if keys[K_w]:#checks keys for direction
            self.changey+=self.accelerationy
            self.onground=False
            self.onrwall=False
            self.onlwall=False
        elif keys[K_s]:
            self.changey-=self.accelerationy
            if self.onground==True and self.digcooldown>self.digcooldowntime: #Dig excecuting map updating
                self.digcooldown=0
                if self.checkOre(self.map[-self.rposx//75][-self.rposy//75+1])==True:
                    self.inventory[self.map[-self.rposx//75][-self.rposy//75+1]-1]+=1
                    self.map[-self.rposx//75][-self.rposy//75+1]=0
                    if self.rposy%screenHeight>75:
                        draw.rect(self.screenmap[self.rposx//screenWidth+1][self.rposy//screenHeight+1],(40,40,40),(screenWidth-abs(self.rposx%screenWidth//75*75)-75,screenHeight-abs(self.rposy%screenHeight//75*75),75,75))
                    else:
                        draw.rect(self.screenmap[self.rposx//screenWidth+1][self.rposy//screenHeight],(40,40,40),(screenWidth-abs(self.rposx%screenWidth//75*75)-75,abs(self.rposy%screenHeight//75*75),75,75))
            self.onground=False
            self.onrwall=False
            self.onlwall=False
        if keys[K_a]:
            self.onrwall=False
            self.changex+=self.accelerationx
            if self.onlwall==True and self.digcooldown>self.digcooldowntime: #if it is on the wall and your moving in that direction
                self.digcooldown=0
                if self.checkOre(self.map[-self.rposx//75-1][-self.rposy//75])==True:#checks the ore and performs ore specific actions
                    self.inventory[self.map[-self.rposx//75-1][-self.rposy//75]-1]+=1
                    self.map[-self.rposx//75-1][-self.rposy//75]=0
                    if self.rposx%screenWidth<(self.surfacex*self.tilesize)-75 :#for the case where you are mining into a screen other than yours
                        draw.rect(self.screenmap[self.rposx//screenWidth+1][self.rposy//screenHeight+1],(40,40,40),(screenWidth-abs(self.rposx%screenWidth//75*75)-150,screenHeight-abs(self.rposy%screenHeight//75*75)-75,75,75))
                    else:
                        draw.rect(self.screenmap[self.rposx//screenWidth+2][self.rposy//screenHeight+1],(40,40,40),(abs(self.rposx%screenWidth//75*75),screenHeight-abs(self.rposy%screenHeight//75*75)-75,75,75))
            self.onground=False
            self.onrwall=False
            self.onlwall=False
        elif keys[K_d]:
            self.onlwall=False
            self.changex-=self.accelerationx
            if self.onrwall==True and self.digcooldown>self.digcooldowntime: #Dig excecuting map updating
                if self.checkOre(self.map[-self.rposx//75+1][-self.rposy//75])==True:
                    self.digcooldown=0
                    self.inventory[self.map[-self.rposx//75+1][-self.rposy//75]-1]+=1
                    self.map[-self.rposx//75+1][-self.rposy//75]=0
                    
                    if self.rposx%screenWidth>75:
                        draw.rect(self.screenmap[self.rposx//screenWidth+1][self.rposy//screenHeight+1],(40,40,40),(screenWidth-abs(self.rposx%screenWidth//75*75),screenHeight-abs(self.rposy%screenHeight//75*75)-75,75,75))
                    else:
                        draw.rect(self.screenmap[self.rposx//screenWidth][self.rposy//screenHeight+1],(40,40,40),(abs(self.rposx%screenWidth//75*75),screenHeight-abs(self.rposy%screenHeight//75*75)-75,75,75))
            self.onground=False
            self.onrwall=False
            self.onlwall=False
        if self.changex>1:#horisontal slow
            self.changex=self.changex/1.02
        elif self.changex<-1:
            self.changex=self.changex/1.02
        #housekeeping with the variables
        self.changey-=self.gravity
        self.rposx=self.posx-self.characterx
        self.rposy=self.posy-self.charactery
        #increase energy when above ground
        if self.posy>-1308:
            if self.energy<self.maxenergy:
                self.energy+=1
            self.total+=self.queuedMoney
            self.queuedMoney = 0
        else:
            self.energy-=self.energydrain
        self.digcooldown=min(self.digcooldown+1, self.digcooldowntime+1) #the countdown to the next dig
        self.onground=False
        self.onrwall=False
        self.onlwall=False
        #           #
        # COLLISION #
        #           #
        if self.map[-(self.rposx)//75][-(self.rposy+int(self.changey)-self.characterRadius)//75]!=0:#botom
            self.posy=((self.rposy-int(self.changey))//75)*75+(401)+self.characterRadius #posy is the top left corner so we add 400 to compensate for player
            self.changey*=-.2
            if self.digcooldown>self.digcooldowntime:
                self.onground=True
        elif self.map[-(self.rposx)//75][-(self.rposy+int(self.changey)+self.characterRadius)//75]!=0:
            self.posy=(self.rposy+int(self.changey)+self.characterRadius)//75*75+399-self.characterRadius #posy is the top left corner so we add 400 to compensate for player
            self.changey*=-.2
        if self.map[-(self.rposx+int(self.changex)-self.characterRadius)//75][-(self.rposy)//75]!=0:#right
            self.posx=((self.rposx-int(self.changex))//75)*75+501+self.characterRadius #posy is the top left corner so we add 400 to compensate for player
            self.changex*=-.2
            if self.digcooldown>self.digcooldowntime:
                self.onrwall=True
        elif self.map[-(self.rposx+int(self.changex)+self.characterRadius)//75][-(self.rposy)//75]!=0:#left
            self.posx=(self.rposx+int(self.changex)+self.characterRadius)//75*75+499-self.characterRadius #posy is the top left corner so we add 400 to compensate for player
            self.changex*=-.2
            if self.digcooldown>self.digcooldowntime:
                self.onlwall=True
        self.posx+=int(self.changex)#Since this needs to be after the colision. The collision is in this function
        self.posy+=int(self.changey)  
        
                                                                                                                                                      
    def blitMap(self):
        if self.posy//screenHeight>=0:#Map borders
            self.posy=-1
            self.changey*=-.5
        if self.posx>=0:
            self.posx=-1
            self.changex*=-.5
        if self.posx<-(self.sizex-10)*self.tilesize:
            self.posx=-(self.sizex-10)*self.tilesize+2
            self.changex*=-.5
        if self.posy<-self.sizey*self.tilesize-1000:
            self.posy=-self.sizey*self.tilesize-1000
            self.changey=0
        try:#trys so it does not crash on the edges
            screen.blit(self.screenmap[self.posx//screenWidth][self.posy//screenHeight],(self.posx%screenWidth,self.posy%screenHeight))#centre
        except:
            pass
        try:
            screen.blit(self.screenmap[self.posx//screenWidth][self.posy//screenHeight+1],(self.posx%screenWidth,self.posy%screenHeight-screenHeight))#Top
        except:
            pass
        try:
            screen.blit(self.screenmap[self.posx//screenWidth+1][self.posy//screenHeight+1],(self.posx%screenWidth-screenWidth,self.posy%screenHeight-screenHeight))#Top Left
        except:
            pass
        try:
            screen.blit(self.screenmap[self.posx//screenWidth+1][self.posy//screenHeight],(self.posx%screenWidth-screenWidth,self.posy%screenHeight))#Left
        except:
            pass
        ####Character drawing
        draw.rect(screen,(255,221,0),(485,385,30,30))
        ####
        if self.energy<0 or self.health<0 or self.lost==True:
            self.lost=True
            self.gameover()
        elif self.score>=100000000 or self.won==True:
            self.gamewon()
    def resetVariables(self):
        self.posx=-self.sizex*self.tilesize//2
        self.won=False
        self.posy=-100
        self.energy=100
        self.health=100
        self.maxhealth=100
        self.maxenergy=100
        self.energydrain=0  # .1 default
        self.digcooldowntime=5 # 20 default
        self.score=0
        self.total=0
        self.queuedMoney = 0
        self.inventory=[0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.dolariumdrill=False
        self.lost=False
        self.generatemap()
        
    def gameover(self):
        gfxdraw.box(screen,(0,0,screenWidth,screenHeight),(255,255,255,200))
        screen.blit(bigfont.render("game over...",1,(0,0,0)),(400,400))
        screen.blit(bigfont.render("Your score was: "+str(self.score),1,(0,0,0)),(370,450))
        screen.blit(bigfont.render("Press space to restart",1,(0,0,0)),(350,480))
        self.energy = 1
        if keys[K_SPACE]:
            self.resetVariables()
            print(self.energy)
            print(self.lost)
    def gamewon(self): #space to continue
        gfxdraw.box(screen,(0,0,screenWidth,screenHeight),(100,100,255,200))
        screen.blit(bigfont.render("You have succeded",1,(0,0,0)),(400,400))
        screen.blit(bigfont.render("Your score was: $"+str(self.score/100000000),1,(0,0,0)),(370,450))
        screen.blit(bigfont.render("Press space to restart",1,(0,0,0)),(350,500))
        self.won=True
        if keys[K_SPACE]:
            self.resetVariables()
    def checkOre(self,ore):
        if ore==0:
            choice(digsounds).play()#Music
            return False
        if ore==1:
            choice(digsounds).play()#Music
            self.score+=1
            self.queuedMoney+=1
            return True
        elif ore==2:
            choice(digsounds).play()#Music
            self.score+=4
            self.queuedMoney+=4
            return True
        elif ore==3:
            choice(digsounds).play()#Music
            self.score+=8
            self.queuedMoney+=8
            return True
        elif ore==4:
            choice(digsounds).play()#Music
            self.score+=16
            self.queuedMoney+=16
            return True
        elif ore==5:
            choice(digsounds).play()#Music
            self.score+=32
            self.queuedMoney+=32
            return True
        elif ore==6:
            choice(digsounds).play()#Music
            self.score+=64
            self.queuedMoney+=64
            return True
        elif ore==7:
            choice(digsounds).play()#Music
            self.score+=128
            self.queuedMoney+=128
            return True
        elif ore==8:
            self.health-=self.lavadamage
            burnt.play()
            return True
        elif ore==9:
            choice(digsounds).play()#Music
            self.score+=256
            self.queuedMoney+=256
            return True
        elif ore==10:
            choice(digsounds).play()#Music
            self.score+=512
            self.queuedMoney+=512
            return True
        elif ore==11:
            choice(digsounds).play()#Music
            self.score+=1024
            self.queuedMoney+=1024
            return True
        elif ore==12:
            choice(digsounds).play()#Music
            self.score+=2048
            self.queuedMoney+=2048
            return True
        elif ore==13 and self.dolariumdigger==True:
            self.score+=10000000
            self.queuedMoney+=10000000
            return True
        return False
    def generatemap(self):
        self.map=[]
        self.screenmap=[]
        for x in range(self.sizex):#creates a 2d list with block id's
            temp=[]
            for y in range(self.sizey):
                temp.append(randint(1,1))
            self.map.append(temp)
        for x in range(5,self.surfacex*self.screenw-3):#creates the sky
            for y in range(0,22):
                self.map[x][y]=0
        #ORES!!!
        for i in range(0,500):#copper #creates a 2d list with block id's adds ores
            tempx,tempy=randint(0,len(self.map)-1),randint(0,len(self.map[0])-121)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=2
        for i in range(0,300):#tin
            tempx,tempy=randint(0,len(self.map)-1),randint(0,len(self.map[0])-121)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=3
        for i in range(0,50):#amythest
            tempx,tempy=randint(0,len(self.map)-1),randint(0,len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=4
        for i in range(0,700):#silver
            #                                              Depth at which spawns start
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.15*self.screenh),len(self.map[0])-1-70)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=5
        for i in range(0,300):#gold
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.3*self.screenh),len(self.map[0])-1-70)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=6
        for i in range(0,100):#emerald
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.4*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=7
        for i in range(0,850):#lava
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.4*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=8
        for i in range(0,50):#rubies
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.5*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=9
        for i in range(0,300):#platinum
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.6*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=10
        for i in range(0,200):#diamonds
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.7*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=11
        for i in range(0,300):#einstinium
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.85*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=12
        for i in range(0,50):#blargite
            tempx,tempy=randint(0,len(self.map)-1),randint(self.surfacey*(.9*self.screenh),len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=13
        for i in range(0,1000):#blargite
            tempx,tempy=randint(0,len(self.map)-1),randint(30,len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=14
        for i in range(0,1000):#blargite
            tempx,tempy=randint(0,len(self.map)-1),randint(70,len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=14
        for i in range(0,1000):#blargite
            tempx,tempy=randint(0,len(self.map)-1),randint(150,len(self.map[0])-1)
            if self.map[tempx][tempy]!=0:
                self.map[tempx][tempy]=14
        for x in range(self.screenw):#adds a screen for each large rect
            temp=[]
            for y in range(self.screenh):
                temp.append(Surface((screenWidth,screenHeight)))
            self.screenmap.append(temp)
        self.progress=0
        self.maxprogress=len(self.screenmap)+14
        display.flip()
        for x in range(len(self.screenmap)):#draws blocks on the screens
            for y in range(0,len(self.screenmap[0])):
                for xx in range(0,self.surfacex):
                    for yy in range(0,self.surfacey):#order of likelyhood to reduce checks for ores
                        #This is to fill in the screens be it with circles rectangles or stone
                        
                        if self.map[x*self.surfacex+xx][y*self.surfacey+yy]==1:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))#Colour gets darker the deeper
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==0:
                            for xxx in range(0,75,5):
                                for yyy in range(0,75,5):
                                    self.screenmap[-x][-y].fill((69-randint(0,5),152-randint(0,15),236-randint(0,25)),(xx*75+xxx,yy*75+yyy,5,5))
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==2:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(10):
                                draw.rect(self.screenmap[-x][-y],(255,123,0),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==3:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(10):
                                draw.rect(self.screenmap[-x][-y],(169,180,182),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==5:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.rect(self.screenmap[-x][-y],(255,255,255),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==4:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(3):
                                draw.circle(self.screenmap[-x][-y],(73,30,125),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5),2)
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==6:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.rect(self.screenmap[-x][-y],(255,204,0),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,3,3))
                        #Emerald
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==7:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.circle(self.screenmap[-x][-y],(19,189,70),(xx*75+randint(5,70)//5*5,yy*75+randint(5,70)//5*5),3)
                        #Lava
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==8:
                            draw.rect(self.screenmap[-x][-y],(255,60,0),(xx*75,yy*75,75,75))
                        #Ruby
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==9:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(7):
                                draw.circle(self.screenmap[-x][-y],(199,44,44),(xx*75+randint(5,70)//5*5,yy*75+randint(5,70)//5*5),3)
                        #Platinum
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==10:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(10):
                                draw.rect(self.screenmap[-x][-y],(176,180,232),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        #Diamonds
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==11:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.circle(self.screenmap[-x][-y],(0,225,255),(xx*75+randint(5,70)//5*5,yy*75+randint(5,70)//5*5),3)
                        #Einstinium
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==12:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.rect(self.screenmap[-x][-y],(13,110,108),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        #blargium
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==13:
                            draw.rect(self.screenmap[-x][-y],(158-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5,173-randint(0,10)-(y*20/self.screenh+1)*5),(xx*75,yy*75,75,75))
                            for i in range(5):
                                draw.rect(self.screenmap[-x][-y],(randint(0,255),randint(0,255),randint(0,255)),(xx*75+randint(0,70)//5*5,yy*75+randint(0,70)//5*5,5,5))
                        elif self.map[x*self.surfacex+xx][y*self.surfacey+yy]==14:#spaces
                            self.map[x*self.surfacex+xx][y*self.surfacey+yy]=0
                            draw.rect(self.screenmap[-x][-y],(40,40,40),(xx*75,yy*75,75,75))
            
            self.progress+=1
            screen.blit(Font.render("Your goal - To reach the end - To experience this world - To prepare yourself - To grow",1,(255,255,255)),(5,10))
            screen.blit(Font.render("Your goal is to earn one dollar...",1,(255,255,255)),(300,40))
            screen.blit(Font.render("WASD - move",1,(255,255,255)),(5,750))
            screen.blit(Font.render("Tab  - menu",1,(255,255,255)),(5,770))
            draw.rect(screen,(100,10,10),(0,400,self.progress/self.maxprogress*screenWidth,20))
            display.flip()
        for i in range(len(self.map)):
            self.map.append(self.map[0])
        for i in range(0,15):
            tempx=randint(400,600)
            tempx2=randint(0,5)
            treeDraw(tempx,screenHeight,100,1,0,0,self.screenmap[-tempx2][-1])
            self.progress+=1
            event.get()
            screen.blit(Font.render("Your goal - To reach the end - To experience this world - To prepare yourself - To grow",1,(255,255,255)),(5,10))
            screen.blit(Font.render("Your goal is to earn one dollar...",1,(255,255,255)),(300,40))
            screen.blit(Font.render("WASD - move",1,(255,255,255)),(5,750))
            screen.blit(Font.render("Tab  - menu",1,(255,255,255)),(5,770))
            draw.rect(screen,(100,10,10),(0,400,self.progress/self.maxprogress*screenWidth,20))
            display.flip()
        return
class UI():
    def __init__(self):
        self.UPGRADE_NUM=3
        self.buttons=[[Rect(650,250,250,40),"Energy+ ",100,1],[Rect(650,310,250,40),"Health+ ",500,0],
                [Rect(650,370,250,40),"Dolarium Digger ",50000,0],[Rect(650,430,250,40),"Energy Drain- ",1000,0],
                [Rect(650,550,250,40),"Teleport ",2500,0],[Rect(650,490,250,40),"Drill Upgrade ",150,0]]
    def drawBars(self):
        BARLENGTH=300
        #Health bar
        gfxdraw.box(screen,(screenWidth-70,100,40,themap.health*2),(255,100,100,150))
        gfxdraw.box(screen,(screenWidth-70,100,40,themap.maxhealth*2),(255,100,100,100))
        gfxdraw.box(screen,(screenWidth-70,100,40,themap.healthcap*2),(255,100, 100, 50))
        #Energy Bar
        energybarOffset=100
        if themap.energy>40:
            gfxdraw.box(screen,(screenWidth-230-energybarOffset,20,themap.energy/themap.energycap*BARLENGTH,30),(30,40,255,150))
        else:
            gfxdraw.box(screen,(screenWidth-230-energybarOffset,20,themap.energy/themap.energycap*BARLENGTH,30),(255,0,0,150))
        gfxdraw.box(screen,(screenWidth-230-energybarOffset,20,BARLENGTH,30),(30,40,255,100))
        gfxdraw.box(screen,(screenWidth-230-energybarOffset,20,themap.energycap/themap.energycap*BARLENGTH,30),(30,40,255,50))
        #Height Bar
        gfxdraw.box(screen,(20,100,30,(-themap.posy-1234)/(themap.sizey*themap.tilesize+1234)*200),(30,40,255,100))
        screen.blit(smallfont.render(str(-(-themap.posy-1234)),1,(0,0,0)),(60,(-themap.posy-1234)/(themap.sizey*themap.tilesize+1234)*200+93))
        gfxdraw.box(screen,(20,100+(-1-1234)/(themap.sizey*themap.tilesize+1234)*200,30,200+abs((-1-1234)/(themap.sizey*themap.tilesize+1234)*200)),(20,100,30,50))
        draw.line(screen,(0,0,0),(20,100),(49,100),2)
        draw.line(screen,(0,0,0),(60,(-themap.posy-1234)/(themap.sizey*themap.tilesize+1234)*200+100),(20,100+(-themap.posy-1234)/(themap.sizey*themap.tilesize+1234)*200))
        #Mining Speed Bar
        gfxdraw.box(screen,(screenWidth-230-energybarOffset,50, themap.digcooldown/(themap.digcooldowntime+1)*BARLENGTH,10),(200,100,10,150))
    def checkButtons(self,mx,my, mousebuttonup): #To go through the list of buttons and check if something collides with its Rect hitbox in the list
        for i in range(0,len(self.buttons)):
            screen.blit(smallfont.render(self.buttons[i][1]+str(self.buttons[i][2]),1,(0,0,0)),(self.buttons[i][0][0]+10,self.buttons[i][0][1]+10))
            if self.buttons[i][0].collidepoint(mx,my):
                gfxdraw.box(screen,self.buttons[i][0],(255,255,255,100))
                if mousebuttonup==True:
                    if self.buttons[i][2] < themap.total:
                        if i==0 and themap.maxenergy<themap.energycap:
                            print("maxenergy+")
                            themap.total-=self.buttons[i][2]
                            self.buttons[i][2]=int(100*1.4**self.buttons[i][self.UPGRADE_NUM])
                            self.buttons[i][self.UPGRADE_NUM] +=1;
                            themap.maxenergy+=10
                        elif i==1 and themap.maxhealth<themap.healthcap:
                            print("maxhealth+")
                            themap.total-=self.buttons[i][2]
                            themap.maxhealth+=10
                            themap.health+=10
                        elif i==2 and themap.dolariumdigger==False:
                            print("dolariumdigger+")
                            themap.total-=self.buttons[i][2]
                            themap.digcooldownimet=10
                            themap.dolariumdigger=True
                            self.buttons[i][self.UPGRADE_NUM] +=1;
                            
                        elif i==3 and themap.energydrain>.05:
                            print("energydrain-")
                            themap.total-=self.buttons[i][2]
                            themap.energydrain-=.01
                            self.buttons[i][2]=int(1000*2**self.buttons[i][self.UPGRADE_NUM])
                            self.buttons[i][self.UPGRADE_NUM] +=1;
                        elif i==4:
                            print("Teleported")
                            themap.total-=self.buttons[i][2]
                            themap.posy=-1
                        elif i==5 and themap.digcooldowntime>15:
                            print("Digspeed+")
                            themap.total-=self.buttons[i][2]
                            self.buttons[i][2]=int(150*2**self.buttons[i][self.UPGRADE_NUM])
                            self.buttons[i][self.UPGRADE_NUM] +=1;
                            if themap.digcooldowntime>40:
                                themap.digcooldowntime-=5
                            else:
                                themap.digcooldowntime-=1
                        
    def Inventory(self, mousebuttonup):
        gfxdraw.box(screen,(125,100,800,700),(255,255,255,100))
        screen.blit(Font.render("Inventory",1,(0,0,0)),(470,150))
        screen.blit(Font.render("Dirt          "+str(themap.inventory[0])+ " * 1        "+" "*(5-(len(str(themap.inventory[0]))))+str(themap.inventory[0]*1),1,(0,0,0)),(150,250))
        screen.blit(Font.render("Copper        "+str(themap.inventory[1])+ " * 4        "+" "*(5-(len(str(themap.inventory[1]))))+str(themap.inventory[1]*4),1,(0,0,0)),(150,280))
        screen.blit(Font.render("Tin           "+str(themap.inventory[2])+ " * 8        "+" "*(5-(len(str(themap.inventory[2]))))+str(themap.inventory[2]*8),1,(0,0,0)),(150,310))
        screen.blit(Font.render("Amethyst      "+str(themap.inventory[3])+ " * 16       "+" "*(5-(len(str(themap.inventory[3]))))+str(themap.inventory[3]*16),1,(0,0,0)),(150,340))
        screen.blit(Font.render("Silver        "+str(themap.inventory[4])+ " * 32       "+" "*(5-(len(str(themap.inventory[4]))))+str(themap.inventory[4]*32),1,(0,0,0)),(150,370))
        screen.blit(Font.render("Gold          "+str(themap.inventory[5])+ " * 64       "+" "*(5-(len(str(themap.inventory[5]))))+str(themap.inventory[5]*64),1,(0,0,0)),(150,430))
        screen.blit(Font.render("Emerald       "+str(themap.inventory[6])+ " * 128      "+" "*(5-(len(str(themap.inventory[6]))))+str(themap.inventory[6]*128),1,(0,0,0)),(150,460))
        screen.blit(Font.render("Ruby          "+str(themap.inventory[8])+ " * 256      "+" "*(5-(len(str(themap.inventory[8]))))+str(themap.inventory[8]*256),1,(0,0,0)),(150,490))
        screen.blit(Font.render("Platinum      "+str(themap.inventory[9])+ " * 512      "+" "*(5-(len(str(themap.inventory[9]))))+str(themap.inventory[9]*512),1,(0,0,0)),(150,520))
        screen.blit(Font.render("Diamond       "+str(themap.inventory[10])+" * 1024     "+" "*(5-(len(str(themap.inventory[10]))))+str(themap.inventory[10]*1024),1,(0,0,0)),(150,550))
        screen.blit(Font.render("Einsteinium   "+str(themap.inventory[11])+" * 2048     "+" "*(5-(len(str(themap.inventory[11]))))+str(themap.inventory[11]*2048),1,(0,0,0)),(150,580))
        screen.blit(Font.render("Dolarium      "+str(themap.inventory[12])+" * 10,000,00"+" "*(5-(len(str(themap.inventory[12]))))+str(themap.inventory[12]*10000000),1,(0,0,0)),(150,610))

        screen.blit(Font.render("Money         "+str(themap.total),1,(0,0,0)),(150,650))
        screen.blit(Font.render("Score         "+str(themap.score)+"/100,000,000",1,(0,0,0)),(150,680))
        self.checkButtons(mx,my, mousebuttonup)
        #engcap
        #hp
        #dolarium
        #teleport
        
themap=theMap(tilesize, surfacex, surfacey, screenw, screenh)
ui=UI()
Whisps=[]
#No wisps
for i in range(20):
    #Whisps.append(whisp())
    pass
    
clock=time.Clock()
while running:
    screen.fill((0,0,0))
    clock.tick(60)
    mousebuttonup=False
    for evnt in event.get():
        if evnt.type == QUIT:
            running = False
        if evnt.type==MOUSEBUTTONUP:
            mousebuttonup=True
    mx, my = mouse.get_pos()
    mb = mouse.get_pressed()
    keys=key.get_pressed()
    themap.moveMap(keys)
    themap.blitMap()
    ui.drawBars()
    for i in range(len(Whisps)):
        Whisps[i].refresh()
    for i in range(len(Whisps)):
        Whisps[i].move()
    if keys[K_TAB]:
        ui.Inventory(mousebuttonup)
    display.flip()
quit()
