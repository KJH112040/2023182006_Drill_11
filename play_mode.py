import random

from pico2d import *
import game_framework

import game_world
from grass import Grass
from boy import Boy
from ball import Ball
from zombie import Zombie

# boy = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)

def init():
    global boy

    grass = Grass()
    game_world.add_object(grass, 0)

    boy = Boy()
    game_world.add_object(boy, 2)

    # fill here
    zombie = [Zombie() for _ in range(5)]
    game_world.add_objects(zombie,1)

    #global balls는 이제 필요 없음: 객체들끼리 알아서 처리하기 떄문
    balls =[Ball(random.randint(100,1600-100),60,0)for _ in range(30)]
    game_world.add_objects(balls,1)

    game_world.add_collision_pair('boy:ball',boy,None)
    for ball in balls:
        game_world.add_collision_pair('boy:ball',None,ball)





def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    # fill here
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    pass

def resume():
    pass

