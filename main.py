
import pygame, random, pygame.freetype, sys, pygame.mixer, asyncio
pygame.init()
pygame.mixer.init()
pygame.font.init()

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
        
    def __str__(self):
        return f"({self.x}, {self.y})"
        
class Direction:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def is_opposite(self, other):
        opposite = Direction(self.x * -1, self.y * -1)
        return opposite.x  == other.x and opposite.y == other.y
    
    def is_valid(self):
        return self.x != 0 or self.y != 0
    
    def __str__(self):
        return f"{self.x}, {self.y}"
    
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
                    r = pygame.Rect(100, 100, 600, 600)
                    pygame.draw.rect(screen, (0, 0, 0), r, 20)
                    text("You Won!", (300, 380), 50, (0, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(1000)
                    sys.exit()
                    

def end():
    screen.fill((255, 255, 255))
    r = pygame.Rect(100, 100, 600, 600)
    pygame.draw.rect(screen, (0, 0, 0), r, 20, border_radius=10)
    text("You got a score of " + str(tummy), (200, 380), 50, (0, 0, 0))
    pygame.display.flip()
    pygame.time.wait(500)
    sys.exit(0)
    # pygame.quit()

def sign(x):
    if x == 0:
        return 0
    else:
        return x / abs(x)

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
    pygame.display.set_caption("Snake!")
    count = 1
    run = False
    dir_changed = False
    remove_tail_times = 0
    music.play(-1)
    step = 0
    remove_tail = True
    title = True
    while title:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                title = False
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button == 1:
                    if e.pos[0] in range(100, 301):
                        if e.pos[1] in range(500, 601):
                            ai = False
                            title = False
                            run = True
                    elif e.pos[0] in range(500, 701):
                        if e.pos[1] in range(500, 601):
                            ai = True
                            title = False
                            run = True
        screen.fill((255, 255, 255))
        text("Snake! By Nano", (125, 100), 100, (0, 0, 0))
        text("Who plays it?", (225, 200), 75, (0, 0, 0))
        player_rect = pygame.Rect(100, 500, 200, 100)
        ai_rect = pygame.Rect(500, 500, 200, 100)
        pygame.draw.rect(screen, (0, 0, 0), ai_rect, border_radius=20, width=10)
        text("You", (145, 525), 80, (0, 0, 0))
        pygame.draw.rect(screen, (0, 0, 0), player_rect, border_radius=20, width=10)
        text("Hamilton*", (520, 535), 50, (0, 0, 0))
        pygame.display.update()
        await asyncio.sleep(0.02)
    
    if ai:
        snake_list = [Block(3, 0), Block(4, 0), Block(5, 0)]
        direction = Direction(-1, 0)
    
    while run:
        mouse_moved = False
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
            
            if e.type == pygame.MOUSEMOTION and not mouse_moved:
                # Rel is relative coordinates, first is X, positive is right, second is Y, positive is down
                x_motion = e.rel[0]
                y_motion = e.rel[1]
                    
                if abs(x_motion) > abs(y_motion):
                    y_motion = 0
                else:
                    x_motion = 0
                x_motion = sign(x_motion)
                y_motion = sign(y_motion)
                new_dir = Direction(x_motion, y_motion)
                if new_dir.is_valid() and not direction.is_opposite(new_dir):
                    mouse_moved = True
                    direction = new_dir
                    dir_changed = True
                
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
        try:
            text("Score: " + str(tummy), (50, 50), 68, (0, 0, 0))
        except:
            pass
        grid()
        pygame.display.flip()
        if not ai:
            await asyncio.sleep(0.1)
        else:
            if tummy < 30:
                await asyncio.sleep(0.01)
            else:
                await asyncio.sleep(0)
        dir_changed = False
        remove_tail = True

if __name__ == "__main__":
    asyncio.run(main())