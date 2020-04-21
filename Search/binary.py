import pygame
import os
import sys
import time
import threading
import random


class Array:
    def __init__(self, *args):
        self.elements = sorted(args)
        self.length = len(args)
        self.newRows = [i for i in range(10, self.length, 10)]
        self.highlighted = set({})
        self.result = -1

    def search(self, element, array=None, start=0):
        if array is None:
            array = self.elements

        if len(array) == 0:
            return -1

        for i, n in enumerate(array):
            self.highlighted.add(i + start)

        time.sleep(0.5)

        middle = len(array) // 2

        self.highlighted.clear()

        if element == array[middle]:
            self.result = middle + start
            return middle
        elif element < array[middle]:
            return self.search(element, array[:middle], 0 + start)
        elif element > array[middle]:
            return self.search(element, array[middle + 1:], middle + start + 1)

        self.highlighted.clear()
        return -1

    def __str__(self):
        return str(self.elements)

    def draw(self):
        win.fill((255, 255, 255))
        font = pygame.font.SysFont('calibri', 30)

        x = 5
        y = 100
        for i, element in enumerate(self.elements):
            colour = (0, 0, 0)
            if i in self.highlighted:
                colour = (0, 255, 0)
            if i == self.result:
                colour = (0, 0, 255)

            if i in self.newRows:
                y += 150
                x = 5

            text = str(element)
            text = font.render(text, True, (255, 255, 255))
            textRect = text.get_rect(center=(x + 50, y + 50))

            pygame.draw.rect(win, colour, (x, y, 100, 100))
            win.blit(text, textRect)

            x += 110


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

win = pygame.display.set_mode((1100, 800))
pygame.display.set_caption('Binary Search')

numbers = Array(*(random.randint(0, 100) for _ in range(40)))

search = threading.Thread(target=numbers.search, args=(34,))
search.start()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    numbers.draw()
    pygame.display.update()
