import pygame,random,os,math
from time import sleep
pygame.init()
w = 1000; h = round(w * .75); d = 15; screen = pygame.display.set_mode((w, h)); game_surface =  pygame.Surface((w, h)); imgh = round(h/d)
img_dic, fire_img, enm_img, sowrd_dic, shooty_dic,sounds = [{} for i in range(6)]; proj_lis,enm_lis,tp_list,exit_list ,enm_proj, close_list = [[] for i in range(6)]
direction_list = ['u','r','d','l']; current_level = ''
def createimg(imgname): return pygame.transform.scale(pygame.image.load(imgname).convert_alpha(), (imgh,imgh))
for i in os.listdir('textures/'): img_dic[i.split('.')[0]] = createimg('textures/'+i)
for i in os.listdir('sounds/'): sounds[i.split('.')[0]] = pygame.mixer.Sound('sounds/'+i)
for y, i in enumerate(direction_list): enm_img[i] = pygame.transform.rotate(img_dic['enemy'],-1*(90*y)+180)
for y, i in enumerate(direction_list): fire_img[i] = pygame.transform.rotate(img_dic['firebolt'],-1*(90*y)+180)
for y, i in enumerate(direction_list): sowrd_dic[i] = pygame.transform.rotate(img_dic['sorwd'],-1*(90*y))
for y, i in enumerate(direction_list): shooty_dic[i] = pygame.transform.rotate(img_dic['shooty'],-1*(90*y))
world = [[ '' for _ in range(50)] for _ in range(50)]
clock = pygame.time.Clock(); running = True; menu = True; myfont = pygame.font.SysFont('Trebuchet MS', 30); time = 0
class player:
    def __init__(self):
        with open('wizdata.txt') as file:
            self.sprites = {}
            with open('worlds/'+loaded_world+'/data.txt')as file:
                for line in file:
                    if line.split(':')[0] == '-':
                        self.y,self.x = [int(line.split(':')[1]),int(line.split(':')[2])]
                        break
            try: self.y -= 0
            except:
                try:
                    for i in range(len(world)):
                        for o in range(len(world[0])):
                            if world[i][o] == '.':
                                self.x,self.y = [o,i]
                                '2' +1
                except: pass
            with open('wizdata.txt') as file:
                for line in file:
                    self.maxmana = int(line.split(':')[0])
                    self.maxhealth = int(line.split(':')[1])
            self.health = self.maxhealth
            self.mana = self.maxmana
            self.rotation = 'u'
            self.ty , self.tx = [self.y,self.x]
            for y, i in enumerate(direction_list): self.sprites[i] = pygame.transform.rotate(img_dic['player'],-1*(90*y)+180)
    def show(self): game_surface.blit(self.sprites[self.rotation],     (round((w/2)-25),round((h/2)-25)))
    def move(self,y,x,r):
        self.rotation = r
        if world[round(self.ty+y)][round(self.tx+x)] == 's': self.health -=1
        if world[round(self.ty+y)][round(self.tx+x)] != '+':
            self.ty += y
            self.tx += x
    def up(self):
        if self.ty > self.y: self.y += 0.1
        if self.ty < self.y: self.y -= 0.1
        if self.tx > self.x: self.x += 0.1
        if self.tx < self.x: self.x -= 0.1
    def re(self): self.tx , self.ty = [self.x,self.y]
    def sowrd(self):
        if self.rotation == 'u':
            screen.blit(sowrd_dic[self.rotation],(round((w/2)-25),round((h/2)-75)))
            for i in close_list:
                if [round(self.y)-1,round(self.x)] ==  [i.y,i.x]: i.delete()
        elif self.rotation == 'r':
            screen.blit(sowrd_dic[self.rotation],(round((w/2)+25),(round(h/2)-25)))
            for i in close_list:
                if [round(self.y),round(self.x)+1] ==  [i.y,i.x]: i.delete()
        elif self.rotation == 'd':
            screen.blit(sowrd_dic[self.rotation],(round((w/2)-25),round((h/2)+25)))
            for i in close_list:
                if [round(self.y)+1,round(self.x)] ==  [i.y,i.x]: i.delete()
        elif self.rotation == 'l':
            screen.blit(sowrd_dic[self.rotation],(round((w/2)-75),round((h/2)-25)))
            for i in close_list:
                if [round(self.y),round(self.x)-1] ==  [i.y,i.x]: i.delete()
        def explode(): pass
class projectile:
    def __init__(self,xy,rotation):
        self.rotation = rotation
        self.x,self.y = xy
        proj_lis.append(self)
    def up(self):
        bpos = [self.y,self.x]
        if self.rotation == 'u':
            if world[self.y-1][self.x] != '+': self.y -= 1
        elif self.rotation == 'r':
            if world[self.y][self.x+1] != '+': self.x += 1
        elif self.rotation == 'd':
            if world[self.y+1][self.x] != '+': self.y += 1
        elif self.rotation == 'l':
            if world[self.y][self.x-1] != '+': self.x -= 1
        if self.y == bpos[0] and self.x == bpos[1]: self.delete()
        for i in close_list:
            if self.y == i.y and self.x == i.x:
                try:
                    i.delete()
                    self.delete()
                except: pass
    def show(self,a,b): game_surface.blit(fire_img[self.rotation],     (a,b))
    def delete(self):
        sounds['boom'].play()
        proj_lis.remove(self)
class enmproj:
    def __init__(self,xy,rotation):
        self.rotation = rotation
        self.x,self.y = xy
        enm_proj.append(self)
    def up(self):
        bpos = [self.y,self.x]
        if self.rotation == 'u':
            if world[self.y-1][self.x] != '+': self.y -= 1
        elif self.rotation == 'r':
            if world[self.y][self.x+1] != '+': self.x += 1
        elif self.rotation == 'd':
            if world[self.y+1][self.x] != '+': self.y += 1
        elif self.rotation == 'l':
            if world[self.y][self.x-1] != '+': self.x -= 1
        if self.y == bpos[0] and self.x == bpos[1]: self.delete()
        if [self.x,self.y] == [round(wiz.x),round(wiz.y)]:
            wiz.health -= 1
            try:
                self.delete()
            except: pass
    def show(self,a,b): game_surface.blit(fire_img[self.rotation],     (a,b))
    def delete(self): enm_proj.remove(self)
class teleporter:
    def __init__(self,xy,xy2):
        tp_list.append(self)
        self.xy = xy
        self.xy2= xy2
    def tp(self,location,obj):
        if location: obj.x , obj.y = self.xy
        else: obj.x , obj.y = self.xy2
        try: obj.re(); upclose()
        except: pass
    def draw(self,a,b): game_surface.blit(img_dic['tp'],     (a,b))
class enemey:
    def __init__(self,xy): self.rotation = 'u'; self.x , self.y = xy; enm_lis.append(self)
    def move(self):
        if self.x > round(wiz.x): self.test(0,-1,'l')
        if self.x < round(wiz.x): self.test(0,1,'r')
        if self.y > round(wiz.y): self.test(-1,0,'u')
        if self.y < round(wiz.y): self.test(1,0,'d')
    def test(self,y,x,r):
        self.rotation = r; a = True
        for i in close_list:
            if self.y+y == i.y and self.x+x == i.x: a = False
        if a:
            if world[self.y+y][self.x+x] != '+': self.y += y; self.x += x
    def show(self,a,b): game_surface.blit(enm_img[self.rotation],     (a,b))
    def delete(self):
        enm_lis.remove(self)
        if self in close_list: close_list.remove(self)
class shooty:
    def __init__(self,xy): self.rotation = 'u'; self.x , self.y = xy; self.health = 1; enm_lis.append(self)
    def move(self):
        if self.x == round(wiz.x) or self.y == round(wiz.y):
            if self.x > round(wiz.x): self.rotation = 'l'
            if self.x < round(wiz.x): self.rotation = 'r'
            if self.y > round(wiz.y): self.rotation = 'u'
            if self.y < round(wiz.y): self.rotation = 'd'
            enmproj([self.x,self.y],self.rotation)
        else:
            if self.x > round(wiz.x): self.test(0,-1,'l')
            if self.x < round(wiz.x): self.test(0,1,'r')
            if self.y > round(wiz.y): self.test(-1,0,'u')
            if self.y < round(wiz.y): self.test(1,0,'d')
    def test(self,y,x,r):
        self.rotation = r
        a = True
        for i in close_list:
            if self.y+y == i.y and self.x+x == i.x: a = False
        if a:
            if world[self.y+y][self.x+x] != '+': self.y += y; self.x += x
    def show(self,a,b): game_surface.blit(shooty_dic[self.rotation],     (a,b))
    def delete(self):
        try:
            if self.health < 1: enm_lis.remove(self)
            else: self.health -= 1
        except: pass
class door:
    def __init__(self,xy,new_level): exit_list.append(self); self.xy = xy; self.level = new_level
    def through(self): load_world(self.level); global wiz; wiz = player();
def saveplayer():
    with open('wizdata.txt','w') as file: file.write(str(wiz.maxmana) +':'+str(wiz.maxhealth)+':')
def load(name):
    global world; global wiz;
    with open(name) as textFile: world = [line.split() for line in textFile]; upclose()
def upclose():
    global close_list; close_list = []
    for i in enm_lis:
        if ((round(wiz.x)+20>i.x or i.x<round(wiz.x)-20) and (round(wiz.y)+20>i.y or i.y<round(wiz.y)-20)): close_list.append(i)
def populate():
    game_surface.fill((0,0,0))
    for x in range(math.ceil(w/imgh+2)):
        for y in range(math.ceil(h/imgh+3)):
            try:
                i = abs(round(wiz.x) - (x -(math.floor((w/imgh)/2)))); o = abs(round(wiz.y) - (y -(math.floor((h/imgh)/2)))+1)
                a = round(round(h/d)*(i-(wiz.x)+9.5)); b = round(round(h/d)*(o-(wiz.y)+7))
                if world[o][i] == ".": game_surface.blit(img_dic['ground2'],     (a,b))
                elif world[o][i] == "+": game_surface.blit(img_dic['wall'],     (a,b))
                elif world[o][i] == "s":
                    game_surface.blit(img_dic['ground2'],     (a,b))
                    game_surface.blit(img_dic['spike'],     (a,b))
                elif world[o][i] == "g":
                    game_surface.blit(img_dic[''],     (a,b))
                    game_surface.blit(img_dic['spike'],     (a,b))
                elif world[o][i] == "g":
                    game_surface.blit(img_dic[''],     (a,b))
                    game_surface.blit(img_dic['spike'],     (a,b))
                elif world[o][i] == "g":
                    game_surface.blit(img_dic[''],     (a,b))
                    game_surface.blit(img_dic['spike'],     (a,b))
                for k in proj_lis:
                    if i == k.x and o == k.y: k.show(a,b)
                for k in enm_proj:
                    if i == k.x and o == k.y: k.show(a,b)
                for k in tp_list:
                    if [i,o] == k.xy: k.draw(a,b)
                    elif [i,o] == k.xy2: k.draw(a,b)
                for k in close_list:
                    if (i == k.x and o == k.y): k.show(a,b)
            except: pass
            wiz.show()
    screen.blit(game_surface,(0,0))
    screen.blit(myfont.render(str(round(clock.get_fps())), False, (255, 0, 0) if clock.get_fps() < 10 else (0,255,0)),(w-imgh,h-imgh))
    screen.blit(img_dic['menu'],(0,0))
    for i in range(wiz.maxhealth):
        if i < wiz.health: screen.blit(img_dic['heart'],(0,imgh+(imgh*i)))
        else: screen.blit(img_dic['dead'],(0,imgh+(imgh*i)))
    for i in range(wiz.maxmana):
        if i < wiz.mana: screen.blit(img_dic['mana'],(imgh,(imgh*i)))
        else: screen.blit(img_dic['emptymana'],(imgh,(imgh*i)))
def menu_draw():
    for i , y in enumerate(os.listdir('worlds')): runtext = myfont.render(y, False, (255, 0, 0)); screen.blit(runtext, (imgh,imgh*i)); screen.blit(img_dic['frog'], (950,imgh*i))
def load_world(name):
    global proj_lis; global enm_lis; global tp_list; global exit_list; proj_lis = []; enm_lis = []; tp_list = []; exit_list = []; load('worlds/'+name+'/map.txt')
    with open('worlds/'+name+'/data.txt') as file:
        for line in file:
            if line.split(':')[0] == 'e': enemey([int(line.split(':')[1]),int(line.split(':')[2])])
            if line.split(':')[0] == 'sh': shooty([int(line.split(':')[1]),int(line.split(':')[2])])
            if line.split(':')[0] == 'tp': teleporter([int(line.split(':')[1]),int(line.split(':')[2])],[int(line.split(':')[3]),int(line.split(':')[4])])
            if line.split(':')[0] == 'ex': door([int(line.split(':')[1]),int(line.split(':')[2])],line.split(':')[3])
menu_draw()
while running:
    pygame.display.update()
    if menu != True:
        time += 1; wiz.up(); populate()
        for i in exit_list:
            if [round(wiz.x),round(wiz.y)] == i.xy: i.through()
        for i in proj_lis: i.up()
        for i in enm_proj: i.up()
        if time%30 == 0:
            upclose()
            for i in close_list:
                if i.x == round(wiz.x) and i.y == round(wiz.y): wiz.health-=1
                i.move()
            for i in tp_list:
                for u in close_list:
                    if [u.x,u.y] == i.xy: i.tp(False,u)
                    elif [u.x,u.y] == i.xy2: i.tp(True,u)
                if [round(wiz.x),round(wiz.y)] == i.xy: i.tp(False,wiz)
                elif [round(wiz.x),round(wiz.y)] == i.xy2: i.tp(True,wiz)
        if time%60 == 0:
            if wiz.mana < wiz.maxmana: wiz.mana += 1
        if wiz.health <1: wiz.health = 4; menu_draw(); menu = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()
        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i , y in enumerate(os.listdir('worlds')):
                    if pygame.mouse.get_pos()[1] < imgh*i+imgh and pygame.mouse.get_pos()[1] > imgh*i: load_world(y); loaded_world = y; wiz = player(); menu = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] < imgh and pygame.mouse.get_pos()[0] < imgh: menu = True; menu_draw()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT: wiz.move(0,1,'r')
                if event.key == pygame.K_LEFT: wiz.move(0,-1,'l')
                if event.key == pygame.K_UP: wiz.move(-1,0,'u')
                if event.key == pygame.K_DOWN: wiz.move(1,0,'d')
                if event.key == pygame.K_z:
                    if wiz.mana > 0: wiz.mana -= 1; projectile([round(wiz.x),round(wiz.y)],wiz.rotation)
                if event.key == pygame.K_x: wiz.sowrd()
    clock.tick(60)
