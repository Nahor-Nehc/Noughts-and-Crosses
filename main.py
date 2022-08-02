import pygame
import sys
import random

pygame.init()

#colours
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED =   (211,   0,   0)
GREEN = (  0, 150,   0)
DGREEN = ( 0, 100,   0)
BLUE =  (  0,   0, 211)
LBLUE = (137, 207, 240)
GREY =  (211, 211, 211)
LBROWN  = (185, 122, 87)
DBROWN = (159, 100, 64)

#general constants
DURATION = 1500 #ms
PADDING = 40

#fonts
FONT = pygame.font.SysFont("calibri.ttf", 300)
SCOREFONT = pygame.font.SysFont("calibri.ttf", 20)
DISPLAYFONT = pygame.font.SysFont("calibri.ttf", 50)

#frames per second
FPS = 30

MODES = ["P v P", "P v C - EASY", "P v C - MEDIUM", "P v C - IMPOSSIBLE"]

#dimensions
WIDTH, HEIGHT = 600 + PADDING*2, 600 + PADDING*2

#window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Noughts and Crosses")
BOXWIDTH = (WIDTH - PADDING*2)/3

P1WINS = pygame.USEREVENT + 1
P2WINS = pygame.USEREVENT + 2
DRAW = pygame.USEREVENT + 3

BOXES = [
  pygame.Rect(PADDING, PADDING, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH, PADDING, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH*2, PADDING, BOXWIDTH, BOXWIDTH),


  pygame.Rect(PADDING, PADDING + BOXWIDTH, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH, PADDING + BOXWIDTH, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH*2, PADDING + BOXWIDTH, BOXWIDTH, BOXWIDTH),

  pygame.Rect(PADDING, PADDING + BOXWIDTH*2, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH, PADDING + BOXWIDTH*2, BOXWIDTH, BOXWIDTH),
  pygame.Rect(PADDING + BOXWIDTH*2, PADDING + BOXWIDTH*2, BOXWIDTH, BOXWIDTH),
]

WINNINGPOSITIONS = [
  [0, 1, 2],
  [3, 4, 5],
  [6, 7, 8],
  [0, 3, 6],
  [1, 4, 7],
  [2, 5, 8],
  [0, 4, 8],
  [2, 4, 6]
  #nice
]  

def checkCase(locations, addition = None):
  if addition != None:
    locations.append(addition)
  for position in range(0, len(WINNINGPOSITIONS)):
    temp = []
    for loc in WINNINGPOSITIONS[position]:
      if loc in locations:
        temp.append(True)
      else:
        temp.append(False)
    
      if temp == [True, True, True]:
        return True

def checkFork(locations, filledSquares):
  winningMoves = 0
  checked = 0
  for pos in range(0, 9):
    if pos not in filledSquares and pos not in locations:
      check = checkCase(locations, addition = pos)
      checked = pos
      if check:
        winningMoves += 1
      locations.remove(checked)

  return winningMoves >= 2

def checkWinningMove(p1locations, p2locations):
  checked = []
  for pos in range(0, 9):
    if pos not in p2locations and pos not in p1locations:
      check = checkCase(p2locations, addition=pos)
      
      checked.append(pos)
      for item in checked:
        p2locations.remove(item)
      checked = []
      if check == True:
        return pos

  return False

class computerMove:
  def easy(p1locations, p2locations):
    #random moves unless winning move exists then 50% chance it does winning move

    #if len(p2locations) >= 2:
    pos = checkWinningMove(p1locations, p2locations)
    if pos != False:
      if random.randint(0, 1) == 1:
        return pos

    cont = True
    while cont:
      pos = random.randint(0, 8)
      if pos not in p1locations and pos not in p2locations:
        return pos

  def medium(p1locations, p2locations):
    #some easy moves, some impossible moves
    chance = random.randint(0, 1)
    if chance == 0:
      return computerMove.easy(p1locations, p2locations)
    else:
      return computerMove.impossible(p1locations, p2locations)

  def impossible(p1locations, p2locations):
    print("\n")
    # algorithm:
    # Check for CPU win move
    print("checking for winning moves")
    pos = checkWinningMove(p1locations, p2locations)
    if pos != False:
      print("won")
      return pos
    # Check for player win move - to block
    print("checking for blocks")
    pos = checkWinningMove(p2locations, p1locations)
    if pos != False:
      print("blocked", p1locations, p2locations)
      return pos
    # Check for CPU fork opportunity - if multiple, choose randomly
    print("checking for forks")
    checked = []
    forks = []
    for pos in range(0, 9):
      if pos not in p1locations and pos not in p2locations:
        p2locations.append(pos)
        if checkFork(p2locations, p1locations):
          forks.append(pos)
        checked.append(pos)
        for item in checked:
          p2locations.remove(item)
        checked = []

    if forks != []:
      print("forked")
      rand = random.randrange(0, len(forks))
      return forks[rand]

    # Check for player fork opportunity, but choose to force a block if there are two potential forks
    print("checking for player forks")
    checked = []
    forks = []
    for pos in range(0, 9):
      if pos not in p1locations and pos not in p2locations:
        p1locations.append(pos)
        check = checkFork(p1locations, p2locations)
        if check:
          print("player has fork opportunity")
          forks.append(pos)
        checked.append(pos)
        for item in checked:
          p1locations.remove(item)
        checked = []

    if len(forks) > 1:
      print("forcing block because player has multiple fork opportunities")
      pass

    elif len(forks) == 1:
      print("blocked fork")
      rand = random.randrange(0, len(forks))
      return forks[rand]

    # Check center
    print("checking centre")
    if 4 not in p1locations and 4 not in p2locations:
      print("placed centre")
      return 4

    # Check corners
    print("checking corners")
    potentials = []
    for i in range(0, 9):
      if i % 2 == 0 and i != 4:
        if i not in p1locations and i not in p2locations:
          potentials.append(i)
    
    if potentials != []:
      rand = random.randrange(0, len(potentials))
      return potentials[rand]

    # Check sides
    print("checking sides")
    potentials = []
    for i in range(0, 9):
      if i % 2 == 1:
        if i not in p1locations and i not in p2locations:
          potentials.append(i)
    
    if potentials != []:
      rand = random.randrange(0, len(potentials))
      print("placed side")
      return potentials[rand]


def updateWin(state, player1Locations, player2Locations, player1Score, player2Score, display, mode, player1Turn):
  pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

  if state == "menu":
    text = SCOREFONT.render("Player1 Score: " + str(player1Score), 1, WHITE)
    WIN.blit(text, (PADDING/2, PADDING/2))

    text = SCOREFONT.render("Player2 Score: " + str(player2Score), 1, WHITE)
    WIN.blit(text, (WIDTH - PADDING/2 - text.get_width(), PADDING/2))

    text = SCOREFONT.render("Press R to reset player scores", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING/2))

    text = DISPLAYFONT.render("Press SPACE to start", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT - PADDING*2))

    text = DISPLAYFONT.render(mode, 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT/2))

    pygame.draw.polygon(WIN, WHITE, [(PADDING*3, HEIGHT/2 + text.get_height()/2), (PADDING*4, HEIGHT/2 + text.get_height()), (PADDING*4, HEIGHT/2)])

    pygame.draw.polygon(WIN, WHITE, [(WIDTH - PADDING*3, HEIGHT/2 + text.get_height()/2), (WIDTH - PADDING*4, HEIGHT/2 + text.get_height()), (WIDTH - PADDING*4, HEIGHT/2)])

    if mode != MODES[0]:
      text = SCOREFONT.render("User is always Player 1", 1, WHITE)
      WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT/2 + HEIGHT/7))

    text = SCOREFONT.render("Use arrow keys to change mode", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT/2 + HEIGHT/10))

  if state == "game":
    for box in BOXES:
      pygame.draw.rect(WIN, WHITE, box, 3)

    for loc in player1Locations:
      text = FONT.render("X", 1, WHITE)
      WIN.blit(text, (BOXES[loc].left + (BOXWIDTH - text.get_width())/2, BOXES[loc].top + (BOXWIDTH - text.get_height())/2+PADDING/3))

    for loc in player2Locations:
      text = FONT.render("O", 1, WHITE)
      WIN.blit(text, (BOXES[loc].left + (BOXWIDTH - text.get_width())/2, BOXES[loc].top + (BOXWIDTH - text.get_height())/2+PADDING/3))

    text = SCOREFONT.render("Player1 Score: " + str(player1Score), 1, WHITE)
    WIN.blit(text, (PADDING/2, PADDING/2))

    text = SCOREFONT.render("Player2 Score: " + str(player2Score), 1, WHITE)
    WIN.blit(text, (WIDTH - PADDING/2 - text.get_width(), PADDING/2))

    text = SCOREFONT.render("Press ESCAPE to quit game", 1, WHITE)
    WIN.blit(text, ((WIDTH - text.get_width())/2, HEIGHT - PADDING/2))

    if player1Turn == True:
      text = SCOREFONT.render("Player1 Turn", 1, WHITE)
      WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING/2))
    elif mode == MODES[0]:
      text = SCOREFONT.render("Player2 Turn", 1, WHITE)
      WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING/2))
    else:
      text = SCOREFONT.render("Computer Turn", 1, WHITE)
      WIN.blit(text, ((WIDTH - text.get_width())/2, PADDING/2))

    if display != None:
      if pygame.time.get_ticks() < display[1] + DURATION:
        text = display[0]
        rectheight = text.get_height() + PADDING*2
        rectwidth = text.get_width() + PADDING*2
        pygame.draw.rect(WIN, GREY, pygame.Rect((WIDTH - rectwidth)/2, (HEIGHT - rectheight)/2, rectwidth, rectheight))
        WIN.blit(text, ((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2))

  pygame.display.flip()

def main():

  state = "menu"

  display = None

  aiWaitTime = random.randint(int(DURATION)/2, int(DURATION*1.6))

  end = False
  endTime = 0

  player1Score = 0
  player2Score = 0

  player1Locations = []
  player2Locations = []

  scoresReset = 0

  player1Turn = True # changes between True and False
  player1TurnEnd = 0

  mode = MODES[0]

  #initiates the clock
  clock = pygame.time.Clock()

  #initiates game loop
  run = True
  while run:

    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()

    if player1Score == "-" and scoresReset + DURATION/2 <= pygame.time.get_ticks():
      player1Score = 0
      player2Score = 0

    if end == True:
      if endTime + DURATION <= pygame.time.get_ticks():
        player1Turn = True
        player1Locations = []
        player2Locations = []
        end = False

    if mode != MODES[0] and player1Turn == False and player1TurnEnd + aiWaitTime <= pygame.time.get_ticks() and end == False:
      if mode == MODES[1]:
        newPos = computerMove.easy(player1Locations, player2Locations)

      elif mode == MODES[2]:
        newPos = computerMove.medium(player1Locations, player2Locations)

      elif mode == MODES[3]:
        newPos = computerMove.impossible(player1Locations, player2Locations)

      aiWaitTime = random.randint(int(DURATION)/2, int(DURATION*1.6))

      player2Locations.append(newPos)
      player1Turn = True

      if checkCase(player2Locations):
        pygame.event.post(pygame.event.Event(P2WINS))

    #for everything that the user has inputted ...
    for event in pygame.event.get():

      #if the 'x' button is pressed ...
      if event.type == pygame.QUIT:

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        sys.exit()

      if event.type == pygame.KEYDOWN:

        if state == "menu":
          if event.key == pygame.K_SPACE:
            state = "game"

          if event.key == pygame.K_LEFT:
            mode = MODES[MODES.index(mode) - 1]
            if mode == MODES[-1]:
              mode = MODES[len(MODES) - 1]
          
          if event.key == pygame.K_RIGHT:
            if mode == MODES[len(MODES) - 1]:
              mode = MODES[0]
            else:
              mode = MODES[MODES.index(mode) + 1]

          if event.key == pygame.K_r:
            player1Score = "-"
            player2Score = "-"
            scoresReset = pygame.time.get_ticks()

        if state == "game":
          if event.key == pygame.K_ESCAPE:
            state = "menu"
            player1Turn = True
            player1Locations = []
            player2Locations = []

      if event.type == pygame.MOUSEBUTTONDOWN:

        if state == "game":

          if (player1Turn == True and mode != MODES[0]) or (mode == MODES[0]):
            for box in BOXES:
              if box.collidepoint(mouse):
                indx = BOXES.index(box)
                if indx not in player1Locations and indx not in player2Locations:
                  if player1Turn == True:
                    player1Locations.append(indx)
                    player1Turn = not player1Turn
                    if mode != MODES[0]:
                      player1TurnEnd = pygame.time.get_ticks()
                  else:
                    if mode == MODES[0]:
                      player2Locations.append(indx)
                      player1Turn = not player1Turn

                  if checkCase(player1Locations):
                    pygame.event.post(pygame.event.Event(P1WINS))

                  elif checkCase(player2Locations):
                    pygame.event.post(pygame.event.Event(P2WINS))

                  elif len(player1Locations) + len(player2Locations) == 9:
                    pygame.event.post(pygame.event.Event(DRAW))

      if event.type == P1WINS:
        display = [DISPLAYFONT.render("Player 1 wins", 1, BLACK), pygame.time.get_ticks()]
        player1Score += 1
        endTime = pygame.time.get_ticks()
        end = True

      if event.type == P2WINS:
        display = [DISPLAYFONT.render("Player 2 wins", 1, BLACK), pygame.time.get_ticks()]
        player2Score += 1
        endTime = pygame.time.get_ticks()
        end = True

      if event.type == DRAW:
        display = [DISPLAYFONT.render("Draw", 1, BLACK), pygame.time.get_ticks()]
        endTime = pygame.time.get_ticks()
        player1Score += 0.5
        player2Score += 0.5
        end = True

    updateWin(state, player1Locations, player2Locations, player1Score, player2Score, display, mode, player1Turn)

main()