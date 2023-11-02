from pico2d import *
import game_world
import game_framework


# Move Speed
PIXEL_PER_METER = 10.0 / 0.3
RUN_SPEED_KMPH = 30.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = RUN_SPEED_MPS * PIXEL_PER_METER

# Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 8
FRAMES_PER_TIME = FRAMES_PER_ACTION * ACTION_PER_TIME


class FlyState:
    @staticmethod
    def enter(bird, e):
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame = (bird.frame + FRAMES_PER_TIME * game_framework.frame_time) % 8
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time


    @staticmethod
    def draw(bird):
        bird.image.clip_draw(int(bird.frame) * 100, bird.action * 100, 100, 100, bird.x, bird.y)


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

    def __init__(self, x = 400, y = 300, velocity = 1):
        if Bird.image == None:
            Bird.image = load_image('bird_animation.png')
        self.x, self.y, self.velocity = x, y, velocity
        self.frame = 0
        self.action = 3
        self.dir = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def draw(self):
        self.state_machine.draw()

    def update(self):
        self.state_machine.update()
