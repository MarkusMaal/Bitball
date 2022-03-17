#moodulite importimine
import pygame
import pygame.gfxdraw
import sys
from random import randint
from libs.game import *
from libs.TextClass import *
from libs.ball import Ball

pygame.init()
pygame.mixer.init()

bgm = False
sfx = True
hidemenu = False

bcollides = True

quickdebug = False

stuckframes = 0
pygame.display.set_icon(pygame.image.load("img/mode_classic.png"))
pygame.display.set_caption("Bitball")

swap = pygame.mixer.Sound("sfx/pop2.wav")
noval = pygame.mixer.Sound("sfx/invalid1.wav")
sels = pygame.mixer.Sound("sfx/wall2.wav")
mbgm = pygame.mixer.music.load("bgm/menu.ogg")

refresh = 60

def UpdateMenu(bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh):
    if sfx:
        if sel == 1 and gm == 4 and pc == 1:
            noval.play()
            return bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu
        else:
            sels.play()
    if sel == 1:
        if bgm: pygame.mixer.music.stop()
        plrs = [plr1, plr2, plr3, plr4]
        if gm == 2 or gm == 4:
            if dl == 1:
                dl = 2
            elif dl == 2:
                dl = 1
            elif dl == 3:
                dl = 4
            elif dl == 4:
                dl = 3
        StartGame(pc, gm, mb, obs, bgm, sfx, dl, dvr, plrs, ds, unjam, rl, bcollides, refresh)
        if gm == 2 or gm == 4:
            if dl == 2:
                dl = 1
            elif dl == 1:
                dl = 2
            elif dl == 4:
                dl = 3
            elif dl == 3:
                dl = 4
        x = 100
        pygame.init()
        pygame.mixer.init()
        screen = pygame.display.set_mode([screen_width-20, screen_height])
        mbgm = pygame.mixer.music.load("bgm/menu.ogg")
        if bgm:
            pygame.mixer.music.play(-1)
    elif sel == 2:
        pc += 1
        if pc == 5: pc = 1
        items[2].text = "Players: " + str(pc)
        if pc < 4:
            items[12].text = "4: None"
        else:
            if items[12].text == "4: None":
                items[12].text = "4: Computer"
                plr4 = 0
        if pc < 3:
            items[11].text = "3: None"
        else:
            if items[11].text == "3: None":
                items[11].text = "3: Computer"
                plr3 = 0
        if pc < 2:
            items[10].text = "2: None"
        else:
            if items[10].text == "2: None":
                items[10].text = "2: Computer"
                plr2 = 0
    elif sel == 3:
        gm += 1
        if gm == 6: gm = 1
        if gm == 1:
            items[3].text = "Mode: Classic"
        elif gm == 2:
            items[3].text = "Mode: Zen"
        elif gm == 3:
            items[3].text = "Mode: Survival"
        elif gm == 4:
            items[3].text = "Mode: Eliminator"
        elif gm == 5:
            items[3].text = "Mode: Developer"
    elif sel == 4:
        if mb:
            mb = False
            items[4].text = "Multiball: Off"
        else:
            mb = True
            items[4].text = "Multiball: On"
    elif sel == 5:
        if obs and unjam:
            unjam = False
            items[5].text = "Obstacles: Random"
        elif obs:
            obs = False
            items[5].text = "Obstacles: Off"
        else:
            obs = True
            unjam = True
            items[5].text = "Obstacles: Fixed"
    elif sel == 6:
        if sfx:
            sfx = False
            items[6].text = "SFX: Off"
        else:
            sfx = True
            items[6].text = "SFX: On"
    elif sel == 7:
        if bgm:
            bgm = False
            pygame.mixer.music.stop()
            items[7].text = "BGM: Off"
        else:
            bgm = True
            pygame.mixer.music.play(-1)
            items[7].text = "BGM: On"
    elif sel == 16:
        if refresh < 250:
            refresh += 5
        else:
            refresh = 5
        for i in range(len(bouncyballs)):
            bouncyballs[i].refresh = refresh
        items[16].text = f"Refresh rate: {refresh}Hz"
    elif sel == 17:
        bg = [randint(0, 100), randint(0, 100), randint(0, 100)]
        bouncyballs = []
        for i in range(randint(2, 50)):
            bouncyballs.append(Ball(randint(0, 15), randint(0, 10), randint(0, 10), 10, 1.2, randint(0, screen_width), randint(0, screen_height), [0, 0], 2, [randint(0, 255), randint(0, 255), randint(0, 255)]))
            bouncyballs[i].refresh = refresh
            bouncyballs[i].end = screen_width - 20
    elif sel == 8:
        if dl == 1:
            items[8].text = "CPU skill: Intermediate"
            dl = 2
        elif dl == 2:
            items[8].text = "CPU skill: Expert"
            dl = 3
        elif dl == 3:
            items[8].text = "CPU skill: God"
            dl = 4
        elif dl == 4:
            items[8].text = "CPU skill: Novice"
            dl = 1
    elif sel == 9:
        if plr1 == 0:
            plr1 += 1
            items[9].text = "1: Keyboard"
        else:
            if joystick_count > plr1 - 1:
                joystick.init()
                enablestick = False
                if joystick.get_numaxes() > 0:
                    enablestick = True
                joyword = "Joypad"
                if enablestick: joyword = "Joystick"
                items[9].text = "1: " + joyword + " " + str(plr1) + ": " + pygame.joystick.Joystick(plr1 - 1).get_name()
                plr1 += 1
            else:
                items[9].text = "1: Computer"
                plr1 = 0
    elif sel == 10:
        if pc > 1:
            if plr2 == 0:
                plr2 += 1
                items[10].text = "2: Keyboard"
            else:
                if joystick_count > plr2 - 1:
                    joystick.init()
                    if joystick.get_numaxes() > 0:
                        enablestick = True
                    joyword = "Joypad"
                    if enablestick: joyword = "Joystick"
                    items[10].text = "2: " + joyword + " " + str(plr2) + ": " + pygame.joystick.Joystick(plr2 - 1).get_name()
                    plr2 += 1
                else:
                    items[10].text = "2: Computer"
                    plr2 = 0
    elif sel == 11:
        if pc > 2:
            if plr3 == 0:
                plr3 += 1
                items[11].text = "3: Keyboard"
            else:
                if joystick_count > plr3 - 1:
                    joystick.init()
                    if joystick.get_numaxes() > 0:
                        enablestick = True
                    joyword = "Joypad"
                    if enablestick: joyword = "Joystick"
                    items[11].text = "3: " + joyword + " " + str(plr3) + ": " + pygame.joystick.Joystick(plr3 - 1).get_name()
                    plr3 += 1
                else:
                    items[11].text = "3: Computer"
                    plr3 = 0
    elif sel == 12:
        if pc > 3:
            if plr4 == 0:
                plr4 += 1
                items[12].text = "4: Keyboard"
            else:
                if joystick_count > plr4 - 1:
                    joystick.init()
                    if joystick.get_numaxes() > 0:
                        enablestick = True
                    joyword = "Joypad"
                    if enablestick: joyword = "Joystick"
                    items[12].text = "4: " + joyword + " " + str(plr4) + ": " + pygame.joystick.Joystick(plr4 - 1).get_name()
                    plr4 += 1
                else:
                    items[12].text = "4: Computer"
                    plr4 = 0
    elif sel == 13:
        if ds:
            ds = False
            items[13].text = "Drop shadows: Off"
        else:
            ds = True
            items[13].text = "Drop shadows: On"
    elif sel == 14:
        if bcollides:
            bcollides = False
            items[14].text = "Old physics: On"
        else:
            bcollides = True
            items[14].text = "Old physics: Off"
    elif sel == 15:
        if rl:
            rl = False
            items[15].text = "Disco lights: Off"
        else:
            rl = True
            items[15].text = "Disco lights: On"
    elif sel == 18:
        pygame.quit()
        sys.exit()
    elif sel == 19:
        hidemenu = (not hidemenu)
    return bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh


if bgm:
        pygame.mixer.music.play(-1)

# thx Nerd Paradise for this code snippet
def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(opacity)        
        target.blit(temp, location)


# player units
# 0  - Computer Player Unit
# 1  - Human (Keyboard)
# 2+ - Human (Controller name)
plr1 = 1
plr2 = 0
plr3 = 0
plr4 = 0

dvr = False
clock = pygame.time.Clock()
bounds = screen_width, screen_height = 660, 650

bg = [randint(0, 100), randint(0, 100), randint(0, 100)]
bouncyballs = []
for i in range(randint(2, 50)):
    bouncyballs.append(Ball(randint(0, 15), randint(0, 10), randint(0, 10), 10, 1.2, randint(0, screen_width), randint(0, screen_height), [0, 0], 2, [randint(0, 255), randint(0, 255), randint(0, 255)]))
    bouncyballs[i].end = screen_width - 20
welcome = pygame.transform.scale(pygame.image.load("img/welcome.png"), [175, 100])
screen = pygame.display.set_mode([screen_width-20, screen_height])
welcome.convert_alpha()

frame = 0
col_rg = 255
col_b = 0
for l in range(5):
    col_rg = l * 1.1
    col_b = l
    for i in range(screen_height):
        col_rg -= 0.2125
        col_b += 0.0125
        
        if col_rg < 0:
            col_rg = 0
        if col_b > 255:
            col_b = 255
        pygame.gfxdraw.hline(screen, 0, screen_width, i, [int(col_rg), int(col_rg), int(col_b)])
    pygame.display.flip()
    clock.tick(60)
if not quickdebug:
        while frame < 800:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            frame += 5
            
            if frame < 128:
                b = frame / 2
                if b > 255:
                    b = 255
                screen.fill([0, 0, b])
            if 128 > frame > 15:
                blit_alpha(screen, welcome, [screen_width // 2 - 100, screen_height // 2 - 50], 2 * frame)
                blit_alpha(screen, pygame.transform.scale(pygame.image.load("img/msoftware.png"), [200, 50]), [screen_width // 2 - 115, screen_height - 80], 2 * frame)
            elif frame >= 128:
                screen.blit(welcome, [screen_width // 2 - 100, screen_height // 2 - 50])
                screen.blit(pygame.transform.scale(pygame.image.load("img/msoftware.png"), [200, 50]), [screen_width // 2 - 115, screen_height - 80])
            pygame.display.flip()
            clock.tick(60)
        frame = 135
        while frame > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            frame -= 5
            b = frame / 2
            screen.fill([0, 0, b])
            
            blit_alpha(screen, welcome, [screen_width // 2 - 100, screen_height // 2 - 50], 2 * frame)
            blit_alpha(screen, pygame.transform.scale(pygame.image.load("img/msoftware.png"), [200, 50]), [screen_width // 2 - 115, screen_height - 80], 2 * frame)
            pygame.display.flip()
            clock.tick(60)
pygame.joystick.init()
enablestick = False

joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    if joystick.get_numaxes() > 0:
         enablestick = True


pc = 1
sel = 1
gm = 1
x = 0
mb = True
dl = 2
ds = True
obs = True
unjam = True
rl = False
items = []
items.append(TextClass("Tahoma", 40, [screen_width // 2 - 60, 20], "Bitball", [randint(105, 255), randint(105, 255), randint(105, 255)]))
items.append(TextClass("Arial", 20, [20, 80], "Play now", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 100], "Players: " + str(pc), [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 120], "Mode: Classic", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 140], "Multiball: On", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 160], "Obstacles: Fixed", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 180], "SFX: On", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 200], "BGM: Off", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 220], "CPU skill: Intermediate", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 260], "1: Keyboard", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 280], "2: None", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 300], "3: None", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 320], "4: None", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 360], "Drop shadows: On", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 380], "Old physics: Off", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 400], "Disco lights: Off", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 420], "Refresh rate: 60Hz", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 440], "Reload menu", [255, 255, 255]))
items.append(TextClass("Arial", 20, [20, 460], "Exit", [255, 255, 255]))
items.append(TextClass("Lucida Console", 10, [5, screen_height - 15], "ver. 1.2b", [255, 255, 255]))
def StartGame(players, mode, mb, obs, bgm, sfx, dl, dvr, plrs, ds, unjam, rl, dcollides, refresh):
    bounds = screen_width, screen_height = players * 300 + 20, 650
    screen = pygame.display.set_mode([screen_width-20, screen_height])
    newgame = Game(screen, bounds, players, mode, mb, obs, bgm, sfx, dl, dvr, plrs, dcollides)
    newgame.unjam = unjam
    newgame.refresh = refresh
    newgame.rl = rl
    newgame.dropshadows = ds
    newgame.NewGame()

if quickdebug:
        plrs = [plr1, plr2, plr3, plr4]
        StartGame(pc, 5, mb, obs, bgm, sfx, dl, dvr, plrs, ds, unjam, rl)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not hidemenu:
                    sel -= 1
                    if sfx: swap.play()
                    if sel == 0: sel = 1
            elif event.key == pygame.K_DOWN:
                if not hidemenu:
                    sel += 1
                    if sfx: swap.play()
                    if sel > len(items) - 1: sel = len(items) - 1
            elif event.key == pygame.K_LEFT:
                if sel == 16:
                    refresh -= 5
                    if refresh < 5:
                        refresh = 5
                    for i in range(len(bouncyballs)):
                        bouncyballs[i].refresh = refresh
                    items[16].text = f"Refresh rate: {refresh}Hz"
            elif event.key == pygame.K_RIGHT:
                if sel == 16:
                    refresh += 5
                    if refresh > 250:
                        refresh = 250
                    for i in range(len(bouncyballs)):
                        bouncyballs[i].refresh = refresh
                    items[16].text = f"Refresh rate: {refresh}Hz"
            elif event.key == pygame.K_RETURN:
                #try:
                #except Exception as e:
                #    print(f"Error: {e}")
                bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh = UpdateMenu(bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh)
                
            elif event.key == pygame.K_F4:
                for ball in bouncyballs:
                    ball.forcex += 10
                    ball.forcey += 10
            elif event.key == pygame.K_F5:
                for ball in bouncyballs:
                    ball.gravity += 0.1
            elif event.key == pygame.K_F3:
                for ball in bouncyballs:
                    ball.gravity -= 0.1
            elif event.key == pygame.K_F6:
                for ball in bouncyballs:
                    ball.size = randint(10, 30)
            elif event.key == pygame.K_F7:
                for ball in bouncyballs:
                    ball.direction = 1
    if x == 0:
        if enablestick and joystick_count > 0:
            for g in range(joystick_count):
                joystick = pygame.joystick.Joystick(g)
                joystick.init()
                for i in range(joystick.get_numhats()):
                    hat = joystick.get_hat(i)
                    if hat[1] == 1:
                        if not hidemenu:
                            sel -= 1
                            if sfx: swap.play()
                            x = 10
                    elif hat[1] == -1:
                        if not hidemenu:
                            sel += 1
                            if sfx: swap.play()
                            x = 10
                if sel > len(items) - 1: sel = len(items) - 1
                if sel == 0: sel = 1
                for i in range(joystick.get_numbuttons()):
                    if i == 0 and joystick.get_button(i) == True:
                        x = 20
                        try:
                            bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh = UpdateMenu(bgm, sfx, pc, gm, mb, obs, unjam, bg, bouncyballs, dl, plr1, plr2, plr3, plr4, ds, enablestick, items, rl, hidemenu, bcollides, refresh)
                        except Exception as e:
                            print(f"Fatal exception: {e}")
    else:
        x -= 1
    tbg = bg
    for i in range(screen_height):
        col_r = tbg[0]
        col_g = tbg[1]
        col_b = tbg[2]
        col_r += 0.2
        col_g += 0.2
        col_b += 0.2
        if col_r > 255: col_r -= 255
        elif col_g > 255: col_g -= 255
        elif col_b > 255: col_b -= 255
        elif col_r < 0: col_r += 255
        elif col_g < 0: col_g += 255
        elif col_b < 0: col_b += 255
        tbg = [col_r, col_g, col_b]
        pygame.gfxdraw.hline(screen, 0, screen_width, i, [int(col_r), int(col_g), int(col_b)])
    for bouncyball in bouncyballs:
        last = bouncyball.positiony
        if bcollides:
            for anotherball in bouncyballs:
                if not anotherball == bouncyball:
                    if pygame.Rect.colliderect(anotherball.GetBallRect(), bouncyball.GetBallRect()):
                        if stuckframes > 0:
                            if anotherball.positiony > anotherball.size:
                                anotherball.positiony -= anotherball.size
                            else:
                                anotherball.positiony += anotherball.size
                            if anotherball.positionx > anotherball.size:
                                anotherball.positionx -= anotherball.size
                            else:
                                anotherball.positionx += anotherball.size
                        if stuckframes > 10:
                            bouncyball.positionx = randint(0, screen_width - bouncyball.size)
                            bouncyball.positiony = randint(0, screen_height - bouncyball.size)
                            break
                        anotherball.forcex = -anotherball.forcex
                        anotherball.forcey = -anotherball.forcey
                        bouncyball.forcex = -anotherball.forcex
                        bouncyball.forcey = -anotherball.forcey
                        stuckframes += 1
        bouncyball.UpdateBall(bounds)
        nxt = bouncyball.positiony
        if int(last) == int(nxt):
            bouncyball.forcey = randint(20, 50)
            bouncyball.forcex = randint(10, 20)
        bouncyball.DrawBall(screen)
    if not hidemenu:
        for i in range(len(items)):
            backupval = items[i].text
            if sel == i:
                value = randint(200, 255)
                items[i].textcolor = [value - 150, value - 50, value]
                if i == 9:
                    items[i].textcolor = [value - 200, value - 200, value]
                elif i == 10:
                    items[i].textcolor = [value, value - 200, value - 200]
                elif i == 11:
                    items[i].textcolor = [value - 200, value, value - 200]
                elif i == 12:
                    items[i].textcolor = [value, value, value - 200]
                items[i].text = "  " + items[i].text
            else:
                if i > 0:
                     items[i].textcolor = [255, 255, 255]
                if i == 0:
                    u = items[i].textcolor
                    hilo = (randint(0, 2) - 1) * 2
                    u[0] += hilo
                    u[1] += hilo
                    u[2] += hilo
                    if u[0] < 0: u[0] += 255
                    if u[1] < 0: u[1] += 255
                    if u[2] < 0: u[2] += 255
                    if u[0] > 255: u[0] -= 255
                    if u[1] > 255: u[1] -= 255
                    if u[2] > 255: u[2] -= 255
                    items[i].textcolor = u
            items[i].BlitText(screen)
            items[i].text = backupval
        if sel == 1:
            screen.blit(pygame.image.load("img/play.png"), [screen_width - 150, screen_height - 150])
        elif sel == 2:
            if pc == 1: screen.blit(pygame.image.load("img/players_1.png"), [screen_width - 150, screen_height - 150])
            elif pc == 2: screen.blit(pygame.image.load("img/players_2.png"), [screen_width - 150, screen_height - 150])
            elif pc == 3: screen.blit(pygame.image.load("img/players_3.png"), [screen_width - 150, screen_height - 150])
            elif pc == 4: screen.blit(pygame.image.load("img/players_4.png"), [screen_width - 150, screen_height - 150])
        elif sel == 3:
            if gm == 1: screen.blit(pygame.image.load("img/mode_classic.png"), [screen_width - 150, screen_height - 150])
            elif gm == 2: screen.blit(pygame.image.load("img/mode_zen.png"), [screen_width - 150, screen_height - 150])
            elif gm == 3: screen.blit(pygame.image.load("img/mode_survival.png"), [screen_width - 150, screen_height - 150])
            elif gm == 4: screen.blit(pygame.image.load("img/mode_eliminator.png"), [screen_width - 150, screen_height - 150])
            elif gm == 5: screen.blit(pygame.image.load("img/mode_void.png"), [screen_width - 150, screen_height - 150])
        elif sel == 4:
            if mb: screen.blit(pygame.image.load("img/multiball_on.png"), [screen_width - 150, screen_height - 150])
            if not mb: screen.blit(pygame.image.load("img/multiball_off.png"), [screen_width - 150, screen_height - 150])
        elif sel == 5:
            if obs and unjam: screen.blit(pygame.image.load("img/obstacles_on.png"), [screen_width - 150, screen_height - 150])
            if obs and not unjam: screen.blit(pygame.image.load("img/obstacles_on2.png"), [screen_width - 150, screen_height - 150])
            if not obs: screen.blit(pygame.image.load("img/obstacles_off.png"), [screen_width - 150, screen_height - 150])
        elif sel == 6:
            if sfx: screen.blit(pygame.image.load("img/sfx_on.png"), [screen_width - 150, screen_height - 150])
            if not sfx: screen.blit(pygame.image.load("img/sfx_off.png"), [screen_width - 150, screen_height - 150])
        elif sel == 7:
            if bgm: screen.blit(pygame.image.load("img/bgm_on.png"), [screen_width - 150, screen_height - 150])
            if not bgm: screen.blit(pygame.image.load("img/bgm_off.png"), [screen_width - 150, screen_height - 150])
        elif sel == 8:
            if dl == 1: screen.blit(pygame.image.load("img/difficulty_novice.png"), [screen_width - 150, screen_height - 150])
            if dl == 2: screen.blit(pygame.image.load("img/difficulty_intermediate.png"), [screen_width - 150, screen_height - 150])
            if dl == 3: screen.blit(pygame.image.load("img/difficulty_expert.png"), [screen_width - 150, screen_height - 150])
            if dl == 4: screen.blit(pygame.image.load("img/difficulty_god.png"), [screen_width - 150, screen_height - 150])
        elif 13 > sel > 8:
            if sel == 9:
                if plr1 == 0:
                    screen.blit(pygame.image.load("img/cpu.png"), [screen_width - 150, screen_height - 150])
                elif plr1 == 1:
                    screen.blit(pygame.image.load("img/human_keyboard.png"), [screen_width - 150, screen_height - 150])
                else:
                    if pygame.joystick.Joystick(plr1 - 2).get_numaxes() > 0:
                        screen.blit(pygame.image.load("img/human_joystick.png"), [screen_width - 150, screen_height - 150])
                    else:
                        screen.blit(pygame.image.load("img/human_joypad.png"), [screen_width - 150, screen_height - 150])
            if sel == 10:
                if pc > 1:
                    if plr2 == 0:
                        screen.blit(pygame.image.load("img/cpu.png"), [screen_width - 150, screen_height - 150])
                    elif plr2 == 1:
                        screen.blit(pygame.image.load("img/human_keyboard.png"), [screen_width - 150, screen_height - 150])
                    else:
                        if pygame.joystick.Joystick(plr2 - 2).get_numaxes() > 0:
                            screen.blit(pygame.image.load("img/human_joystick.png"), [screen_width - 150, screen_height - 150])
                        else:
                            screen.blit(pygame.image.load("img/human_joypad.png"), [screen_width - 150, screen_height - 150])
                else:
                    screen.blit(pygame.image.load("img/disable.png"), [screen_width - 150, screen_height - 150])
            if sel == 11:
                if pc > 2:
                    if plr3 == 0:
                        screen.blit(pygame.image.load("img/cpu.png"), [screen_width - 150, screen_height - 150])
                    elif plr3 == 1:
                        screen.blit(pygame.image.load("img/human_keyboard.png"), [screen_width - 150, screen_height - 150])
                    else:
                        if pygame.joystick.Joystick(plr3 - 2).get_numaxes() > 0:
                            screen.blit(pygame.image.load("img/human_joystick.png"), [screen_width - 150, screen_height - 150])
                        else:
                            screen.blit(pygame.image.load("img/human_joypad.png"), [screen_width - 150, screen_height - 150])
                else:
                    screen.blit(pygame.image.load("img/disable.png"), [screen_width - 150, screen_height - 150])
            if sel == 12:
                if pc > 3:
                    if plr4 == 0:
                        screen.blit(pygame.image.load("img/cpu.png"), [screen_width - 150, screen_height - 150])
                    elif plr4 == 1:
                        screen.blit(pygame.image.load("img/human_keyboard.png"), [screen_width - 150, screen_height - 150])
                    else:
                        if pygame.joystick.Joystick(plr4 - 2).get_numaxes() > 0:
                            screen.blit(pygame.image.load("img/human_joystick.png"), [screen_width - 150, screen_height - 150])
                        else:
                            screen.blit(pygame.image.load("img/human_joypad.png"), [screen_width - 150, screen_height - 150])
                else:
                    screen.blit(pygame.image.load("img/disable.png"), [screen_width - 150, screen_height - 150])
        elif sel == 13:
            if ds:
                screen.blit(pygame.image.load("img/dropshadow.png"), [screen_width - 150, screen_height - 150])
            else:
                screen.blit(pygame.image.load("img/ddropshadow.png"), [screen_width - 150, screen_height - 150])
        elif sel == 14:
            if bcollides:
                screen.blit(pygame.image.load("img/collides.png"), [screen_width - 150, screen_height - 150])
            else:
                screen.blit(pygame.image.load("img/ncollides.png"), [screen_width - 150, screen_height - 150])
        elif sel == 15:
            if rl:
                screen.blit(pygame.image.load("img/disco.png"), [screen_width - 150, screen_height - 150])
            else:
                screen.blit(pygame.image.load("img/nodisco.png"), [screen_width - 150, screen_height - 150])
        elif sel == len(items) - 3:
            screen.blit(pygame.image.load("img/reload_menu.png"), [screen_width - 150, screen_height - 150])
        elif sel == len(items) - 2:
            screen.blit(pygame.image.load("img/exit.png"), [screen_width - 150, screen_height - 150])
    if stuckframes > 0:
        stuckframes -= 1
    if stuckframes > 10:
        stuckframes -= 10
    if stuckframes > 100:
        stuckframes -= 100
    pygame.display.flip()
    clock.tick(refresh)


