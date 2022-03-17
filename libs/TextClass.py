import pygame
pygame.font.init()

class TextClass:

    def __init__ (self, fontfamily = "Arial", textsize = 18, textlocation = [0, 0], text = "", textcolor = [255, 255, 255]):
        self.fontfamily = fontfamily
        self.textsize = textsize
        self.textlocation = textlocation
        self.text = text
        self.rendered_text = ""
        self.rendered_color = [255, 0, 255]
        self.textcolor = textcolor
        self.font = None
        self.render = None

    def BlitText(self, screen):
        if not (self.text == self.rendered_text and self.rendered_color == self.textcolor):
            if self.font == None:
                self.font = pygame.font.SysFont(self.fontfamily, self.textsize)
            self.render = self.font.render(self.text, True, self.textcolor)
            self.rendered_text = self.text
            self.rendered_color = self.textcolor
        screen.blit(self.render, self.textlocation)
