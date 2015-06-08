from planet import Planet
from BasicAnt import BasicAnt
from time import sleep

X_SIZE, Y_SIZE = 40, 27
earth = Planet(size=(X_SIZE, Y_SIZE), AntClass1=BasicAnt, AntClass2=BasicAnt)

BasicAnt.planet = earth


for i in range(1000):
    earth.advance()
    print earth
    sleep(0.3)

print earth
