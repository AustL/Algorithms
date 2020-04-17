import math
import os
import threading
import time
import pygame
import sys

from collections import deque


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start = False
        self.end = False
        self.obstacle = False
        self.parent = None

        self.gCost = math.inf
        self.hCost = math.inf
        self.fCost = math.inf

    def calculateNeighbours(self, parent):
        for node in self.getNeighbours():
            node.calculateCosts(parent)

    def calculateCosts(self, parent):
        gCost = self.distanceTo(parent) + parent.gCost
        hCost = self.distanceTo(grid.endNode)
        fCost = gCost + hCost

        self.gCost = min(gCost, self.gCost)
        self.hCost = min(hCost, self.hCost)

        self.fCost = min(fCost, self.fCost)

        if fCost == self.fCost:
            self.parent = parent

        grid.open.add(self)

    def distanceTo(self, other):
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)

        return abs(dx - dy) * 10 + min(dx, dy) * 14

    def getNeighbours(self):
        neighbours = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == j == 0:
                    continue
                x = self.x + i
                y = self.y + j

                if 0 <= x < grid.width and 0 <= y < grid.height:
                    node = grid.getNodeAt(x, y)
                    if not node.obstacle and node not in grid.closed:
                        neighbours.append(node)

        return neighbours

    def __repr__(self):
        return f'({self.x}, {self.y})'

    def __lt__(self, other):
        if self.fCost < other.fCost:
            return True

        elif self.fCost == other.fCost:
            return self.hCost < other.hCost

        return False

    def contains(self, x, y):
        return (0 < x - (self.x * (BORDER + NODE_WIDTH) + BORDER) < NODE_WIDTH and
                0 < y - (self.y * (BORDER + NODE_WIDTH) + BORDER) < NODE_WIDTH)

    def draw(self, colour):
        x, y = self.x * (BORDER + NODE_WIDTH) + BORDER, self.y * (BORDER + NODE_WIDTH) + BORDER
        pygame.draw.rect(win, colour, (x, y, NODE_WIDTH, NODE_WIDTH))

        if self.fCost != math.inf:
            text = str(self.fCost)
            text = pygame.font.SysFont('calibri', FONT_SIZE).render(text, True, (0, 0, 0))
            textRect = text.get_rect(center=(x + NODE_WIDTH // 2, y + NODE_WIDTH // 2))

            win.blit(text, textRect)


class Grid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.nodes = [[Node(x, y) for x in range(width)] for y in range(height)]

        self.startNode = None
        self.endNode = None
        self.closed = set({})
        self.open = set({})
        self.path = set({})

    def setObstacle(self, *args):
        for x, y in args:
            self.getNodeAt(x, y).obstacle = True

    def setStartNode(self, node):
        self.startNode = node
        node.start = True

    def removeStartNode(self):
        self.startNode.start = False
        self.startNode = None

    def setEndNode(self, node):
        self.endNode = node
        node.end = True

    def removeEndNode(self):
        self.endNode.end = False
        self.endNode = None

    def isReady(self):
        if not self.startNode or not self.endNode:
            return False
        return True

    def minOpenNode(self):
        lowest = None

        for node in self.open:
            if lowest is None:
                lowest = node
            elif node < lowest:
                lowest = node

        return lowest

    def getNodeAt(self, x, y):
        return self.nodes[y][x]

    def getNodeAtMouse(self, x, y):
        for row in self.nodes:
            for node in row:
                if node.contains(x, y):
                    return node

        return None

    def findPath(self):
        self.startNode.gCost = 0
        self.startNode.fCost = 0
        self.open.add(self.startNode)

        node = self.startNode
        node.calculateNeighbours(self.startNode)
        node = self.minOpenNode()

        while node != self.endNode:
            time.sleep(0.01)
            node.calculateNeighbours(node)
            node = self.minOpenNode()
            self.closed.add(node)
            self.open.remove(node)

        while node != self.startNode:
            self.path.add(node)
            node = node.parent

        self.path.add(node)

    def draw(self):
        win.fill((0, 0, 0))

        for row in self.nodes:
            for node in row:
                colour = (255, 255, 255)
                if node in grid.open:
                    colour = (0, 255, 0)
                if node in grid.closed:
                    colour = (255, 0, 0)
                if node in grid.path:
                    colour = (0, 0, 255)
                if node.obstacle:
                    colour = (0, 0, 0)
                if node.start or node.end:
                    colour = (0, 0, 255)
                node.draw(colour)


NODE_WIDTH = 24
BORDER = 2
GRID_WIDTH = 40
GRID_HEIGHT = 30
FONT_SIZE = 10

mouseDown = False
allowInput = True
selectionHistory = deque()

os.environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()
win = pygame.display.set_mode((GRID_WIDTH * (BORDER + NODE_WIDTH) + BORDER,
                               GRID_HEIGHT * (BORDER + NODE_WIDTH) + BORDER), pygame.RESIZABLE)
pygame.display.set_caption('A* Algorithm')

grid = Grid(GRID_WIDTH, GRID_HEIGHT)

path = threading.Thread(target=grid.findPath)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and allowInput:
            if event.button == pygame.BUTTON_LEFT:
                mouseDown = True

            elif event.button == pygame.BUTTON_RIGHT:
                selection = grid.getNodeAtMouse(*pygame.mouse.get_pos())
                if selection:
                    if not grid.startNode:
                        if selection not in selectionHistory:
                            selectionHistory.append(selection)
                        grid.setStartNode(selection)
                    elif not grid.endNode:
                        if selection not in selectionHistory:
                            selectionHistory.append(selection)
                        grid.setEndNode(selection)

        if event.type == pygame.MOUSEBUTTONUP and allowInput:
            mouseDown = False

        if event.type == pygame.KEYDOWN and allowInput:
            if event.key == pygame.K_RETURN:
                if grid.isReady():
                    path.start()
                    allowInput = False
            elif event.key == pygame.K_BACKSPACE:
                if selectionHistory:
                    lastSelection = selectionHistory.pop()
                    if lastSelection == grid.startNode:
                        grid.removeStartNode()
                    elif lastSelection == grid.endNode:
                        grid.removeEndNode()
                    lastSelection.obstacle = False

    if mouseDown and allowInput:
        selection = grid.getNodeAtMouse(*pygame.mouse.get_pos())
        if selection:
            if selection not in selectionHistory:
                selectionHistory.append(selection)
            selection.obstacle = True

    grid.draw()
    pygame.display.update()
