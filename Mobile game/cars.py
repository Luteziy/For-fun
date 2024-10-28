import pygame
from pygame.locals import *
import random

pygame.init()

width = 500
height = 500
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Race')

#colors
gray = (100, 100, 100)
green= (76, 208, 56)
red = (200, 0, 0)
yellow = (255, 232, 0)
white = (255, 255, 255)

gameover = False
speed = 2
score = 0

#markers size
marker_width = 10
marker_height = 50

#road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)

# x coordinates of lanes
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# for animation move
lane_marker_move_y = 0


class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y ):
        pygame.sprite.Sprite.__init__(self)

        # scale the image don so it fits in the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('Player_s_car.png')
        super().__init__(image, x, y)

# player star conditions
player_x = 250
player_y = 400

#create player
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y)
player_group.add(player)

# load random cars
image_filenames = ['car_1.png']
vehicle_images = []
for image_filenames in image_filenames:
    image = pygame.image.load(image_filenames)
    vehicle_images.append(image)

#spirite group for vehicle_images
vehicle_group = pygame.sprite.Group()

boom = pygame.image.load('boom.png')
boom_rect = boom.get_rect()

#game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type ==QUIT:
            running = False

        #move left and right
        if event.type == KEYDOWN:

            if event.key == K_a and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            elif event.key == K_d and player.rect.center[0] < right_lane:
                player.rect.x += 100

            # check collision
            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):

                    gameover = True

                    # place car next to other car
                    if event.key == K_a:
                        player.rect.left = vehicle.rect.right
                        boom_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    elif event.key == K_d:
                        player.rect.right = vehicle.rect.left
                        boom_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1]) / 2]



    #draw grass
    screen.fill(green)

    pygame.draw.rect(screen, gray, road)

    #draw edge markers
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)


    # draw the lane markers
    lane_marker_move_y += speed *2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0
    for y in range(marker_height * -2, height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane +45, y + lane_marker_move_y, marker_width, marker_height))


    # draw player car
    player_group.draw(screen)

    #add up to two cars
    if len(vehicle_group) < 2:
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False

        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / - 2)
            vehicle_group.add(vehicle)

    #move
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        #remove from screen end
        if vehicle.rect.top >= height:
            vehicle.kill()

            #add score
            score += 1

            if score > 0 and score % 5 == 0:
                speed += 1

    vehicle_group.draw(screen)

    font = pygame.font.Font(pygame.font.get_default_font(), 16)
    text = font.render('Score: ' + str(score), True, white)
    text_rect = text.get_rect()
    text_rect.center = (50, 450)
    screen.blit(text, text_rect)

    #
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        gameover = True
        boom_rect.center = [player.rect.center[0], player.rect.top]

    # display gameover text
    if gameover:
        screen.blit(boom, boom_rect)

        pygame.draw.rect(screen, red, (0, 50, width, 100))
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render('Game Over! Try again? Enter Y or N', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width / 2, 100)
        screen.blit(text, text_rect)


    pygame.display.update()

    while gameover:

        clock.tick(fps)

        for event in pygame.event.get():

            if event.type == QUIT:
                gameover = False
                running = False

            # yes or no
            if event.type == KEYDOWN:
                if event.key == K_y:
                    gameover = False
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                elif event.key == K_n:
                    gameover = False
                    running = False

pygame.quit()
