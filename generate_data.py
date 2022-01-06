import random
import os

open('size_buildings.txt', 'w').close()
open('size_poles.txt', 'w').close()

x = 25
y = 3*x
buildings = []
poles = []
i = 1
j = 900000

for _ in range(x):
    cor_x, cor_y = random.uniform(19.606553368263526,19.643349669677963), random.uniform(50.162267420560866,50.17665245038774)
    buildings.append((i,cor_x,cor_y))
    i+=1

for _ in range(x):
    cor_x, cor_y = random.uniform(19.620553368263526,19.622349669677963), random.uniform(50.168267420560866,50.16965245038774)
    buildings.append((i,cor_x,cor_y))
    i+=1

with open('size_buildings.txt', "w") as f:
    for el in buildings:
        f.write(str(el[2])+' '+str(el[1])+' '+str(el[0]))
        f.write('\n')  



for _ in range(x):
    cor_x, cor_y = random.uniform(19.606553368263526,19.643349669677963), random.uniform(50.162267420560866,50.17665245038774)
    poles.append((j,cor_x,cor_y))
    j+=1

for _ in range(x):
    cor_x, cor_y = random.uniform(19.620553368263526,19.622349669677963), random.uniform(50.168267420560866,50.16965245038774)
    poles.append((j,cor_x,cor_y))
    j+=1


with open('size_poles.txt', "w") as f:
    for el in poles:
        f.write(str(el[2])+' '+str(el[1])+' '+str(el[0]))
        f.write('\n')  