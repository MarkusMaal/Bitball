import pygame
class Obstacle:
    def __init__(self, bounce, size_x, size_y, location_x, location_y, color, life = False, breakab = True, multi = False):
        self.bouncy = bounce
        self.size_x = size_x
        self.size_y = size_y
        self.location_x = location_x
        self.location_y = location_y
        self.color = color
        self.breakable = breakab
        self.life = life
        self.multi = multi

    def BounceFeedback(self, rect1, position, forcex, forcey, ball):
        rect2 = pygame.Rect(self.location_x, self.location_y, self.size_x, self.size_y)
        if pygame.Rect.colliderect(rect1, rect2):
            if position[1] <= self.location_y + forcey:
                if forcey > 0:
                    return [(position[0] - (self.location_x + (self.size_x / 2)))/4, -1-self.bouncy-forcey]
                else:
                    return [(position[0] - (self.location_x + (self.size_x / 2)))/4, -1-self.bouncy]
            elif position[1] >= self.location_y + forcey:
                if forcey > 0:
                    return [0, 1+self.bouncy-forcey]
                else:
                    return [0, 1+self.bouncy]
            elif position[0] > self.location_x + self.size_x and position[1] < self.location_y + size_y and position[1] > self.location_y:
                ball.collides[0] = 1
                ball.FlipBall()
            elif position[0] < self.location_x and position[1] < self.location_y + size_y and position[1] > self.location_y:
                ball.collides[0] = -1
                ball.FlipBall()
        return [0, 0]

    def DrawObstacle(self, screen):
        rectable = pygame.Rect(self.location_x, self.location_y, self.size_x, self.size_y)
        pygame.draw.rect(screen, self.color, rectable)
