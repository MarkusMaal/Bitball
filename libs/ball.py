import pygame
pygame.mixer.init()
# wall = pygame.mixer.Sound("sfx/wall3.wav")
class Ball:
    def __init__(self, weight, forcey, forcex, size, gravity, positiony, positionx, collides, direction, color=[255, 255, 255], start=0, end=300):
        self.weight = weight
        self.forcey = forcey
        self.forcex = forcex
        self.size = size
        self.gravity = gravity
        self.positiony = positiony
        self.positionx = positionx
        self.collides = collides
        self.direction = direction
        self.color = color
        self.start = start
        self.legacy = False
        self.refresh = 60
        self.end = end

    def UpdateBall(self, bounds):
        grav = self.gravity/self.refresh
        if self.forcex > 0: self.forcex -= grav
        if self.forcex < 0: self.forcex += grav
        if self.direction == 2: self.forcey += (self.gravity * self.weight) / self.refresh
        elif self.direction == 1: self.forcey += (self.gravity * self.weight) / self.refresh
        if self.positionx >= self.end - self.size * grav:
            self.collides[0] = 1
            self.forcex = -self.forcex
            #self.color = [255, 255, 255]
            # wall.play()
        if self.positiony >= bounds[1] - (self.size * self.gravity)/self.refresh:
            self.collides[1] = 1
            self.positiony = bounds[1] - self.size
            #self.color = [255, 255, 255]
            # wall.play()
        if self.positiony <= self.size * 2:
            self.collides[1] = -1
            #self.color = [255, 255, 255]
            # wall.play()
        if self.positionx < self.start + self.size:
            self.collides[0] = -1
            #self.color = [255, 255, 255]
            # wall.play()
        else:
            if not self.legacy:
                self.collides[0] = 0
        if self.forcey < 0:
            if self.direction == 2: self.direction = 1
        if self.collides[1] == 1:
            self.forcey = -(self.forcey // (self.refresh*0.03))
            self.collides[1] = 0
            self.direction = 1
        if self.collides[1] == -1:
            self.direction = 2
        if self.collides[0] == 1:
            if self.forcex > 0:
                self.forcex = -(self.forcex / (self.refresh*0.03))
        if self.collides[0] == -1:
            if self.forcex < 0:
                self.forcex = -(self.forcex / (self.refresh*0.03))
        if self.forcey == 0.0:
            self.forcey += grav * 100
        self.positiony += self.forcey
        self.positionx += self.forcex
    def ChangeDir(self):
        if not self.collides[0] == 0: print(self.collides[0])
        if self.collides[0] == 1:
            if self.forcex > 0:
                self.forcex = -(self.forcex / 2)
        elif self.collides[0] == -1:
            if self.forcex < 0:
                self.forcex = -(self.forcex / 2)
        self.collides[0] = 0
    
    def FlipBall(self):
        if self.forcex > 0:
            self.forcex -= 2 * self.forcex
        elif self.forcex < 0:
            self.forcex += 2 * self.forcex

    def DrawBall(self, screen):
        try:
            pygame.draw.circle(screen, self.color, [int(self.positionx), int(self.positiony)], self.size)
        except:
            pass

    def GetBallRect(self):
        rectable = pygame.Rect(self.positionx - self.size, self.positiony - self.size, self.size * 2, self.size * 2)
        return rectable
