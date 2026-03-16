import pygame
import asyncio,time
import random
import math

pygame.init()
pygame.mixer.init()

class _SilentSound:
    def play(self): pass
    def stop(self): pass

bullet_sound = _SilentSound()
Scary_metal_sound = _SilentSound()
metal_bang = _SilentSound()
scary_sound1 = _SilentSound()
scary_sound2 = _SilentSound()
scary_sound3 = _SilentSound()
end_sound = _SilentSound()
switch_equipment = _SilentSound()
switch_equipment1 = _SilentSound()
gun_upgrade_sound = _SilentSound()
click_sound = _SilentSound()
mouse_sound = _SilentSound()


WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
distance_game = True
damage=3
enemy_type=0
gun_type="pistol_1"
stamina=100
remaining_minigames = [0, 1, 2]  # 0=math, 1=timing, 2=memory
random.shuffle(remaining_minigames)

size = 15
CELL_SIZE = min(WIDTH, HEIGHT) // size
WALL_THICKNESS = 4
MAZE_OFFSET_X = (WIDTH - size * CELL_SIZE) // 2
MAZE_OFFSET_Y = (HEIGHT - size * CELL_SIZE) // 2

FOG_RADIUS = 120
GUN_FOG_RADIUS = 70   # reduced torch radius when gun is drawn
AMMO = 10             

global_damage_state=0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Web Pygame Template")

math_mini,timing_mini,memory_mini=False,False,False

minigames_list=[math_mini,timing_mini,memory_mini]
random.shuffle(minigames_list)

def target(tx,ty):
    pygame.draw.circle(screen,(220,0,0),(tx,ty),20)
    pygame.draw.circle(screen,(255,255,255),(tx,ty),15)
    pygame.draw.circle(screen,(220,0,0),(tx,ty),10)
    pygame.draw.circle(screen,(255,255,255),(tx,ty),2)

async def math_mini_game():
    answers=[12,1,15]
    user_inputs=["","",""]
    current_q=0
    active_input=""
    result_msg=""
    result_timer=0
    clock=pygame.time.Clock()
    running=True
    while running:
        screen.fill((20,20,60))
        font_big=pygame.font.SysFont("arial",36)
        font_med=pygame.font.SysFont("arial",24)
        font_small=pygame.font.SysFont("arial",20)
        try:
            img=pygame.image.load(f"math_mini-game{current_q+1}.png").convert_alpha()
            screen.blit(img,(0,0))
        except:
            img=pygame.Surface((WIDTH,HEIGHT)); img.fill((20,20,60))
            screen.blit(img,(0,0))
        input_box=pygame.Rect(WIDTH//2-100,340,200,40)
        pygame.draw.rect(screen,(60,60,100),input_box)
        pygame.draw.rect(screen,WHITE,input_box,2)
        input_surf=font_med.render(active_input,True,WHITE)
        screen.blit(input_surf,(input_box.x+8,input_box.y+8))
        if result_timer>0:
            col=(0,200,0) if result_msg=="Correct!" else (200,0,0)
            msg_surf=font_big.render(result_msg,True,col)
            screen.blit(msg_surf,(WIDTH//2-msg_surf.get_width()//2,420))
            result_timer-=1
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    try:
                        val=int(active_input)
                        if val==answers[current_q]:
                            result_msg="Correct!"
                            result_timer=60
                            active_input=""
                            current_q+=1
                            if current_q>=3:
                                await asyncio.sleep(0.5)
                                return True
                        else:
                            result_msg="Wrong! Try again."
                            result_timer=60
                            active_input=""
                    except:
                        active_input=""
                elif event.key==pygame.K_BACKSPACE:
                    active_input=active_input[:-1]
                else:
                    if event.unicode.isdigit() or (event.unicode=='-' and len(active_input)==0):
                        active_input+=event.unicode
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)
    return True

async def time_game():
    yvals=[]
    for y in range(3):
        deviation=random.randint(10,260)
        val=100+deviation
        yvals.append(val)
    clock=pygame.time.Clock()
    completed=[False,False,False]
    index=0
    running=True
    result_msg=""
    result_timer=0
    while running:
        screen.fill((28,28,28))
        font_big=pygame.font.SysFont("arial",36)
        font_med=pygame.font.SysFont("arial",24)
        
        for x in range(3):
            panel_x=88+(150*x)
            pygame.draw.rect(screen,(38,38,38),(panel_x,138,54,326),border_radius=4)
            pygame.draw.rect(screen,(70,70,70),(panel_x,138,54,326),2,border_radius=4)
       
        for x in range(3):
            spark_x=115+(150*x)
            pygame.draw.line(screen,(200,220,80),(spark_x-8,128),(spark_x,118),2)
            pygame.draw.line(screen,(200,220,80),(spark_x,118),(spark_x+8,128),2)
        index+=1
        all_done=True
        for x in range(3):
            if not completed[x]:
                all_done=False
               
                pygame.draw.rect(screen,(100,85,0),(100+(150*x),150,30,300))
                pygame.draw.rect(screen,(240,230,140),(100+(150*x),150,30,300),2)
                zone_y=yvals[x]
                pygame.draw.rect(screen,(0,200,0),(100+(150*x),zone_y,30,40))
                drop_y=(index*3)%450+50
                
                pygame.draw.rect(screen,(200,200,200),(100+(150*x),drop_y,30,50))
                pygame.draw.rect(screen,(240,240,240),(100+(150*x),drop_y,30,50),2)
            else:
                pygame.draw.rect(screen,(80,68,0),(100+(150*x),150,30,300))
                pygame.draw.rect(screen,(255,210,0),(100+(150*x),150,30,300),2)
                bolt_x=115+(150*x)
                bolt_pts=[(bolt_x,160),(bolt_x-6,188),(bolt_x+2,188),(bolt_x-4,216),(bolt_x+10,180),(bolt_x+2,180),(bolt_x+8,160)]
                pygame.draw.polygon(screen,(255,220,40),bolt_pts)
        if all_done:
            return True
        if result_timer>0:
            col=(255,200,0) if "Hit" in result_msg else (200,80,0)
            msg_surf=font_big.render(result_msg,True,col)
            screen.blit(msg_surf,(WIDTH//2-msg_surf.get_width()//2,500))
            result_timer-=1
        hint=font_med.render("Press any key to catch the next bar",True,(140,140,140))
        screen.blit(hint,(WIDTH//2-hint.get_width()//2,560))
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type==pygame.KEYDOWN:
                drop_y=(index*3)%450+50
                hit_any=False
                for col in range(3):
                    if not completed[col]:
                        zone_y=yvals[col]
                        if zone_y<=drop_y<=zone_y+40 or zone_y<=drop_y+50<=zone_y+40:
                            completed[col]=True
                            result_msg=f"Hit!"
                            result_timer=60
                            hit_any=True
                            break
                if not hit_any:
                    result_msg=f"Missed! Try again."
                    result_timer=50
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)
    return True

async def memory_game():
    clock=pygame.time.Clock()
    firstrec=pygame.Rect(221,103,90,71)
    middlerec=pygame.Rect(325,263,90,71)
    threerec=pygame.Rect(418,103,90,71)
    rects=[firstrec,middlerec,threerec]
    answer_sequence=[0,1,2]

    def reset_show():
        return True, 0, 120

    show_phase, show_index, show_timer = reset_show()
    current_answer=0
    running=True
    while running:
        screen.fill((20,20,60))
        if show_phase:
            try:
                img=pygame.image.load(f"memory_game{show_index+1}.png").convert_alpha()
                screen.blit(img,(0,0))
            except:
                s=pygame.Surface((WIDTH,HEIGHT)); s.fill((20,20,60)); screen.blit(s,(0,0))
            show_timer-=1
            if show_timer<=0:
                show_index+=1
                show_timer=120
                if show_index>=4:
                    show_phase=False
        else:
            try:
                img=pygame.image.load("memory_game1.png").convert_alpha()
                screen.blit(img,(0,0))
            except:
                s=pygame.Surface((WIDTH,HEIGHT)); s.fill((20,20,60)); screen.blit(s,(0,0))
            for r in rects:
                pygame.draw.rect(screen,(100,100,200),r,3)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            if event.type==pygame.MOUSEBUTTONDOWN and event.button==1 and not show_phase:
                mx,my=pygame.mouse.get_pos()
                for i,r in enumerate(rects):
                    if r.collidepoint(mx,my):
                        if i==answer_sequence[current_answer]:
                            current_answer+=1
                            if current_answer>=len(answer_sequence):
                                return True
                        else:
                            for _ in range(20):
                                overlay=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA)
                                overlay.fill((180,0,0,160))
                                screen.blit(overlay,(0,0))
                                pygame.display.flip()
                                await asyncio.sleep(0)
                                clock.tick(60)
                            current_answer=0
                            show_phase=True
                            show_index=0
                            show_timer=120
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)
    return True

def distance_finder(x1,y1,x2,y2): # uses manhattan distance to find distance
    # uses manhattan distances instead of straight line distance as you can't travel just using in a line to the end goal
    distance=abs(x1-x2)+abs(y1-y2) # takes x and y distance and adds them up.
    # straight line distance | distance=((x1-x2)**2+(y1-y2)**2)**(1/2)
    return distance

def distance_estimation(x1,x2,y1,y2):
     '''Uses straight line distance as the goal of this function is to be a rough estimation, instead of manhattan distance as that would give a fairly accurate representation of distance in the maze
     it works by finding side lengths of a triangle by taking the difference in x,y coordinates. Then using a^2+b^2=c^2'''
     distance=((x1-x2)**2+(y1-y2)**2)**(1/2)
     '''Side lengths of triangle can be found by the difference between their start and end points, so by by subtracting both start and end points of both of the side lengths,
     we find the difference between the x,y coordinates and the difference is how far apart they are (their distance) or the change between the coordinate values of the points or the change needed for them to be equal, again thats just the distance. With the sidelengths we can then be use them in a^2+b^2=c^2.
     To get straight line distance
     '''
     return distance

class bullets:
    def __init__(self):
        self.bullet_lis=[]
        pass
    def move(self, enemy):
        global global_damage_state,damage
        to_remove = []
        for index, t in enumerate(self.bullet_lis):
            change_x=t[0]+t[2]
            change_y=t[1]+t[3]
            self.bullet_lis[index][0]=change_x
            self.bullet_lis[index][1]=change_y
            if change_x>800 or change_x<0:
                to_remove.append(index)
            elif change_y>600 or change_y<0:
                to_remove.append(index)
            else:
                pygame.draw.circle(screen,(175, 155, 96),(int(change_x),int(change_y)),5)
                ex, ey = cell_to_pixel(enemy.currx, enemy.curry)
                if ex <= change_x <= ex + CELL_SIZE and ey <= change_y <= ey + CELL_SIZE:
                    global_damage_state+=damage
                    sound_choice=random.randint(1,2)
                    w=random.randint(10,30)
                    h=random.randint(10,30)
                    deviationx=random.randint(1,20)
                    deviationy=random.randint(1,20)
                    blur(ex-20,ey-20,w,h)
                    if sound_choice==1:
                        Scary_metal_sound.play()
                    else:
                        metal_bang.play()
                    if global_damage_state>=9:
                        enemy.stunned_timer = 600
                        to_remove.append(index)
                        global_damage_state=0
                    enemy.hit_flash_timer = 60
                    enemy.last_hit_ex = ex
                    enemy.last_hit_ey = ey
        for index in reversed(to_remove):
            self.bullet_lis.pop(index)

    def shoot(self,mousex,mousey,playerx,playery):

        base_length=mousex-playerx
        '''Difference between the mousex and playerx x-vals tells the you the amount of units of x that changed between their x-coords, 
        or how many units of x they are apart. Which is distance, which is the length of that side of the triangle which is the base.'''
        
        height=mousey-playery
        '''Same logic for base_length calculation but applies for y values or height.'''

        hypotenus=(height**2+base_length**2)**(1/2) #c^2=a^2+b^2
        '''Now we got all the sides of the triangle'''

        if hypotenus == 0:# zero division error
            return
        
        angle=height/hypotenus # gives sin value for triangle's angle
        angle1=base_length/hypotenus # gives cos value for triangle's angle
        
        y_change=(angle*50) #moves in 50 units of y (or y values), multiplied by the angle meaning depending on the angle it will move the full 50 or 0 y values
        x_change=(angle1*50) #moves in 50 units of x (or x values), multiplied by the angle meaning depending on the angle it will move the full 50 or 0 x values

        bullet_val=[playerx,playery,x_change,y_change]
        self.bullet_lis.append(bullet_val)

class shotgun_shells(bullets):
    def shoot(self,mousex,mousey,playerx,playery):
        base_length=mousex-playerx
        '''Difference between the mousex and playerx x-vals tells the you the amount of units of x that changed between their x-coords, 
        or how many units of x they are apart. Which is distance, which is the length of that side of the triangle which is the base.'''
        
        height=mousey-playery
        '''Same logic for base_length calculation but applies for y values or height.'''

        height-=30
        for t in range(3):
            if base_length==0:
                base_length=1
            angle=math.atan(height/base_length) # finds angle
            height+=30 # adds 3 different variations of y values resulting the shells spreading out
            y_change=math.sin(angle)*50 
            x_change=math.cos(angle)*50
            if playerx>mousex:
                '''if mousex less then playerx then mouse's x value is behind player so pi/2 to 3pi/2, x should be negative 
                but tan is negative pi-2pi, so atan would return a postive angle when it should be negative, for x so we flip it.'''
                x_change*=-1
                y_change*=-1 
            bullet_val=[playerx,playery,x_change,y_change]
            self.bullet_lis.append(bullet_val)

class squid_bullets(bullets):
    def move(self, sub_x, sub_y, sub_w, sub_h, player_health_ref):
        to_remove = []
        for index, t in enumerate(self.bullet_lis):
            change_x = t[0] + t[2] * 0.12
            change_y = t[1] + t[3] * 0.12
            self.bullet_lis[index][0] = change_x
            self.bullet_lis[index][1] = change_y
            if change_x > WIDTH or change_x < 0 or change_y > HEIGHT or change_y < 0:
                to_remove.append(index)
            else:
                pygame.draw.circle(screen, (200, 50, 50), (int(change_x), int(change_y)), 7)
                pygame.draw.circle(screen, (255, 255, 255), (int(change_x), int(change_y)), 3)
                if sub_x <= change_x <= sub_x + sub_w and sub_y <= change_y <= sub_y + sub_h:
                    player_health_ref[0] -= 10
                    sound_choice = random.randint(1, 2)
                    if sound_choice == 1:
                        Scary_metal_sound.play()
                    else:
                        metal_bang.play()
                    to_remove.append(index)
        for index in reversed(to_remove):
            if index < len(self.bullet_lis):
                self.bullet_lis.pop(index)

        

class greedy_algo():
    def __init__(self, x, y, endx, endy, maze_lis):
        global enemy_type,remaining_minigames
        self.currx = x
        self.curry = y
        self.endx = endx
        self.endy = endy
        self.steps = 0
        self.open_list = []
        self.maze_lis = maze_lis
        self.last_move = None
        self.g_scores = {}
        self.closed_list = set()
        self.g_scores[(x, y)] = 0
        self.path = []
        self.path_index = 0
        self.stunned_timer = 0
        self.hit_flash_timer = 0
        self.last_hit_ex = 0
        self.last_hit_ey = 0
        self.enemy_type = False
        if len(remaining_minigames)==1:
            self.enemy_type=True
        enemy_type=self.enemy_type
        self.find_path()

    def find_path(self):
        self.open_list = [(0, self.currx, self.curry)]
        came_from = {}

        while self.open_list:
            self.open_list.sort()
            f_score, curr_x, curr_y = self.open_list.pop(0)

            if curr_x == self.endx and curr_y == self.endy:
                path = [(curr_x, curr_y)]
                while (curr_x, curr_y) in came_from:
                    curr_x, curr_y = came_from[(curr_x, curr_y)]
                    path.append((curr_x, curr_y))
                path.reverse()
                self.path = path
                return

            if (curr_x, curr_y) in self.closed_list:
                continue
            self.closed_list.add((curr_x, curr_y))

            neighbors = [
                [curr_x + 1, curr_y], [curr_x - 1, curr_y],
                [curr_x, curr_y + 1], [curr_x, curr_y - 1]
            ]

            for x, y in neighbors:
                if x < 0 or y < 0 or y >= size or x >= size:
                    continue
                if (x, y) in self.closed_list:
                    continue
                cell_index = curr_y * size + curr_x
                curr_cell = self.maze_lis[cell_index]
                can_move = False
                if x > curr_x:
                    if curr_cell[2] == 0: can_move = True
                elif x < curr_x:
                    if curr_cell[4] == 0: can_move = True
                elif y > curr_y:
                    if curr_cell[3] == 0: can_move = True
                elif y < curr_y:
                    if curr_cell[1] == 0: can_move = True

                if can_move:
                    new_g = self.g_scores.get((curr_x, curr_y), 0) + 1
                    if (x, y) not in self.g_scores or new_g < self.g_scores[(x, y)]:
                        self.g_scores[(x, y)] = new_g
                        h_score = distance_finder(x, y, self.endx, self.endy)
                        f_score = new_g + h_score
                        self.open_list.append((f_score, x, y))
                        came_from[(x, y)] = (curr_x, curr_y)

    def recalculate(self, endx, endy):
        self.endx = endx
        self.endy = endy
        self.path = []
        self.path_index = 0
        self.open_list = []
        self.closed_list = set()
        self.g_scores = {(self.currx, self.curry): 0}
        self.find_path()

    def pick_cell_to_move(self):
        if self.path_index >= len(self.path):
            return None, None, None
        next_pos = self.path[self.path_index]
        return next_pos[0], next_pos[1], None

    def move(self, x, y, g_score=None):
        if x is not None and y is not None:
            cell_index = self.curry * size + self.currx
            self.maze_lis[cell_index][0] = "v"
            self.steps += 1
            self.last_move = (self.currx, self.curry)
            self.currx = x
            self.curry = y
            self.path_index += 1

def chamber_generation(size):
    maze = []
    total_cells = size * size
    for i in range(total_cells):
        up    = '1' if i < size else 1
        left  = '1' if i % size == 0 else 1
        down  = '1' if i >= total_cells - size else 1
        right = '1' if (i + 1) % size == 0 else 1
        maze.append(["o", up, right, down, left])
    return maze

def maze_generation(maze, size, start_ind):
    stack = [start_ind]
    maze[start_ind][0] = "v"
    direction_lis_base = [(-size, 1, 3), (1, 2, 4), (size, 3, 1), (-1, 4, 2)]
    while stack:
        current_cell_ind = stack[-1]
        directions = direction_lis_base[:]
        random.shuffle(directions)
        moved = False
        for dr, my_wall, their_wall in directions:
            next_ind = current_cell_ind + dr
            if dr == -1 and current_cell_ind % size == 0: continue
            if dr == 1 and (current_cell_ind + 1) % size == 0: continue
            if not (0 <= next_ind < size * size): continue
            if maze[next_ind][0] == "o":
                maze[current_cell_ind][my_wall] = 0
                maze[next_ind][their_wall] = 0
                maze[next_ind][0] = "v"
                stack.append(next_ind)
                moved = True
                break
        if not moved:
            stack.pop()

def draw_maze(maze, size, offset_x, offset_y, cell_size=CELL_SIZE):
    for r in range(size):
        for c in range(size):
            cell = maze[r * size + c]
            up, right, down, left = cell[1:]
            x = offset_x + c * cell_size
            y = offset_y + r * cell_size
            wall_col = (40, 0, 25)
            if up    == 1 or up    == '1': pygame.draw.line(screen, wall_col, (x, y),             (x + cell_size, y),             WALL_THICKNESS)
            if right == 1 or right == '1': pygame.draw.line(screen, wall_col, (x + cell_size, y), (x + cell_size, y + cell_size), WALL_THICKNESS)
            if down  == 1 or down  == '1': pygame.draw.line(screen, wall_col, (x, y + cell_size), (x + cell_size, y + cell_size), WALL_THICKNESS)
            if left  == 1 or left  == '1': pygame.draw.line(screen, wall_col, (x, y),             (x, y + cell_size),             WALL_THICKNESS)

def cell_to_pixel(cx, cy):
    return MAZE_OFFSET_X + cx * CELL_SIZE, MAZE_OFFSET_Y + cy * CELL_SIZE

def can_move_direction(maze, cell_cx, cell_cy, dx, dy):
    if cell_cx < 0 or cell_cy < 0 or cell_cx >= size or cell_cy >= size:
        return False
    cell = maze[cell_cy * size + cell_cx]
    if dx ==  1: return cell[2] == 0
    if dx == -1: return cell[4] == 0
    if dy ==  1: return cell[3] == 0
    if dy == -1: return cell[1] == 0
    return False

def blur(x,y,width,height):
    xdistance=abs(x-width)
    ydistance=abs(y-height)
    blur_amount=((xdistance*0.7)+(ydistance*0.7))/2
    blur_amount=math.ceil(blur_amount)
    pygame.draw.rect(screen,(255,255,255),(x,y,width,height))
    for i in range(blur_amount):
        randomx=random.randint(x,x+width)
        randomy=random.randint(y,y+height)
        sizex=random.randint(1,3)
        sizey=random.randint(1,3)
        sizex-=1
        sizey-=1
        color_dev_r=random.randint(1,14)
        color_dev_g=random.randint(1,14)
        color_dev_b=random.randint(1,14)
        pygame.draw.rect(screen,(0+color_dev_r,0+color_dev_g,0+color_dev_b),(randomx,randomy,4+sizex,4+sizey))

class eyes():
    def __init__(self,col,p_col,eyex,eyey):
        self.eye_color=col
        self.p_col=p_col
        self.x=eyex
        self.y=eyey
    def look(self,subx,suby):
        base_length=self.x-subx
        '''Difference between the eyex and subx x-vals tells the you the amount of units of x that changed between their x-coords, 
        or how many units of x they are apart. Which is distance, which is the length of that side of the triangle which is the base.'''
        
        height=self.y-suby
        '''Same logic for base_length calculation but applies for y values or height.'''

        hypotenus=(height**2+base_length**2)**(1/2) #c^2=a^2+b^2
        '''Now we got all the sides of the triangle'''

        if hypotenus == 0:# zero division error
            return
        
        angle=math.asin(height/hypotenus) # finds angle

        x_change=math.cos(angle)*5 
        y_change=math.sin(angle)*5

        if subx<self.x:
            x_change*=-1 # qaudrant flipping pi/2 to 3pi/2 or when sub is behind eye.

        y_change*=-1 # pygame y axis is flipped top is zero, so to go down instead of a negative number you need a postive number to be added
        pygame.draw.circle(screen,self.eye_color,(self.x,self.y),10)
        pygame.draw.circle(screen,(0,0,0),(self.x+x_change,self.y+y_change),5)

def get_lab_floor(seed=42):
    rng = random.Random(seed)
    floor = pygame.Surface((WIDTH, HEIGHT))
    floor.fill((65, 48, 65))
    small_tile = 10
    for x in range(0, WIDTH, small_tile):
        for y in range(0, HEIGHT, small_tile):
            v = rng.randint(-6, 6)
            base = tuple(max(0, min(255, c + v)) for c in (65, 48, 65))
            rect = pygame.Rect(x, y, small_tile, small_tile)
            pygame.draw.rect(floor, base, rect)
            pygame.draw.rect(floor, (45, 38, 55), rect, 1)

    for r in range(size):
        for c in range(size):
            x = MAZE_OFFSET_X + c * CELL_SIZE
            y = MAZE_OFFSET_Y + r * CELL_SIZE
            pygame.draw.rect(floor, (48, 41, 58), pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 1)
            if rng.random() < 0.18:
                gx = x + rng.randint(5, CELL_SIZE - 8)
                gy = y + rng.randint(5, CELL_SIZE - 8)
                gr = rng.randint(3, 6)
                grim = (rng.randint(38, 53), rng.randint(33, 48), rng.randint(50, 65))
                pygame.draw.circle(floor, grim, (gx, gy), gr)
            if rng.random() < 0.04:
                dx = x + CELL_SIZE // 2
                dy = y + CELL_SIZE // 2
                pygame.draw.circle(floor, (40, 33, 50), (dx, dy), 5)
                pygame.draw.circle(floor, (65, 58, 75), (dx, dy), 5, 1)
                pygame.draw.line(floor, (65, 58, 75), (dx - 4, dy), (dx + 4, dy), 1)
                pygame.draw.line(floor, (65, 58, 75), (dx, dy - 4), (dx, dy + 4), 1)

    return floor

def draw_torch_light(torch_cx, torch_cy, flicker_offset=0, radius_override=None):
    radius = (radius_override if radius_override is not None else FOG_RADIUS) + flicker_offset
    surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    surf.fill((0, 0, 0, 255))

    steps = 60
    for i in range(steps, 0, -1):
        r_px = int(radius * i / steps)
        t = i / steps

        if t > 0.6:
            inner_t = (t - 0.6) / 0.4
            red   = 255
            green = int(255 * inner_t)
            blue  = int(255 * inner_t)
            alpha = int(25 * (1 - inner_t))
        elif t > 0.2:
            mid_t = (t - 0.2) / 0.4
            red   = 0
            green = 0
            blue  = 0
            alpha = int(180 * (1 - mid_t) + 20)
        else:
            edge_t = t / 0.2
            red   = 0
            green = 0
            blue  = 0
            alpha = int(255 * (1 - edge_t))

        pygame.draw.circle(surf, (red, green, blue, alpha), (torch_cx, torch_cy), r_px)

    screen.blit(surf, (0, 0))

def draw_muzzle_flash(cx, cy, angle_deg):
    """Brief bright white-yellow burst at the gun muzzle when fired."""
    flash_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.circle(flash_surf, (255, 255, 200, 220), (cx, cy), 14)
    pygame.draw.circle(flash_surf, (255, 220, 80, 160),  (cx, cy), 22)
    pygame.draw.circle(flash_surf, (255, 120, 20, 80),   (cx, cy), 32)
    screen.blit(flash_surf, (0, 0))

def make_gun_surface():
    global gun_type
    if gun_type=="pistol_1":
        gun_img = pygame.image.load("pistol.png").convert_alpha()
        gun_img = pygame.transform.scale(gun_img, (36, 18))
    if gun_type=="pistol_2":
        gun_img = pygame.image.load("pistol2.png").convert_alpha()
        gun_img = pygame.transform.scale(gun_img, (36, 18))
    if gun_type=="shotgun":
        gun_img = pygame.image.load("shotgun.png").convert_alpha()
        gun_img = pygame.transform.scale(gun_img, (45, 20))
    if gun_type=="AR":
        gun_img = pygame.image.load("AR.png").convert_alpha()
        gun_img = pygame.transform.scale(gun_img, (45, 20))
    if gun_type=="sniper":
        gun_img = pygame.image.load("sniper.png").convert_alpha()
        gun_img = pygame.transform.scale(gun_img, (45, 20))
    pivot = (8, 11)  
    return gun_img, pivot

def draw_gun(player_cx, player_cy, mouse_x, mouse_y, gun_surf, gun_pivot):
    dx = mouse_x - player_cx
    dy = mouse_y - player_cy
    angle_deg = -math.degrees(math.atan2(dy, dx))  # pygame y-axis is flipped

    rotated = pygame.transform.rotate(gun_surf, angle_deg)

    pivot_rotated = pygame.math.Vector2(gun_pivot).rotate(-angle_deg)
    blit_pos = (player_cx - pivot_rotated.x - rotated.get_width()  // 2 + gun_surf.get_width()  // 2,
                player_cy - pivot_rotated.y - rotated.get_height() // 2 + gun_surf.get_height() // 2)

    screen.blit(rotated, blit_pos)

    muzzle_local = pygame.math.Vector2(35 - gun_pivot[0], 7 - gun_pivot[1])
    muzzle_world = pygame.math.Vector2(player_cx, player_cy) + muzzle_local.rotate(-angle_deg)
    return int(muzzle_world.x), int(muzzle_world.y), angle_deg

def draw_gun_at_angle(player_cx, player_cy, gun_surf, gun_pivot, angle_deg):
    rotated = pygame.transform.rotate(gun_surf, angle_deg)
    pivot_rotated = pygame.math.Vector2(gun_pivot).rotate(-angle_deg)
    blit_pos = (player_cx - pivot_rotated.x - rotated.get_width() // 2 + gun_surf.get_width() // 2,
                player_cy - pivot_rotated.y - rotated.get_height() // 2 + gun_surf.get_height() // 2)
    screen.blit(rotated, blit_pos)

def draw_enemy(ex, ey, stunned, seed):
    global enemy_type
    if enemy_type==False:
        if stunned: 
            img_name="enemy_stunned.png" 
        else:
            img_name="enemy.png"
        enemy_img = pygame.image.load(img_name).convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (CELL_SIZE, CELL_SIZE))
        screen.blit(enemy_img, (ex, ey))
    else:
        eye_col = (180,0,0)
        line_col=(250,0,0)
        if stunned:
            eye_col=(0,0,180)
            line_col=(0,0,250)
        pygame.draw.polygon(screen,(54,54,54),[(ex,ey+30),(ex+20,ey),(ex+40,ey+30)])
        pygame.draw.polygon(screen,(54,54,54),[(ex,ey+10),(ex+20,ey+40),(ex+40,ey+10)])
        pygame.draw.circle(screen, eye_col, (ex+20, ey+20),7)# 20 or cell size/4d
        pygame.draw.line(screen,line_col,(ex+17,ey+23),(ex+23,ey+17),3)
    if stunned: 
        w=random.randint(10,40)
        h=random.randint(10,40)
        x_devi=random.randint(10,30)
        y_devi=random.randint(10,30)
        blur(ex+x_devi,ey+y_devi,w,h)
        blur(ex+x_devi-30,ey+y_devi-30,w,h)

def draw_player(playerx, playery, width, height):
    pygame.draw.rect(screen, (25, 25, 25), (playerx, playery, width, height))
    pygame.draw.rect(screen, (60, 60, 60), (playerx, playery, width, height), 2)
    eye_radius = max(2, width // 8)
    eye_y = playery + height // 2
    eye_spacing = width // 3
    pygame.draw.circle(screen, (0, 200, 0), (playerx + eye_spacing, eye_y), eye_radius)
    pygame.draw.circle(screen, (0, 200, 0), (playerx + eye_spacing * 2, eye_y), eye_radius)

def draw_torch(playerx, playery, width, height, flicker_offset):
    torch_w, torch_h = 10, 40
    torch_x = playerx + width + 2
    torch_y = playery + height // 2 - 30

    try:
        img_name = "torch_lit.png" if flicker_offset > 0 else "torch.png"
        torch_img = pygame.image.load(img_name).convert_alpha()
        torch_img = pygame.transform.scale(torch_img, (torch_w, torch_h))
        screen.blit(torch_img, (torch_x, torch_y))
    except FileNotFoundError:
        pygame.draw.rect(screen, (80, 42, 12), (torch_x, torch_y, 6, torch_h))

    flame_cx = torch_x + torch_w // 2
    flame_cy = torch_y - 2 + flicker_offset // 2

    return flame_cx, flame_cy

def draw_text(surf, text, x, y, size=24, color=BLACK):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    surf.blit(text_surface, (x, y))

def draw_text_centered(surf, text, cy, size=24, color=WHITE):
    font = pygame.font.SysFont("arial", size)
    text_surface = font.render(text, True, color)
    x = (WIDTH - text_surface.get_width()) // 2
    surf.blit(text_surface, (x, cy))

def draw_image(surf, image_surface, x, y):
    if isinstance(image_surface, pygame.Surface):
        surf.blit(image_surface, (x, y))

async def clean_animation():
    for i in range(0, 101, 2):
        pygame.draw.circle(screen, BLACK, (400, 300), 10 * i)
        pygame.display.flip()
        await asyncio.sleep(0)
    for i in range(100, -1, -2):
        pygame.draw.circle(screen, BLACK, (400, 300), 10 * i)
        pygame.display.flip()
        await asyncio.sleep(0)

async def game_over_screen():
    """Flash red then show GAME OVER, wait for keypress to restart."""
    for alpha in range(0, 200, 10):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((180, 0, 0, alpha))
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        await asyncio.sleep(0)

    for _ in range(30):
        await asyncio.sleep(0)

    for alpha in range(200, 256, 4):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        await asyncio.sleep(0)

    screen.fill(BLACK)

    img=pygame.image.load(f"skull.png").convert_alpha()
    screen.blit(img,(150,50))
    draw_text_centered(screen, "GAME OVER", HEIGHT // 2 - 50, size=72, color=(200, 0, 0))
    draw_text_centered(screen, "The cyborg got you.", HEIGHT // 2 + 20, size=28, color=(180, 80, 80))
    draw_text_centered(screen, "Press any key to try again.", HEIGHT // 2 + 65, size=22, color=(130, 130, 130))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                waiting = False
        await asyncio.sleep(0)

    return True

async def you_win_screen():
    """Display a You Win screen and wait for keypress."""
    screen.fill(BLACK)
    draw_text_centered(screen, "YOU WIN!", HEIGHT // 2 - 60, size=80, color=(0, 220, 80))
    draw_text_centered(screen, "Facility repaired. You escaped.", HEIGHT // 2 + 20, size=28, color=(180, 220, 180))
    draw_text_centered(screen, "Press any key to quit.", HEIGHT // 2 + 65, size=22, color=(130, 130, 130))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                waiting = False
        await asyncio.sleep(0)

def build_game_state():
    """Create and return a fresh maze + enemy + player state."""
    global global_damage_state
    maze = chamber_generation(size)
    maze_generation(maze, size, 0)
    for cell in maze:
        cell[0] = "o"

    player_cell = [0, 0]
    px, py = cell_to_pixel(0, 0)
    player_pos = [px + 2, py + 2]
    player_size = CELL_SIZE - 4

    enemy = greedy_algo(size - 1, size - 1, 0, 0, maze)
    global_damage_state=0

    all_cells = [(c, r) for r in range(size) for c in range(size) if not (c==0 and r==0) and not (c==size-1 and r==size-1)]
    box_positions = random.sample(all_cells, 5)

    return maze, player_cell, player_pos, player_size, enemy, box_positions

def get_gun_fog_radius(g_type):
    if g_type == "pistol_1":
        return 70
    elif g_type == "pistol_2":
        return 95
    elif g_type == "shotgun":
        return 70
    elif g_type == "AR":
        return 95
    elif g_type == "sniper":
        return 110
    return 70

def get_upgrade_threshold(g_type):
    if g_type == "pistol_1":
        return 1
    elif g_type == "pistol_2":
        return 4
    elif g_type == "shotgun":
        return 7
    elif g_type == "AR":
        return 12
    return None

def get_next_gun(g_type):
    order = ["pistol_1", "pistol_2", "shotgun", "AR", "sniper"]
    idx = order.index(g_type)
    if idx + 1 < len(order):
        return order[idx + 1]
    return g_type

def get_ammo_for_gun(g_type):
    if g_type == "AR":
        return 15
    return 10

def get_damage_for_gun(g_type):
    if g_type == "sniper":
        return 9
    elif g_type == "AR":
        return 5
    return 3

def _make_gun_surface_for(g_type):
    """Temporary gun surface builder used by the upgrade animation."""
    sizes = {
        "pistol_1": ("pistol.png",  (36, 18)),
        "pistol_2": ("pistol2.png", (36, 18)),
        "shotgun":  ("shotgun.png", (45, 20)),
        "AR":       ("AR.png",      (45, 20)),
        "sniper":   ("sniper.png",  (45, 20)),
    }
    fname, scale = sizes.get(g_type, ("pistol.png", (36, 18)))
    img = pygame.image.load(fname).convert_alpha()
    img = pygame.transform.scale(img, scale)
    return img, (8, 11)

async def gun_upgrade_animation(player_cx, player_cy, old_gun_surf, old_gun_pivot, new_gun_type_name, floor_img, maze, box_positions, box_img, enemy, player_pos, player_size, frame_count_val):
    clock = pygame.time.Clock()
    total_frames = 90
    swap_frame = total_frames * 3 // 4  #67th frame
    new_gun_surf, _ = _make_gun_surface_for(new_gun_type_name)               
    showing_new = False                                                       
    for f in range(total_frames + 1):
        t = f / total_frames
        angle = 360 * t * t if t < 0.5 else 360 * (1 - (1 - t) * (1 - t) * 0.5 + 0.5 * t)
        angle = 360 * f / total_frames
        ease = math.sin(math.pi * t)
        smooth_angle = 360 * (t - (1 / (2 * math.pi)) * math.sin(2 * math.pi * t))
        if f >= swap_frame and not showing_new:  
            showing_new = True                   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill(BLACK)
        screen.blit(floor_img, (0, 0))
        draw_maze(maze, size, MAZE_OFFSET_X, MAZE_OFFSET_Y)
        for bx, by in box_positions:
            bpx, bpy = cell_to_pixel(bx, by)
            screen.blit(box_img, (bpx + 10, bpy + 10))
        ex, ey = cell_to_pixel(enemy.currx, enemy.curry)
        draw_enemy(ex, ey, enemy.stunned_timer > 0, enemy.currx * 100 + enemy.curry)
        draw_player(player_pos[0], player_pos[1], player_size, player_size)
        orbit_radius = 28 + int(18 * math.sin(math.pi * t))
        orbit_x = player_cx + int(orbit_radius * math.cos(math.radians(smooth_angle)))
        orbit_y = player_cy + int(orbit_radius * math.sin(math.radians(smooth_angle)))
        orbit_surf = new_gun_surf if showing_new else old_gun_surf  # ← CHANGED (was just old_gun_surf)
        rotated = pygame.transform.rotate(orbit_surf, -smooth_angle)  # ← CHANGED
        screen.blit(rotated, (orbit_x - rotated.get_width() // 2, orbit_y - rotated.get_height() // 2))
        flicker = int(math.sin(frame_count_val * 0.3) * 2)
        draw_torch_light(player_cx, player_cy, flicker_offset=flicker, radius_override=GUN_FOG_RADIUS)
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

TUTORIAL_SIZE = 13
TUTORIAL_CELL = 40
TUTORIAL_OFFSET_X = (WIDTH - TUTORIAL_SIZE * TUTORIAL_CELL) // 2
TUTORIAL_OFFSET_Y = (HEIGHT - 80 - TUTORIAL_SIZE * TUTORIAL_CELL) // 2


def draw_tutorial_hud(lines):
    bar_y = HEIGHT - 80
    pygame.draw.rect(screen, (0, 0, 0), (0, bar_y, WIDTH, 80))
    pygame.draw.line(screen, (80, 80, 80), (0, bar_y), (WIDTH, bar_y), 2)
    font_large = pygame.font.SysFont("arial", 22, bold=True)
    font_small = pygame.font.SysFont("arial", 17)
    start_y = bar_y + (80 - len(lines) * 26) // 2
    for i, line in enumerate(lines):
        font = font_large if i == 0 else font_small
        col = (255, 255, 255) if i == 0 else (180, 180, 180)
        surf = font.render(line, True, col)
        screen.blit(surf, ((WIDTH - surf.get_width()) // 2, start_y + i * 26))


async def tutorial():
    clock = pygame.time.Clock()

    tut_maze = []
    total = TUTORIAL_SIZE * TUTORIAL_SIZE
    for i in range(total):
        tut_maze.append(["o",
            '1' if i < TUTORIAL_SIZE else 1,
            '1' if (i + 1) % TUTORIAL_SIZE == 0 else 1,
            '1' if i >= total - TUTORIAL_SIZE else 1,
            '1' if i % TUTORIAL_SIZE == 0 else 1])
    stack = [0]
    tut_maze[0][0] = "v"
    dir_base = [(-TUTORIAL_SIZE,1,3),(1,2,4),(TUTORIAL_SIZE,3,1),(-1,4,2)]
    while stack:
        cur = stack[-1]
        dirs = dir_base[:]
        random.shuffle(dirs)
        moved = False
        for dr, mw, tw in dirs:
            nxt = cur + dr
            if dr == -1 and cur % TUTORIAL_SIZE == 0: continue
            if dr ==  1 and (cur+1) % TUTORIAL_SIZE == 0: continue
            if not (0 <= nxt < total): continue
            if tut_maze[nxt][0] == "o":
                tut_maze[cur][mw] = 0
                tut_maze[nxt][tw] = 0
                tut_maze[nxt][0] = "v"
                stack.append(nxt)
                moved = True
                break
        if not moved:
            stack.pop()

    def can_move(cx, cy, dx, dy):
        if cx < 0 or cy < 0 or cx >= TUTORIAL_SIZE or cy >= TUTORIAL_SIZE:
            return False
        cell = tut_maze[cy * TUTORIAL_SIZE + cx]
        if dx ==  1: return cell[2] == 0
        if dx == -1: return cell[4] == 0
        if dy ==  1: return cell[3] == 0
        if dy == -1: return cell[1] == 0

    def tpx(cx, cy):
        return TUTORIAL_OFFSET_X + cx * TUTORIAL_CELL + 2, TUTORIAL_OFFSET_Y + cy * TUTORIAL_CELL + 2

    def cell_centre(cx, cy):
        return TUTORIAL_OFFSET_X + cx * TUTORIAL_CELL + TUTORIAL_CELL // 2, \
               TUTORIAL_OFFSET_Y + cy * TUTORIAL_CELL + TUTORIAL_CELL // 2

    all_inner = [(c, r) for r in range(TUTORIAL_SIZE) for c in range(TUTORIAL_SIZE)
                 if not (c == 0 and r == 0) and not (c == TUTORIAL_SIZE-1 and r == TUTORIAL_SIZE-1)]
    target_cells = random.sample(all_inner, 3)
    targets_hit = [False, False, False]

    p_cell = [0, 0]
    shoot_bullets = bullets()

    screen.fill((10, 10, 20))
    draw_text_centered(screen, "TUTORIAL", HEIGHT//2 - 70, size=60, color=(255, 220, 60))
    draw_text_centered(screen, "Learn the controls before entering the facility.", HEIGHT//2, size=24, color=(180, 180, 180))
    draw_text_centered(screen, "Press any key to begin.", HEIGHT//2 + 50, size=20, color=(120, 120, 120))
    pygame.display.flip()
    waiting = True
    while waiting:
        for e in pygame.event.get():
            if e.type == pygame.QUIT: return
            if e.type == pygame.KEYDOWN: waiting = False
        await asyncio.sleep(0)

    await clean_animation()

    while True:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        all_hit = all(targets_hit)
        reached_goal = p_cell == [TUTORIAL_SIZE-1, TUTORIAL_SIZE-1]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); return
            if event.type == pygame.KEYDOWN:
                cx, cy = p_cell
                if   event.key == pygame.K_a and can_move(cx, cy, -1,  0): p_cell[0] -= 1
                elif event.key == pygame.K_d and can_move(cx, cy,  1,  0): p_cell[0] += 1
                elif event.key == pygame.K_w and can_move(cx, cy,  0, -1): p_cell[1] -= 1
                elif event.key == pygame.K_s and can_move(cx, cy,  0,  1): p_cell[1] += 1
                if all_hit and p_cell == [TUTORIAL_SIZE-1, TUTORIAL_SIZE-1]:
                    await asyncio.sleep(0.3)
                    screen.fill((0, 0, 0))
                    draw_text_centered(screen, "TUTORIAL COMPLETE", HEIGHT//2-40, size=52, color=(0, 220, 80))
                    draw_text_centered(screen, "Press any key to begin.", HEIGHT//2+40, size=20, color=(100, 100, 100))
                    pygame.display.flip()
                    waiting = True
                    while waiting:
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT: return
                            if e.type == pygame.KEYDOWN: waiting = False
                        await asyncio.sleep(0)
                    await clean_animation()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ppx, ppy = tpx(p_cell[0], p_cell[1])
                pcx = ppx + (TUTORIAL_CELL - 4) // 2
                pcy = ppy + (TUTORIAL_CELL - 4) // 2
                shoot_bullets.shoot(mouse_x, mouse_y, pcx, pcy)
                try: bullet_sound.play()
                except: pass

        screen.fill((10, 10, 20))
        pygame.draw.rect(screen, (30, 20, 30),
                         (TUTORIAL_OFFSET_X, TUTORIAL_OFFSET_Y,
                          TUTORIAL_SIZE * TUTORIAL_CELL, TUTORIAL_SIZE * TUTORIAL_CELL))

        gx = TUTORIAL_OFFSET_X + (TUTORIAL_SIZE-1) * TUTORIAL_CELL
        gy = TUTORIAL_OFFSET_Y + (TUTORIAL_SIZE-1) * TUTORIAL_CELL
        goal_col = (0, 200, 80, 70) if all_hit else (80, 80, 80, 50)
        gs = pygame.Surface((TUTORIAL_CELL, TUTORIAL_CELL), pygame.SRCALPHA)
        gs.fill(goal_col)
        screen.blit(gs, (gx, gy))
        lbl_col = (0, 230, 80) if all_hit else (100, 100, 100)
        lbl = pygame.font.SysFont("arial", 10, bold=True).render("GOAL", True, lbl_col)
        screen.blit(lbl, (gx + (TUTORIAL_CELL - lbl.get_width())//2, gy + (TUTORIAL_CELL - lbl.get_height())//2))

        for r in range(TUTORIAL_SIZE):
            for c in range(TUTORIAL_SIZE):
                cell = tut_maze[r * TUTORIAL_SIZE + c]
                x = TUTORIAL_OFFSET_X + c * TUTORIAL_CELL
                y = TUTORIAL_OFFSET_Y + r * TUTORIAL_CELL
                wc = (180, 100, 100)
                if cell[1]==1 or cell[1]=='1': pygame.draw.line(screen,wc,(x,y),(x+TUTORIAL_CELL,y),WALL_THICKNESS)
                if cell[2]==1 or cell[2]=='1': pygame.draw.line(screen,wc,(x+TUTORIAL_CELL,y),(x+TUTORIAL_CELL,y+TUTORIAL_CELL),WALL_THICKNESS)
                if cell[3]==1 or cell[3]=='1': pygame.draw.line(screen,wc,(x,y+TUTORIAL_CELL),(x+TUTORIAL_CELL,y+TUTORIAL_CELL),WALL_THICKNESS)
                if cell[4]==1 or cell[4]=='1': pygame.draw.line(screen,wc,(x,y),(x,y+TUTORIAL_CELL),WALL_THICKNESS)

        for i, (tc, tr) in enumerate(target_cells):
            if not targets_hit[i]:
                tx, ty = cell_centre(tc, tr)
                target(tx, ty)

        ppx, ppy = tpx(p_cell[0], p_cell[1])
        draw_player(ppx, ppy, TUTORIAL_CELL - 4, TUTORIAL_CELL - 4)

        pcx = ppx + (TUTORIAL_CELL - 4) // 2
        pcy = ppy + (TUTORIAL_CELL - 4) // 2

        to_remove = []
        for idx, b in enumerate(shoot_bullets.bullet_lis):
            ox, oy = b[0], b[1]
            b[0] += b[2]; b[1] += b[3]
            if b[0] < 0 or b[0] > WIDTH or b[1] < 0 or b[1] > HEIGHT:
                to_remove.append(idx); continue
            pygame.draw.circle(screen, (175, 155, 96), (int(b[0]), int(b[1])), 3)
            hit = False
            for i, (tc, tr) in enumerate(target_cells):
                if targets_hit[i]: continue
                tx, ty = cell_centre(tc, tr)
                steps = max(1, int(((b[2]**2 + b[3]**2)**0.5) / 7))
                for s in range(steps + 1):
                    t = s / steps
                    sx = ox + b[2] * t
                    sy = oy + b[3] * t
                    if ((sx - tx)**2 + (sy - ty)**2)**0.5 <= 14:
                        targets_hit[i] = True
                        to_remove.append(idx)
                        try: metal_bang.play()
                        except: pass
                        hit = True
                        break
                if hit: break
        for idx in reversed(to_remove):
            if idx < len(shoot_bullets.bullet_lis): shoot_bullets.bullet_lis.pop(idx)

        pygame.draw.line(screen, (220,220,80), (mouse_x-8, mouse_y), (mouse_x+8, mouse_y), 1)
        pygame.draw.line(screen, (220,220,80), (mouse_x, mouse_y-8), (mouse_x, mouse_y+8), 1)
        pygame.draw.circle(screen, (220,220,80), (mouse_x, mouse_y), 5, 1)

        hits_left = sum(1 for h in targets_hit if not h)
        if hits_left > 0:
            draw_tutorial_hud([f"Shoot all {hits_left} target(s), then reach the GREEN cell.",
                               "WASD to move.  LEFT CLICK to shoot.  SPACE toggles torch / weapon."])
        else:
            draw_tutorial_hud(["All targets hit!  Reach the GREEN cell to finish.",
                               "In the real maze: SPACE swaps torch and weapon.  Watch the stamina bar on the right — moving drains it!"])

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

async def lab_intro():
    """Submarine descent intro: player watches the sub sink into the deep ocean before entering the lab."""
    clock = pygame.time.Clock()

    PHASE_DESCEND_1  = 480
    SHARK_PAUSE_LEN  = 150
    PHASE_DESCEND_2  = 200
    WHALE_PAUSE_LEN  = 180
    PHASE_DESCEND_3  = 90
    TOTAL_FRAMES = PHASE_DESCEND_1 + SHARK_PAUSE_LEN + PHASE_DESCEND_2 + WHALE_PAUSE_LEN + PHASE_DESCEND_3

    DARK_START = 400
    sub_w, sub_h = 180, 90

    try:
        sub_img = pygame.image.load("sub.png").convert_alpha()
        sub_img = pygame.transform.scale(sub_img, (sub_w, sub_h))
    except:
        sub_img = None
    try:
        shark_img = pygame.image.load("greenland_shark.png").convert_alpha()
        shark_img = pygame.transform.scale(shark_img, (260, 120))
    except:
        shark_img = None
    try:
        whale_img = pygame.image.load("sperm_whale_and_squid.png").convert_alpha()
        whale_img = pygame.transform.scale(whale_img, (420, 210))
    except:
        whale_img = None

    SHARK_START  = PHASE_DESCEND_1
    SHARK_END    = SHARK_START + SHARK_PAUSE_LEN
    EYES3_START  = SHARK_END + 30
    EYES4_START  = SHARK_END + 90
    WHALE_START  = SHARK_END + PHASE_DESCEND_2
    WHALE_END    = WHALE_START + WHALE_PAUSE_LEN

    
    light_texts = [
        "Descending to Research Lab 453...",
        "Depth: 847m — pressure nominal.",
        "Warning: Uncharted trench detected below.",
    ]
    light_text_schedule = [(30, 190), (220, 370), (395, DARK_START - 5)]
    TEXT_BLUR_IN  = 30
    TEXT_BLUR_OUT = 30

    SEA_TOTAL_H = 2800
    DESCEND_TOTAL = PHASE_DESCEND_1 + PHASE_DESCEND_2 + PHASE_DESCEND_3
    sub_world_y_at_shark = int((PHASE_DESCEND_1 / DESCEND_TOTAL) * (SEA_TOTAL_H - sub_h))
    sub_world_y_at_whale = int(((PHASE_DESCEND_1 + PHASE_DESCEND_2) / DESCEND_TOTAL) * (SEA_TOTAL_H - sub_h))

    
    eye_pairs = [
        (420, 220, sub_world_y_at_shark - 80,  580,  90),
        (460, 160, sub_world_y_at_shark + 60,  640,  90),
        (EYES3_START, 200, sub_world_y_at_whale - 70, 600, 100),
        (EYES4_START, 170, sub_world_y_at_whale + 50, 630, 100),
    ]

    NUM_PARTICLES = 36
    part_x   = [random.randint(0, WIDTH)       for _ in range(NUM_PARTICLES)]
    part_y   = [random.uniform(0, SEA_TOTAL_H) for _ in range(NUM_PARTICLES)]
    part_r   = [random.randint(2, 5)            for _ in range(NUM_PARTICLES)]
    part_spd = [random.uniform(0.5, 1.4)        for _ in range(NUM_PARTICLES)]

    NUM_BIO = 22
    bio_x   = [random.randint(0, WIDTH)        for _ in range(NUM_BIO)]
    bio_y   = [random.randint(0, SEA_TOTAL_H)  for _ in range(NUM_BIO)]
    bio_col = [(random.randint(0,80), random.randint(180,255), random.randint(120,220)) for _ in range(NUM_BIO)]
    bio_r   = [random.randint(2, 4)             for _ in range(NUM_BIO)]
    bio_spd = [random.uniform(0.1, 0.4)         for _ in range(NUM_BIO)]

    wake = []

    NUM_FISH = 12
    fish = [(random.randint(0, WIDTH), random.randint(100, SEA_TOTAL_H // 2),
             random.randint(14, 32), random.choice([-1, 1])) for _ in range(NUM_FISH)]

    ray_xs = [random.randint(50, WIDTH - 50) for _ in range(7)]

    whale_sound_played = False

    for frame in range(TOTAL_FRAMES):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        if frame < SHARK_START:
            descent_frames = frame
            sub_world_y = int((descent_frames / DESCEND_TOTAL) * (SEA_TOTAL_H - sub_h))
        elif frame < SHARK_END:
            sub_world_y = sub_world_y_at_shark
        elif frame < WHALE_START:
            descent_frames = PHASE_DESCEND_1 + (frame - SHARK_END)
            sub_world_y = int((descent_frames / DESCEND_TOTAL) * (SEA_TOTAL_H - sub_h))
        elif frame < WHALE_END:
            sub_world_y = sub_world_y_at_whale
        else:
            descent_frames = PHASE_DESCEND_1 + PHASE_DESCEND_2 + (frame - WHALE_END)
            sub_world_y = int((descent_frames / DESCEND_TOTAL) * (SEA_TOTAL_H - sub_h))

        cam_y = sub_world_y - HEIGHT // 2 + sub_h // 2
        cam_y = max(0, min(cam_y, SEA_TOTAL_H - HEIGHT))

        if frame < DARK_START:
            darkness = 0.0
        elif frame < SHARK_START:
            darkness = min(0.55, (frame - DARK_START) / (SHARK_START - DARK_START) * 0.55)
        elif frame < SHARK_END:
            darkness = 0.55
        elif frame < WHALE_START:
            darkness = min(0.92, 0.55 + (frame - SHARK_END) / PHASE_DESCEND_2 * 0.37)
        elif frame < WHALE_END:
            darkness = 0.92
        else:
            darkness = min(1.0, 0.92 + (frame - WHALE_END) / PHASE_DESCEND_3 * 0.08)

        r_col = int(15  * (1 - darkness) + 1  * darkness)
        g_col = int(100 * (1 - darkness) + 5  * darkness)
        b_col = int(175 * (1 - darkness) + 12 * darkness)
        screen.fill((r_col, g_col, b_col))

        if darkness < 0.6:
            ray_alpha = int(26 * (1 - darkness / 0.6))
            ray_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            for rx in ray_xs:
                sway = int(math.sin(frame * 0.011 + rx * 0.04) * 22)
                pts = [(rx + sway - 20, 0), (rx + sway + 20, 0),
                       (rx - 50, HEIGHT), (rx + 50, HEIGHT)]
                pygame.draw.polygon(ray_surf, (190, 235, 255, ray_alpha), pts)
            screen.blit(ray_surf, (0, 0))

        grad_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for gy in range(0, HEIGHT, 4):
            ga = int(gy / HEIGHT * 70 * (1 - darkness * 0.6))
            pygame.draw.rect(grad_surf, (0, 8, 28, ga), (0, gy, WIDTH, 4))
        screen.blit(grad_surf, (0, 0))

        vign = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        vign_str = 80 + int(darkness * 100)
        for vi in range(40):
            va = int(vign_str * (1 - vi / 40) * 0.6)
            pygame.draw.rect(vign, (0, 0, 0, va), (vi, vi, WIDTH - vi*2, HEIGHT - vi*2), 1)
        screen.blit(vign, (0, 0))

        for i in range(NUM_PARTICLES):
            part_y[i] -= part_spd[i]
            if part_y[i] < 0:
                part_y[i] = SEA_TOTAL_H
            by_screen = part_y[i] - cam_y
            if 0 <= by_screen <= HEIGHT:
                ba = max(0, int(100 * (1 - darkness)))
                if ba > 0:
                    bs = pygame.Surface((part_r[i]*2+2, part_r[i]*2+2), pygame.SRCALPHA)
                    pygame.draw.circle(bs, (190, 230, 255, ba), (part_r[i]+1, part_r[i]+1), part_r[i], 1)
                    screen.blit(bs, (part_x[i], int(by_screen)))

        if darkness > 0.3:
            for i in range(NUM_BIO):
                bio_y[i] -= bio_spd[i]
                if bio_y[i] < 0:
                    bio_y[i] = SEA_TOTAL_H
                by_screen = bio_y[i] - cam_y
                if 0 <= by_screen <= HEIGHT:
                    ba = int(max(0, min(180, (darkness - 0.3) / 0.7 * 180)) * (0.6 + 0.4 * math.sin(frame * 0.07 + i)))
                    if ba > 10:
                        bs = pygame.Surface((bio_r[i]*4, bio_r[i]*4), pygame.SRCALPHA)
                        pygame.draw.circle(bs, (*bio_col[i], ba), (bio_r[i]*2, bio_r[i]*2), bio_r[i])
                        screen.blit(bs, (bio_x[i] - bio_r[i], int(by_screen) - bio_r[i]))

        if darkness < 0.45:
            fish_alpha = int(75 * (1 - darkness / 0.45))
            for fi, (fx, fy_world, fsize, fdir) in enumerate(fish):
                fy_screen = fy_world - cam_y
                if 0 <= fy_screen <= HEIGHT:
                    drift_x = (fx + frame * fdir * 0.55) % WIDTH
                    fs = pygame.Surface((fsize * 2, fsize), pygame.SRCALPHA)
                    bc = (140, 200, 230, fish_alpha)
                    pygame.draw.ellipse(fs, bc, (0, fsize // 4, int(fsize * 1.5), fsize // 2))
                    tail_pts = [(0, 0), (fsize // 2, fsize // 2), (0, fsize)] if fdir > 0 else \
                               [(fsize*2, 0), (int(fsize*1.5), fsize//2), (fsize*2, fsize)]
                    pygame.draw.polygon(fs, bc, tail_pts)
                    screen.blit(fs, (int(drift_x), int(fy_screen) - fsize // 2))

        paused = (SHARK_START <= frame < SHARK_END) or (WHALE_START <= frame < WHALE_END)
        sway_x = int(math.sin(frame * 0.015) * 6) if not paused else 0
        sub_screen_x = WIDTH // 2 - sub_w // 2 + sway_x
        sub_screen_y = sub_world_y - cam_y

        sub_cx = sub_screen_x + sub_w // 2
        sub_cy = sub_screen_y + sub_h // 2

        if not paused and frame % 4 == 0:
            wake.append([sub_screen_x + 4 + random.randint(-4, 4),
                         sub_world_y + sub_h // 2 + random.randint(-8, 8),
                         random.randint(2, 4), max(0, int(90 * (1 - darkness)))])
        for wb in wake:
            wb[1] -= 0.6
            wb[3] -= 3
        wake[:] = [wb for wb in wake if wb[3] > 0]
        for wb in wake:
            wys = wb[1] - cam_y
            if 0 <= wys <= HEIGHT:
                ws = pygame.Surface((wb[2]*2+2, wb[2]*2+2), pygame.SRCALPHA)
                pygame.draw.circle(ws, (200, 235, 255, wb[3]), (wb[2]+1, wb[2]+1), wb[2], 1)
                screen.blit(ws, (int(wb[0]), int(wys)))

        porthole_cx = sub_screen_x + int(sub_w * 0.72)
        porthole_cy = sub_screen_y + sub_h // 2
        glow_alpha = max(0, int(70 * (1 - darkness * 0.6)))
        if glow_alpha > 0:
            glow_surf = pygame.Surface((90, 90), pygame.SRCALPHA)
            pygame.draw.circle(glow_surf, (200, 235, 170, glow_alpha), (45, 45), 42)
            screen.blit(glow_surf, (porthole_cx - 45, porthole_cy - 45))

        if frame < DARK_START:
            for idx, (txt_start, txt_end) in enumerate(light_text_schedule):
                if txt_start <= frame <= txt_end:
                    progress = frame - txt_start
                    duration = txt_end - txt_start
                    if progress < TEXT_BLUR_IN:
                        blur(WIDTH//2 - 250, 70, 500, 34)
                    elif progress > duration - TEXT_BLUR_OUT:
                        blur(WIDTH//2 - 250, 70, 500, 34)
                    else:
                        draw_text_centered(screen, light_texts[idx], 74, size=22, color=(210, 240, 255))

        if sub_img:
            screen.blit(sub_img, (sub_screen_x, sub_screen_y))
        else:
            pygame.draw.rect(screen, (80, 80, 100), (sub_screen_x, sub_screen_y, sub_w, sub_h))
            pygame.draw.circle(screen, (200, 220, 255), (sub_screen_x + sub_w - 20, sub_screen_y + sub_h // 2), 8)

        if frame >= DARK_START:
            for pair_idx, (pair_frame, lx, world_y, rx, duration) in enumerate(eye_pairs):
                if pair_frame <= frame < pair_frame + duration:
                    screen_y = int(world_y - cam_y)
                    for cx_eye in [lx, rx]:
                        for ex_eye in [cx_eye - 15, cx_eye + 15]:
                            e = eyes((160, 0, 0), (0, 0, 0), ex_eye, screen_y)
                            e.look(sub_cx, sub_cy)

            if SHARK_START <= frame < SHARK_END:
                slide_in  = min(1.0, (frame - SHARK_START) / 40)
                shark_sx  = int(WIDTH + 30 - slide_in * (WIDTH * 0.52 + 30))
                shark_sy  = HEIGHT // 2 + 70
                if shark_img:
                    screen.blit(shark_img, (shark_sx, shark_sy))
                else:
                    pygame.draw.ellipse(screen, (30, 100, 30), (shark_sx, shark_sy, 260, 80))
                draw_tutorial_hud(["A Greenland shark most of them are blind due to parasites.",
                                   "They can still navigate with electro-reception and magentic fields"])

            if frame >= WHALE_START:
                if not whale_sound_played:
                    click_sound.play()
                    whale_sound_played = True
                if frame < WHALE_START + 20:
                    blur(0, 0, WIDTH, HEIGHT)
                else:
                    slide_in = min(1.0, (frame - (WHALE_START + 20)) / 50)
                    if whale_img:
                        whale_sx = int(-whale_img.get_width() + slide_in * (WIDTH // 2 - 30))
                        whale_sy = HEIGHT // 2 - 90
                        screen.blit(whale_img, (whale_sx, whale_sy))
                    else:
                        pygame.draw.ellipse(screen, (40, 40, 60), (WIDTH//2-210, HEIGHT//2-50, 420, 130))
                    draw_tutorial_hud(["A sperm whale. It stunned the giant squid with its clicks, then killed it",
                                       "the whale can navigate using ecolocation in the dark."])

        if darkness > 0:
            dark_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_surf.fill((0, 0, 0, int(darkness * 215)))
            screen.blit(dark_surf, (0, 0))

        depth_m = int((sub_world_y / SEA_TOTAL_H) * 3500)
        draw_text(screen, f"{depth_m}m", WIDTH - 80, HEIGHT - 30, size=18, color=(160, 210, 255))

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

def boss_fight_cyborg_squid(frame, max_height, squid_bx, squid_by, col, w):
    y_val=math.cos(frame)*max_height+squid_by # math.cos is a repeating function
    '''every 360 (360 degrees is the same as 0 degrees in a circle) frames y_val repeats, 0-180 going from max to minimum 180-360 going from minimum to maximum
    add the boss's y value and then boss becomes mid-line'''
    # adding i*10 offsets the cosine phase per segment, so each segment is at a different point
    # in the wave cycle giving the tentacle a snake-like ripple rather than all moving together
    num_tentacles = 4
    spacing = 40
    for i in range(num_tentacles):
        left_x = squid_bx - 10 - i * spacing
        left_x1 = squid_bx - 10 - (i + 1) * spacing
        right_x = squid_bx + 10 + i * spacing
        right_x1 = squid_bx + 10 + (i + 1) * spacing
        y_left = math.cos(frame + i * 10) * max_height + squid_by
        y_left1 = math.cos(frame + (i + 1) * 10) * max_height + squid_by
        pygame.draw.line(screen, col, (left_x, y_left), (left_x1, y_left1), w)
        pygame.draw.line(screen, col, (right_x, y_left), (right_x1, y_left1), w)

def draw_squid_head(bx, by):
    """Draw the robotic squid head: squid mantle shape with fins, hexagon red eye. bx/by is bottom-middle of rectangle."""
    mantle_w = 60
    mantle_h = 150
    mantle_x = bx - mantle_w // 2
    mantle_top_y = by - mantle_h

    mantle_pts = [
        (bx, mantle_top_y),
        (bx + mantle_w // 2, mantle_top_y + 40),
        (bx + mantle_w // 2, by - 30),
        (bx + 10, by),
        (bx - 10, by),
        (bx - mantle_w // 2, by - 30),
        (bx - mantle_w // 2, mantle_top_y + 40),
    ]
    pygame.draw.polygon(screen, (40, 40, 60), mantle_pts)
    pygame.draw.polygon(screen, (0, 200, 80), mantle_pts, 2)

    fin_left = [(bx - mantle_w // 2, mantle_top_y + 40), (bx - mantle_w // 2 - 28, mantle_top_y + 80), (bx - mantle_w // 2, mantle_top_y + 110)]
    fin_right = [(bx + mantle_w // 2, mantle_top_y + 40), (bx + mantle_w // 2 + 28, mantle_top_y + 80), (bx + mantle_w // 2, mantle_top_y + 110)]
    pygame.draw.polygon(screen, (30, 30, 50), fin_left)
    pygame.draw.polygon(screen, (0, 200, 80), fin_left, 2)
    pygame.draw.polygon(screen, (30, 30, 50), fin_right)
    pygame.draw.polygon(screen, (0, 200, 80), fin_right, 2)

    hex_cx = bx
    hex_cy = mantle_top_y + 65
    hex_r = 18
    hex_pts = []
    for k in range(6):
        angle_rad = math.radians(60 * k - 30)
        hex_pts.append((hex_cx + hex_r * math.cos(angle_rad), hex_cy + hex_r * math.sin(angle_rad)))
    pygame.draw.polygon(screen, (80, 0, 0), hex_pts)
    pygame.draw.polygon(screen, (220, 0, 0), hex_pts, 2)
    pygame.draw.circle(screen, (255, 0, 0), (hex_cx, hex_cy), 10)
    glow_surf = pygame.Surface((hex_r * 4, hex_r * 4), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (255, 0, 0, 60), (hex_r * 2, hex_r * 2), hex_r * 2)
    screen.blit(glow_surf, (hex_cx - hex_r * 2, hex_cy - hex_r * 2))

    for px in range(mantle_x + 6, mantle_x + mantle_w - 6, 10):
        pygame.draw.line(screen, (0, 80, 40), (px, hex_cy + 28), (px, by - 8), 1)
    pygame.draw.line(screen, (0, 120, 50), (mantle_x + 6, hex_cy + 18), (mantle_x + mantle_w - 6, hex_cy + 18), 1)


async def boss_fight():
    """Boss fight: player controls sub horizontally, shoots the cyborg squid below. Squid shoots back."""
    global global_damage_state, damage, gun_type

    clock = pygame.time.Clock()

    sub_w, sub_h = 180, 90
    sub_x = WIDTH // 2 - sub_w // 2
    sub_y = 80
    sub_speed = 5

    try:
        sub_img = pygame.image.load("sub.png").convert_alpha()
        sub_img = pygame.transform.scale(sub_img, (sub_w, sub_h))
    except:
        sub_img = None

    for intro_frame in range(180):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        t = intro_frame / 179
        sub_intro_y = int(HEIGHT * 0.7 - t * (HEIGHT * 0.7 - sub_y))
        screen.fill((1, 5, 12))
        if sub_img:
            screen.blit(sub_img, (WIDTH // 2 - sub_w // 2, sub_intro_y))
        else:
            pygame.draw.rect(screen, (80, 80, 100), (WIDTH // 2 - sub_w // 2, sub_intro_y, sub_w, sub_h))
        if intro_frame < 60:
            alpha = min(255, intro_frame * 6)
            blur(WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 40)
            txt_surf = pygame.font.SysFont("arial", 36, bold=True).render("NEW CYBORG", True, (220, 80, 80))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (WIDTH // 2 - txt_surf.get_width() // 2, HEIGHT // 2 - 18))
        elif intro_frame < 90:
            blur(WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 40)
        else:
            alpha = min(255, (intro_frame - 90) * 6)
            blur(WIDTH // 2 - 200, HEIGHT // 2 - 20, 400, 40)
            txt_surf = pygame.font.SysFont("arial", 36, bold=True).render("GIANT SQUID", True, (80, 200, 220))
            txt_surf.set_alpha(alpha)
            screen.blit(txt_surf, (WIDTH // 2 - txt_surf.get_width() // 2, HEIGHT // 2 - 18))
        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

    boss_health = [100]
    player_health = [100]
    boss_damage_accumulated = 0

    squid_bx = WIDTH // 2
    squid_by = HEIGHT - 100

    gun_surf, gun_pivot = _make_gun_surface_for(gun_type)

    if gun_type == "shotgun":
        player_bullets = shotgun_shells()
    else:
        player_bullets = bullets()

    enemy_bullets = squid_bullets()

    squid_shoot_timer = 0
    SQUID_SHOOT_DELAY = 90

    muzzle_flash_timer = 0
    MUZZLE_FLASH_DURATION = 4
    last_muzzle_pos = (0, 0)
    last_muzzle_angle = 0

    frame = 0

    NUM_BOSS_PARTICLES = 24
    bp_x = [random.randint(0, WIDTH) for _ in range(NUM_BOSS_PARTICLES)]
    bp_y = [random.uniform(0, HEIGHT) for _ in range(NUM_BOSS_PARTICLES)]
    bp_r = [random.randint(2, 4) for _ in range(NUM_BOSS_PARTICLES)]
    bp_spd = [random.uniform(0.3, 0.9) for _ in range(NUM_BOSS_PARTICLES)]

    NUM_BOSS_FISH = 8
    boss_fish = [(random.randint(0, WIDTH), random.randint(HEIGHT // 4, HEIGHT - 60),
                  random.randint(12, 26), random.choice([-1, 1])) for _ in range(NUM_BOSS_FISH)]

    ammo = get_ammo_for_gun(gun_type)
    ammo_regen_timer = 0
    AMMO_REGEN_DELAY = 120

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if ammo > 0:
                    sub_cx = sub_x + sub_w // 2
                    sub_cy = sub_y + sub_h // 2
                    bullet_sound.play()
                    player_bullets.shoot(mouse_x, mouse_y, sub_cx, sub_cy)
                    ammo -= 1
                    muzzle_flash_timer = MUZZLE_FLASH_DURATION

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and sub_x > 0:
            sub_x -= sub_speed
        if keys[pygame.K_d] and sub_x + sub_w < WIDTH:
            sub_x += sub_speed

        r_ocean = int(1 + frame * 0.003 * 2) % 8 + 1
        g_ocean = int(5 + frame * 0.002 * 3) % 12 + 5
        b_ocean = int(12 + frame * 0.001 * 5) % 20 + 10
        screen.fill((r_ocean, g_ocean, b_ocean + 10))

        for i in range(NUM_BOSS_PARTICLES):
            bp_y[i] -= bp_spd[i]
            if bp_y[i] < 0:
                bp_y[i] = HEIGHT
                bp_x[i] = random.randint(0, WIDTH)
            ba = random.randint(40, 80)
            bs = pygame.Surface((bp_r[i]*2+2, bp_r[i]*2+2), pygame.SRCALPHA)
            pygame.draw.circle(bs, (150, 200, 255, ba), (bp_r[i]+1, bp_r[i]+1), bp_r[i], 1)
            screen.blit(bs, (int(bp_x[i]), int(bp_y[i])))

        for fi, (fx, fy, fsize, fdir) in enumerate(boss_fish):
            drift_x = (fx + frame * fdir * 0.4) % WIDTH
            fs = pygame.Surface((fsize * 2, fsize), pygame.SRCALPHA)
            bc = (80, 140, 180, 50)
            pygame.draw.ellipse(fs, bc, (0, fsize // 4, int(fsize * 1.5), fsize // 2))
            tail_pts = [(0, 0), (fsize // 2, fsize // 2), (0, fsize)] if fdir > 0 else \
                       [(fsize*2, 0), (int(fsize*1.5), fsize//2), (fsize*2, fsize)]
            pygame.draw.polygon(fs, bc, tail_pts)
            screen.blit(fs, (int(drift_x), fy - fsize // 2))

        tentacle_col = (0, 180, 80)
        tentacle_w = 3
        boss_fight_cyborg_squid(frame * 0.05, 90, squid_bx, squid_by, tentacle_col, tentacle_w)

        draw_squid_head(squid_bx, squid_by)

        sub_cx = sub_x + sub_w // 2
        sub_cy = sub_y + sub_h // 2

        if sub_img:
            screen.blit(sub_img, (sub_x, sub_y))
        else:
            pygame.draw.rect(screen, (80, 80, 100), (sub_x, sub_y, sub_w, sub_h))
            pygame.draw.circle(screen, (200, 220, 255), (sub_x + sub_w - 20, sub_y + sub_h // 2), 8)

        muzzle_x, muzzle_y, shot_angle = draw_gun(sub_cx, sub_cy, mouse_x, mouse_y, gun_surf, gun_pivot)
        last_muzzle_pos = (muzzle_x, muzzle_y)
        last_muzzle_angle = shot_angle

        if muzzle_flash_timer > 0:
            draw_muzzle_flash(muzzle_x, muzzle_y, shot_angle)
            muzzle_flash_timer -= 1

        class _FakeBossTarget:
            def __init__(self):
                self.currx = 0
                self.curry = 0
                self.stunned_timer = 0
                self.hit_flash_timer = 0
                self.last_hit_ex = 0
                self.last_hit_ey = 0

        class _BossWrapper:
            def __init__(self, bx_ref, by_ref, health_ref, accum_ref):
                self.bx = bx_ref
                self.by = by_ref
                self.health = health_ref
                self.accum = accum_ref
                self.stunned_timer = 0
                self.hit_flash_timer = 0
                self.last_hit_ex = 0
                self.last_hit_ey = 0
                self.currx = 0
                self.curry = 0

        boss_hit_flash = [0]

        to_remove = []
        for index, t in enumerate(player_bullets.bullet_lis):
            change_x = t[0] + t[2]
            change_y = t[1] + t[3]
            player_bullets.bullet_lis[index][0] = change_x
            player_bullets.bullet_lis[index][1] = change_y
            if change_x > WIDTH or change_x < 0 or change_y > HEIGHT or change_y < 0:
                to_remove.append(index)
            else:
                pygame.draw.circle(screen, (175, 155, 96), (int(change_x), int(change_y)), 5)
                hit_rect_x = squid_bx - 30
                hit_rect_y = squid_by - 150
                hit_rect_w = 60
                hit_rect_h = 150
                if hit_rect_x <= change_x <= hit_rect_x + hit_rect_w and hit_rect_y <= change_y <= hit_rect_y + hit_rect_h:
                    boss_damage_accumulated += damage
                    boss_health[0] = max(0, 100 - boss_damage_accumulated)
                    boss_hit_flash[0] = 20
                    sound_choice = random.randint(1, 2)
                    if sound_choice == 1:
                        Scary_metal_sound.play()
                    else:
                        metal_bang.play()
                    to_remove.append(index)
        for index in reversed(to_remove):
            if index < len(player_bullets.bullet_lis):
                player_bullets.bullet_lis.pop(index)

        if boss_hit_flash[0] > 0:
            flash_s = pygame.Surface((60, 150), pygame.SRCALPHA)
            flash_s.fill((255, 80, 0, int(180 * boss_hit_flash[0] / 20)))
            screen.blit(flash_s, (squid_bx - 30, squid_by - 150))
            boss_hit_flash[0] -= 1

        squid_shoot_timer += 1
        if squid_shoot_timer >= SQUID_SHOOT_DELAY:
            squid_shoot_timer = 0
            enemy_bullets.shoot(sub_cx, sub_cy, squid_bx, squid_by - 40)

        enemy_bullets.move(sub_x, sub_y, sub_w, sub_h, player_health)

        ammo_regen_timer += 1
        if ammo_regen_timer >= AMMO_REGEN_DELAY:
            ammo_regen_timer = 0
            max_ammo = get_ammo_for_gun(gun_type)
            if ammo < max_ammo:
                ammo += 1

        pygame.draw.rect(screen, (30, 30, 50), (0, 0, WIDTH, 36))
        boss_bar_w = int((boss_health[0] / 100) * 300)
        pygame.draw.rect(screen, (60, 0, 0), (WIDTH // 2 - 150, 8, 300, 20))
        pygame.draw.rect(screen, (200, 0, 50), (WIDTH // 2 - 150, 8, boss_bar_w, 20))
        pygame.draw.rect(screen, (255, 80, 80), (WIDTH // 2 - 150, 8, 300, 20), 2)
        draw_text(screen, "BOSS", WIDTH // 2 - 180, 8, size=18, color=(220, 80, 80))

        player_bar_w = max(0, int((player_health[0] / 100) * 200))
        pygame.draw.rect(screen, (0, 40, 0), (10, 8, 200, 20))
        pygame.draw.rect(screen, (0, 180, 80), (10, 8, player_bar_w, 20))
        pygame.draw.rect(screen, (0, 255, 100), (10, 8, 200, 20), 2)
        draw_text(screen, "SUB", 215, 8, size=18, color=(80, 220, 80))

        ammo_col = (220, 220, 100) if ammo > 3 else (220, 60, 60)
        draw_text(screen, f"AMMO: {ammo}", 10, 42, size=18, color=ammo_col)

        draw_text_centered(screen, "A  D  to move    CLICK to shoot", HEIGHT - 22, size=16, color=(120, 120, 120))

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)
        frame += 1

        if boss_health[0] <= 0:
            return True

        if player_health[0] <= 0:
            end_sound.play()
            return False


async def main():
    global stamina, gun_type, damage, GUN_FOG_RADIUS,remaining_minigames
    global bullet_sound, Scary_metal_sound, metal_bang, scary_sound1, scary_sound2
    global scary_sound3, end_sound, switch_equipment, switch_equipment1
    global gun_upgrade_sound, click_sound, mouse_sound

    #sound effects
    try: bullet_sound = pygame.mixer.Sound("gunshot.ogg")
    except Exception as e: print("gunshot.ogg failed:", e)
    try: Scary_metal_sound = pygame.mixer.Sound("scary_metal_sound.ogg")
    except Exception as e: print("scary_metal_sound.ogg failed:", e)
    try: metal_bang = pygame.mixer.Sound("metal_hit.ogg")
    except Exception as e: print("metal_hit.ogg failed:", e)
    try: scary_sound1 = pygame.mixer.Sound("scary_sound1.ogg")
    except Exception as e: print("scary_sound1.ogg failed:", e)
    try: scary_sound2 = pygame.mixer.Sound("scary_sound2.ogg")
    except Exception as e: print("scary_sound2.ogg failed:", e)
    try: scary_sound3 = pygame.mixer.Sound("scary_sound3.ogg")
    except Exception as e: print("scary_sound3.ogg failed:", e)
    try: end_sound = pygame.mixer.Sound("scary_end.ogg")
    except Exception as e: print("scary_end.ogg failed:", e)
    try: switch_equipment = pygame.mixer.Sound("weapon_switch.ogg")
    except Exception as e: print("weapon_switch.ogg failed:", e)
    try: switch_equipment1 = pygame.mixer.Sound("switch.ogg")
    except Exception as e: print("switch.ogg failed:", e)
    try: gun_upgrade_sound = pygame.mixer.Sound("swish.ogg")
    except Exception as e: print("swish.ogg failed:", e)
    try: click_sound = pygame.mixer.Sound("sperm_whale.ogg")
    except Exception as e: print("sperm_whale.ogg failed:", e)
    try: mouse_sound = pygame.mixer.Sound("mouse_sound.ogg")
    except Exception as e: print("mouse_sound.ogg failed:", e)

    try:
        pygame.mixer.music.load("scary_bg_music.ogg")
    except:
        pass

    try:
        pygame.mixer.music.play(-1)
    except:
        pass
    floor_img = get_lab_floor()
    menu_imgs = []
    for i, fname in enumerate(["menu_frame.png","menu_frame1.png","menu_frame2.png","menu_frame3.png","menu_frame4.png"]):
        try:
            menu_imgs.append(pygame.image.load(fname).convert_alpha())
        except:
            s = pygame.Surface((WIDTH, HEIGHT)); s.fill((20, 20, 60)); menu_imgs.append(s)
    menu_index = 0

    maze, player_cell, player_pos, player_size, enemy, box_positions = build_game_state()
    boxes_collected = 0

    clock = pygame.time.Clock()
    menu_active = True
    game_active = False
    enemy_move_timer = 0
    ENEMY_MOVE_DELAY = 20
    frame_count = 0

    gun_drawn = False
    gun_type = "pistol_1"
    damage = get_damage_for_gun(gun_type)
    GUN_FOG_RADIUS = get_gun_fog_radius(gun_type)
    ammo = get_ammo_for_gun(gun_type)
    muzzle_flash_timer = 0
    MUZZLE_FLASH_DURATION = 4
    last_muzzle_pos = (0, 0)
    last_muzzle_angle = 0
    HIT_FLASH_DURATION = 60
    bullet_mgr = bullets()

    player_stunned_timer = 0

    upgrade_animation_active = False

    gun_surf, gun_pivot = make_gun_surface()

    

    minigame_funcs = [math_mini_game, time_game, memory_game]

    sound_or_nah = 0

    box_img = pygame.image.load("gun_box.png").convert_alpha()
    box_img = pygame.transform.scale(box_img, (20, 20))
    box_img_hud = pygame.transform.scale(box_img, (40, 40))

    running = True
    while running:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if menu_active:
                    menu_index += 1
                    mouse_sound.play()
                    if menu_index >= len(menu_imgs):
                        menu_active = False
                        await clean_animation()
                        await tutorial()
                        await clean_animation()
                        await lab_intro()
                        await clean_animation()
                        game_active = True
                elif game_active:
                    if event.key == pygame.K_SPACE:
                        gun_drawn = not gun_drawn
                        if gun_drawn:
                            switch_equipment.play()
                        else:
                            switch_equipment1.play()

                    cx, cy = player_cell[0], player_cell[1]
                    moved = False
                    if stamina>0:
                        if event.key == pygame.K_a and can_move_direction(maze, cx, cy, -1, 0) and player_stunned_timer==0:
                            player_cell[0] -= 1
                            moved = True
                            
                        elif event.key == pygame.K_d and can_move_direction(maze, cx, cy, 1, 0) and player_stunned_timer==0:
                            player_cell[0] += 1
                            moved = True
                        
                        elif event.key == pygame.K_w and can_move_direction(maze, cx, cy, 0, -1) and player_stunned_timer==0:
                            player_cell[1] -= 1
                            moved = True
                            
                        elif event.key == pygame.K_s and can_move_direction(maze, cx, cy, 0, 1) and player_stunned_timer==0:
                            player_cell[1] += 1
                            moved = True

                    if event.key == pygame.K_e and game_active:
                        cell_tuple = (player_cell[0], player_cell[1])
                        if cell_tuple in box_positions:
                            box_positions.remove(cell_tuple)
                            boxes_collected += 1
                            threshold = get_upgrade_threshold(gun_type)
                            if threshold is not None and boxes_collected >= threshold:
                                next_gun = get_next_gun(gun_type)
                                if next_gun != gun_type:
                                    player_cx = player_pos[0] + player_size // 2
                                    player_cy = player_pos[1] + player_size // 2
                                    old_surf = gun_surf
                                    old_pivot = gun_pivot
                                    gun_upgrade_sound.play()
                                    await gun_upgrade_animation(player_cx, player_cy, old_surf, old_pivot, next_gun, floor_img, maze, box_positions, box_img, enemy, player_pos, player_size, frame_count)
                                    gun_type = next_gun
                                    damage = get_damage_for_gun(gun_type)
                                    GUN_FOG_RADIUS = get_gun_fog_radius(gun_type)
                                    ammo = get_ammo_for_gun(gun_type)
                                    if gun_type == "shotgun":
                                        bullet_mgr = shotgun_shells()
                                    else:
                                        bullet_mgr = bullets()
                                    gun_surf, gun_pivot = make_gun_surface()
                                    switch_equipment.play()

                    if moved:
                        stamina-=10
                        px, py = cell_to_pixel(player_cell[0], player_cell[1])
                        player_pos[0] = px + 2
                        player_pos[1] = py + 2
                        enemy.recalculate(player_cell[0], player_cell[1])

                        if player_cell[0] == size - 1 and player_cell[1] == size - 1:
                            if remaining_minigames:
                                await clean_animation()
                                game_index = remaining_minigames.pop(0)
                                await minigame_funcs[game_index]()
                                if not remaining_minigames:
                                    await clean_animation()
                                    boss_won = await boss_fight()
                                    if boss_won:
                                        await you_win_screen()
                                    running = False
                                else:
                                    
                                    await clean_animation()
                                    maze, player_cell, player_pos, player_size, enemy, box_positions = build_game_state()
                                    stamina+=50
                                    if stamina>100:
                                        stamina=50
                                    enemy_move_timer = 0
                                    frame_count = 0
                                    gun_drawn = False
                                    muzzle_flash_timer = 0
                                    player_stunned_timer = 0
                                    if gun_type == "shotgun":
                                        bullet_mgr = shotgun_shells()
                                    else:
                                        bullet_mgr = bullets()
                                    floor_img = get_lab_floor(seed=random.randint(0, 9999))

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_active and gun_drawn and ammo > 0:
                    playerx = player_pos[0] + player_size // 2
                    playery = player_pos[1] + player_size // 2
                    bullet_sound.play()
                    bullet_mgr.shoot(mouse_x, mouse_y, playerx, playery)
                    ammo -= 1
                    muzzle_flash_timer = MUZZLE_FLASH_DURATION
                    last_muzzle_pos = (mouse_x, mouse_y)

        if game_active:
            if enemy.stunned_timer > 0:
                enemy.stunned_timer -= 1
            else:
                enemy_move_timer += 1
                if enemy_move_timer >= ENEMY_MOVE_DELAY:
                    enemy_move_timer = 0
                    if enemy.path_index >= len(enemy.path):
                        enemy.recalculate(player_cell[0], player_cell[1])
                    nx, ny, _ = enemy.pick_cell_to_move()
                    enemy.move(nx, ny)

                if enemy.currx == player_cell[0] and enemy.curry == player_cell[1]:
                    end_sound.play()
                    game_active = False
                    should_restart = await game_over_screen()
                    if not should_restart:
                        running = False
                    else:
                        maze, player_cell, player_pos, player_size, enemy, box_positions = build_game_state()
                        enemy_move_timer = 0
                        frame_count = 0
                        stamina=100
                        gun_drawn = False
                        muzzle_flash_timer = 0
                        if gun_type == "shotgun":
                            bullet_mgr = shotgun_shells()
                        else:
                            bullet_mgr = bullets()
                        player_stunned_timer = 0
                        await clean_animation()
                        game_active = True
                    continue
            frame_count += 1
            if frame_count%30==0:
                stamina+=10
                if stamina>100:
                    stamina=100
            if muzzle_flash_timer > 0:
                muzzle_flash_timer -= 1
            if enemy.hit_flash_timer > 0:
                enemy.hit_flash_timer -= 1
        screen.fill(BLACK)

        if menu_active:
            draw_image(screen, menu_imgs[menu_index], 0, 0)
        elif game_active:
            screen.blit(floor_img, (0, 0))
            draw_maze(maze, size, MAZE_OFFSET_X, MAZE_OFFSET_Y)

            goal_x, goal_y = cell_to_pixel(size - 1, size - 1)
            goal_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            goal_surf.fill((0, 180, 80, 60))
            screen.blit(goal_surf, (goal_x, goal_y))

            for bx, by in box_positions:
                bpx, bpy = cell_to_pixel(bx, by)
                screen.blit(box_img, (bpx+10, bpy+10))
                if (bx, by) == (player_cell[0], player_cell[1]):
                    font_e = pygame.font.SysFont("arial", 16)
                    e_surf = font_e.render("[E]", True, (255, 220, 80))
                    screen.blit(e_surf, (bpx + 5, bpy - 14))

            ex, ey = cell_to_pixel(enemy.currx, enemy.curry)
            draw_enemy(ex, ey, enemy.stunned_timer > 0, enemy.currx * 100 + enemy.curry)

            if enemy.hit_flash_timer > 0:
                alpha = int(200 * (enemy.hit_flash_timer / HIT_FLASH_DURATION))
                hit_surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
                hit_surf.fill((255, 80, 0, alpha))
                screen.blit(hit_surf, (enemy.last_hit_ex, enemy.last_hit_ey))

            draw_player(player_pos[0], player_pos[1], player_size, player_size)

            flicker = int(math.sin(frame_count * 0.3) * 2)
            player_cx = player_pos[0] + player_size // 2
            player_cy = player_pos[1] + player_size // 2

            if gun_drawn:
                muzzle_x, muzzle_y, shot_angle = draw_gun(
                    player_cx, player_cy, mouse_x, mouse_y, gun_surf, gun_pivot)
                last_muzzle_pos = (muzzle_x, muzzle_y)
                last_muzzle_angle = shot_angle

                if muzzle_flash_timer > 0:
                    draw_muzzle_flash(muzzle_x, muzzle_y, shot_angle)

                draw_torch_light(player_cx, player_cy,
                                 flicker_offset=flicker, radius_override=GUN_FOG_RADIUS)
            else:
                flame_x, flame_y = draw_torch(
                    player_pos[0], player_pos[1], player_size, player_size, flicker)
                draw_torch_light(flame_x, flame_y, flicker_offset=flicker)

            bullet_mgr.move(enemy)

            dist = distance_estimation(player_cell[0], enemy.currx, player_cell[1], enemy.curry)
            amount = dist * 250
            if not (amount < 100):
                sound_or_nah = random.randint(1, math.ceil(amount))
            if sound_or_nah == 1:
                scary_sound1.play()
            if sound_or_nah == 20:
                scary_sound2.play()
            if sound_or_nah == 99:
                scary_sound3.play()
            if enemy.enemy_type:
                dis=distance_estimation(player_cx,player_cy,ex,ey)
                dis*=5
                dis+=2
                dis=math.ceil(dis)
                sonar_boom=random.randint(1,dis)
                if 1==sonar_boom and player_stunned_timer==0:
                    click_sound.play()
                    player_stunned_timer=120
            if player_stunned_timer>0:
                blur(0,0,WIDTH,HEIGHT)
                player_stunned_timer-=1
            draw_text(screen, f"Distance from creature: {dist:.1f}", 20, 20, size=24, color=WHITE)

            draw_text(screen, f"Repairs left: {len(remaining_minigames)}", WIDTH - 200, 20, size=22, color=(100, 220, 100))

            if gun_drawn:
                ammo_col = (220, 220, 100) if ammo > 3 else (220, 60, 60)
                draw_text(screen, f"AMMO: {ammo}", 20, 52, size=22, color=ammo_col)
                if ammo == 0:
                    draw_text(screen, "OUT OF AMMO", 20, 78, size=18, color=(200, 50, 50))
            else:
                screen.blit(box_img_hud, (20, 52))
                next_threshold = get_upgrade_threshold(gun_type)
                if next_threshold is not None:
                    draw_text(screen, f"x{boxes_collected}/{next_threshold}", 65, 62, size=22, color=WHITE)
                else:
                    draw_text(screen, f"x{boxes_collected}", 65, 62, size=22, color=WHITE)

            if enemy.stunned_timer > 0:
                seconds_left = math.ceil(enemy.stunned_timer / 60)
                draw_text(screen, f"STUNNED: {seconds_left}s", 20, 104, size=18, color=(100, 100, 220))
            pygame.draw.rect(screen,WHITE,(720,100,30,400),5)
            pygame.draw.rect(screen,WHITE,(720,500-4*stamina,30,4*stamina))

        pygame.display.flip()
        await asyncio.sleep(0)
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    asyncio.run(main())