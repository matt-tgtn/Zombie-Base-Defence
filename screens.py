import pygame
from pygame.locals import KEYDOWN, K_ESCAPE

class Screens:
    def __init__(self, size):
        self.size = size

    def gameIntro(self):
        pygame.init()
        running = 1
        clock = pygame.time.Clock()

        font = pygame.font.Font(None, 40)
        font2 = pygame.font.Font(None, 30)
        yellow = 255,255,0
        hum = 2, 81, 76
        
        #TODO: Make this code screen size relative and cleaner

        screen = pygame.display.set_mode(self.size)
        screen.fill([135,206,250])

        ren = font.render("Welcome to Zombie Base Defence!", 1, yellow)
        screen.blit(ren, (20,120))

        ren = font2.render("v0.0.1", 1, hum)
        screen.blit(ren, (240, 200))
        ren = font2.render("Press any key to continue.", 1, hum)
        screen.blit(ren, (140, 400))
        ren = font2.render("ESC to quit.", 1, hum)
        screen.blit(ren, (140, 450))

        while running:
            clock.tick(55)
            pygame.display.flip()
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        raise SystemExit()
                    else:
                        return

    def roundIntro(self, level):
        pygame.init()
        running = 1
        clock = pygame.time.Clock()

        font = pygame.font.Font(None, 60)
        font2 = pygame.font.Font(None, 40)
        yellow = 255,255,0
        hum = 2, 81, 76


        screen = pygame.display.set_mode(self.size)
        screen.fill([135,206,250])

        ren = font.render("Round %s"%(level), 1, yellow)
        screen.blit(ren, (140,120))

        ren = font2.render("Get ready...", 1, hum)
        screen.blit(ren, (150, 200))
        ren = font2.render("Press any key to continue.", 1, hum)
        screen.blit(ren, (100, 400))


        while running:
            clock.tick(55)
            pygame.display.flip()
            pygame.event.pump()

            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        raise SystemExit()
                    else:
                        return

