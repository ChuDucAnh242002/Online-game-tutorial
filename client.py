import pygame
from network import Network
import pickle

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 700, 700

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

CLOCK = pygame.time.Clock()

FPS = 60

# Color
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (128, 128, 128)

# Size
PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100

class Button:
    def __init__(self, text, x ,y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y +self.height:
            return True
        else: return False

def redrawWindow(win, game, p):
    win.fill(GREY)

    if not(game.connected()):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("Waiting for Player...", 1, RED, True)
        win.blit(text, (WIDTH // 2 - text.get_width() / 2, HEIGHT // 2 - text.get_height() / 2 ))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponents", 1, (0, 255, 255))
        win.blit(text, (380, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.bothWent():
            text1 = font.render(move1, 1, (0,0,0))
            text2 = font.render(move2, 1, (0, 0, 0))
        else:
            if game.p1Went and p == 0:
                text1 = font.render(move1, 1, (0,0,0))
            elif game.p1Went:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))

            if game.p2Went and p == 1:
                text2 = font.render(move2, 1, (0,0,0))
            elif game.p2Went:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, BLACK), Button("Scissors", 250, 500, RED), Button("Paper", 450, 500, GREEN)]
def main():
    run = True
    n = Network()

    player = int(n.getP())
    print("You are player", player)

    while run:

        CLOCK.tick(FPS)
        try:
            game = n.send("get")
        except:
            print("1")
            run = False
            print("Couldn't get game")
            break

        if game.bothWent():
            redrawWindow(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("2")
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.winner() == 1 and player == 1) or (game.winner == 0 and player == 0):
                text = font.render("You Won!", 1, RED)
            elif game.winner() == -1:
                text = font.render("Tie Game!", 1, RED)
            else:
                text = font.render("You Lost...", 1, RED)

            win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1Went:
                                n.send(btn.text)
                        else:
                            if not game.p2Went:
                                n.send(btn.text)

        redrawWindow(win, game, player)

def menu_screen():
    run = True
    
    while run:
        CLOCK.tick(FPS)
        win.fill(GREY)
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, RED)

        win.blit(text, (WIDTH // 2 - text.get_width() /2 , HEIGHT // 2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

if __name__ == "__main__":
    while True:
        menu_screen()