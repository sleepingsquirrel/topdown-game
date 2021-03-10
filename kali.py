import pygame,os
pygame.init()
sounds = {}
for i in os.listdir('sounds/'): sounds[i.split('.')[0]] = pygame.mixer.Sound('sounds/'+i)
while True: sounds['boom'].play()
