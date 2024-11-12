import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk']

class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/"+ name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self):
        self.x, self.y = random.randint(800, 1600), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.hp =2
        self.font = load_font('ENCR10B.TTF', 60)
        self.hp_bar = load_font('ENCR10B.TTF', 36)
        self.game_over=0
        self.size=2


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 1600:
            self.dir = -1
        elif self.x < 0:
            self.dir = 1
        self.x = clamp(0, self.x, 1600)
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, self.size*100, self.size*100)
        else:
            Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, self.size*100, self.size*100)
        draw_rectangle(*self.get_bb())
        if self.size==2:self.hp_bar.draw(self.x-50, self.y+100, f'Hp:{self.hp}', (255, 0, 0))
        if self.size==1:self.hp_bar.draw(self.x-35, self.y+50, f'Hp:{self.hp}', (255, 0, 0))
        if self.game_over==1:self.font.draw(700,300,'GAME OVER',(255,0,0))

    def handle_event(self, event):
        pass

    def get_bb(self):
        if self.size==2:
            if self.dir==1: return self.x - 50, self.y - 100, self.x+30,self.y+100
            if self.dir==-1: return self.x - 10, self.y - 100, self.x+50,self.y+100
        if self.size==1:
            if self.dir==1: return self.x - 30, self.y - 50, self.x+30,self.y+50
            if self.dir==-1: return self.x - 20, self.y - 50, self.x+30,self.y+50

    def handle_collision(self, group, other):
        if group=='boy:zombie':
            self.game_over=1
            game_framework.quit()
            pass
        if group=='ball:zombie':
            self.hp-=1
            if self.hp==1:
                self.size -=1
                self.y-=50
            pass
            if self.hp==0:
                game_world.remove_object(self)
        pass