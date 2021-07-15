import pygame
from pygame.locals import *
import random as rd


class FlappyBird:
    def __init__(self):
        self.initialisation()
        self.fenetre = pygame.display.set_mode((400, 512))
        self.playing = False
        self.base = pygame.image.load("imgs/base.png")
        self.bg = pygame.image.load("imgs/bg.png")
        self.aileH = pygame.image.load("imgs/bird1.png")
        self.aileN = pygame.image.load("imgs/bird2.png")
        self.aileB = pygame.image.load("imgs/bird3.png")
        self.obstacleBas = pygame.transform.scale2x(pygame.image.load("imgs/pipe1.png"))
        self.rectObstacleBas = []
        self.obstacleHaut = pygame.transform.scale2x(pygame.image.load("imgs/pipe2.png"))
        self.rectObstacleHaut = []
        self.reduce = -5  # vitesse de defilement de la base  et des obstacles
        self.rectListeBase = []
        self.time = pygame.time.Clock()
        self.seqVoler = 2
        self.seqObstacle = 1
        self.birdPos = self.aileH.get_rect()
        self.birdPos.center = (200, 200)
        self.graviter = 4  # gravité que subit l'oiseau
        self.vide = 80  # représente l'espace entre l'obstacle haut et bas lors de l'affichage
        self.randPos = [-10, -20, -5]
        self.score = 0
        self.listeScore = ["imgs/score/0.png", "imgs/score/1.png", "imgs/score/2.png", "imgs/score/3.png",
                           "imgs/score/4.png", "imgs/score/5.png", "imgs/score/6.png", "imgs/score/7.png",
                           "imgs/score/8.png", "imgs/score/9.png"]
        self.listeScoreBlocker = [False, False, False]
        self.titre = ["imgs/titre/gameover.png", "imgs/titre/get ready.png", "imgs/titre/nom.png"]
        self.btn = ["imgs/boutons/pause.png", "imgs/boutons/play.png", "imgs/boutons/scoreBtn.png",
                    "imgs/boutons/startBtn.png", "imgs/boutons/tap.png"]

    def initialisation(self):
        pygame.init()

    def initialisationObstacle(self):
        distance = 450
        for k in range(3):
            rect = self.obstacleHaut.get_rect()
            rect.x = self.obstacleHaut.get_rect().x + distance
            rect1 = self.obstacleBas.get_rect()
            rect1.x = self.obstacleBas.get_rect().x + distance
            self.rectObstacleHaut.append(rect)
            self.rectObstacleBas.append(rect1)
            distance += 200

        for l in range(3):
            rect = self.base.get_rect()
            rect.y = 400
            self.rectListeBase.append(rect)

    def initialisationScore(self):
        id = 0
        for k in self.listeScore:
            self.listeScore[id] = pygame.transform.scale(pygame.image.load(k), (27, 35))
            id += 1

    def initialisationTitreEtBtn(self):
        id = 0
        for k in self.titre:
            self.titre[id] = pygame.transform.scale2x(pygame.image.load(k))
            id += 1
        id = 0
        for l in self.btn:
            self.btn[id] = pygame.transform.scale2x(pygame.image.load(l))
            id += 1

    def afficherScore(self):
        dixieme = self.score // 10  # pour recuperer la première valeur
        if dixieme == 0:
            rect = self.listeScore[self.score].get_rect()
            rect.center = (200, 50)
            self.fenetre.blit(self.listeScore[self.score], rect)
        else:
            rect = self.listeScore[dixieme].get_rect()
            rect.center = (180, 50)
            self.fenetre.blit(self.listeScore[dixieme], rect)
            unite = self.score % 10
            rect1 = self.listeScore[unite].get_rect()
            rect1.center = (205, 50)
            self.fenetre.blit(self.listeScore[unite], rect1)

    def afficherFond(self):
        self.fenetre.blit(self.bg, (0, 0))
        self.fenetre.blit(self.bg, (288, 0))

    def afficherBase(self, position, color):
        self.fenetre.blit(self.base, position)
        # pygame.draw.rect(self.fenetre, color, position, 1)

    def generateNumber(self):
        return -(rd.randint(80, 100))

    def basePositionInitial(self):
        self.rectListeBase[1].left = self.rectListeBase[0].right
        self.rectListeBase[2].left = self.rectListeBase[1].right

    def afficherObstacleHaut(self, index):
        self.rectObstacleHaut[index].y = self.randPos[index]
        self.fenetre.blit(self.obstacleHaut, self.rectObstacleHaut[index])

    def afficherObstacleBas(self, index):
        # depend de l'affichage de obstacle haut <rect>
        self.rectObstacleBas[index] = self.obstacleBas.get_rect()
        self.rectObstacleBas[index].x = self.rectObstacleHaut[index].x
        self.rectObstacleBas[index].y = self.rectObstacleHaut[index].bottom + self.vide
        self.fenetre.blit(self.obstacleBas, self.rectObstacleBas[index])
        # pygame.draw.rect(self.fenetre, (255, 0, 0), self.rectObstacleBas[index], 1)

    def defilerObstacle(self):
        for k in range(3):
            self.rectObstacleHaut[k].left += self.reduce
            if self.rectObstacleHaut[k].right <= 0:
                self.randPos[k] = self.generateNumber()
                self.rectObstacleHaut[k].left = 570
            self.afficherObstacleHaut(k)
            self.afficherObstacleBas(k)

    def augmenterScore(self):
        # False False False
        # print(self.listeScoreBlocker)
        # print(self.rectObstacleHaut)
        i = 0
        while i < 3:
            if self.rectObstacleHaut[i].right < self.birdPos.left:
                if self.listeScoreBlocker[i] == False:
                    self.score += 1
                    self.listeScoreBlocker[i] = True
            if self.rectObstacleHaut[i].right >= 520:
                self.listeScoreBlocker[i] = False
            i += 1

    def defilerBase(self):
        # l'idee est de dessiné la meme image a des endroits différents
        for k in range(3):
            if self.rectListeBase[k].right <= 0 and k == 0:
                self.rectListeBase[k].left = self.rectListeBase[k + 2].right
            if self.rectListeBase[k].right <= 0 and k == 1:
                self.rectListeBase[k].left = self.rectListeBase[k - 1].right
            if self.rectListeBase[k].right <= 0 and k == 2:
                self.rectListeBase[k].left = self.rectListeBase[k - 1].right
            self.rectListeBase[k].left += self.reduce
            self.afficherBase(self.rectListeBase[k], (255, 0, 0))

    def sequence_voler(self):
        self.limite()
        if self.seqVoler > 3:
            self.seqVoler = 1
        if self.seqVoler == 1:
            rect = self.aileH.get_rect()
            # rect.center = self.birdPos
            self.vole(self.aileH, self.birdPos)
        elif self.seqVoler == 2:
            rect = self.aileN.get_rect()
            # rect.center = self.birdPos
            self.vole(self.aileN, self.birdPos)
        elif self.seqVoler == 3:
            rect = self.aileB.get_rect()
            # rect.center = self.birdPos
            self.vole(self.aileB, self.birdPos)

        self.seqVoler += 1

    def vole(self, image, position):
        self.fenetre.blit(image, position)
        # pygame.draw.rect(self.fenetre, (255, 0, 0), position, 2)

    def limite(self):
        # gestion de la limite de l'ecran
        if self.birdPos.bottom > 400:
            self.birdPos.bottom = 400
        if self.birdPos.top <= 0:
            self.birdPos.top = 0

    def collision(self):
        i = 0
        while i < 3:
            if self.birdPos.colliderect(self.rectObstacleHaut[i]) == True or self.birdPos.colliderect(
                    self.rectObstacleBas[i]) == True:
                print("self.playing = False")
                # Menu game over et retry
            i += 1

    def afficherTitre(self):
        # self.fenetre.blit(self.titre[1], (50, 50))
        self.fenetre.blit(self.titre[2], (100, 100))

    def afficherBtn(self):
        play_rect = self.btn[1].get_rect()
        play_rect.center = (200, 300)
        self.fenetre.blit(self.btn[1], play_rect)

    def Menu(self):
        self.initialisationObstacle()
        self.basePositionInitial()
        self.initialisationScore()
        self.initialisationTitreEtBtn()
        while not self.playing:
            # on affiche le menu
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playing = False
                else:
                    if event.type == MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0] == 1:
                            self.playing = True
                            # self.birdPos.bottom -= 0
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            self.playing = True
                            # self.birdPos.bottom -= 35
                            # print("saut")
                        if event.key == K_p:
                            print("Menu pause")
            self.time.tick(20)
            self.fenetre.fill((255, 255, 255))
            self.afficherFond()
            self.sequence_voler()
            self.defilerBase()
            self.afficherTitre()
            pygame.display.update()
        flappy.run()

    def pause(self):
        # implementation du menu pause
        print("pause")
        boucle = True
        while boucle:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playing = False
                    boucle = False
                else:
                    if event.type == KEYDOWN or MOUSEBUTTONDOWN:
                        if event.key == K_p:
                            print('appui sur p')
                        if pygame.mouse.get_pressed()[0] == 1:
                            boucle = False
                            # on continue le jeu s'il tape sur clique gauche
                            # boucle = False
                        if event.key == K_SPACE:
                            boucle = False
            self.time.tick(20)
            self.fenetre.blit(self.btn[0], (0,0))
            self.fenetre.blit(self.btn[1], (30,0))
            pygame.display.flip()

    def run(self):
        # self.initialisationObstacle()
        # self.basePositionInitial()
        # self.initialisationScore()
        # self.initialisationTitreEtBtn()
        while self.playing:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.playing = False
                else:
                    if event.type == MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[0] == 1:
                            self.birdPos.bottom -= 35
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            self.birdPos.bottom -= 35
                            # print("saut")
                        if event.key == K_p:
                            print("Menu pause")
                            self.pause()
            self.birdPos.bottom += self.graviter
            self.time.tick(20)
            self.fenetre.fill((255, 255, 255))
            self.afficherFond()
            self.sequence_voler()
            self.defilerObstacle()
            self.defilerBase()
            self.augmenterScore()
            self.afficherScore()
            self.collision()
            pygame.display.update()


if __name__ == '__main__':
    flappy = FlappyBird()
    flappy.playing = False
    flappy.Menu()

