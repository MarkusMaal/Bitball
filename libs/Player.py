from random import *
class Player:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.down = []
        self.level = 0
        self.score = 0
        self.extraframes = 0
        self.sleep = 0
        self.bouncy = []
        self.controllable = False
        self.base_ball = None
        self.zall = None
        self.automatic = False
        self.immortal = False
        self.difficulty = 0
        self.unbreakables = []
        self.lastx = 0
        self.stuckframes = 0
        self.balls = []
        self.multiframes = 0
        self.timeleft = 0
        self.enablestick = False
        self.stickid = 0
        self.skipme = False
    
    def automove(self, dl):
        cpu_range = randint(8, 20)
        cpu_speed = randint(1, 10)
        if dl == 4:
            cpu_range = randint(8, 20)
            cpu_speed = randint(1, 10)
        elif dl == 1:
            cpu_range = randint(15, 50)
            cpu_speed = randint(1, 3)
        elif dl == 2:
            cpu_range = randint(20, 25)
            cpu_speed = randint(1, 5)
        elif dl == 3:
            cpu_range = randint(12, 30)
            cpu_speed = randint(1, 5)
        if self.bouncy[0].location_x + (self.bouncy[0].size_x // 2) < self.zall.positionx - cpu_range:
            if self.bouncy[0].location_x < self.end - 50:
                return self.bouncy[0].location_x + cpu_speed
        elif self.bouncy[0].location_x + (self.bouncy[0].size_x // 2) > self.zall.positionx + cpu_range:
            if self.bouncy[0].location_x > self.start - 50:
                return self.bouncy[0].location_x - cpu_speed
        else:
            self.down = 0
            cpu_range = randint(8, 20)
            cpu_speed = randint(1, 5)
        return self.bouncy[0].location_x
        
    