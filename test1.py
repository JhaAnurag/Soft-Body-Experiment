import pygame
import sys
import colorsys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 600, 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Springy Rectangular Softbody")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLACK = (0,0,0)

Background_color = BLACK
LineColor = WHITE

k,kx = 1,1 #Border Offset Multiplier

# Controls
following_mouse = True


class Circle: #It acts like the vertex of the softbody

    def __init__(self, x, y, vx, vy, color, radius):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.radius = radius


# Circle instances for drawing the simple square softbody
circle = Circle(screen_width // 2, screen_height // 2, 0, 0, BLUE, 20) #acts like the center of the shape the next are the four vertices of the square
circle2 = Circle(screen_width // 2, screen_height // 2, 0, 0, RED, 20)
circle3 = Circle(screen_width // 2, screen_height // 2, 0, 0, RED, 20)
circle4 = Circle(screen_width // 2, screen_height // 2, 0, 0, RED, 20)
circle5 = Circle(screen_width // 2, screen_height // 2, 0, 0, RED, 20)

spring_constant = 0.05  # stiffness of the spring
damping_factor = 0.08 # damping
COR_Main = 0.8  # coefficient of restitution
GravConst = 0.6 # gravitational constant

def spring_motion(position, velocity, target, spring_constant, damping_factor): #,grav=False #(the grav is from an earlier attempt to implement gravity, kept just for reference)
    displacement = target - position
    spring_force = spring_constant * displacement
    damping_force = velocity * damping_factor
    acceleration = spring_force - damping_force
    velocity += acceleration
    position += velocity
    return position, velocity


# Main game loop
running = True
rand = 0 #for generating random number
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if (
                event.key == pygame.K_SPACE
            ):  # can be used to stop and start the simulation, not implemented yet
                # following_mouse = not following_mouse
                pass
    rand = random.random()
    right_mouse_pressed = pygame.mouse.get_pressed()[0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    print(circle.x, "-", circle.y, ":", circle.vx, "-", circle.vy) #printing the values of the centeral circle
    
    def reset():
        c.vx = 0
        c.vy = 0
            
    for c in [circle5, circle2, circle3, circle4, circle]:
        COR = COR_Main
        if  c == circle:
            COR = 0.8*COR_Main # workaround to make the central circle less bouncy, i will work on making a version without the central circle, possible??
        #for setting the velocity to zero if very small to prevent microjumps
        if abs(c.vx) < 0.2:
            c.vx = 0
        if abs(c.vy) < 0.2:
            c.vy = 0
        #border collision detection, have to write a seperate collision detection system for when two entities collide
        if c.x < c.radius*k*kx:
            c.x = c.radius*k*kx
            c.vx *= -COR
        elif c.x > screen_width - c.radius*k*kx:
            c.x = screen_width - c.radius*k*kx
            c.vx *= -COR
        if c.y < c.radius*k:
            c.y = c.radius*k
            c.vy *= -COR
        elif c.y > screen_height - c.radius*k:
            c.y = screen_height - c.radius*k
            c.vy *= -COR
            
    if right_mouse_pressed:#for moving the central vertex when mouse is pressed
        rand = random.random()
        circle.x, circle.vx = spring_motion(
            circle.x, circle.vx, mouse_x, spring_constant, damping_factor
        )
        circle.y, circle.vy = spring_motion(
            circle.y, circle.vy, mouse_y, spring_constant, damping_factor
        )
    else:# only gravity will affect
        circle.vy += GravConst #calculation of gravity
        circle.x += circle.vx
        circle.y += circle.vy
    
    #applying the spring motion to all the shapes, square drawn by offsetting the vertices by some pixel from the central pixel
    circle2.x, circle2.vx = spring_motion(
        circle2.x, circle2.vx, circle.x - 100, spring_constant, damping_factor
    )
    circle2.y, circle2.vy = spring_motion(
        circle2.y, circle2.vy, circle.y - 100, spring_constant, damping_factor
    )

    circle3.x, circle3.vx = spring_motion(
        circle3.x, circle3.vx, circle.x + 100, spring_constant, damping_factor
    )
    circle3.y, circle3.vy = spring_motion(
        circle3.y, circle3.vy, circle.y - 100, spring_constant, damping_factor
    )

    circle4.x, circle4.vx = spring_motion(
        circle4.x, circle4.vx, circle.x - 100, spring_constant, damping_factor
    )
    circle4.y, circle4.vy = spring_motion(
        circle4.y, circle4.vy, circle.y + 100, spring_constant, damping_factor
    )

    circle5.x, circle5.vx = spring_motion(
        circle5.x, circle5.vx, circle.x + 100, spring_constant, damping_factor
    )
    circle5.y, circle5.vy = spring_motion(
        circle5.y, circle5.vy, circle.y + 100, spring_constant, damping_factor
    )



    screen.fill(Background_color)
    
    #for the color changing effect with velocity
    h = abs(circle.vy/100)
    h = h%1
    l,s=0.5,1
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    VelocityColor  = (int(r * 255), int(g * 255), int(b * 255))
    
    for c1, c2 in zip(
        [circle5, circle2, circle3, circle4], [circle3, circle4, circle2, circle5]
    ):
        pygame.draw.line(screen, VelocityColor, (c1.x, c1.y), (c2.x, c2.y), 2) #drawing the edges of the square

    for c1 in [circle5, circle2, circle3, circle4]:
        c1.vy += GravConst*4
        c1.y += c1.vy
        pygame.draw.line(screen, VelocityColor, (c1.x, c1.y), (circle.x, circle.y), 2) #drawing the lines from the central to the vertices
        
    pygame.draw.circle(screen, VelocityColor, (circle.x, circle.y), circle.radius)
    pygame.draw.circle(screen, circle2.color, (circle2.x, circle2.y), circle.radius)
    pygame.draw.circle(screen, circle3.color, (circle3.x, circle3.y), circle.radius)
    pygame.draw.circle(screen, circle4.color, (circle4.x, circle4.y), circle.radius)
    pygame.draw.circle(screen, circle5.color, (circle5.x, circle5.y), circle.radius)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()

# adding center of mass
# also instead of making a seperate calculation for the x and the y coordinate why not make the function calcluate the spring force on the both sides of the line if length of line == current length, but i think its more memory consuming
