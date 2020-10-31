import pygame
from collections import deque
from priority_queue import PQ

pygame.time.Clock().tick(10)

pygame.init()

DISPLAY_SIZE = 500

rows = 25

gap = DISPLAY_SIZE // rows

screen = pygame.display.set_mode((DISPLAY_SIZE, DISPLAY_SIZE))

screen.fill((255, 255, 255))


class Node:
    def __init__(self, i, j, gap, rows):
        self.i = i
        self.j = j
        self.gap = gap
        self.x = i * gap
        self.y = j * gap
        self.state = 0
        self.parent = None
        self.neighbours = []
        if i:
            self.neighbours.append((i - 1, j))
        if j:
            self.neighbours.append((i, j - 1))
        if i != rows - 1:
            self.neighbours.append((i + 1, j))
            # if j != rows - 1:
            #     self.neighbours.append((i + 1, j + 1))
            # if j:
            #     self.neighbours.append((i + 1, j - 1))

        if j != rows - 1:
            self.neighbours.append((i, j + 1))
            # if i != rows - 1:
            #     self.neighbours.append((i + 1, j + 1))
            # if i:
            #     self.neighbours.append((i - 1, j + 1))

    def draw(self, screen, state=0):
        self.state = state if state or self.state else -1
        pygame.draw.rect(screen, cmap[self.state],
                         (self.x, self.y, self.gap, self.gap))
        pygame.display.update()


def draw_gridlines(gap, screen):
    for i in range(1, rows):
        pygame.draw.line(screen, BLACK, (0, i * gap), (DISPLAY_SIZE, i * gap))
        for j in range(1, rows):
            pygame.draw.line(screen, BLACK, (j * gap, 0),
                             (j * gap, DISPLAY_SIZE))
    pygame.display.update()


def pos_to_index(pos, gap):
    x, y = pos
    return (x // gap), (y // gap)


RED = (255, 61, 0)
GREEN = (29, 233, 182)
BLUE = (0, 176, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BROWN = (121, 85, 72)
VISIT_COLOR = (187, 222, 251)

cmap = {0: WHITE, -1: BROWN, 1: GREEN, 2: RED,
        3: VISIT_COLOR, 'CURRENT': (255, 234, 0), 'PATH': (234, 255, 0), 'TO_VISIT': (123, 200, 210)}

mat = [[Node(i, j, gap, rows) for j in range(rows)] for i in range(rows)]


def dfs(screen, grid, start, end, gap):
    stk = [start]
    while stk:
        a, b = stk.pop()
        top = grid[a][b]

        # top.draw(screen, 'CURRENT')
        # draw_gridlines(gap, screen)

        for (i, j) in grid[a][b].neighbours:
            if grid[i][j].state == 2:
                while top.parent:
                    grid[top.i][top.j].draw(screen, 'PATH')
                    top = top.parent
                    draw_gridlines(gap, screen)
                return

            if not grid[i][j].state:
                grid[i][j].parent = top
                stk.append((i, j))
                grid[i][j].draw(screen, 'TO_VISIT')
                draw_gridlines(gap, screen)

        top.draw(screen, 3 if (a, b) != start else 1)
        draw_gridlines(gap, screen)


def bfs(screen, grid, start, end, gap):
    q = deque([start])
    while q:
        a, b = q.popleft()
        top = grid[a][b]

        top.draw(screen, 'CURRENT')
        draw_gridlines(gap, screen)

        for (i, j) in grid[a][b].neighbours:
            if (i, j) == end:
                while top.parent:
                    grid[top.i][top.j].draw(screen, 'PATH')
                    top = top.parent
                    draw_gridlines(gap, screen)
                return

            if not grid[i][j].state:
                grid[i][j].parent = top
                q.append((i, j))

                grid[i][j].draw(screen, 'TO_VISIT')
                draw_gridlines(gap, screen)

        top.draw(screen, 3 if (a, b) != start else 1)
        draw_gridlines(gap, screen)


class AstarCarrier:
    poss_dis_left = 0
    dis_till_now = 0
    total_dis = 0

    def __init__(self, xy, par=None):
        self.xy = xy
        self.parent = par

    def redo(self, other):
        self.poss_dis_left = other.poss_dis_left
        self.dis_till_now = other.dis_till_now
        self.total_dis = other.total_dis
        self.parent = other.parent

    def __eq__(self, other):
        return self.total_dis == other.total_dis

    def __lt__(self, other):
        return self.total_dis < other.total_dis

    def __gt__(self, other):
        return self.total_dis > other.total_dis


def astar(screen, grid, start, end, gap):
    to_visit = [AstarCarrier((start[0], start[1]))]
    astar_node_map = {}
    astar_node_map[start] = to_visit[0]
    to_visit = PQ(to_visit, lambda x: x.xy)
    visited = set()

    while to_visit:
        top = to_visit.pop()
        visited.add(top.xy)

        if top.xy == end:
            return

        x, y = top.xy
        top_spot = grid[x][y]

        grid[x][y].draw(screen, 'CURRENT')
        draw_gridlines(gap, screen)

        for i in top_spot.neighbours:
            if i == end:
                while top.parent:
                    grid[top.xy[0]][top.xy[1]].draw(screen, 'PATH')
                    top = top.parent
                    draw_gridlines(gap, screen)
                return

            if not grid[i[0]][i[1]].state and i not in visited:
                n = AstarCarrier(i, top)
                n.dis_till_now = top.dis_till_now + 1
                # n.dis_till_now = abs(start[0] - i[0]) + abs(start[1] - i[1])
                n.poss_dis_left = abs(end[0] - i[0])**2 + abs(end[1] - i[1])**2
                # n.poss_dis_left = abs(end[0] - i[0]) + abs(end[1] - i[1])
                n.total_dis = n.dis_till_now + n.poss_dis_left
                to_visit.push(n)
                astar_node_map[i] = n

                grid[i[0]][i[1]].draw(screen, 'TO_VISIT')
                draw_gridlines(gap, screen)

        grid[x][y].draw(screen, 3 if (x, y) != start else 1)
        draw_gridlines(gap, screen)

    return


def end_game(screen, DISPLAY_SIZE):

    screen.fill((255, 255, 255))
    x, y = DISPLAY_SIZE // 2, DISPLAY_SIZE // 3
    ft = pygame.font.Font('freesansbold.ttf', 32)
    ft = ft.render('Finished !!', True, BLACK)
    fr = ft.get_rect()
    fr.center = (x, y)
    screen.blit(ft, fr)
    x, y = DISPLAY_SIZE // 4, DISPLAY_SIZE // 3 * 2
    reset_text = pygame.font.Font('freesansbold.ttf', 32)
    reset_text = reset_text.render('Reset !!', True, BLACK)
    reset = reset_text.get_rect()
    reset.center = (x, y)
    screen.blit(reset_text, reset)
    x, y = 3 * DISPLAY_SIZE // 4, DISPLAY_SIZE // 3 * 2
    quit_text = pygame.font.Font('freesansbold.ttf', 32)
    quit_text = quit_text.render('Quit ?', True, BLACK)
    quit = quit_text.get_rect()
    quit.center = (x, y)
    screen.blit(quit_text, quit)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                p = pygame.mouse.get_pos()
                if quit.collidepoint(p):
                    pygame.quit()
                if reset.collidepoint(p):
                    return False


def delay(t):
    exit_time = pygame.time.get_ticks() + t
    while pygame.time.get_ticks() < exit_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


while True:

    selection = None

    for i in mat:
        for j in i:
            j.state = 0
            j.parent = None

    screen.fill((255, 255, 255))

    while not selection:
        text_x = DISPLAY_SIZE // 2
        text_y = [(DISPLAY_SIZE // 5) * i for i in range(1, 5)]

        # text_rect = [(text_x-50 , y-50 , 50 , 50) for y in text_y]
        text = ['Choose Algorithm ?', 'DFS', 'BFS', 'A*']
        a = []
        for t, y in zip(text, text_y):
            font = pygame.font.Font('freesansbold.ttf', 32)
            text = font.render(t, True, BLACK)
            textRect = text.get_rect()
            textRect.center = (text_x, y)
            a.append((text, textRect))

        for i in a:
            screen.blit(i[0], i[1])
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed()[0]:
                p = pygame.mouse.get_pos()
                for i, v in enumerate(a):
                    if v[1].collidepoint(p):
                        selection = i
                        break

    screen.fill((255, 255, 255))
    delay(200)
    LAST = (-1, -1)
    start, end = None, None
    playing = True

    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            draw_gridlines(gap, screen)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and start and end:
                if selection == 1:
                    dfs(screen, mat, start, end, gap)
                elif selection == 2:
                    bfs(screen, mat, start, end, gap)
                elif selection == 3:
                    astar(screen, mat, start, end, gap)

                delay(1200)
                playing = end_game(screen, DISPLAY_SIZE)
                break

            elif pygame.mouse.get_pressed()[0]:
                x, y = pos_to_index(pygame.mouse.get_pos(), gap)
                if LAST == (x, y):
                    continue
                LAST = (x, y)
                n, s = mat[x][y], 0
                if start == (x, y):
                    start = None
                elif end == (x, y):
                    end = None
                elif not start:
                    start, s = (x, y), 1
                elif not end:
                    end, s = (x, y), 2
                n.draw(screen, s)

            # pygame.display.update()
