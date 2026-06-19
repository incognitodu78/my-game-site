from pygame.constants import MOUSEBUTTONDOWN
import pygame
import random
import sys, os

pygame.init()


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


clock = pygame.time.Clock()


class Jeu:
    def __init__(self):
        pygame.display.set_caption("Cursed village")
        pygame.display.set_icon(pygame.image.load(resource_path("Assets/Image/Icone.png")))

        pygame.mixer.init()
        pygame.mixer.music.load(resource_path("Assets/Sons/Ap musique.mp3"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.reboot = False
        self.gagner = False

        self.dev = True
        self.enjeu = False
        self.azerty = False
        self.qwerty = False
        self.keys = None
        self.sans_bordure = False
        self.choix_utilisateur = False
        self.spawn_mob = True
        self.histoire_start = False
        self.quitter = False
        self.arret_en_court = False
        self.reset = False
        self.bloque_haut = False
        self.bloque_bas = False
        self.bloque_droite = False
        self.bloque_gauche = False

        self.vitesse = 3
        self.x = -1360
        self.y = -2500
        self.pos_joueur_x = 0
        self.pos_joueur_y = 0
        self.temps = 0
        self.vie_joueur = 100

        self.positions_bat_x = [2200, 1450, 1650, 2150, 2400, 1700]
        self.positions_bat_y = [2000, 1800, 1500, 1700, 1800, 2000]

        self.positions_mob_x = []
        self.positions_mob_y = []

        self.ap_lobby = pygame.image.load(resource_path("Assets/Image/Ap_lobby.png"))
        self.ap_ath = pygame.image.load(resource_path("Assets/Image/Ap_ATH.png"))
        self.ap = pygame.image.load(resource_path("Assets/Image/Arrière plan.png"))
        self.batiment = pygame.image.load(resource_path("Assets/Image/Batiment 1.png"))
        self.btn_play = pygame.image.load(resource_path("Assets/Image/Bouton play.png"))
        self.btn_azerty = pygame.image.load(resource_path("Assets/Image/Bouton azerty.png"))
        self.btn_qwerty = pygame.image.load(resource_path("Assets/Image/Bouton qwerty.png"))
        self.case_princip = pygame.image.load(resource_path("Assets/Image/Case principale.png"))
        self.case_util = pygame.image.load(resource_path("Assets/Image/Case utilisé.png"))
        self.joueur_devant = pygame.image.load(resource_path("Assets/Image/Personnage principale devant.png"))
        self.joueur_derriere = pygame.image.load(resource_path("Assets/Image/Personnage principale derrière.png"))
        self.joueur_gauche = pygame.image.load(resource_path("Assets/Image/Personnage principale gauche.png"))
        self.joueur_droite = pygame.image.load(resource_path("Assets/Image/Personnage principale droite.png"))
        self.pnj = pygame.image.load(resource_path("Assets/Image/PNJ 1.png"))
        self.btn_quitter = pygame.image.load(resource_path("Assets/Image/Bouton quitter.png"))
        self.btn_continuer = pygame.image.load(resource_path("Assets/Image/Bouton continuer.png"))
        self.btn_parametre = pygame.image.load(resource_path("Assets/Image/btn paramètre.png"))

        self.son_degat_joueur = pygame.mixer.Sound(resource_path("Assets/Sons/pv joueur.wav"))
        self.son_gagnant = pygame.mixer.Sound(resource_path("Assets/Sons/winner.wav"))
        self.son_monstre_dead = pygame.mixer.Sound(resource_path("Assets/Sons/kill slime.wav"))
        self.son_game_over = pygame.mixer.Sound(resource_path("Assets/Sons/Game over.wav"))
        self.son_attaque_joueur = pygame.mixer.Sound(resource_path("Assets/Sons/attaque joueur.wav"))

        self.joueur = self.joueur_derriere

        self.btn_play_hitbox = self.btn_play.get_rect()
        self.btn_play_hitbox.topleft = (400, 550)

        self.btn_azerty_hitbox = self.btn_azerty.get_rect()
        self.btn_azerty_hitbox.topleft = (100, 250)

        self.btn_qwerty_hitbox = self.btn_qwerty.get_rect()
        self.btn_qwerty_hitbox.topleft = (700, 250)

        self.btn_quitter_oui_hitbox = self.btn_quitter.get_rect()
        self.btn_quitter_oui_hitbox.topleft = (400, 300)

        self.btn_quitter_non_hitbox = self.btn_continuer.get_rect()
        self.btn_quitter_non_hitbox.topleft = (650, 300)

        self.canvas = pygame.display.set_mode((1280, 720))
        self.canvas.blit(self.ap_lobby, (0, 0))

        self.hitbox_batiment = self.batiment.get_rect()


        self.hitbox_joueur = self.joueur_devant.get_rect()
        self.hitbox_joueur.topleft = (600, 400)

    def cliquer_bouton(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.quitter = True

        if self.quitter:
            police_ecriture = pygame.font.Font(None, 70)
            texte = police_ecriture.render("Voulez-vous quitter ?", True, (255, 255, 255))
            self.canvas.fill((0, 0, 0))
            self.canvas.blit(texte, (400, 100))
            self.canvas.blit(self.btn_quitter, (400, 300))
            self.canvas.blit(self.btn_continuer, (650, 300))

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_quitter_oui_hitbox.collidepoint(event.pos):
                    self.arret_en_court = True
                elif self.btn_quitter_non_hitbox.collidepoint(event.pos):
                    self.quitter = False

            return

        if self.reset:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if self.btn_quitter_oui_hitbox.collidepoint(event.pos):
                    self.arret_en_court = True
                elif self.btn_quitter_non_hitbox.collidepoint(event.pos):
                    pass
                    # self.reboot = True    // activer ceci pour activer l'option de reset

            return

        if not self.quitter:
            if not self.enjeu and not self.choix_utilisateur:
                self.canvas.blit(self.btn_play, (400, 550))

                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.btn_play_hitbox.collidepoint(event.pos):
                            self.canvas.fill((0,0,0))
                            self.canvas.blit(self.btn_azerty, (100, 250))
                            self.canvas.blit(self.btn_qwerty, (700, 250))
                            self.choix_utilisateur = True

            if self.choix_utilisateur and not self.enjeu:
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            try:
                                if self.btn_azerty_hitbox.collidepoint(event.pos):
                                    self.azerty = True
                                    self.qwerty = False
                                if self.btn_qwerty_hitbox.collidepoint(event.pos):
                                    self.azerty = False
                                    self.qwerty = True
                            except AttributeError:
                                return
                            finally:
                                if self.azerty or self.qwerty:
                                    self.enjeu = True


    def changer_ap(self):
        if self.enjeu and not self.quitter:
            self.canvas.blit(self.ap, (self.x, self.y))
            self.canvas.blit(self.joueur, (600, 400))

    def deplacement(self):
        self.keys = pygame.key.get_pressed()

        if self.enjeu and not self.quitter and not self.histoire_start:

            if self.azerty:

                if not self.sans_bordure and self.x < -403 and not self.bloque_gauche:
                    if self.keys[pygame.K_q]:
                        self.x += self.vitesse
                        self.pos_joueur_x += self.vitesse
                        self.joueur = self.joueur_gauche
                if self.sans_bordure:
                    if self.keys[pygame.K_q]:
                        self.x += self.vitesse
                        self.pos_joueur_x += self.vitesse

                if not self.sans_bordure and self.x > -2390 and not self.bloque_droite:
                    if self.keys[pygame.K_d]:
                        self.x -= self.vitesse
                        self.pos_joueur_x -= self.vitesse
                        self.joueur = self.joueur_droite
                if self.sans_bordure:
                    if self.keys[pygame.K_d]:
                        self.x -= self.vitesse
                        self.pos_joueur_x -= self.vitesse

                if not self.sans_bordure and self.y < -602 and not self.bloque_haut:
                    if self.keys[pygame.K_z]:
                        self.y += self.vitesse
                        self.pos_joueur_y += self.vitesse
                        self.joueur = self.joueur_derriere
                if self.sans_bordure:
                    if self.keys[pygame.K_z]:
                        self.y += self.vitesse
                        self.pos_joueur_y += self.vitesse

                if not self.sans_bordure and self.y > -2550 and not self.bloque_bas:
                    if self.keys[pygame.K_s]:
                        self.y -= self.vitesse
                        self.pos_joueur_y -= self.vitesse
                        self.joueur = self.joueur_devant
                if self.sans_bordure:
                    if self.keys[pygame.K_s]:
                        self.y -= self.vitesse
                        self.pos_joueur_y -= self.vitesse


            elif self.qwerty:
                if not self.sans_bordure and self.x < -403 and not self.bloque_gauche:
                    if self.keys[pygame.K_a]:
                        self.x += self.vitesse
                        self.pos_joueur_x += self.vitesse
                        self.joueur = self.joueur_gauche
                if self.sans_bordure:
                    if self.keys[pygame.K_a]:
                        self.x += self.vitesse
                        self.pos_joueur_x += self.vitesse

                if not self.sans_bordure and self.x > -2380 and not self.bloque_droite:
                    if self.keys[pygame.K_d]:
                        self.x -= self.vitesse
                        self.pos_joueur_x -= self.vitesse
                        self.joueur = self.joueur_droite
                if self.sans_bordure:
                    if self.keys[pygame.K_d]:
                        self.x -= self.vitesse
                        self.pos_joueur_x -= self.vitesse

                if not self.sans_bordure and self.y < -533 and not self.bloque_haut:
                    if self.keys[pygame.K_w]:
                        self.y += self.vitesse
                        self.pos_joueur_y += self.vitesse
                        self.joueur = self.joueur_derriere
                if self.sans_bordure:
                    if self.keys[pygame.K_w]:
                        self.y += self.vitesse
                        self.pos_joueur_y += self.vitesse

                if not self.sans_bordure and self.y > -2550 and not self.bloque_bas:
                    if self.keys[pygame.K_s]:
                        self.y -= self.vitesse
                        self.pos_joueur_y -= self.vitesse
                        self.joueur = self.joueur_devant
                if self.sans_bordure:
                    if self.keys[pygame.K_s]:
                        self.y -= self.vitesse
                        self.pos_joueur_y -= self.vitesse

    def afficher_batiment(self):
        if self.enjeu and not self.quitter:
            for i in range(len(self.positions_bat_x)):
                self.canvas.blit(self.batiment, (self.positions_bat_x[i] + self.x,
                                                 self.positions_bat_y[i] + self.y))

    def cheat_code(self):
        self.pos_joueur_x = self.x + 1360
        self.pos_joueur_y = self.y + 2500
        if self.enjeu and not self.quitter:
            if self.dev:

                if self.keys[pygame.K_c]:
                    self.vitesse += 20
                    print("Débogage : vitesse augmenté")
                    pygame.time.wait(200)
                if self.keys[pygame.K_v] and self.vitesse > 3:
                    self.vitesse = 3
                    print("Débogage : vitesse réinitialisé")
                    pygame.time.wait(200)

                if self.keys[pygame.K_n]:
                    self.sans_bordure = True
                    print("Débogage : bordure désactivé")
                if self.keys[pygame.K_m]:
                    self.sans_bordure = False
                    print("Débogage : bordure activé")

                if self.keys[pygame.K_l]:
                    print(self.pos_joueur_x, self.pos_joueur_y, "//", self.x, self.y)
                    pygame.time.wait(200)

                if self.keys[pygame.K_x]:
                    self.vie_joueur = 100

    def loot(self):
        data = pygame.font.Font(None, 45)
        text = data.render(("HP : " + str(self.vie_joueur)), True, (255,255,255))
        if self.enjeu and not self.quitter and not self.histoire_start:
            self.canvas.blit(self.ap_ath, (5,550))

            self.canvas.blit(self.case_princip, (1150, 600))
            self.canvas.blit(self.case_princip, (1000, 600))
            self.canvas.blit(self.case_princip, (850, 600))
            self.canvas.blit(self.case_util, (700, 600))

            self.canvas.fill((0, 0, 0), (70, 605, 510, 60))
            self.canvas.fill((255,0,0), (75,610,self.vie_joueur * 5,50))
            self.canvas.blit(text, (80, 620))

    def collision_bat(self):
        if self.enjeu and not self.quitter:
            self.bloque_haut = False
            self.bloque_bas = False
            self.bloque_droite = False
            self.bloque_gauche = False

            for i in range(len(self.positions_bat_x)):

                self.hitbox_batiment.topleft = (self.positions_bat_x[i] + self.x, self.positions_bat_y[i] + self.y)

                dx_left = abs(self.hitbox_joueur.right - self.hitbox_batiment.left)
                dx_right = abs(self.hitbox_joueur.left - self.hitbox_batiment.right)
                dy_top = abs(self.hitbox_joueur.bottom - self.hitbox_batiment.top)
                dy_bottom = abs(self.hitbox_joueur.top - self.hitbox_batiment.bottom)

                min_collision = min(dx_left, dx_right, dy_top, dy_bottom)

                if self.hitbox_batiment.colliderect(self.hitbox_joueur):

                    if min_collision == dx_left:
                        self.bloque_droite = True

                    elif min_collision == dx_right:
                        self.bloque_gauche = True

                    elif min_collision == dy_top:
                        self.bloque_bas = True

                    elif min_collision == dy_bottom:
                        self.bloque_haut = True




    def game_over(self):
        data = pygame.font.Font(None, 100)
        texte = data.render("GAME OVER", True, (255,255,255))
        if self.vie_joueur <= 0:
            self.enjeu = False
            self.canvas.fill((0,0,0))
            self.canvas.blit(texte, (400, 150))
            self.canvas.blit(self.btn_quitter, (400, 300))
            self.canvas.blit(self.btn_continuer, (650, 300))
            if not self.reset:
                self.son_game_over.play()
            self.reset = True

    def winner(self):
        if self.enjeu and not self.quitter and self.gagner:
            data = pygame.font.Font(None, 300)
            text = data.render("YOU WIN!", True, (255,255,255))
            self.canvas.blit(text, (140, 290))
            self.son_gagnant.play()
            self.enjeu = False



class Histoire(Jeu):
    def __init__(self):
        super().__init__() #permet d'appeler la classe parente
        self.choix_lettre = "Press 'ENTER' to continue"
        self.info_texte = "Salutation voyageur"
        self.level_hist = 0
        self.debug_click = 0
        self.hist_att = False
        self.fin_debut_hist = False
        self.hist_fin = False
        self.discution_pnj = False
        self.ap_indic = pygame.image.load(resource_path("Assets/Image/Ap_indic.png"))
        self.ap_texte = pygame.image.load(resource_path("Assets/Image/Ap_texte.png"))

    def debut_hist(self):
        police_ecriture = pygame.font.Font(None, 48)
        police_ecriture2 = pygame.font.Font(None, 38)
        texte1 = police_ecriture.render("PRESS 'ENTER'", True, (255,255,255))

        if not self.quitter:
            self.canvas.blit(self.pnj, (2150 + self.x, 1925 + self.y))

        if self.enjeu and not self.quitter:
            if -1414 >= self.x >= -1690 and -1627 <= self.y <= -1399 and not self.histoire_start:
                self.canvas.blit(texte1, (1000, 50))
                self.canvas.blit(self.ap_indic, (975, 20))

                if self.keys[pygame.K_RETURN] and not self.histoire_start and self.debug_click >= 1:
                    self.discution_pnj = True
                    self.histoire_start = True
                    self.debug_click = 0

            if self.histoire_start and not self.hist_fin:
                texte2 = police_ecriture.render(self.info_texte, True, (255, 255, 255))
                texte1 = police_ecriture2.render(self.choix_lettre, True, (255,255,255))
                self.canvas.blit(self.ap_texte, (45, 500))
                self.canvas.blit(texte1, (450, 505))
                self.canvas.blit(texte2, (100, 585))
                if self.keys[pygame.K_RETURN] and self.level_hist == 0 and self.debug_click >= 1:
                    self.info_texte = "Le village va mal"
                    self.level_hist = 1
                    self.debug_click = 0
                if self.keys[pygame.K_RETURN] and self.level_hist == 1 and self.debug_click >= 1:
                    self.info_texte = "Aide nous"
                    self.level_hist = 2
                    self.debug_click = 0
                if self.keys[pygame.K_RETURN] and self.level_hist == 2 and self.debug_click >= 1:
                    self.info_texte = "Ramène-moi 5 âme de slime ou plus"
                    self.level_hist = 3
                    self.debug_click = 0
                if self.keys[pygame.K_RETURN] and self.level_hist == 3 and self.debug_click >= 1:
                    self.info_texte = "Cette épée te sera utile"
                    self.choix_lettre =  "Press 'ENTER' to finish"
                    self.level_hist = 4
                    self.debug_click = 0
                if self.keys[pygame.K_RETURN] and self.level_hist == 4 and self.debug_click >= 1:
                    self.info_texte = "Salutation voyageur"
                    self.histoire_start = False
                    self.hist_att = True
                    self.level_hist = 0
                    self.fin_debut_hist = True
                    self.discution_pnj = False
                    self.debug_click = 0

            elif self.hist_fin:
                if self.discution_pnj:
                    self.gagner = True

class Monstres(Histoire):
    def __init__(self):
        super().__init__()

        self.att_monstre = pygame.image.load(resource_path("Assets/Image/Particule attaque slime.png"))
        self.monstre_gauche = pygame.image.load(resource_path("Assets/Image/Monstre gauche.png"))
        self.monstre_droite = pygame.image.load(resource_path("Assets/Image/Monstre droite.png"))
        self.ame_monstre = pygame.image.load(resource_path("Assets/Image/Ame monstre.png"))
        self.arme = pygame.image.load(resource_path("Assets/Image/épée.png"))
        self.monstre = self.monstre_droite

        self.coord_gauche = None
        self.coord_droite = None
        self.coord_bas = None
        self.coord_haut = None

        self.degat = False

        self.deplacement_attaque = 0
        self.direction_att = 0
        self.degat_frame_debug = 0
        self.coldown_attaque_joueur = 0
        self.ame_collecte = 0

        self.vie_monstre = [100, 100, 100, 100, 100, 100]
        self.monstre_dead = []

        self.hitbox_monstre = self.monstre_droite.get_rect()

        self.hitbox_attaque_monstre_gauche = self.att_monstre.get_rect()
        self.hitbox_attaque_monstre_droite = self.att_monstre.get_rect()
        self.hitbox_attaque_monstre_bas = self.att_monstre.get_rect()
        self.hitbox_attaque_monstre_haut = self.att_monstre.get_rect()

    def spawn_monstre(self):
        if self.enjeu and not self.quitter:
            if self.spawn_mob:
                for x in range(0, 6):
                    aleatoire_x = random.randint(1000, 2850)
                    aleatoire_y = random.randint(1000, 2700)
                    self.positions_mob_x.append(aleatoire_x)
                    self.positions_mob_y.append(aleatoire_y)
                self.spawn_mob = False
            for i in range(len(self.positions_mob_x)):
                self.canvas.blit(self.monstre, (self.positions_mob_x[i] + self.x,
                                                 self.positions_mob_y[i] + self.y))

    def suivie_monstres(self):
        if self.hist_att:
            if self.temps <= 2 and not self.quitter:
                self.positions_mob_x = [x +3 for x in self.positions_mob_x]
                self.monstre = self.monstre_droite
            if  5 <= self.temps < 7 and not self.quitter:
                self.positions_mob_x = [x -3 for x in self.positions_mob_x]
                self.monstre = self.monstre_gauche
            if self.temps == 9 and not self.quitter:
                self.temps = 1

    def attaque_monstre(self):
        pos_j_x = 600 - self.x
        pos_j_y = 400 - self.y
        if self.hist_att and not self.quitter:
            for i in range(len(self.positions_mob_x)):
                gauche = False
                droite = False
                haut = False
                bas = False
                if pos_j_x >= self.positions_mob_x[i] -200:
                    gauche = True
                if pos_j_x <= self.positions_mob_x[i] +200:
                    droite = True
                if pos_j_y >= self.positions_mob_y[i] -200:
                    haut = True
                if pos_j_y <= self.positions_mob_y[i] +200:
                    bas = True

                if gauche and droite and haut and bas:
                    self.deplacement_attaque = 0


                    if self.deplacement_attaque == 0:
                        direction_gauche = pos_j_x - (pos_j_x - self.direction_att)
                        pos_gauche = direction_gauche + self.x
                        self.coord_gauche = self.positions_mob_x[i] + pos_gauche, self.positions_mob_y[i] + self.y
                        self.canvas.blit(self.att_monstre, (self.coord_gauche[0], self.coord_gauche[1]))
                        self.degat = True

                        direction_droite = pos_j_x - (pos_j_x + self.direction_att)
                        pos_droite = direction_droite + self.x
                        self.coord_droite = self.positions_mob_x[i] + pos_droite, self.positions_mob_y[i] + self.y
                        self.canvas.blit(self.att_monstre, (self.coord_droite[0], self.coord_droite[1]))
                        self.degat = True

                        direction_bas = pos_j_y - (pos_j_y + self.direction_att)
                        pos_bas = direction_bas + self.y
                        self.coord_bas = self.positions_mob_x[i] + self.x, self.positions_mob_y[i] + pos_bas
                        self.canvas.blit(self.att_monstre, (self.coord_bas[0], self.coord_bas[1]))
                        self.degat = True

                        direction_haut = pos_j_y - (pos_j_y - self.direction_att)
                        pos_haut = direction_haut + self.y
                        self.coord_haut = self.positions_mob_x[i] + self.x, self.positions_mob_y[i] + pos_haut
                        self.canvas.blit(self.att_monstre, (self.coord_haut[0], self.coord_haut[1]))
                        self.degat = True

                    self.direction_att += 3
                    if self.deplacement_attaque == 0.5:
                        self.deplacement_attaque = 0
                    if self.direction_att > 200:
                        self.direction_att = 0

    def degat_attaque(self):
        if self.hist_att and not self.quitter:
            if self.degat:
                self.hitbox_attaque_monstre_gauche.topleft = (self.coord_gauche[0], self.coord_gauche[1])
                self.hitbox_attaque_monstre_droite.topleft = (self.coord_droite[0], self.coord_droite[1])
                self.hitbox_attaque_monstre_bas.topleft = (self.coord_bas[0], self.coord_bas[1])
                self.hitbox_attaque_monstre_haut.topleft = (self.coord_haut[0], self.coord_haut[1])

                hitboxs = [
                    self.hitbox_attaque_monstre_gauche,
                    self.hitbox_attaque_monstre_droite,
                    self.hitbox_attaque_monstre_bas,
                    self.hitbox_attaque_monstre_haut
                ]
                for hitbox in hitboxs:
                    if self.degat_frame_debug > 1:
                        if self.hitbox_joueur.colliderect(hitbox):
                            self.vie_joueur -= 30
                            self.degat_frame_debug = 0
                            if not self.reset:
                                self.son_degat_joueur.play()
                            break
                        if self.hitbox_joueur.colliderect(hitbox):
                            self.vie_joueur -= 30
                            self.degat_frame_debug = 0
                            if not self.reset:
                                self.son_degat_joueur.play()
                            break
                        if self.hitbox_joueur.colliderect(hitbox):
                            self.vie_joueur -= 30
                            self.degat_frame_debug = 0
                            if not self.reset:
                                self.son_degat_joueur.play()
                            break
                        if self.hitbox_joueur.colliderect(hitbox):
                            self.vie_joueur -= 30
                            self.degat_frame_debug = 0
                            if not self.reset:
                                self.son_degat_joueur.play()
                            break

    def attaque_joueur(self):
        pos_joueur_x = 600 - self.x
        pos_joueur_y = 400 - self.y
        if self.hist_att and not self.quitter:

            for x in range(len(self.positions_mob_x)):
                self.canvas.fill((186, 0, 0), (self.positions_mob_x[x] + 5 + self.x,
                                               self.positions_mob_y[x] + self.y, self.vie_monstre[x] / 2, 5))

                gauche = False
                droite = False
                haut = False
                bas = False
                if pos_joueur_x >= self.positions_mob_x[x] - 75:
                    gauche = True
                if pos_joueur_x <= self.positions_mob_x[x] + 75:
                    droite = True
                if pos_joueur_y >= self.positions_mob_y[x] - 75:
                    haut = True
                if pos_joueur_y <= self.positions_mob_y[x] + 75:
                    bas = True

                if gauche and droite and haut and bas:
                    data = pygame.font.Font(None, 35)
                    text = data.render("Press 'E' for attack", False, (255, 255, 255))
                    self.canvas.blit(text, (900,100))
                    if self.keys[pygame.K_e]:
                        if self.coldown_attaque_joueur >= 0.5:
                            self.vie_monstre[x] -= 20
                            self.son_attaque_joueur.play()
                            self.coldown_attaque_joueur = 0
                if self.vie_monstre[x] <= 0:
                    del self.vie_monstre[x]
                    del self.positions_mob_x[x]
                    del self.positions_mob_y[x]
                    self.ame_collecte += 1
                    self.son_monstre_dead.play()
                    self.monstre_dead.append(self.ame_collecte)
                    break

    def ame_collector(self):
        arme = pygame.transform.smoothscale(self.arme, (20, 20))
        arme_inverse_x = pygame.transform.flip(arme, True, False)
        arme_inverse_y = pygame.transform.flip(arme, False, True)
        chiffre = len(self.monstre_dead)
        data = pygame.font.Font(None, 35)
        text = data.render(str(chiffre), False, (0, 0, 0))
        if self.enjeu and not self.quitter and not self.gagner:
            if len(self.monstre_dead) > 0:
                self.canvas.blit(self.ame_monstre, (855, 600))
                self.canvas.blit(text, (910, 650))

            if self.ame_collecte >= 5:
                self.hist_fin = True

            if self.fin_debut_hist and not self.gagner:
                self.canvas.blit(self.arme, (715, 610))
                if self.joueur == self.joueur_droite:
                    self.canvas.blit(arme, (620, 420))
                if self.joueur == self.joueur_gauche:
                    self.canvas.blit(arme_inverse_x, (585, 420))
                if self.joueur == self.joueur_devant:
                    self.canvas.blit(arme_inverse_y, (605, 430))
                if self.joueur == self.joueur_derriere:
                    self.canvas.blit(arme, (640, 415))


    def reset_world(self):
        self.reset = False
        self.reboot = False
        self.enjeu = True

        self.histoire_start = False
        self.quitter = False
        self.arret_en_court = False

        self.joueur = self.joueur_derriere

        self.vitesse = 3
        self.x = -1360
        self.y = -2500
        self.pos_joueur_x = 0
        self.pos_joueur_y = 0
        self.temps = 0
        self.vie_joueur = 100

        self.positions_bat_x = [2200, 1450, 1650, 2150, 2400, 1700]
        self.positions_bat_y = [2000, 1800, 1500, 1700, 1800, 2000]

        self.choix_lettre = "Press '->' to continue"
        self.info_texte = "Salutation voyageur"
        self.level_hist = 0
        self.hist_att = False

        self.monstre = self.monstre_droite

        self.coord_gauche = None
        self.coord_droite = None
        self.coord_bas = None
        self.coord_haut = None

        self.degat = False

        self.deplacement_attaque = 0
        self.direction_att = 0
        self.degat_frame_debug = 0


start_time = pygame.time.get_ticks()
jeu = Monstres()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        jeu.cliquer_bouton(event)
    jeu.deplacement()
    jeu.changer_ap()
    jeu.afficher_batiment()
    jeu.suivie_monstres()
    jeu.collision_bat()
    jeu.spawn_monstre()
    jeu.attaque_monstre()
    jeu.degat_attaque()
    jeu.attaque_joueur()
    jeu.loot()
    jeu.ame_collector()
    jeu.debut_hist()
    jeu.game_over()
    jeu.winner()
    #jeu.reset_world()  fonction pas à jour, variable manquante
    jeu.cheat_code()

    if jeu.arret_en_court:
        running = False

    if jeu.reboot:
        jeu.reset_world()

    if jeu.enjeu and not jeu.quitter:
        curent_time = pygame.time.get_ticks()
        if curent_time - start_time >= 1000:
            jeu.temps += 1
            jeu.deplacement_attaque += 1
            jeu.degat_frame_debug += 1
            jeu.coldown_attaque_joueur += 1
            jeu.debug_click += 1
            start_time = curent_time

    if jeu.reset:
        pygame.mixer.music.stop()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
