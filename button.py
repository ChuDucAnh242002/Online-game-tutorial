class Button:
    def __init__(self, text, x ,y, image):
        self.text = text
        self.x = x
        self.y = y
        self.image = image
        self.width = 150
        self.height = 150

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y +self.height:
            return True
        else: return False