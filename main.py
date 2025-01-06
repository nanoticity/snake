
import pygame, random, pygame.freetype, sys, pygame.mixer, asyncio
pygame.init()
pygame.mixer.init()

SIZE = [800, 800]
screen = pygame.display.set_mode(SIZE)
block_size = 40
tummy = 3
if __name__ == "__main__":
    music = pygame.mixer.Sound("snake.wav")
else:
    music = pygame.mixer.Sound("/lib/python3.12/site-packages/snake/snake.wav")

def grid():
    global block_size
    gridx = block_size
    gridy = block_size
    while gridx < SIZE[0]:
        pygame.draw.line(screen, (0, 0, 0), (gridx, 0), (gridx, SIZE[1]), 1)
        gridx += block_size

    while gridy < SIZE[1]:
        pygame.draw.line(screen, (0, 0, 0), (0, gridy), (SIZE[0], gridy), 1)
        gridy += block_size

def shift(array, dir, remove_tail = True):
    if remove_tail:
        array = array[:-1]
    new_head = Block(array[0].x + dir.x, array[0].y + dir.y)
    array.insert(0, new_head)
    return array

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.r = pygame.Rect(self.x * block_size, self.y * block_size, block_size, block_size)
    
    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.r)
        
class Direction:
    def __init__(self, x, y):
        assert x == 0 and abs(y) == 1 or y == 0 and abs(x) == 1, "Not a direction vector"
        self.x = x
        self.y = y
    
    def is_opposite(self, other):
        opposite = Direction(self.x * -1, self.y * -1)
        return opposite.x  == other.x and opposite.y == other.y
    
class Apple:
    def __init__(self):
        self.x = random.randint(0, int(SIZE[0] / block_size) - 1)
        self.y = random.randint(0, int(SIZE[1] / block_size) - 1)
        
    def get_rect(self):
        return pygame.Rect(self.x * block_size, self.y * block_size, block_size, block_size)
    
    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), self.get_rect())
    
    def reset(self):
        self.x = random.randint(0, int(SIZE[0] / block_size) - 1)
        self.y = random.randint(0, int(SIZE[1] / block_size) - 1)
        for b in snake_list:
            if self.x == b.x and self.y == b.y:
                try:
                    self.reset()
                except RecursionError:
                    screen.fill((255, 255, 255))
                    r = pygame.Rect(160, 160, 600, 600)
                    pygame.draw.rect(screen, (0, 0, 0), r, 20)
                    text("You Won!", (300, 320), 50, (0, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    sys.exit()
                    

def end():
    screen.fill((255, 255, 255))
    music.stop()
    r = pygame.Rect(100, 100, 600, 600)
    pygame.draw.rect(screen, (0, 0, 0), r, 20)
    text("You got a score of " + str(tummy), (200, 380), 50, (0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(1000)
    sys.exit()

def text(to_write, pos, size, color):
        font = pygame.font.Font(None, size)
        text = font.render(to_write, True, color)
        textpos = text.get_rect(x = pos[0], y = pos[1])
        screen.blit(text, textpos)
        
snake_list = [Block(6, 4), Block(5, 4), Block(4, 4)]
        
async def main():
    global snake_list
    global tummy
    direction = Direction(1, 0)

    apple = Apple()

    crazy = False
    ai = False
    if ai:
        snake_list = [Block(3, 0), Block(4, 0), Block(5, 0)]
        direction = Direction(-1, 0)
    
    count = 1
    run = True
    dir_changed = False
    remove_tail_times = 0
    music.play(-1)
    step = 0
    remove_tail = True
    
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN and not dir_changed and not ai:
                key_dir = {
                    pygame.K_LEFT: Direction(-1, 0), 
                    pygame.K_UP: Direction(0, -1), 
                    pygame.K_RIGHT: Direction(1, 0), 
                    pygame.K_DOWN: Direction(0, 1)
                }
                
                try:
                    new_dir = key_dir[e.key]
                    if not direction.is_opposite(new_dir):
                        direction = new_dir
                        dir_changed = True
                except:
                    pass
            if e.type == pygame.KEYDOWN and not ai:
                if e.key == pygame.K_c:
                    crazy = not crazy
                    fps = 10
        screen.fill((255, 255, 255))
        apple.draw()
        if pygame.Rect.colliderect(snake_list[0].r, apple.get_rect()):
            remove_tail_times += 3
            if crazy:
                fps += 5
            apple.reset()
        if remove_tail_times > 0:
            remove_tail = False
            remove_tail_times -= 1
            tummy += 1
        snake_list = shift(snake_list, direction, remove_tail)
        for b in snake_list:
            b.draw()
        for b in snake_list[1:]:
            if b.x == snake_list[0].x and b.y == snake_list[0].y:
                end()
        if ai:
            if count == 3:
                direction = Direction(0, 1)
            if count > 10 and count < 382:
                if snake_list[0].y == 19:
                    if step == 0:
                        direction = Direction(1, 0)
                        step += 1
                    elif step == 1:
                        direction = Direction(0, -1)
                        step = 0
                elif snake_list[0].y == 1:
                    if step == 0:
                        direction = Direction(1, 0)
                        step += 1
                    elif step == 1:
                        direction = Direction(0, 1)
                        step = 0
            if count == 384:
                direction = Direction(-1, 0)
            if count == 400:
                count = 0
            count += 1
        if snake_list[0].x >= 20 or snake_list[0].x < 0 or snake_list[0].y >= 20 or snake_list[0].y < 0:
            end()
        text("Score: " + str(tummy), (50, 50), 68, (0, 0, 0))
        
        grid()
        pygame.display.flip()
        if not ai:
            await asyncio.sleep(0.1)
        dir_changed = False
        remove_tail = True

if __name__ == "__main__":
    asyncio.run(main())