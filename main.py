from pynput import keyboard
from map import Map
from clouds import Clouds
import time
import os
import json
from helicopter import Helicopter as Hel


TICK_SLEEP = 0.05       #частота обновления поля
TREE_UPDATE = 50        #частота обновления деревьев
CLOUDS_UPDATE = 100     #частота обновления облаков
FIRE_UPDATE = 75        #частота обновления огня
MAP_W, MAP_H = 20, 10   #размер карты


field = Map(MAP_W,MAP_H)
clouds = Clouds(MAP_W,MAP_H)
hel = Hel(MAP_W,MAP_H)
tick = 1 


MOVES = {'w':(-1, 0), 'd':(0,1), 's':(1,0), 'a':(0, -1) } #привязка клавиши к "координатам" 

def process_key(key):  
    global hel, tick, clouds, field
    c = key.char.lower() 

    #helicopter moves
    if c in MOVES.keys():
        dx, dy = MOVES[c][0], MOVES[c][1]  
        hel.move(dx, dy)
    #save game
    elif c == 'f':
        data = {'helicopter':hel.export_data(),
                'clouds':clouds.export_data(),
                'field':field.export_data(),
                'tick':tick}
        with open('level.json', 'w') as lvl:
            json.dump(data, lvl)
    #load game
    elif c == 'g':
        with open('level.json', 'r') as lvl:
            data = json.load(lvl)
            hel.import_data(data['helicopter'])
            tick = data['tick'] or 1
            field.import_data(data['field'])
            clouds.import_data(data['clouds'])

# реализация передвижения после отжатия клавиши
listener = keyboard.Listener(
    on_press=None,
    on_release=process_key)
listener.start()


while True:
    os.system("clear")
    field.process_helicopter(hel, clouds)
    hel.print_stats()
    field.print_map(hel, clouds)
    print('tick -', tick)
    tick += 1
    time.sleep(TICK_SLEEP)
    if (tick % TREE_UPDATE == 0):
        field.generate_tree()
    if (tick % FIRE_UPDATE == 0):
        field.update_fires()
    if (tick % CLOUDS_UPDATE == 0):
        clouds.update()
