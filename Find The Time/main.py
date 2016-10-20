import pygame, random, time

# pygame and screen init
pygame.init()
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.SWSURFACE, 24)

# asset loading
buttonSheet = pygame.image.load("buttons.png")
spriteSheet = pygame.image.load("clocks.png")
mask = pygame.image.load("ui_mask.png")
font = pygame.font.Font("pn.ttf", 55)
daleSheet = pygame.image.load("icon_spritesheet.png")


# colors
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
lightBlue = (153, 217, 234)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)

levelCap = 12

sprites = []
# number of sprites per row/col of sheet
sheetSide = 24
# number of pixels per side of sprite
spriteSide = 16
# background selection color of mouse
mouseColor = (174, 225, 238)

# populate sprites list with clock sprite surfaces
for j in range(sheetSide):
    for k in range(sheetSide):
        surf = pygame.Surface((spriteSide, spriteSide))
        surf.blit(spriteSheet, (0, 0), (spriteSide * j, spriteSide * k, spriteSide, spriteSide))
        sprites.append(surf)

highScoreRect = pygame.Rect(590, 50, 160, 40)
curTimeRect = pygame.Rect(590, 115, 160, 40)
curLevelRect = pygame.Rect(590, 180, 160, 40)
resetRect = pygame.Rect(580, 435, 180, 60)
quitRect = pygame.Rect(580, 500, 180, 60)

daleSurf = pygame.Surface((150, 150))
daleSheetRect = pygame.Rect(0, 0, 150, 150)
daleRect = pygame.Rect(595, 257, 150, 150)
daleSurf.set_colorkey((255, 174, 201))
daleSurf.blit(daleSheet, (0, 0), daleSheetRect)

title = pygame.image.load("title_screen.png")
credit = pygame.image.load("credit_screen.png")

firstRun = True

def main():
    set_startTime()
    set_grid(screen)
    
def game_over(surf, win):
    if win:
        cT = get_currentTime()
        hS = get_highScore()
        if cT < hS:
            set_highScore(cT)
            surf.blit(credit, (50, 50))
        elif cT > hS:
            surf.blit(credit, (50, 50))
    elif not win:
        surf.blit(credit, (50, 50))
    surf.blit(daleSurf, (daleRect))
    surf.blit(buttonSheet, (resetRect), (0, 0, 180, 60))
    surf.blit(buttonSheet, (quitRect), (0, 120, 180, 60))
    pygame.display.flip()
    time.sleep(5)
    set_done()
    
def get_mousePos(trueVal = True):
    if trueVal:
        global mouseX, mouseY
        mouseX = pygame.mouse.get_pos()[0]
        mouseY = pygame.mouse.get_pos()[1]
    elif not trueVal:
        return mouseX + 1, mouseY + 1

def get_mouseLeft(event):
    global leftClick
    if event.type == pygame.MOUSEBUTTONUP:
        return True
    return False

def get_mouseHeld():
    global leftHeld
    if pygame.mouse.get_pressed()[0]:
        return True
    return False
    
def set_grid(surf):
    global grid
    grid = Grid(surf)

def get_gameRect():
    global gameRect
    gameRect = pygame.Rect(50, 50, 500, 500)
    return gameRect

def set_done():
    global done
    done = True
    return done

def get_done():
    return done

def get_startTime():
    return startTime

def set_startTime():
    global startTime
    startTime = time.time()
    return startTime

def get_currentTime():
    currentTime = (round(time.time() - get_startTime(), 1))
    return currentTime

def get_highScore():
    global hiscOld
    hiscFile = open("highscores.txt", "r")
    hiscOld = float(hiscFile.read())
    hiscFile.close()
    return hiscOld
    
def set_highScore(score):
    global hiscNew
    hiscNew = open("highscores.txt", "w")
    hiscNew.write(str(score))
    hiscNew.close()

def panels(surf):
    draw_info(surf)
    
    if resetRect.collidepoint(get_mousePos(False)) and get_mouseLeft(event):
        main()
    if quitRect.collidepoint(get_mousePos(False)) and get_mouseLeft(event):
        game_over(surf, False)

def draw_info(surf):
    highScoreText = font.render(str(get_highScore()), 0, black)
    curTimeText = font.render(str(get_currentTime()), 0, black)
    curLevelText = font.render(str(grid.level - 1), 0, black)
    surf.blit(highScoreText, (700, 45))
    surf.blit(curTimeText, (700, 110))
    surf.blit(curLevelText, (725, 175))

def draw_reset(surf):
    surf.blit(buttonSheet, (resetRect), (0, 0, 180, 60))
    if pygame.mouse.get_pressed()[0] and resetRect.collidepoint(get_mousePos(False)):
        surf.blit(buttonSheet, (resetRect), (0, 60, 180, 60))

def draw_quit(surf):
    surf.blit(buttonSheet, (quitRect), (0, 120, 180, 60))
    if pygame.mouse.get_pressed()[0] and quitRect.collidepoint(get_mousePos(False)):
        surf.blit(buttonSheet, (quitRect), (0, 180, 180, 60))
      
#------------------------------------------------------------------------------------------------------------------------------------#

class Grid(object):
    def __init__(self, surf, n = 1):
        self.level = n
        self.side = 500
        self.clocks = []
        self.solution = None
        self.build(surf)
        self.displaying_solution = False
    def build(self, surf):
        del self.clocks[:]
        # calculate clock radius by size of game window and number of clocks
        self.rad = int(self.side / self.level)
        for i in range(self.level):
            for j in range(self.level):
                # go through each row and column and create a clock object with a random sprite (w/ random color)
                x = (j * self.side / self.level) + 50
                y = (i * self.side / self.level) + 50
                currentSprite = sprites[random.randint(0, len(sprites) - 1)]
                
                # check for clock duplicates
                indexList = []
                while True:
                    spriteIndex = random.randint(0, len(sprites) - 1)
                    if spriteIndex not in indexList:
                        indexList.append(spriteIndex)
                        break
                    else:
                        continue

                # scale each sprite to center on the screen and colorkey
                tempSprite = pygame.transform.scale(sprites[spriteIndex], (self.rad, self.rad))
                tempSprite.set_colorkey((255, 174, 201))
                self.clocks.append(Clock(x, y, tempSprite))
                
        # solution clock is randomly picked from the list of clocks
        self.solution = self.clocks[random.randint(0, len(self.clocks) - 1)]
        
        # increment level number
        self.level += 1

        if not firstRun:
            surf.fill(lightBlue, get_gameRect())
            draw_info(surf)
            self.display_solution(surf)
            draw_reset(surf)
            draw_quit(surf)

    def update(self, surf):
        if self.level >= levelCap:
            game_over(surf, True)
        skip = False
        if not skip:
            for clock in self.clocks:
                if get_gameRect().collidepoint(get_mousePos(False)):
                    self.display_selectionSquare(surf)
                    if self.solution.rect.collidepoint(get_mousePos(False)) and get_mouseLeft(event):
                        self.build(surf)
                        skip = True
                        return skip
                if (clock != self.solution) and get_mouseLeft(event):
                    game_over(surf, False)
                elif not get_gameRect().collidepoint(get_mousePos(False)):
                    self.display_solution(surf)
                else:
                    self.displaying_solution = False
            
    def render(self, surf):
        # display entire grid
        if not self.displaying_solution:
            for clock in self.clocks:
                clock.render(surf)

    def display_selectionSquare(self, surf):
        for clock in self.clocks:
            if clock.rect.collidepoint(get_mousePos(False)):
                pygame.draw.rect(surf, mouseColor, (clock.rect.x, clock.rect.y, clock.width, clock.height))

    def display_solution(self, surf):
        self.displaying_solution = True
        tempSurf = pygame.transform.scale(self.solution.sprite, (500, 500))
        surf.blit(tempSurf, (50, 50))
            
class Clock(object):
    def __init__(self, x, y, sprite):
        self.x = x
        self.y = y
        self.sprite = sprite
        self.width = self.sprite.get_width()
        self.height = self.width
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surf):
        surf.blit(self.sprite, (self.x, self.y))
        
# main function and loop start
main()
firstRun = False
done = False
key = False
while not done:
    # break statements
    event = pygame.event.poll()
    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
        done = True
    
    # input handling
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            main()

    get_mousePos()
    get_mouseLeft(event)

    screen.fill((200,200,200))
    screen.blit(mask, (0, 0))
    grid.update(screen)
    grid.render(screen)
    panels(screen)
    draw_quit(screen)
    draw_reset(screen)
    screen.blit(daleSurf, (daleRect))

##    while not key:
##        pygame.event.pump()
##        if get_gameRect().collidepoint(get_mousePos(False)) and get_mouseLeft():
##            key = True
##            break
##        pygame.display.flip()

    if get_currentTime() > 60:
        game_over(screen, False)
    
    pygame.display.flip()
pygame.display.quit()



























    
