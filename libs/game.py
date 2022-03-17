#moodulite importimine
import pygame
import sys
from random import randint
from libs.ball import *
from libs.obstacles import *
from libs.TextClass import *
from libs.Player import *
pygame.init()
pygame.mixer.init()
class Game:
    def __init__(self, screen, bounds, players, gamemode, mb, obs, bgm, sfx, dl, dvr, plrs, dcollides, unjam=False, xts=False, cg=False, time=16*150, dropshadows=True):
        self.screen = screen
        self.bounds = bounds
        self.gamemode = gamemode
        self.players = players
        self.mb = mb
        self.obs = obs
        self.bgm = bgm
        self.sfx = sfx
        self.dl = dl
        self.exit = xts
        self.cleargame = cg
        self.time = time
        self.dvr = dvr
        self.plrs = plrs
        self.unjam = unjam
        self.dcollides = dcollides
        self.dropshadows = dropshadows
        self.refresh = 60


    def PauseMenu(self):
        if self.bgm: pygame.mixer.music.pause()
        screen = self.screen
        clock = pygame.time.Clock()
        paused = True
        colour = [randint(0, 100), randint(0, 100), randint(0, 100)]
        sel = 1
        items = []
        swap = pygame.mixer.Sound("sfx/wall2.wav")
        sels = pygame.mixer.Sound("sfx/pop2.wav")
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 50, self.bounds[1] // 2 - 40], "Game menu", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 2 - 20], "Resume", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 2], "Reset game", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 2 + 20], "Return to main menu", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 2 + 40], "Exit Bitball", [255, 255, 255]))
        enablestick = False
        debounce = 20
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if joystick.get_numaxes() > 0:
                enablestick = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_UP:
                        if sel > 1:
                            if self.sfx: sels.play()
                            sel -= 1
                    elif event.key == pygame.K_DOWN:
                        if sel < 4:
                            if self.sfx: sels.play()
                            sel += 1
                    elif event.key == pygame.K_RETURN:
                        if self.sfx: swap.play()
                        if sel == 1:
                            paused = False
                            if self.bgm: pygame.mixer.music.unpause()
                        if sel == 2:
                            paused = False
                            if self.bgm: pygame.mixer.music.play()
                            self.cleargame = True
                        if sel == 3:
                            self.exit = True
                            if self.bgm: pygame.mixer.music.unpause()
                            paused = False
                        if sel == 4:
                            pygame.quit()
                            sys.exit()
            
            pygame.draw.rect(screen, colour, pygame.Rect([self.bounds[0] // 2 - 135, self.bounds[1] // 2 - 45], [250, 115]))
            value = randint(200, 255)
            items[sel].textcolor = [value - 150, value - 50, value]
            for i in range(len(items)):
                if not sel == i:
                    items[i].textcolor = [255, 255, 255]
                    if not i == 0: items[i].textlocation[0] = self.bounds[0] // 2 - 125
                else:
                    items[i].textlocation[0] = self.bounds[0] // 2 - 115
                items[i].BlitText(screen)
                
            if enablestick:
                debounce -= 1
                if debounce <= 0:
                    for g in range(joystick_count):
                        joystick = pygame.joystick.Joystick(g)
                        joystick.init()
                        for i in range(joystick.get_numhats()):
                            hat = joystick.get_hat(i)
                            if hat[1] == 1:
                                sel -= 1
                                if self.sfx: sels.play()
                                debounce = 10
                            elif hat[1] == -1:
                                sel += 1
                                if self.sfx: sels.play()
                                debounce = 10
                        if sel > len(items) - 1: sel = len(items) - 1
                        for i in range(joystick.get_numbuttons()):
                            if i == 0 and joystick.get_button(i) == True:
                                if self.sfx: swap.play()
                                if sel == 1:
                                    paused = False
                                    if self.bgm: pygame.mixer.music.unpause()
                                if sel == 2:
                                    paused = False
                                    if self.bgm: pygame.mixer.music.play()
                                    self.cleargame = True
                                if sel == 3:
                                    self.exit = True
                                    if self.bgm: pygame.mixer.music.unpause()
                                    paused = False
                                if sel == 4:
                                    pygame.quit()
                                    sys.exit()
                            elif i == 9 and joystick.get_button(i) == True:
                                paused = False
                                if self.bgm: pygame.mixer.music.unpause()
                                debounce = 20
            pygame.display.flip()
            clock.tick(self.refresh)

    def GGMenu(self, playresults):
        if self.bgm: pygame.mixer.music.pause()
        screen = self.screen
        clock = pygame.time.Clock()
        paused = True
        colour = [randint(0, 100), randint(0, 100), randint(0, 100)]
        sel = 1
        items = []
        bg = (105 - randint(0, 80), 255 - randint(0, 80), 255 - randint(0, 80))
        tbg = bg
        enablestick = False
        debounce = 20
        joystick_count = pygame.joystick.get_count()
        bestscore = 0
        bestplayer = 0
        for i, player in enumerate(playresults):
            if player[1] > bestscore:
                bestscore = player[1]
                bestplayer = i
            elif player[1] == bestscore:
                bestplayer = 9
                break
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if joystick.get_numaxes() > 0:
                enablestick = True
        for i in range(self.bounds[1]):
            col_r = tbg[0]
            col_g = tbg[1]
            col_b = tbg[2]
            col_r -= 0.2
            col_g -= 0.2
            col_b -= 0.2
            if col_r < 0: col_r = 0.2
            if col_g < 0: col_g = 0.2
            if col_b < 0: col_b = 0.2
            tbg = [col_r, col_g, col_b]
            pygame.gfxdraw.hline(screen, 0, self.bounds[0], i, [int(col_r), int(col_g), int(col_b)])
        a = TextClass("Arial", 22, [self.bounds[0] // 2 - 55, 20], "Game over")
        a.textcolor = [255, 0, 0]
        a.BlitText(screen)
        scorepos = 20, 70
        pygame.draw.rect(screen, colour, pygame.Rect([10, 60], [self.bounds[0] - 40, scorepos[1] + 20 + 80 * (self.players - 1)]))
        for i in range(self.players):
            a = TextClass("Arial", 16, scorepos, "Player " + str(i + 1))
            a.BlitText(screen)
            a = TextClass("Arial", 14, [scorepos[0] + 20, scorepos[1] + 20], "Level " + str(playresults[i][0]))
            a.BlitText(screen)
            a = TextClass("Arial", 14, [scorepos[0] + 20, scorepos[1] + 40], "Score: " + str(playresults[i][1]))
            a.BlitText(screen)
            scorepos = scorepos[0], scorepos[1] + 80
        scorepos = 20, self.bounds[1] - 50
        if len(playresults) > 1:
            a = TextClass("Arial", 24, scorepos, "Winner: Player " + str(bestplayer + 1))
            if bestplayer == 9:
                a = TextClass("Arial", 24, scorepos, "Multiple winners")
        else:
            a = TextClass("Arial", 24, scorepos, "Single player")
        a.BlitText(screen)
        swap = pygame.mixer.Sound("sfx/wall2.wav")
        sels = pygame.mixer.Sound("sfx/pop2.wav")
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 50, self.bounds[1] // 1.2 - 40], "Game ended", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 1.2 - 20], "Reset game", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 1.2], "Return to main menu", [255, 255, 255]))
        items.append(TextClass("Arial", 18, [self.bounds[0] // 2 - 125, self.bounds[1] // 1.2 + 20], "Exit Bitball", [255, 255, 255]))
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                        pygame.mixer.music.play(-1)
                    elif event.key == pygame.K_UP:
                        if sel > 1:
                            if self.sfx: sels.play()
                            sel -= 1
                    elif event.key == pygame.K_DOWN:
                        if sel < 3:
                            if self.sfx: sels.play()
                            sel += 1
                    elif event.key == pygame.K_RETURN:
                        if self.sfx: swap.play()
                        if sel == 1:
                            paused = False
                            if self.bgm: pygame.mixer.music.play()
                            self.cleargame = True
                        if sel == 2:
                            self.exit = True
                            if self.bgm: pygame.mixer.music.unpause()
                            paused = False
                        if sel == 3:
                            pygame.quit()
                            sys.exit()
            if enablestick:
                debounce -= 1
                if debounce <= 0:
                    for g in range(joystick_count):
                        joystick = pygame.joystick.Joystick(g)
                        joystick.init()
                        for i in range(joystick.get_numhats()):
                            hat = joystick.get_hat(i)
                            if hat[1] == 1:
                                if sel > 1:
                                    if self.sfx: sels.play()
                                    sel -= 1
                                debounce = 10
                            elif hat[1] == -1:
                                if sel < 3:
                                    if self.sfx: sels.play()
                                    sel += 1
                                debounce = 10
                        if sel > len(items) - 1: sel = len(items) - 1
                        for i in range(joystick.get_numbuttons()):
                            if i == 0 and joystick.get_button(i) == True:
                                if self.sfx: swap.play()
                                if sel == 1:
                                    paused = False
                                    if self.bgm: pygame.mixer.music.play()
                                    self.cleargame = True
                                if sel == 2:
                                    self.exit = True
                                    if self.bgm: pygame.mixer.music.unpause()
                                    paused = False
                                if sel == 3:
                                    pygame.quit()
                                    sys.exit()
            pygame.draw.rect(screen, colour, pygame.Rect([self.bounds[0] // 2 - 135, self.bounds[1] // 1.2 - 45], [250, 90]))
            value = randint(200, 255)
            items[sel].textcolor = [value - 150, value - 50, value]
            for i in range(len(items)):
                if not sel == i:
                    items[i].textcolor = [255, 255, 255]
                    if not i == 0: items[i].textlocation[0] = self.bounds[0] // 2 - 125
                else:
                    items[i].textlocation[0] = self.bounds[0] // 2 - 115
                items[i].BlitText(screen)
            pygame.display.flip()
            clock.tick(self.refresh)
    def NewGame(self):
        screen_height = self.bounds[1]
        screen_width = self.bounds[0]
        self.time = 0
        if self.gamemode == 2:
            self.time = 4/15 * self.refresh * 150
        bounds = self.bounds
        # bounds = screen_width, screen_height = 1220, 650
        pop = pygame.mixer.Sound("sfx/pop1.wav")
        bfx = pygame.mixer.Sound("sfx/trampoline1.wav")
        if self.bgm:
            main = pygame.mixer.music.load("bgm/classic_mode.ogg")
            if self.gamemode == 1: main = pygame.mixer.music.load("bgm/classic_mode.ogg")
            elif self.gamemode == 2: main = pygame.mixer.music.load("bgm/zen_mode.ogg")
            elif self.gamemode == 3: main = pygame.mixer.music.load("bgm/survival_mode.ogg")
            elif self.gamemode == 4: main = pygame.mixer.music.load("bgm/eliminator.ogg")
            else: main = pygame.mixer.music.load("bgm/compvoid.ogg")
            pygame.mixer.music.play(-1)
        clock = pygame.time.Clock()
        #ekraani seadistamine
        #screen = pygame.display.set_mode([screen_width-20, screen_height])
        screen = self.screen

        bg = True
        dev = False
        hitbox = False
        text = True
        immortal = False
        if self.gamemode == 5: immortal = True
        precision = False
        cpu_speed = randint(2, 10)
        cpu_range = randint(5, 10)
        playable = 999
        for i in range(self.players):
            if self.plrs[i] == 1:
                playable = i
        multiframes = 0
        def CreatePlayer(start, end, idx):
            plr = Player()
            plr.down = 0
            plr.level = 1
            plr.lives = 1
            if self.gamemode == 3: plr.lives = 5
            elif self.gamemode == 2: plr.lives = 999
            elif self.gamemode == 4: plr.lives = 999
            plr.score = 0
            plr.extraframes = 0
            plr.sleep = 6.25 * (4/15) * self.refresh
            plr.difficulty = self.dl
            plr.unbreakables = 0
            plr.automatic = True
            plr.balls = []
            plr.zall = Ball(15, 1, 0.1, 10, 1.2, randint(400, 500), start + randint(100, 200), [0, 0], 2)
            plr.zall.refresh = self.refresh
            plr.base_ball = plr.zall
            plr.start = start
            plr.end = end
            if not self.dcollides:
                plr.zall.legacy = True
            for i in range(1):
                plr.zall = Ball(15, 1, 0.1, 10, 1.2, randint(400, 500), start + randint(100, 200), [0, 0], 2)
                plr.zall.start = plr.start
                plr.zall.end = plr.end
                plr.zall.refresh = self.refresh
                plr.base_ball = plr.zall                                                    
                if not self.dcollides:
                    plr.zall.legacy = True
                plr.balls.append(plr.zall)
            refresh = self.refresh
            if refresh < 60:
                refresh = 120-refresh
            elif refresh > 60:
                refresh = 250-refresh
            if idx == 0:
                plr.bouncy = [Obstacle((refresh) * 3/10, 100, 10, randint(start+100, end-100), 550, [0, 0, 255], False, False)]
            elif idx == 1:
                plr.bouncy = [Obstacle((refresh) * 3/10, 100, 10, randint(start+100, end-100), 550, [255, 0, 0], False, False)]
            elif idx == 2:
                plr.bouncy = [Obstacle((refresh) * 3/10, 100, 10, randint(start+100, end-100), 550, [0, 255, 0], False, False)]
            elif idx == 3:
                plr.bouncy = [Obstacle((refresh) * 3/10, 100, 10, randint(start+100, end-100), 550, [255, 255, 0], False, False)]
            if True:
                for j in range(0, plr.level * 10, 10):
                    col = [randint(50, 200), randint(50, 200), randint(50, 200)]
                    for i in range(0, 300, 50):
                        b = randint(0, 4)
                        plr.bouncy.append(Obstacle(self.refresh/20, 50, 10, start + i, j, col))
                if not self.gamemode == 3:
                    plr.bouncy[randint(1, len(plr.bouncy) - 1)].life = True               
            lastpos = pygame.mouse.get_pos()
            plr.lastx = 999
            plr.stuckframes = 0
            plr.multiframes = 0
            plr.timeleft = self.time
            if self.gamemode == 4:
                plr.timeleft = 4/15 * self.refresh * 90
            plr.enablestick = False
            plr.controllable = False
            stickid = 0
            return plr
        
        debounce = 0
        sections = []

        for i in range(self.players):
            sections.append(CreatePlayer((i * 300 - 20) + 20, (i * 300 - 20) + 20 + 300, i))
            if self.plrs[i] == 1:
                sections[-1].enablestick = False
                sections[-1].stickid = 0
                sections[-1].automatic = False
                sections[-1].controllable = True
            elif self.plrs[i] > 1:
                sections[-1].enablestick = True
                sections[-1].stickid = self.plrs[i] - 2
                sections[-1].automatic = False
                sections[-1].controllable = True
        enablestick = False
        joystick_count = pygame.joystick.get_count()
        if joystick_count > 0: 
            pygame.joystick.init()
        """
        if joystick_count > 0:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            if joystick.get_numaxes() > 0:
                enablestick = True"""
        precision = False
        dopause = False
        lastbest = 0
        showbest = 0
        #eelrenderda tekstid, et jõudlust parandada
        scoretext2 = TextClass("Segoe UI", 18, [10, 10], "Score: 0", [0, 0, 0])
        scoretext = TextClass("Segoe UI", 18, [12, 12], "Score: 0", [255, 255, 255])        
        leveltext2 = TextClass("Segoe UI", 18, [10, 30], "Level: 0", [0, 0, 0])
        leveltext = TextClass("Segoe UI", 18, [12, 32], "Level: 0", [255, 255, 255])       
        jacks = TextClass("Segoe UI", 18, [12, 52], "Bonus: 1x", [0, 0, 0])
        jack = TextClass("Segoe UI", 18, [10, 50], "Bonus: 1x", [255, 255, 255])
        timeup = TextClass("Segoe UI", 24, [0, 0], "Time's up!", [255, 255, 255])
        gameover = TextClass("Segoe UI", 24, [0, 0], "Game over", [255, 0, 0])
        readytext = TextClass("Segoe UI", 24, [0, 0], "Ready", [255, 255, 255])
        extratext = TextClass("Segoe UI", 24, [0, 0], "Extra ball", [0, 150, 255])
        multitext = TextClass("Segoe UI", 24, [0, 0], "Multiball!", [200, 150, 50])
        secsleft = TextClass("Segoe UI", 24, [0, 0], "0 secs", [255, 255, 255])
        debugtext = TextClass("Segoe UI", 20, [0, 0] , "New leader: None" , [255, 255, 255])
        ultrafast = False
        #jätka lõputult ekraanile joonistamist
        while True:
            if self.exit: break
            setupxts = False
            #if bg: screen.fill([0, 0, 0])
            lowestscore = 999999999999
            lowestplayer = None
            elims = 0
            skips = 0
            for x in range(len(sections)):
            #defineeri mängija
                player = sections[x]
                start = player.start
                scoretext.textlocation = [start + 10, 10]
                scoretext2.textlocation = [start + 12, 12]
                end = player.end
                down = player.down
                level = player.level
                
                score = player.score
                extraframes = player.extraframes
                sleep = player.sleep
                #if self.gamemode == 4: sleep = 0
                bouncy = player.bouncy
                controllable = player.controllable
                base_ball = player.base_ball
                zall = player.zall
                automatic = player.automatic
                immortal = player.immortal
                difficulty = player.difficulty
                unbreakables = player.unbreakables
                lastx = player.lastx
                stuckframes = player.stuckframes
                balls = player.balls
                multiframes = player.multiframes
                timeleft = player.timeleft
                if self.dcollides:
                    for anotherball in balls:
                        if not anotherball == zall:
                            if pygame.Rect.colliderect(zall.GetBallRect(), anotherball.GetBallRect()):
                                if stuckframes > 0:
                                    anotherball.positionx += anotherball.size
                                    anotherball.positiony -= anotherball.size
                                anotherball.forcex = -anotherball.forcex
                                #anotherball.forcey = -anotherball.forcey
                                zall.forcex = -zall.forcex
                                #zall.forcey = -zall.forcey
                                stuckframes += 1
                try:
                    if self.rl:
                        avg_cols = [0, 0, 0]
                        for ball in balls:
                            avg_cols[0] += abs(ball.positionx)
                            avg_cols[1] += abs(ball.positiony)
                            avg_cols[2] += abs(ball.color[2])
                        subject = [avg_cols[0] // abs(len(balls)) + 1, avg_cols[1] // abs(len(balls)) + 1, avg_cols[2] // abs(len(balls)) + 1]
                    else:
                        subject = bouncy[1].color
                except:
                    subject = bouncy[0].color
                if level > 0:
                    bg = (255 - subject[0], 255 - subject[1], 255 - subject[2])
                if True:
                    tbg = bg
                    for i in range(screen_height):
                        col_r = tbg[0]
                        col_g = tbg[1]
                        col_b = tbg[2]
                        col_r -= 0.2
                        col_g -= 0.2
                        col_b -= 0.2
                        if col_r < 0: col_r = 0.2
                        if col_g < 0: col_g = 0.2
                        if col_b < 0: col_b = 0.2
                        tbg = [col_r, col_g, col_b]
                        pygame.gfxdraw.hline(screen, start, end, i, [int(col_r), int(col_g), int(col_b)])
                else:
                    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect((start, 0), (end, screen_height)))
                
                if player.skipme:
                    sections[x].lives = 0
                    player.lives = 0
                    balls = []
                    controllable = False
                    enablestick = False
                    extraframes -= 1
                    gameover.textlocation = [start+((end - start) // 2 - 55), screen_height // 2 - 12]
                    gameover.BlitText(screen)
                    elims += 1
                if self.gamemode == 4 and timeleft == 0:
                    for plr in sections:
                        timeleft = 60 * (4/15) * self.refresh
                        plr.timeleft = 60 * (4/15) * self.refresh
                        self.timeleft = 60 * (4/15) * self.refresh
                    worstscore = 99999999999999
                    worstplayer = 0
                    for i, plr in enumerate(sections):
                        if plr.skipme == False:
                            if plr.score <= worstscore:
                                worstplayer = i
                                worstscore = plr.score
                    sections[worstplayer].skipme = True
                enablestick = player.enablestick
                if not enablestick:
                    down = 0
                joystick = None
                if enablestick:
                    joystick = pygame.joystick.Joystick(player.stickid)
                    joystick.init()
                for event in pygame.event.get():
            #ohutu sulgemine (sündmus)
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            dopause = True
                    if x == playable:
                        if event.type == pygame.KEYDOWN:
                            if sleep > 900: sleep = 6.25 * (4/15) * self.refresh
                            if event.key == pygame.K_SPACE:
                                if self.gamemode == 5:
                                    zall.forcey = -12
                            elif event.key == pygame.K_F1:
                                if not text:
                                    text = True
                                else:
                                    text = False
                            elif event.key == pygame.K_F2:
                                self.cleargame = True
                            elif event.key == pygame.K_F3:
                                if not dev:
                                    dev = True
                                else:
                                    dev = False
                            elif event.key == pygame.K_F4:
                                if not hitbox:
                                    hitbox = True
                                else:
                                    hitbox = False
                            elif event.key == pygame.K_F5:
                                if not bg:
                                    bg = True
                                else:
                                    bg = False
                            if self.gamemode == 5:
                                if event.key == pygame.K_F6:
                                    if not immortal:
                                        immortal = True
                                    else:
                                        immortal = False
                                elif event.key == pygame.K_F7:
                                    sleep = 6.25 * (4/15) * self.refresh
                                    print("Custom ball cheat.")
                                    zall.size=int(input("Ball radius (Aesthetic change)?"))
                                    zall.weight=float(input("Mass (Bigger value means faster fall time)?"))
                                    zall.gravity=float(input("Gravity (Positive values go down, negative values go up)?"))
                                    zall.direction=int(input("Direction (2=Down, 1=Up)?"))
                                    base_ball = zall
                                elif event.key == pygame.K_F8:
                                    if controllable:
                                        if zall.gravity > 0:
                                            base_ball.gravity = -1.2
                                            zall.gravity = -1.2
                                    else:
                                        if zall.gravity > 0:
                                            sections[playable][10].gravity = -1.2
                                            sections[playable][11].gravity = -1.2
                                            
                                elif event.key == pygame.K_F9:
                                    if controllable:
                                        if zall.gravity < 0:
                                            base_ball.gravity = 1.2
                                            zall.gravity = 1.2
                                    else:
                                        if zall.gravity < 0:
                                            sections[playable][10].gravity = 1.2
                                            sections[playable][11].gravity = 1.2
                                elif event.key == pygame.K_F10:
                                    zall.forcex += randint(-10, 10)
                                    zall.forcey += randint(-10, 10)
                                elif event.key == pygame.K_F11:
                                    if not automatic:
                                        automatic = True
                                    else:
                                        automatic = False
                                elif event.key == pygame.K_l:
                                    if self.gamemode == 5:
                                        if len(bouncy) > 0:
                                            player.bouncy = [player.bouncy[-1]]
                                            bouncy = [player.bouncy[-1]]
                                        else:
                                            player.level = 1
                                elif event.key == pygame.K_j:
                                    bouncy = []
                                    player.bouncy = []
                                    goods = 1
                                    unbreakables = 1
                                    player.level -= 2
                                    level -= 2
                                elif event.key == pygame.K_h:
                                    if self.gamemode == 5:
                                        player.lives += 1
                                elif event.key == pygame.K_d:
                                    if self.gamemode == 5:
                                        player.lives -= 1

                                        
                if controllable:
                    if enablestick:
                        if not automatic:
                            if joystick.get_axis(0) * 5 > 0:
                                if bouncy[0].location_x < end - 50:
                                    bouncy[0].location_x += joystick.get_axis(0) * 5
                            else:
                                if bouncy[0].location_x > start - 50:
                                    bouncy[0].location_x += joystick.get_axis(0) * 5
                                
                            for i in range(joystick.get_numhats()):
                                hat = joystick.get_hat(i)
                                if hat[0] == -1:
                                    if bouncy[0].location_x > start - 50:
                                        bouncy[0].location_x -= 15
                                elif hat[0] == 1:
                                    if bouncy[0].location_x < end - 50:
                                        bouncy[0].location_x += 15
                    else:
                        if x == playable:
                            pressed = pygame.key.get_pressed()
                            if not (pressed[pygame.K_LEFT] or pressed[pygame.K_RIGHT]):
                                if controllable:
                                    down = 0
                            if pressed[pygame.K_LEFT]:
                                if controllable:
                                    if not precision:
                                        if bouncy[0].location_x > start - 50:
                                            bouncy[0].location_x -= 15
                                    else:
                                        if bouncy[0].location_x > start - 50:
                                            bouncy[0].location_x -= 5
                            elif pressed[pygame.K_RIGHT]:
                                if controllable:
                                    if not precision:
                                        if bouncy[0].location_x < end - 50:
                                            bouncy[0].location_x += 15
                                    else:
                                        if bouncy[0].location_x < end - 50:
                                            bouncy[0].location_x += 5
                            if pressed[pygame.K_LCTRL]:
                                precision = True
                            else:
                                precision = False
                            
                        #if not mouse_pos == lastpos:
                        #    down = mouse_pos[0] - lastpos[0]
                        #    lastpos = pygame.mouse.get_pos()
                if enablestick:
                    if debounce == 0:
                        for i in range(joystick.get_numbuttons()):
                            if i == 0 and joystick.get_button(i) == True:
                                if not text:
                                    text = True
                                else:
                                    text = False
                                debounce = 20
                            elif i == 1 and joystick.get_button(i) == True:
                                debounce = 20
                                self.cleargame = True
                            elif i == 2 and joystick.get_button(i) == True:
                                if self.gamemode == 5:
                                    zall.forcey = -12
                                    debounce = 20
                            elif i == 3 and joystick.get_button(i) == True:
                                if self.gamemode == 5:
                                    zall.forcex += randint(-10, 10)
                                    zall.forcey += randint(-10, 10)
                                    debounce = 20
                            elif i == 4 and joystick.get_button(i) == True:
                                if not dev:
                                    dev = True
                                else:
                                    dev = False
                                debounce = 20
                            elif i == 5 and joystick.get_button(i) == True:
                                if not automatic:
                                    automatic = True
                                else:
                                    automatic = False
                                debounce = 20
                            elif i == 6 and joystick.get_button(i) == True:
                                if self.gamemode == 5:
                                    if zall.gravity > 0:
                                        base_ball.gravity = -1.2
                                        zall.gravity = -1.2
                                    debounce = 20
                            elif i == 7 and joystick.get_button(i) == True:
                                if self.gamemode == 5:
                                    if zall.gravity < 0:
                                        base_ball.gravity = 1.2
                                        zall.gravity = 1.2
                                    debounce = 20
                            elif i == 8 and joystick.get_button(i) == True:
                                if self.gamemode == 5:
                                    if not immortal:
                                        immortal = True
                                    else:
                                        immortal = False
                                    debounce = 20
                            elif i == 9 and joystick.get_button(i) == True:
                                dopause = True
                                debounce = 20
                for i in range(len(balls)):
                    for obstacle in bouncy:
                        zall = balls[i]
                        appliedforce = obstacle.BounceFeedback(zall.GetBallRect(), [zall.positionx, zall.positiony], 1, zall.forcey, zall)
                        if not appliedforce == [0, 0]:
                            if obstacle.breakable:
                                score += 1
                            if obstacle.life == True:
                                if player.lives < 6:
                                    player.lives += 1
                                    extraframes = 18.75 * (4/15) * self.refresh
                            elif obstacle.multi == True:
                                multiframes = 18.75 * (4/15) * self.refresh
                                for i in range(randint(1, 5)):
                                    e = Ball(15, 0.1 * randint(1, 2), randint(1, 2), randint(5, 10), 1.2, obstacle.location_y + randint(-20, 20), obstacle.location_x + randint(-20, 20), [0, 0], 2)
                                    e.refresh = self.refresh
                                    e.start = start
                                    e.end = end
                                    score += (level * 6 - goods - unbreakables - 1) * i * 10                                    
                                    if not self.dcollides:
                                        e.legacy = True
                                    balls.append(e)
                            zall.color = obstacle.color
                            if obstacle.breakable:
                                obstacle.location_x = -21552
                                if self.sfx: pop.play()
                            else:
                                if self.sfx: bfx.play()
                        zall.forcex += appliedforce[0]
                        zall.forcey += appliedforce[1]
                    balls[i] = zall
                goods = len(bouncy)
                
                for obstacle in bouncy:
                    if obstacle.location_x == -21552: goods -= 1
                    elif obstacle.location_x < player.start:
                        backup = obstacle.location_x
                        obstacle.size_x += backup - player.start
                        obstacle.location_x = start
                        obstacle.DrawObstacle(screen)
                        obstacle.size_x -= backup - player.start
                        obstacle.location_x = backup
                    else:
                        obstacle.DrawObstacle(screen)
            
                        
                jackpot_min = (level * 6 - goods - unbreakables - 1)
                for cnt, e in enumerate(balls):
                    zall = e
                    if cnt > 15:
                        balls = balls[:15]
                        print("Warning: Too many balls! Reducing the number of balls....")
                        break
                    if zall.positiony > screen_height - zall.size:
                        if not immortal:
                            balls.remove(zall)
                            if player.lives > 0:
                                if len(balls) == 0:
                                    sleep = 6.25 * (4/15) * self.refresh
                                if not self.gamemode == 2:
                                    if len(balls) == 0: player.lives -= 1
                                if player.lives == 0: sleep = 6.25 * (4/15) * self.refresh
                                if player.lives > 0:
                                    if len(balls) == 0: zall.positiony = 500                 
                                    if not self.dcollides:
                                        zall.legacy = True
                                    if len(balls) == 0:
                                        zall.positiony = 500
                                        zall.forcex = 1
                                        zall.forcey = 1
                                        balls.append(zall)
                                score -= 10
                                zall = base_ball
                                break
                            else:
                                if not immortal:
                                    if len(balls) == 0:
                                        zall.positiony -= 20
                                        zall.forcex = 0
                                        zall.forcey = 0
                                        if player.lives > -4:
                                            player.lives -= 1                                                                            
                                        if not self.dcollides:
                                            zall.legacy = True
                                        balls.append(zall)
                        else:
                            zall.color = "#ff0000"
                            player.lives -= 1
                            if player.lives == 0 and len(balls) == 0:
                                player.lives = -1
                            elif player.lives == -5:
                                player.lives = -4
                    
                    if sleep == 0: zall.UpdateBall(bounds)
                    if sleep > 0:
                        sleep -= 1
                    if hitbox: pygame.draw.rect(screen, (255, 0, 0), zall.GetBallRect())
                    zall.DrawBall(screen)

                if not level == 0:
                    if goods - unbreakables <= 1:
                        level += 1
                        if level == 64: dead = True
                        score += level * 100
                        bouncy = []
                        zall.positiony = 500
                        zall.forcex = 1
                        zall.forcey = 1
                        balls = [zall]
                        try:
                            base_ball = balls[i]
                        except:
                            base_ball = balls[0]
                            
                        refresh = self.refresh
                        if refresh < 60:
                            refresh = 120-refresh
                        elif refresh > 60:
                            refresh = 250-refresh
                        if x == 0:
                            bouncy = [Obstacle((refresh) * 3/10, 100 - level, 10, randint(start+100, end-100), 550, [0, 0, 255], False, False)]
                        elif x == 1:
                            bouncy = [Obstacle((refresh) * 3/10, 100 - level, 10, randint(start+100, end-100), 550, [255, 0, 0], False, False)]
                        elif x == 2:
                            bouncy = [Obstacle((refresh) * 3/10, 100 - level, 10, randint(start+100, end-100), 550, [0, 255, 0], False, False)]
                        elif x == 3:
                            bouncy = [Obstacle((refresh) * 3/10, 100 - level, 10, randint(start+100, end-100), 550, [255, 255, 0], False, False)]
                        #down = 0
                        unbreakables = 0
                        prev_y = 0
                        prev_x = 0
                        for j in range(0, level * 10, 10):
                            col = [randint(50, 200), randint(50, 200), randint(50, 200)]
                            for i in range(0, 300, 50):
                                b = randint(0, 4)
                                cy = (j // 10)
                                cx = (i // 50)
                                gen = True
                                if self.unjam:
                                    if abs(cy - prev_y) > 2 and abs(cx - prev_x) > 2:
                                        prev_y = cy
                                        prev_x = cx
                                    else:
                                        gen = False
                                bouncy.append(Obstacle((120-self.refresh)/20, 50, 10, start + i, j, col))
                                if self.obs:
                                    if j > 50:
                                        if b > 1 and gen:
                                            bouncy[-1].breakable = False
                                            bouncy[-1].color = [128, 128, 128]
                                            bouncy[-1].bouncy = self.refresh/30
                                            unbreakables += 1
                        if len(bouncy) > 2:
                            if self.mb:
                                ino = randint(1, len(bouncy) - 1)
                                bouncy[ino].color = [200, 128, 0]
                                bouncy[ino].multi = True
                            ino = randint(1, len(bouncy) - 1)
                            if bouncy[ino].breakable == True:
                                if not self.gamemode == 3:
                                    if randint(1, 4) > 1:
                                        bouncy[ino].life = True
                                        bouncy[ino].color = [0, 255, 255]
                                    
                        if not self.gamemode == 5:
                            sleep = 6.25 * (4/15) * self.refresh
                if len(balls) < 2:
                    multiframes = 0
                if not (self.gamemode == 2 or self.gamemode == 4):
                    if player.lives > 0:
                        for i in range(20, 30 * (player.lives - 1), 30):
                            if not immortal:
                                pygame.draw.circle(screen, [255, 255, 255], [player.start + i, 600], 10)
                            else:
                                pygame.draw.circle(screen, [0, 255, 0], [player.start + i, 600], 10)
                    else:
                        for i in range(20, 30 * (-player.lives), 30):
                            pygame.draw.circle(screen, [255, 0, 0], [player.start + i, 600], 10)
                else:
                    dontdiscount = False
                    for plr in sections:
                        if plr.sleep > 0:
                            dontdiscount = True
                    if not ((self.gamemode == 4) and (dontdiscount)):
                        secsleft.textlocation = [start + 30, 600]
                        secsleft.text = str(int(timeleft // ((4/15)*self.refresh))) + " secs"
                        secsleft.BlitText(screen)

                if dev:
                    debugtext = TextClass("Segoe UI", 12, [start+10, 80], "Fx=" + str(zall.forcex) + "; Fy=" + str(zall.forcey), [255, 255, 255])
                    debugtext.BlitText(screen)
                    debugtext = TextClass("Segoe UI", 12, [start+10, 70], "G=" + str(zall.gravity) + "; m=" + str(zall.weight) + "; nballs=" + str(len(balls)), [255, 255, 255])
                    debugtext.BlitText(screen)
                    debugtext = TextClass("Segoe UI", 12, [start+10, 90], "Direction " + str(zall.direction) + "; Collisions: " + str(zall.collides), [255, 255, 255])
                    debugtext.BlitText(screen)
                    debugtext = TextClass("Segoe UI", 12, [start+10, 100], "X: " + str(zall.positionx), [255, 255, 255])
                    debugtext.BlitText(screen)
                    debugtext = TextClass("Segoe UI", 12, [start+10, 110], "Y: " + str(zall.positiony), [255, 255, 255])
                    debugtext.BlitText(screen)
                    debugtext = TextClass("Segoe UI", 12, [start+10, 120], "Tickers: sleep=" + str(sleep) + ", extraball=" + str(extraframes) + ", stuckframes=" + str(stuckframes) + ", debounce=" + str(debounce), [255, 255, 255])
                    debugtext.BlitText(screen)
                hasmulti = False
                for ob in bouncy:
                    if ob.multi and ob.location_x >= 0 and ob.location_y >= 0:
                        hasmulti = True
                if text:
                    scoretext.text = "Score: " + str(score)
                    scoretext2.text = "Score: " + str(score)
                    if self.dropshadows:
                        scoretext2.BlitText(screen)
                    
                    block = "blocks"
                    if goods - unbreakables - 1 == 1:
                        block = "block"
                    if self.dropshadows:
                        leveltext2.text = "Level: " + str(level) + " (" + str(goods - unbreakables - 1) + f" {block} left)"
                        leveltext2.textlocation = [start+12, 32]
                        leveltext2.BlitText(screen)
                    
                    leveltext.text = "Level: " + str(level) + " (" + str(goods - unbreakables - 1) + f" {block} left)"
                    leveltext.textlocation = [start+10, 30]
                    if self.mb and jackpot_min > 1 and hasmulti:
                        if self.dropshadows:
                            jacks.text = "Bonus: " + str(jackpot_min) + "x"
                            jacks.textlocation = [start+12, 52]
                            jacks.BlitText(screen)
                        jack.text = "Bonus: " + str(jackpot_min) + "x"
                        jack.textlocation = [start+10, 50]
                        jack.BlitText(screen)
                    leveltext.BlitText(screen)
                    scoretext.BlitText(screen)
                if sleep == 998: sleep = 999
                if timeleft <= 0 and self.gamemode == 2:
                    timeup.textlocation = [start+((end - start) // 2 - 40), screen_height // 2 - 12]
                    timeup.BlitText(screen)
                    extraframes -= 1
                elif sleep > 0:
                    if player.lives == 0:
                        gameover.textlocation = [start+((end - start) // 2 - 55), screen_height // 2 - 12]
                        gameover.BlitText(screen)
                    else:
                        readytext.textlocation = [start+((end - start) // 2 - 25), screen_height // 2 - 12]
                        readytext.BlitText(screen)
                elif extraframes > 0:
                    extratext.textlocation = [start+((end - start) // 2 - 40), screen_height // 2 - 12]
                    extratext.BlitText(screen)
                    extraframes -= 1
                elif multiframes > 0:
                    multitext.textlocation = [start+((end - start) // 2 - 40), screen_height // 2 - 12]
                    multitext.BlitText(screen)
                    multiframes -= 1
                if debounce > 0: debounce -= 1

                if sleep == 0:
                    if round(lastx, 4) == round(zall.positionx, 4):
                        if stuckframes > 10:
                            zall.forcex += randint(-10, 10)
                            zall.forcey += randint(-10, 10)
                        else:
                            stuckframes += 1
                    else:
                        stuckframes = 0
                else:
                    stuckframes = 0
                if self.gamemode == 2:
                    if sleep < 1:
                        timeleft -= 0.25
                        if timeleft <= 0:
                            timeleft = 0
                            player.lives = 0
                            balls = []
                lastx = zall.positionx
                if automatic:
                    bouncy[0].location_x = player.automove(self.dl)
                if self.gamemode == 4:
                    dontdiscount = False
                    for plr in sections:
                        if plr.sleep > 0:
                            dontdiscount = True
                    if not dontdiscount:
                        timeleft -= 0.25
                        if timeleft <= 0:
                            timeleft = 0
                player.start = start
                player.end = end
                player.down = down
                player.level = level
                player.score = score
                player.extraframes = extraframes
                player.sleep = sleep
                player.bouncy = bouncy
                player.controllable = controllable
                player.base_ball = base_ball
                player.zall = zall
                player.automatic = automatic
                player.immortal = immortal
                player.difficulty = difficulty
                player.unbreakables = unbreakables
                player.lastx = lastx
                player.stuckframes = stuckframes
                player.balls = balls
                player.multiframes = multiframes
                player.timeleft = timeleft
                player.enablestick = enablestick
                sections[x] = player
            skips = 0
            for player in sections:
                if player.skipme == True:
                    skips += 1
            zerolives = 0
            plr_res = []
            best = 0
            maxsc = 0
            if not immortal:
                for i, pl in enumerate(sections):
                    plr_res.append([pl.level, pl.score])
                    if pl.lives == 0:
                        zerolives += 1
                    if pl.score > maxsc:
                        best = i
                        maxsc = pl.score
            if not best == lastbest:
                showbest = 150
            if showbest > 0:
                showbest -= 1
                debugtext.textlocation = [bounds[0] // 2 - 100, bounds[1] - 100]
                debugtext.text = "New leader: Player " + str(best + 1)
                debugtext.BlitText(screen)
            lastbest = best
            if self.gamemode == 4 and skips == 4:
                self.GGMenu(plr_res)
            elif zerolives == len(sections):
                self.GGMenu(plr_res)
            pygame.display.flip()
            if not ultrafast:
                clock.tick(self.refresh)
            if dopause:
                self.PauseMenu()
                dopause = False
            if setupxts:
                self.exit = True
                pygame.quit()
            if self.cleargame:
                sections = []
                if self.gamemode == 2:
                    self.time = 4/15 * self.refresh * 150
                elif self.gamemode == 4:
                    self.time = 4/15 * self.refresh * 60
                for i in range(self.players):
                    sections.append(CreatePlayer((i * 300 - 20) + 20, (i * 300 - 20) + 20 + 300, i))
                    if self.plrs[i] == 1:
                        sections[-1].automatic = False
                        sections[-1].controllable = True
                    elif self.plrs[i] > 1:
                        sections[-1].enablestick = True
                        sections[-1].stickid = self.plrs[i] - 2
                        sections[-1].automatic = False
                        sections[-1].controllable = True
                    if not self.gamemode == 4: timeleft = 4/15 * self.refresh * 150
                    if self.gamemode == 4: timeleft = 4/15 * self.refresh * 60
                playable = 0
                for i in range(self.players):
                    if self.plrs[i] == 1:
                        playable = i
                self.cleargame = False
            if elims > len(sections):
                self.GGMenu(plr_res)
