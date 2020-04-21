import pygame
import os
import sys
import time
import threading
import random


class Array:
    def __init__(self, *args):
        self.elements = args
        self.highlighted = set({})
        self.result = -1

    def search(self, element, array=None, start=0):
        if array is None:
            array = self.elements

        for i, n in enumerate(array):
            self.highlighted.add(i + start)

        time.sleep(0.5)

        if len(array) == 1:
            if element == array[0]:
                return 0 + start
            else:
                return -1

        middle = len(array) // 2

        left = array[:middle]
        right = array[middle:]

        self.highlighted.clear()

        result = self.search(element, left, 0 + start)
        if result != -1:
            self.result = result
            return result

        result = self.search(element, right, middle + start)
        if result != -1:
            self.result = result
            return result

        self.highlighted.clear()
        return -1

    def __str__(self):
        return str(self.elements)

    def draw(self):
        win.fill((255, 255, 255))
        font = pygame.font.SysFont('calibri', 30)

        x = 5
        y = 200
        for i, element in enumerate(self.elements):
            colour = (0, 0, 0)
            if i in self.highlighted:
                colour = (0, 255, 0)
            if i == self.result:
                colour = (0, 0, 255)

            text = str(element)
            text = font.render(text, True, (255, 255, 255))
            textRect = text.get_rect(center=(x + 50, y + 50))

            pygame.draw.rect(win, colour, (x, y, 100, 100))
            win.blit(text, textRect)

            x += 110


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()

win = pygame.display.set_mode((1100, 600))
pygame.display.set_caption('Binary Search')

numbers = Array(*(random.randint(0, 100) for _ in range(10)))

search = threading.Thread(target=numbers.search, args=(numbers.elements[3],))
search.start()

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    numbers.draw()
    pygame.display.update()
