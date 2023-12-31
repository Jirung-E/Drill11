from pico2d import *
import game_world
import game_framework
import random


# Move Speed
PIXEL_PER_METER = 10.0 / 0.3
SPEED_KMPH = 30.0
SPEED_MPM = (SPEED_KMPH * 1000.0 / 60.0)
SPEED_MPS = (SPEED_MPM / 60.0)
SPEED_PPS = SPEED_MPS * PIXEL_PER_METER

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_TIME = FRAMES_PER_ACTION * ACTION_PER_TIME

# 2m
SIZE_W = PIXEL_PER_METER * 2
SIZE_H = PIXEL_PER_METER * 2


class FlyState:
    @staticmethod
    def enter(bird, e):
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % 14
        bird.x += bird.dir * SPEED_PPS * game_framework.frame_time
        if bird.x < 25 or bird.x > 1600 - 25:
            bird.dir *= -1


    @staticmethod
    def draw(bird):
        # bird.image.clip_draw(0, 0, 183, 168, bird.x, bird.y, SIZE_W, SIZE_H)
        flip = 'h' if bird.dir == -1 else ''
        if bird.frame < 4:
            bird.image.clip_composite_draw(int(bird.frame) * 183, 0, 183, 168, 0, flip, bird.x, bird.y, SIZE_W, SIZE_H)
        elif bird.frame < 9:
            bird.image.clip_composite_draw((int(bird.frame)-4) * 183, 170, 183, 168, 0, flip, bird.x, bird.y, SIZE_W, SIZE_H)
        else:
            bird.image.clip_composite_draw((int(bird.frame)-9) * 183, 340, 183, 168, 0, flip, bird.x, bird.y, SIZE_W, SIZE_H)


class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = FlyState

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        return False

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    image = None

    def __init__(self):
        if Bird.image == None:
            Bird.image = load_image('bird_animation.png')
        self.x = random.randint(100, 1600 - 100)
        self.y = random.randint(300, 600 - 100)
        self.dir = random.choice([-1, 1])
        self.frame = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
