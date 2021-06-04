import pygame, sys
from pygame.locals import *

pygame.init()
display = pygame.display.set_mode([400, 400])
pygame.display.set_caption('trial one')
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()