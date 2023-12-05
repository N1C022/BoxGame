import pygame

SCREEN = WIDTH, HEIGHT = 300, 300
CELLSIZE = 40
PADDING = 20
ROWS = COLS = (WIDTH - 4 * PADDING) // CELLSIZE
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.NOFRAME)

WHITE = (255, 255, 255)
RED = (252, 91, 122)
BLUE = (78, 193, 246)
GREEN = (0, 255, 0)
PURPLE = (160, 32, 240)
ORANGE = (255, 165, 0)
BLACK = (12, 12, 12)

player1: dict = {"name":"", "color":None}
player2: dict = {"name":"", "color":None}
font = pygame.font.SysFont('Calibri(Body)', 25)

COLORS = {
    "RED": RED,
    "BLUE": BLUE,
    "GREEN": GREEN,
    "PURPLE": PURPLE,
    "ORANGE": ORANGE,
}

def get_player_color():
    color = input("Choose a color: RED, BLUE, GREEN, PURPLE or ORANGE").upper()
    while color not in COLORS:
        color = input("Choose a color: RED, BLUE, GREEN, PURPLE or ORANGE").upper()
    return COLORS[color]

player1["name"] = input("Enter Player1's Name")
player1["color"] = get_player_color()
player2["name"] = input("Enter Player2's Name")
player2["color"] = get_player_color()

class Box:
  def __init__(self, r, c):
    self.r = r
    self.c = c
    self.index = self.r * ROWS + self.c

    self.rect = pygame.Rect((self.c*CELLSIZE + 2*PADDING, self.r*CELLSIZE + 3*PADDING, CELLSIZE, CELLSIZE))
    self.left = self.rect.left
    self.top = self.rect.top
    self.right = self.rect.right
    self.bottom = self.rect.bottom
    self.edges = [
            [(self.left, self.top), (self.right, self.top)],
            [(self.right, self.top), (self.right, self.bottom)],
            [(self.right, self.bottom), (self.left, self.bottom)],
            [(self.left, self.bottom), (self.left, self.top)]
           ]
    self.sides = [False]*4
    self.winner = None

  def checkwin(self, winner):
    if not self.winner:
      if self.sides == [True]*4:
        self.winner = winner
        if winner == 'P1':
          self.color = player1["color"]
        else:
          self.color = player2["color"]
        self.text = font.render(self.winner, True, WHITE)

        return 1
    return 0

  def update(self, win):
    if self.winner:
      pygame.draw.rect(win, self.color, self.rect)
      win.blit(self.text, (self.rect.centerx-5, self.rect.centery-7))

    for index, side in enumerate(self.sides):
      if side:
        pygame.draw.line(win, WHITE, (self.edges[index][0]),
                    (self.edges[index][1]), 2)

def create_boxes():
    return [Box(r, c) for r in range(ROWS) for c in range(COLS)]

def reset_boxs():
  pos = None
  boxy = None
  up = False
  right = False
  bottom = False
  left = False
  return pos, boxy, up, right, bottom, left

def reset_score():
  fillcount = 0
  p1_score = 0
  p2_score = 0
  return fillcount, p1_score, p2_score

def reset_player():
  turn = 0
  players = ['P1', 'P2']
  player = players[turn]
  next_turn = False
  return turn, players, player, next_turn

gameover = False
boxs = create_boxes()
pos, boxy, up, right, bottom, left = reset_boxs()
fillcount, p1_score, p2_score = reset_score()
turn, players, player, next_turn = reset_player()

running = True
while running:
  win.fill(BLACK)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

    if event.type == pygame.MOUSEBUTTONDOWN:
      pos = event.pos

    if event.type == pygame.MOUSEBUTTONUP:
      pos = None

    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        running = False

      if event.key == pygame.K_r:
        gameover = False
        boxs = create_boxes()
        pos, boxy, up, right, bottom, left = reset_boxs()
        fillcount, p1_score, p2_score = reset_score()
        turn, players, player, next_turn = reset_player()

      if not gameover:
        if event.key == pygame.K_UP:
          up = True
        if event.key == pygame.K_RIGHT:
          right = True
        if event.key == pygame.K_DOWN:
          bottom = True
        if event.key == pygame.K_LEFT:
          left = True

    if event.type == pygame.KEYUP:
      if event.key == pygame.K_UP:
        up = False
      if event.key == pygame.K_RIGHT:
        right = False
      if event.key == pygame.K_DOWN:
        bottom = False
      if event.key == pygame.K_LEFT:
        left = False

  for r in range(ROWS+1):
    for c in range(COLS+1):
      pygame.draw.circle(win, WHITE, (c*CELLSIZE + 2*PADDING, r*CELLSIZE + 3*PADDING), 2)
  for box in boxs:
    box.update(win)
    if pos and box.rect.collidepoint(pos):
      boxy = box

  if boxy:
    index = boxy.index
    if not boxy.winner:
      pygame.draw.circle(win, RED, (boxy.rect.centerx, boxy.rect.centery), 2)

    if up and not boxy.sides[0]:
      boxy.sides[0] = True
      if index - ROWS >= 0:			
        boxs[index-ROWS].sides[2] = True
        next_turn = True
    if right and not boxy.sides[1]:
      boxy.sides[1] = True
      if (index + 1) % COLS > 0:
        boxs[index+1].sides[3] = True
        next_turn = True
    if bottom and not boxy.sides[2]:
      boxy.sides[2] = True
      if index + ROWS < len(boxs):			
        boxs[index+ROWS].sides[0] = True
        next_turn = True
    if left and not boxy.sides[3]:
      boxy.sides[3] = True
      if (index % COLS) > 0:
        boxs[index-1].sides[1] = True
        next_turn = True

    res = boxy.checkwin(player)
    if res:
      fillcount += res
      if player == 'P1':
        p1_score += 1
      else:
        p2_score += 1
      if fillcount == ROWS * COLS:
        print(p1_score, p2_score)
        gameover = True

    if next_turn:
      turn = (turn + 1) % len(players)
      player = players[turn]
      next_turn = False

  p1img = font.render(f'{player1["name"]} : {p1_score}', True, WHITE)
  p1rect = p1img.get_rect()
  p1rect.x, p1rect.y = PADDING, 15

  p2img = font.render(f'{player2["name"]} : {p2_score}', True, WHITE)
  p2rect = p2img.get_rect()
  p2rect.right, p2rect.y = WIDTH-2*PADDING, 15

  win.blit(p1img, p1rect)
  win.blit(p2img, p2rect)
  if player == 'P1':
    pygame.draw.line(win, WHITE, (p1rect.x, p1rect.bottom+2), 
              (p1rect.right, p1rect.bottom+2), 1)
  else:
    pygame.draw.line(win, WHITE, (p2rect.x, p2rect.bottom+2), 
              (p2rect.right, p2rect.bottom+2), 1)

  if gameover:
    rect = pygame.Rect((50, 100, WIDTH-100, HEIGHT-200))
    pygame.draw.rect(win, BLACK, rect)
    pygame.draw.rect(win, RED, rect, 2)

    over = font.render('Game Over', True, WHITE)
    win.blit(over, (rect.centerx-over.get_width()/2, rect.y + 10))

    winner = '1' if p1_score > p2_score else '2'
    winner_img = font.render(f'Player {winner} Won', True, GREEN)
    win.blit(winner_img, (rect.centerx-winner_img.get_width()/2, rect.centery- 10))

    msg = 'Press r:restart, q:quit'
    msgimg = font.render(msg, True, RED)
    win.blit(msgimg, (rect.centerx-msgimg.get_width()/2, rect.centery + 20))

  pygame.draw.rect(win, WHITE, (0,0,WIDTH,HEIGHT),2, border_radius=10)
  pygame.display.update()

pygame.quit()
