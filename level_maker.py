import tkinter as tk
import os
def create_new():
    name = input('name: ')
    os.makedirs("worlds/"+name)
    with open('worlds/'+name+'/data.txt','a'): pass
    widdth = range(int(input('widdth: ')))
    with open('worlds/'+name+'/map.txt','a') as file:
        for i in range(int(input('height: '))):
            for i in widdth:
                file.write('. ')
            file.write('\n')
create_new()
