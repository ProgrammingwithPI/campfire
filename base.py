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
                    if sound_choice==1:
                        Scary_metal_sound.play()
                    else:
                        metal_bang.play()
                    if global_damage_state==9:
                        enemy.stunned_timer = 600
                        to_remove.append(index)
                        global_damage_state=0
        for index in reversed(to_remove):
            self.bullet_lis.pop(index)

    def shoot(self,mousex,mousey,playerx,playery):

        base_length=mousex-playerx
        '''Difference between the mousex and playerx x-vals tells the you the amount of x values that changed between their x-coords, 
        or how many units of x they are apart. Which is distance, which is the length of that side of the triangle which is the base.'''
        
        height=mousey-playery
        '''Same logic for base_length calculation but applies for y values or height.'''

        hypotenus=(height**2+base_length**2)**(1/2) #c^2=a^2+b^2
        '''Now we got all the sides of the triangle and can do trig'''

        if hypotenus == 0:# zero division error
            return
        
        angle=height/hypotenus # gives sin value for triangle's angle
        angle1=base_length/hypotenus # gives cos value for triangle's angle
        
        y_change=(angle*50) #moves in 50 units of y (or y values), multiplied by the angle meaning depending on the angle it will move the full 50 or 0 y values
        x_change=(angle1*50) #moves in 50 units of x (or x values), multiplied by the angle meaning depending on the angle it will move the full 50 or 0 x values

        bullet_val=[playerx,playery,x_change,y_change]
        self.bullet_lis.append(bullet_val)
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