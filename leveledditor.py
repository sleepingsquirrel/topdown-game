import pygame,random,os,math
from time import sleep
pygame.init()
w = 1000
h = round(w * .75)
d = 15
screen = pygame.display.set_mode((w, h))
current = ''
imgh = round(h/d)
img_dic = {}
fire_img = {}
enm_img = {}
proj_lis = []
enm_lis = []
tp_list = []
exit_list = []
barrow = '+'
tempfortp = [True,[0,0]]
def createimg(imgname): return pygame.transform.scale(pygame.image.load(imgname), (imgh,imgh))
for i in os.listdir('textures/'): img_dic[i.split('.')[0]] = createimg('textures/'+i)
for i in os.listdir('enemy/'): enm_img[i.split('.')[0]] = createimg('enemy/'+i)
world = [[ '' for _ in range(50)] for _ in range(50)]
clock = pygame.time.Clock()
running = True
menu = True
myfont = pygame.font.SysFont('Trebuchet MS', 30)
time = 0
class player:
    def __init__(self):
        self.sprites = {}
        def first():
            for i in range(len(world)):
                for o in range(len(world[0])):
                    if world[i][o] == '.': return i,o
        self.health = 4
        self.y , self.x = first()
        self.rotation = 'u'
        for i in os.listdir('player/'): self.sprites[i.split('.')[0]] = createimg('player/'+i)
    def show(self,a,b): screen.blit(self.sprites[self.rotation],     (a,b))
    def move(self,y,x,r):
        self.rotation = r
        self.y += y
        self.x += x
class teleporter:
    def __init__(self,xy,xy2):
        tp_list.append(self)
        self.xy = xy
        self.xy2= xy2
    def draw(self,a,b): screen.blit(img_dic['tp'],     (a,b))
class enemey:
    def __init__(self,xy):
        self.rotation = 'u'
        self.x , self.y = xy
        enm_lis.append(self)
    def test(self,y,x,r):
        self.rotation = r
        a = True
        for i in enm_lis:
            if self.y+y == i.y and self.x+x == i.x: a = False
        if a:
            if world[self.y+y][self.x+x] != '+':
                self.y += y
                self.x += x
    def show(self,a,b): screen.blit(enm_img[self.rotation],     (a,b))
    def delete(self): enm_lis.remove(self)
class door:
    def __init__(self,xy,new_level):
        exit_list.append(self)
        self.xy = xy
        self.level = new_level
    def through(self): load_world(self.level)
def load(name):
    global world
    global wiz
    with open(name) as textFile: world = [line.split() for line in textFile]
    wiz = player()
def populate():
    screen.fill((0,0,0))
    for i in range(len(world[0])):
        for o in range(len(world)):
            if wiz.x + 11 > i and wiz.y+9>o:
                if wiz.x - 11 < i and wiz.y-9<o:
                    a = round(round(h/d)*(i-wiz.x+9.5))
                    b = round(round(h/d)*(o-wiz.y+7))
                    if world[o][i] == ".": screen.blit(img_dic['ground2'],     (a,b))
                    elif world[o][i] == "+": screen.blit(img_dic['wall'],     (a,b))
                    elif world[o][i] == "s":
                        screen.blit(img_dic['ground2'],     (a,b))
                        screen.blit(img_dic['spike'],     (a,b))
                    for k in proj_lis:
                        if i == k.x and o == k.y: k.show(a,b)
                    for k in tp_list:
                        if [i,o] == k.xy: k.draw(a,b)
                        elif [i,o] == k.xy2: k.draw(a,b)
                    for k in enm_lis:
                        if i == k.x and o == k.y: k.show(a,b)
                    if i == wiz.x and o == wiz.y: wiz.show(a,b)
    screen.blit(myfont.render(str(round(clock.get_fps())), False, (255, 0, 0) if clock.get_fps() < 10 else (0,255,0)),(950,700))
    screen.blit(img_dic['menu'],(0,0))
    screen.blit(img_dic['save'],(950,0))
    screen.blit(img_dic['change'],(900,0))
    for i in range(wiz.health): screen.blit(img_dic['heart'],(0,50+(50*i)))
def menu_draw():
    for i , y in enumerate(os.listdir('worlds')):
        runtext = myfont.render(y, False, (255, 0, 0))
        screen.blit(runtext, (50,50*i))
        screen.blit(img_dic['frog'], (950,50*i))
def listToString(s): return (' '.join(s))

def load_world(name):
    global proj_lis
    global enm_lis
    global tp_list
    global exit_list
    global current
    current = name
    proj_lis = []
    enm_lis = []
    tp_list = []
    exit_list = []
    load('worlds/'+y+'/map.txt')
    with open('worlds/'+y+'/data.txt') as file:
        for line in file:
            if line.split(':')[0] == 'e': enemey([int(line.split(':')[1]),int(line.split(':')[2])])
            if line.split(':')[0] == 'tp': teleporter([int(line.split(':')[1]),int(line.split(':')[2])],[int(line.split(':')[3]),int(line.split(':')[4])])
            if line.split(':')[0] == 'ex': door([int(line.split(':')[1]),int(line.split(':')[2])],line.split(':')[3])
menu_draw()
while running:
    pygame.display.update()
    if menu != True:
        time += 1
        populate()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: quit()
        if menu:
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i , y in enumerate(os.listdir('worlds')):
                    if pygame.mouse.get_pos()[1] < 50*i+50 and pygame.mouse.get_pos()[1] > 50*i :
                        load_world(y)
                        menu = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode_click = pygame.mouse.get_pressed()
                mouse_X = wiz.x + (math.floor((pygame.mouse.get_pos()[0] + (imgh*0.5) )/ math.floor(h/d))-10)
                mouse_Y = wiz.y + (math.floor(pygame.mouse.get_pos()[1] / math.floor(h/d))-7)
                print(mouse_X,mouse_Y)
                if pygame.mouse.get_pos()[0] < 50 and pygame.mouse.get_pos()[1] < 50:
                    menu = True
                    menu_draw()
                    continue
                elif pygame.mouse.get_pos()[0] > 950 and pygame.mouse.get_pos()[1] < 50:
                    with open('worlds/'+current+'/data.txt','w') as file:
                        for i in enm_lis: file.write('e:'+str(i.x)+':'+str(i.y)+':'+'\n')
                        for i in tp_list: file.write('tp:'+str(i.xy[0])+':'+str(i.xy[1])+':'+str(i.xy2[0])+':'+str(i.xy2[1])+':'+'\n')
                        for i in exit_list: file.write('ex:'+str(i.xy[0])+':'+str(i.xy[1])+':'+i.level +':''\n')
                    with open('worlds/'+current+'/map.txt','w') as file:
                        for i in world:
                            file.write(listToString(i)+'\n')
                    continue
                elif pygame.mouse.get_pos()[0] > 900 and pygame.mouse.get_pos()[1] < 50 and pygame.mouse.get_pos()[0] < 950:
                    barrow = input('change to: ')
                    continue
                if barrow == 'e': enemey([mouse_X,mouse_Y])
                elif barrow == 'tp':
                    if tempfortp[0]:
                        tempfortp[1] = [mouse_X,mouse_Y]
                        tempfortp[0] = False
                    else:
                        teleporter(tempfortp[1],[mouse_X,mouse_Y])
                        tempfortp[0] = True
                elif barrow == 'ex': door([mouse_X,mouse_Y],input('name of map: '))
                else: world[mouse_Y][mouse_X] = barrow



            if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: wiz.move(0,1,'r')
                    if event.key == pygame.K_LEFT: wiz.move(0,-1,'l')
                    if event.key == pygame.K_UP: wiz.move(-1,0,'u')
                    if event.key == pygame.K_DOWN: wiz.move(1,0,'d')
    clock.tick(60)
