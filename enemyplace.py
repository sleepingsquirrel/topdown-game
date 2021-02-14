import random
def p(n):
    return range(len(n))
name = input('name: ')
with open('worlds/'+name+'/map.txt') as textFile: world = [line.split() for line in textFile]
with open('worlds/'+name+'/data.txt','a') as file:
    for i in p(world):
        for y in p(world[0]):
            if world[i][y] == '.':
                if random.randint(0,20) == 0:
                    file.write('e:'+ str(y)+':'+str(i)+':'+'\n')
