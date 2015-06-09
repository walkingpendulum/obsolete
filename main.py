from Planet import Planet
from BasicStrategy import BasicAnt, BasicBase
from time import sleep


X_SIZE, Y_SIZE = 40, 27

Earth = Planet(size=(X_SIZE, Y_SIZE),
               AntClass1=BasicAnt,
               BaseClass1=BasicBase,
               AntClass2=BasicAnt,
               BaseClass2=BasicBase)
BasicAnt.planet = Earth


for i in range(1000):
    Earth.advance()
    print Earth
    sleep(0.3)

print Earth
