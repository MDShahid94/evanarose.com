import pygame
import pymunk
import pymunk.pygame_util
import time
import random
import sys
import argparse
from pygame.locals import *
from math import sqrt, sin, cos, pi
from functools import reduce
import ast

start_time = time.time()

# Parse arguments

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--visualization', dest="vis", type=bool,
                    default=False,
                    help='visualization on/off')

parser.add_argument('-np', '--num-players', dest="num_players", type=int,
                    default=2,
                    help='1 Player or 2 Player')

parser.add_argument('-c', '--color', dest="color", type=str,
                    default="Black",
                    help='Legal color to pocket')

parser.add_argument('-rr', '--', dest="render_rate", type=int,
                    default=20,
                    help='Render every nth frame')

parser.add_argument('-rs', '--random-seed', dest="rng", type=int,
                    default=0,
                    help='Random Seed')

parser.add_argument('-log', '--log', dest="log", type=str,
                    default="log.txt",
                    help='Name of logfile')

args = parser.parse_args()
vis = args.vis
num_players = args.num_players
color = args.color
render_rate = args.render_rate
random.seed(args.rng)
log = args.log

# Global Variables


STATIC = 1  # Velocity below which an object is considered to be static
MIN_FORCE = 15000  # Min Force to hit the striker
MAX_FORCE = 30000  # Max force to hit the striker
TIME_STEP = 14.0  # Step size for pymunk
TICKS_LIMIT = 3000  # Max ticks to consider

BOARD_SIZE = 800
BOARD_DAMPING = 0.95  # Velocity fall per second

BOARD_WALLS_SIZE = BOARD_SIZE * 2 / 75
WALLS_ELASTICITY = 0.7

X_PADDING_LEFT = 155
X_PADDING_RIGHT = 645
P1_STRIKER_POS = 108
P2_STRIKER_POS = BOARD_SIZE - 108
MIN_ANGLE = -45
MAX_ANGLE = 225

COIN_MASS = 1
COIN_RADIUS = 15.01
COIN_ELASTICITY = 0.5

STRIKER_MASS = 2.8
STRIKER_RADIUS = 20.6
STRIKER_ELASTICITY = 0.7

POCKET_RADIUS = 22.51

STRIKER_COLOR = [65, 125, 212, 255]
POCKET_COLOR = [0, 0, 0, 255]
BLACK_COIN_COLOR = [43, 43, 43, 255]
WHITE_COIN_COLOR = [169, 121, 47, 255]
RED_COIN_COLOR = [169, 53, 53, 255]
BOARD_WALLS_COLOR = [56, 32, 12, 255]
BOARD_COLOR = [242, 209, 158, 255]

# Array of initial coin positions
INITIAL = [(399, 368), (437, 420), (372, 424), (336, 366), (400, 332), (463, 367), (464, 434), (400, 468), (337, 433),
           (400, 400), (401, 432), (363, 380), (428, 376), (370, 350), (430, 346),
           (470, 400), (430, 450), (370, 454), (330, 400)]

INITIAL_STATE = {'White_Locations': [(399, 368), (437, 420), (372, 424), (336, 366), (400, 332),
                                     (463, 367), (464, 434), (400, 468), (337, 433)],
                 'Red_Location': [(400, 400)],
                 'Score': 0,
                 'Black_Locations': [(401, 432), (363, 380), (428, 376), (370, 350), (430, 346),
                                     (470, 400), (430, 450), (370, 454), (330, 400)]}


##########################################################################


def main():
    state = INITIAL_STATE
    turn = 0
    while len(state["Black_Locations"]) + len(state["White_Locations"]) + len(state["Red_Location"]) > 0:
        state = play(state)
        turn += 1
    last_msg = "Cleared Board in: " + str(turn) + " Turn. Realtime taken: " + str(time.time() - start_time)
    print(last_msg)
    logger(log, last_msg)


def play(state):
    while 1:
        prev_state = state
        action = new_action(state)

        space = pymunk.Space()
        init_space(space)
        pockets, striker = init_board(space, state, action)

        reward = scoring(space, pockets, striker, False)

        if reward > 0:
            playable, next_state = get_state(space)
            if playable:
                next_score = prev_state["Score"] + reward
                next_state["Score"] = next_score
                print(next_score)
                logger(log, str(action))
                if vis:
                    visualize(prev_state, action)
                return next_state


def visualize(state, action):
    pygame.init()
    clock = pygame.time.Clock()

    score = state["Score"]

    space = pymunk.Space()
    init_space(space)
    pockets, striker = init_board(space, state, action)

    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    background = BACKGROUND('use_layout.png', [0, 0])

    pygame.display.set_caption("Carom RL Simulation")
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks = 0
    while 1:
        if ticks % render_rate == 0:
            local_vis = True
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    sys.exit(0)
        else:
            local_vis = False

        ticks += 1

        if local_vis:
            screen.blit(background.image, background.rect)
            space.debug_draw(draw_options)

        score += scoring(space, pockets, striker, True)

        if local_vis:
            font = pygame.font.Font(None, 25)
            text = font.render("Score: " +
                               str(score), True, (220, 220, 220))
            screen.blit(text, (BOARD_SIZE / 2 - 40, 780, 0, 0))

            text = font.render("Time Elapsed: " +
                               str(round(time.time() - start_time, 2)), True, (50, 50, 50))
            screen.blit(text, (BOARD_SIZE / 3 + 57, 25, 0, 0))

            if ticks == 1:
                draw_arrow(screen, action[0], action[1], action[2])

            pygame.display.flip()
            if ticks == 1:
                time.sleep(1)
            clock.tick()

        if is_static(space) or ticks > TICKS_LIMIT:
            return


def scoring(space, pockets, striker, in_vis):
    reward = 0

    while 1:
        space.step(1 / TIME_STEP)

        for pocket in pockets:
            if dist(pocket.body.position, striker[0].position) < POCKET_RADIUS - STRIKER_RADIUS + (
                    STRIKER_RADIUS * 0.75):
                return 0

            for coin in space.shapes:
                if dist(pocket.body.position, coin.body.position) < POCKET_RADIUS - COIN_RADIUS + (COIN_RADIUS * 0.75):
                    if coin.color == BLACK_COIN_COLOR:
                        reward += 1
                        space.remove(coin, coin.body)
                    if coin.color == WHITE_COIN_COLOR:
                        reward += 1
                        space.remove(coin, coin.body)
                    if coin.color == RED_COIN_COLOR:
                        reward += 3
                        space.remove(coin, coin.body)

        if in_vis:
            return reward
        elif is_static(space):
            return reward


def get_state(space):
    new_state = {"Black_Locations": [], "White_Locations": [], "Red_Location": [], "Score": 0}
    for coin in space.shapes:
        if coin.color == BLACK_COIN_COLOR:
            new_state["Black_Locations"].append(coin.body.position)
        if coin.color == WHITE_COIN_COLOR:
            new_state["White_Locations"].append(coin.body.position)
        if coin.color == RED_COIN_COLOR:
            new_state["Red_Location"].append(coin.body.position)

    foul_queen = len(new_state["Black_Locations"]) == 0 and len(new_state["White_Locations"]) == 0 and len(
        new_state["Red_Location"]) > 0
    invalid_queen = len(new_state["Black_Locations"]) == 9 and len(
        new_state["White_Locations"]) == 9 and len(
        new_state["Red_Location"]) > 0

    playable = not (foul_queen or invalid_queen)
    return playable, new_state


def dist(p1, p2):
    return sqrt(pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2))


def is_static(space):
    for shape in space.shapes:
        if abs(shape.body.velocity[0]) > STATIC or abs(shape.body.velocity[1]) > STATIC:
            return False
    return True


def new_action(state):
    action = [validate_position(random.randrange(X_PADDING_LEFT, X_PADDING_RIGHT), state),
              (random.randrange(MIN_ANGLE, MAX_ANGLE) * pi) / 180.0, random.randrange(MIN_FORCE, MAX_FORCE)]
    return action


def validate_position(position, state):
    if num_players == 1:
        y_pos = P1_STRIKER_POS
    else:
        y_pos = P2_STRIKER_POS

    tmp_state = state.copy()

    try:
        del tmp_state["Score"]
    except KeyError:
        pass
    tmp_state = list(tmp_state.values())
    tmp_state = reduce(lambda x, y: x + y, tmp_state)

    check = 0
    fuse = 10

    while check == 0 and fuse > 0:
        fuse -= 1
        check = 1
        for coin in tmp_state:
            if dist((position, y_pos), coin) < STRIKER_RADIUS + COIN_RADIUS:
                check = 0
                position = random.randrange(X_PADDING_LEFT, X_PADDING_RIGHT)

    return position


def init_space(space):
    space.damping = BOARD_DAMPING
    space.threads = 2


def init_board(space, state, action):
    state = ast.literal_eval(str(state).replace("Vec2d", ""))

    init_walls(space)
    pockets = init_pockets(space)
    init_coins(space, state["Black_Locations"], state["White_Locations"], state["Red_Location"])
    striker = init_striker(space, action)
    return pockets, striker


def init_walls(space):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    walls = [pymunk.Segment(body, (0, 0), (0, BOARD_SIZE), BOARD_WALLS_SIZE),
             pymunk.Segment(body, (0, 0), (BOARD_SIZE, 0), BOARD_WALLS_SIZE),
             pymunk.Segment(
                 body, (BOARD_SIZE, BOARD_SIZE), (BOARD_SIZE, 0), BOARD_WALLS_SIZE),
             pymunk.Segment(
                 body, (BOARD_SIZE, BOARD_SIZE), (0, BOARD_SIZE), BOARD_WALLS_SIZE)
             ]
    for wall in walls:
        wall.color = BOARD_WALLS_COLOR
        wall.elasticity = WALLS_ELASTICITY
    space.add(walls[0], walls[1], walls[2], walls[3], body)


def init_pockets(space):
    pockets = []
    for i in [(44.1, 44.1), (755.9, 44.1), (755.9, 755.9), (44.1, 755.9)]:
        inertia = pymunk.moment_for_circle(0.1, 0, POCKET_RADIUS, (0, 0))
        body = pymunk.Body(0.1, inertia)
        body.position = i
        shape = pymunk.Circle(body, POCKET_RADIUS, (0, 0))
        shape.color = POCKET_COLOR
        shape.collision_type = 2
        shape.filter = pymunk.ShapeFilter(categories=0b1000)
        space.add(body, shape)
        pockets.append(shape)
        del body
        del shape
    return pockets


def init_striker(space, action):
    passthrough = pymunk.Segment(space.static_body, (0, 0), (0, 0), 5)
    passthrough.collision_type = 2
    passthrough.filter = pymunk.ShapeFilter(categories=0b1000)

    inertia = pymunk.moment_for_circle(STRIKER_MASS, 0, STRIKER_RADIUS, (0, 0))
    body = pymunk.Body(STRIKER_MASS, inertia)
    if num_players == 1:
        body.position = (action[0], P1_STRIKER_POS)
    else:
        body.position = (action[0], P2_STRIKER_POS)
    body.apply_force_at_world_point((cos(action[1]) * action[2], sin(action[1]) * action[2]),
                                    body.position + (STRIKER_RADIUS * 0, STRIKER_RADIUS * 0))
    shape = pymunk.Circle(body, STRIKER_RADIUS, (0, 0))
    shape.elasticity = STRIKER_ELASTICITY
    shape.color = STRIKER_COLOR

    mask = pymunk.ShapeFilter.ALL_MASKS() ^ passthrough.filter.categories

    sf = pymunk.ShapeFilter(mask=mask)
    shape.filter = sf
    shape.collision_type = 2
    space.add(body, shape)
    return [body, shape]


def init_coins(space, coords_black, coords_white, coord_red):
    coins = []
    inertia = pymunk.moment_for_circle(COIN_MASS, 0, COIN_RADIUS, (0, 0))

    passthrough = pymunk.Segment(space.static_body, (0, 0), (0, 0), 5)
    passthrough.collision_type = 2
    passthrough.filter = pymunk.ShapeFilter(categories=0b1000)

    for coord in coords_black:
        body = pymunk.Body(COIN_MASS, inertia)
        body.position = coord
        shape = pymunk.Circle(body, COIN_RADIUS, (0, 0))
        shape.elasticity = COIN_ELASTICITY
        shape.color = BLACK_COIN_COLOR

        mask = pymunk.ShapeFilter.ALL_MASKS() ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf
        shape.collision_type = 2

        space.add(body, shape)
        coins.append(shape)
        del body
        del shape

    for coord in coords_white:
        body = pymunk.Body(COIN_MASS, inertia)
        body.position = coord
        shape = pymunk.Circle(body, COIN_RADIUS, (0, 0))
        shape.elasticity = COIN_ELASTICITY
        shape.color = WHITE_COIN_COLOR

        mask = pymunk.ShapeFilter.ALL_MASKS() ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf
        shape.collision_type = 2

        space.add(body, shape)
        coins.append(shape)
        del body
        del shape

    for coord in coord_red:
        body = pymunk.Body(COIN_MASS, inertia)
        body.position = coord
        shape = pymunk.Circle(body, COIN_RADIUS, (0, 0))
        shape.elasticity = COIN_ELASTICITY
        shape.color = RED_COIN_COLOR
        mask = pymunk.ShapeFilter.ALL_MASKS() ^ passthrough.filter.categories

        sf = pymunk.ShapeFilter(mask=mask)
        shape.filter = sf
        shape.collision_type = 2

        space.add(body, shape)
        coins.append(shape)
        del body
        del shape


def draw_arrow(screen, position, angle, force):
    length = STRIKER_RADIUS + force / 500.0
    startpos_x = position
    if num_players == 1:
        startpos_y = P1_STRIKER_POS
    else:
        startpos_y = P2_STRIKER_POS
    endpos_x = startpos_x + cos(angle) * length
    endpos_y = startpos_y - length * sin(angle)
    pygame.draw.line(
        screen, (50, 255, 50), (endpos_x, endpos_y), (startpos_x, startpos_y), 3)
    pygame.draw.circle(screen, (50, 255, 50),
                       (int(endpos_x), int(endpos_y)), 5)


def logger(logs, msg):
    f = open("logs/" + logs, "a")
    f.write(msg + "\n")
    f.close()


class BACKGROUND(pygame.sprite.Sprite):

    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


if __name__ == "__main__":
    main()
