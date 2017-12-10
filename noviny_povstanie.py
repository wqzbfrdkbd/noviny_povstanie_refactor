#!/usr/bin/env python
# -*- coding: utf-8 -*-
####################################################################
#
#   Zdroje:
#   Pozadie1: http://worldartsme.com/landscape-clipart.html#gal_post_5381_landscape-clipart-1.jpg
#   Pozadie_menu: http://clipartfreefor.com/files/1/12063_landscape-clipart.html
#
#   noviny_povstanie.py
#   1/2016 - 4/2016
#   Vytvorené pomocou Python 2.7.11 a pygame 1.9.2a0
#
#   Miroslav Dzuriš
#   SPŠE-PO IV.SA
#   2015 / 2016
#
#   Nečakaj žiadne špeciálne pravidlá, no priprav sa
#   na hordu nepriateľských novín
#   pripravených na boj s tebou vlnu za vlnou.
#   Tak  nezabudaj chrániť svoju základňu.
#   Máš 5 bodov zdravia a možnosti ako sa vylepšovať.   
#   No to neznamená, že to budeš mať ľahké...
#   Veľa šťastia. ;)
#
#   Ovládanie: šípka doľava a doprava - pohyb, medzerník - streľba
#   ESC - pauza, ENTER - potvrdenie položky v menu
#
#
####################################################################

# Importovanie modulov
import random
import os
import sys
import math

# Ak nie je modul pygame nainštalovaný vopred, tak je možnosť použiť lokálnu zálohu
#sys.path.append("moduly") 

# Importovanie modulu pygame
import pygame
from pygame.locals import *

# Globálne premenné
from konstanty import *

from skore import *
from noviny import *
from noviny_bonus import *
from noviny_boss import *
from tablet import *
from strela import *
from grafika import *
from zvuky import *
from menu import *

# Definovanie tried
# Každá trieda osbsahuje povinné premenné self.image a self.rect
# kvôli tomu, aby metóda Sprite mala čo, self.image(obrázok), a kam, self.rect(súradnice), vykresľovať


# Hlavná funkcia
def main():
    """
    Hlavná funkcia, je funkcia ktorá je volaná pri spustení hry.

    Načíta všetko potrebné a potom spustí hlavnú slučku,
    ktorá sa opakuje až kým neskončí hra
    """

    # Lokálne konštanty
    STAV_MENU_HLAVNE = 0    
    STAV_VYHRA = 1
    STAV_PREHRA = 2
    STAV_MENU_AKO = 3
    STAV_V_HRE = 4
    STAV_MENU_OBCHOD = 5
    STAV_MENU_PAUSE = 6


    # Načítanie modulu pygame
    pygame.init()

    # Nastavenie pozicie okna na horny kraj obrazovky
    #os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
    # Nastavenie pozicie okna na stred obrazovky
    os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'
    
    # Zadefinovanie lokálnych premenných
    # Základné hodnoty skóre
    skore_zivoty = 5
    skore_peniaze = 0
    skore_zivoty_zakladne = 15
    skore_uroven = 1
    skore_pod_uroven = 1
    skore_skore = 0

    # Boolean určujúci rozdielne vykresľovanie pre 1. úroveň
    uroven_1 = True

    # Premenné slúžiace na pohyb strel v hre
    cas_strely = 0
    cas_strely_noviny = 0
    # Premenné slúžiace na umiernený pohyb v menu medzi položkami
    oneskorenie_enter = 0
    oneskorenie_sipky = 0

    # Premenné určujúce základné hodnoty obchodu
    ob_tablet_rychlost = 9.0
    ob_tablet_rychlost_lvl = 1
    ob_strelba_rychlost = 300
    ob_strelba_rychlost_lvl = 1
    ob_strela_pocet = 1

    # Pomocné premenné pre bochod
    index_obchod = 0
    cena = 0
    meno = ""
    extra = ""
    obchod = False
    obchod_pokracuj = False

    # Premenná určujúca počiatočný počet životov Boss-ov
    boss_hp = 100

    # Načítanie skóra zo súbora
    try:
        HIGHSCORE = [line.rstrip('\n') for line in open('highscore.txt')]
    except IOError:
        highscore = file("highscore.txt", "w")
        highscore.write(str(0))
        highscore.close()
        HIGHSCORE = [line.rstrip('\n') for line in open('highscore.txt')]

    # Stav = čo sa aktuálne deje - čo je vykreslene na obrazovke
    stav = STAV_MENU_HLAVNE

    # Nastavenie základných parametrov pygame
    hodiny = pygame.time.Clock()
    obrazovka = pygame.display.set_mode((VELKOST_OKNA_X, VELKOST_OKNA_Y))#, pygame.FULLSCREEN
    pozadie = pygame.image.load('obrazky/pozadia/pozadie1.bmp').convert()

    # Prispôsobenie herného okna
    pygame.display.set_caption('Noviny - Povstanie')
    pygame.mouse.set_visible(0)
    ikona = pygame.image.load("ikona.ico")
    pygame.display.set_icon(ikona)

    # Vytvorenie skupín objektov a pridanie niektorých objektov do skupín
    noviny = pygame.sprite.RenderUpdates()
    noviny_ozbrojene = pygame.sprite.RenderUpdates()
    noviny_boss = pygame.sprite.RenderUpdates()
    noviny_bonus = pygame.sprite.RenderUpdates()

    skore = pygame.sprite.RenderUpdates()
    skore.add(Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))

    tablet = pygame.sprite.RenderUpdates()
    tablet.add(Tablet())
    
    strely = pygame.sprite.RenderUpdates()

    explozie = pygame.sprite.RenderUpdates()
    
    strely_noviny = pygame.sprite.RenderUpdates()

    hranica = pygame.sprite.RenderUpdates()
    hranica.add(Hranica())

    skore_bar = pygame.sprite.RenderUpdates()
    skore_bar.add(Skore_bar())
    
    # Načítanie triedy Zvuky
    zvuk = Zvuky()

    # Zadefinovanie všetkych položiek všetkých menu
    menu_hlavne = Menu()
    menu_hlavne.polozka_pridaj(u"Nová Hra")
    menu_hlavne.polozka_pridaj(u"Pokračovať v hre")
    menu_hlavne.polozka_pridaj(u"Ako Hrať")
    menu_hlavne.polozka_pridaj("Koniec")

    menu_ako = Menu()
    menu_ako.polozka_pridaj(u"Späť")
    menu_ako.riadok_pridaj(u"Ovládanie:")
    menu_ako.riadok_pridaj(u"pohyb: šípky doľava a doprava, streľba: medzerník")
    menu_ako.riadok_pridaj(u"pauza: ESCAPE, potvrdenie menu: ENTER")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Máš 5 životov tabletu a 15 životov základne.")
    menu_ako.riadok_pridaj(u"Môžeš sa vylepšovať, ak nato máš peniaze.")
    menu_ako.riadok_pridaj(u"V bonusových úrovniach čakaj nečakané ;).")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Cieľ hry:")
    menu_ako.riadok_pridaj(u"Zničiť všetky noviny!")
    menu_ako.riadok_pridaj("")
    menu_ako.riadok_pridaj(u"Najvyššie skóre: " + str(HIGHSCORE[0]))

    menu_obchod = Menu_Obchod()
    menu_obchod.polozka_pridaj(u"Kúpiť")
    menu_obchod.polozka_pridaj(u"Pokračovať v hre")

    menu_pause = Menu()
    menu_pause.polozka_pridaj(u"Pokračovať v hre")
    menu_pause.polozka_pridaj(u"Hlavné menu")

    menu_prehra = Menu()
    menu_prehra.riadok_pridaj("PREHRAL SI!")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj("")
    menu_prehra.riadok_pridaj(u"Stlač ESC pre návrat do menu.")

    menu_vyhra = Menu()
    menu_vyhra.riadok_pridaj("VYHRAL SI!")
    menu_vyhra.riadok_pridaj(u"Porazil si všetky noviny!")
    menu_vyhra.riadok_pridaj(u"Snáď už natrvalo!")
    menu_vyhra.riadok_pridaj(u"Stlač ESC pre návrat do menu.")

    # Hlavná slučka
    while 1:
        # Počíta čas od spustenia hry
        cas = pygame.time.get_ticks()

        stlacena_klavesa = pygame.key.get_pressed()

        # Načítanie vstupu
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()        

        if stav == STAV_V_HRE:
            
            if stlacena_klavesa[K_LEFT]:
                smer = 0
            elif stlacena_klavesa[K_RIGHT]:
                smer = 1
            else:
                smer = 3

            if stlacena_klavesa[K_SPACE]:
                vystrelene = 1
            else:
                vystrelene = 0

            if stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
                stav = STAV_MENU_PAUSE
                oneskorenie_enter = cas + 250

            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
               

            # Vystrelenie strely
            if vystrelene == 1 and cas > cas_strely:
                cas_strely = cas + ob_strelba_rychlost
                for p in range(0, ob_strela_pocet):
                  a, b, c, d = tablet_zoznam[0]
                  if p == 2:
                    strely.add(Strela((a+25-(1*20), b-29)))
                    break                  
                  strely.add(Strela((a+25+(p*20), b-29)))

                zvuk.strela_p()


            # Odstránenie všetkých objektov z obrazovky,
            # aby nedošlo k efektu, kedy objekty pri pohybe nechávajú
            # za sebou svojú vlastnú stopu
            tablet.clear(obrazovka, pozadie)
            noviny.clear(obrazovka, pozadie)
            noviny_ozbrojene.clear(obrazovka, pozadie)
            noviny_boss.clear(obrazovka, pozadie)
            noviny_bonus.clear(obrazovka, pozadie) 
            strely.clear(obrazovka, pozadie)
            strely_noviny.clear(obrazovka, pozadie)
            explozie.clear(obrazovka, pozadie)
            hranica.clear(obrazovka, pozadie)
            skore_bar.clear(obrazovka, pozadie)
            skore.clear(obrazovka, pozadie)


            # Aktualizácia všetkých objektov - zavolanie metód update v triedach
            tablet.update(smer, ob_tablet_rychlost)
            noviny.update(cas)
            noviny_ozbrojene.update(cas)
            noviny_boss.update(cas)
            noviny_bonus.update(cas)
            strely.update()
            strely_noviny.update()
            explozie.update(cas)
           

            # Detekcia kolízie objektov
            for i in pygame.sprite.groupcollide(noviny, strely, True, True):
                # a,b = x,y súradnice objektu, c,d = šírka a výška objektu
                a, b, c, d = i.rect
                # vytvorenie explózie a pripísanie skóre a peňazí
                explozie.add(Explozia((a-20, b-20)))
                skore_peniaze += 10
                skore_skore += 15
                # Spustenie zvuku explózie
                zvuk.explozia_p()

            for i in pygame.sprite.groupcollide(tablet, noviny, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()

            for i in pygame.sprite.groupcollide(noviny_ozbrojene, strely, True, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_peniaze += 15
                skore_skore += 20
                zvuk.explozia_p()

            for i in pygame.sprite.groupcollide(tablet, noviny_ozbrojene, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()

            for i in pygame.sprite.groupcollide(tablet, strely_noviny, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a-20, b-20)))
                skore_zivoty -= 1
                zvuk.poskodenie_p()


            for i in pygame.sprite.groupcollide(hranica, noviny, False, True):
                skore_zivoty_zakladne -= 1
                
            for i in pygame.sprite.groupcollide(hranica, noviny_ozbrojene, False, True):
                skore_zivoty_zakladne -= 1

            for i in pygame.sprite.groupcollide(hranica, noviny_bonus, False, True):
                pass

            # Detekcia kolízie pre Boss-ov
            for i in pygame.sprite.groupcollide(noviny_boss, strely, False, True):
                a, b, c, d = i.rect
                explozie.add(Explozia((a+random.randrange(0,384), b+250)))
                boss_hp -= 1
                if boss_hp == 0:
                    skore_peniaze += 500
                    skore_skore += 1000
                    noviny_boss.empty()
                    
            # Detekcia kolízie v bonusovej úrovni
            if skore_uroven == 1 and skore_pod_uroven == 6:
                for i in pygame.sprite.groupcollide(tablet, noviny_bonus, False, True):
                    a, b, c, d = i.rect
                    explozie.add(Explozia((a-20, b-20)))
                    skore_peniaze += 10
                    zvuk.explozia_p()
                    
            if skore_uroven == 3 and skore_pod_uroven == 6:
                for i in pygame.sprite.groupcollide(noviny_bonus, strely, True, True):
                    a, b, c, d = i.rect
                    explozie.add(Explozia((a-20, b-20)))
                    skore_peniaze += 25
                    skore_skore += 30
                    zvuk.explozia_p()

            # Priradnie všetkých aktuálnych objektov do zoznamov
            tablet_zoznam = tablet.draw(obrazovka)
            noviny_zoznam = noviny.draw(obrazovka)
            noviny_ozbrojene_zoznam = noviny_ozbrojene.draw(obrazovka)
            noviny_boss_zoznam = noviny_boss.draw(obrazovka)
            noviny_bonus_zoznam = noviny_bonus.draw(obrazovka)     
            strely_zoznam = strely.draw(obrazovka)
            strely_noviny_zoznam = strely_noviny.draw(obrazovka)
            explozie_zoznam = explozie.draw(obrazovka)
            hranica_zoznam = hranica.draw(obrazovka)
            skore_bar_zoznam = skore_bar.draw(obrazovka)
            skore_zoznam = skore.draw(obrazovka)

            # Nastavovanie bar-u a skóre pri Boss úrovni
            if len(noviny_boss_zoznam) != 0:    
                skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, boss_hp, skore_peniaze, skore_skore)
                skore_bar.update(1)
            else:
                skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)
                skore_bar.update(0)

            # Streľba nepriateľov
            if len(noviny_ozbrojene_zoznam) != 0 and cas > cas_strely_noviny and len(strely_noviny_zoznam) < len(noviny_ozbrojene_zoznam):
                cas_strely_noviny = cas + 250
                a, b, c, d = noviny_ozbrojene_zoznam[random.randrange(0, len(noviny_ozbrojene_zoznam))]
                if b > 0:
                    strely_noviny.add(strela_noviny((a+20, b+50)))

            if len(noviny_boss_zoznam) != 0 and cas > cas_strely_noviny:
                cas_strely_noviny = cas + 350
                a, b, c, d = noviny_boss_zoznam[0]
                if b > 0:
                    e = [90, 135, 180, 225, 270]
                    strely_noviny.add(strela_noviny((a+random.choice(e), b+150)))
                

            # Spustenie novej "vlny", ak na obrazovke už nie sú žiadne noviny
            if len(noviny_zoznam) == 0 and len(noviny_ozbrojene_zoznam) == 0 and len(noviny_boss_zoznam) == 0 and len(noviny_bonus_zoznam) == 0:

                #herne pole je 5 x 4 
                #1,3,6 nestrielaju
                #2,4,5,7 strielaju

                # Generovanie úrovni hry zo súborov
                # a jej následné vykresľovanie
                # Jeden znak značí jedného nepriateľa
                
                # Generovanie 1. úrovne je rozdielne,
                # pretože pred ňou nemôže byť žiadne menu obchod
                if uroven_1:
                    f = file("urovne/1/uroven_1_1.txt")
                    l=f.readline()
                    y=0
                    while l!="":
                      for x in xrange(len(l)):
                          if l[x]=="1":
                              noviny.add(Noviny_1(x,y))
                          elif l[x]=="2":
                              noviny_ozbrojene.add(Noviny_2(x,y))
                          elif l[x]=="3":
                              noviny.add(Noviny_3(x,y))
                          elif l[x]=="4":
                              noviny_ozbrojene.add(Noviny_4(x,y))
                          elif l[x]=="5":
                              noviny_ozbrojene.add(Noviny_5(x,y))
                          elif l[x]=="6":
                              noviny.add(Noviny_6(x,y))
                          elif l[x]=="7":
                              noviny_ozbrojene.add(Noviny_7(x,y))                          
                          elif l[x]=="8":
                              noviny_bonus.add(Noviny_bonus_1(x,y))
                          elif l[x]=="9":
                              noviny_boss.add(Noviny_boss_12())
                              
                      l=f.readline()
                      y+=1
                    f.close()
                    uroven_1 = False
                   
                else:
                    menu_obchod.polozka_nastav(0)
                    index_obchod = 0
                    stav = STAV_MENU_OBCHOD             
                    skore_pod_uroven += 1

                    if skore_pod_uroven == 6 and skore_uroven == 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1

                    if skore_pod_uroven == 8 and skore_uroven != 2:
                        skore_uroven += 1
                        skore_pod_uroven = 1
                        
                    level_name = "urovne/" + str(skore_uroven) + "/uroven_" + str(skore_uroven) + "_" + str(skore_pod_uroven)  + ".txt"
               
                    try:
                        skore_peniaze += 150
                        skore_skore += 500
                        f = file(level_name)
                        l=f.readline()
                        y=0
                        while l!="":
                          for x in xrange(len(l)):
                              if l[x]=="1":
                                  noviny.add(Noviny_1(x,y, skore_uroven))
                              elif l[x]=="2":
                                  noviny_ozbrojene.add(Noviny_2(x,y, skore_uroven))
                              elif l[x]=="3":
                                  noviny.add(Noviny_3(x,y, skore_uroven))
                              elif l[x]=="4":
                                  noviny_ozbrojene.add(Noviny_4(x,y, skore_uroven))
                              elif l[x]=="5":
                                  noviny_ozbrojene.add(Noviny_5(x,y, skore_uroven))
                              elif l[x]=="6":
                                  noviny.add(Noviny_6(x,y, skore_uroven))
                              elif l[x]=="7":
                                  noviny_ozbrojene.add(Noviny_7(x,y, skore_uroven))                          
                              elif l[x]=="8":
                                  noviny_bonus.add(Noviny_bonus_1(x,y))
                              elif l[x]=="9":
                                  noviny_boss.add(Noviny_boss_12(skore_uroven))
                              elif l[x]=="a":
                                  for x in range(0,69):
                                      noviny_bonus.add(Noviny_bonus_2())
                              elif l[x]=="b":
                                  boss_hp = 150
                                  noviny_boss.add(Noviny_boss_12(skore_uroven))
                                                                    
                          l=f.readline()
                          y+=1
                        f.close()
                        
                    # Ak hráč prejde všetke úrovne, vyhráva
                    except IOError:
                        stav = STAV_VYHRA       
                
            # Aktualizácia, čiže prevednie akejkoľvek zmeny na objekte
            # a vykreslenie všetkých objektov
            pygame.display.update(tablet_zoznam)
            pygame.display.update(noviny_zoznam)
            pygame.display.update(noviny_ozbrojene_zoznam)
            pygame.display.update(noviny_boss_zoznam)
            pygame.display.update(noviny_bonus_zoznam)
            pygame.display.update(strely_zoznam)
            pygame.display.update(strely_noviny_zoznam)
            pygame.display.update(explozie_zoznam)
            pygame.display.update(hranica_zoznam)
            pygame.display.update(skore_bar_zoznam)
            pygame.display.update(skore_zoznam)

            # Koniec hry, ak hráčovi dojdú životy tabletu alebo základni
            if skore_zivoty < 1 or skore_zivoty_zakladne < 1:
              stav = STAV_PREHRA
              Zvuky().explozia_p(1)
                
            # Zadefinovanie počtu snímkov za sekundu (FPS)
            hodiny.tick(60)
          
            
        elif stav == STAV_MENU_OBCHOD:

            obchod_pokracuj = True
            # Zapísanie najvyššieho skóre do súboru
            try:
                highscore = file("highscore.txt", "r")
                HIGHSCORE = highscore.readlines()
                highscore.close()
                if float(HIGHSCORE[0]) < skore_skore:
                    highscore = file("highscore.txt", "w")
                    highscore.write(str(skore_skore))
                    highscore.close()
            except (IOError, IndexError):
                highscore = file("highscore.txt", "w")
                highscore.write(str(0))
                highscore.close()
                
            # Prekreslenie obrazovky s obchod menu
            obrazovka.blit(Menu_Obchod.vykresli_obchod_menu(menu_obchod, index_obchod, cena, meno, extra),(0,0))

            skore_bar_zoznam = skore_bar.draw(obrazovka)
            skore_zoznam = skore.draw(obrazovka)
            pygame.display.update(skore_zoznam)
            strely = pygame.sprite.RenderUpdates()
            tablet = pygame.sprite.RenderUpdates()
            strely_noviny = pygame.sprite.RenderUpdates()
            explozie = pygame.sprite.RenderUpdates()
            tablet.add(Tablet())            

            # Zadefinovanie rôznych položiek obchodu
            if index_obchod == 0:
              cena = 300
              meno = u"Život tabletu"
              extra = ""
              
            elif index_obchod == 1:
              cena = 450
              meno = u"Rýchlejší tablet"
              extra = u"Aktuálna úroveň: %d" % ob_tablet_rychlost_lvl
              if ob_tablet_rychlost_lvl == 5:
                extra = u"Aktuálna úroveň: %d" % ob_tablet_rychlost_lvl + "(MAX)"
              
            elif index_obchod == 2:
              cena = 200
              meno = u"Život základne"
              extra = ""

            elif index_obchod == 3:
              cena = 350
              meno = u"Rýchlejšia Zbraň"
              extra = u"Aktuálna úroveň: %d" % ob_strelba_rychlost_lvl
              if ob_strelba_rychlost_lvl == 10:
                extra = u"Aktuálna úroveň: %d" % ob_strelba_rychlost_lvl + "(MAX)"                

            elif index_obchod == 4:
              cena = 950
              meno = u"Nová Zbraň"
              extra = u"Aktuálna úroveň: %d" % ob_strela_pocet
              if ob_strela_pocet == 3:
                extra = u"Aktuálna úroveň: %d" % ob_strela_pocet + "(MAX)"

            # Interakcia v menu
            if stlacena_klavesa[K_UP]:
                menu_obchod.kurzor_obchod()
                obchod = True
               
            if stlacena_klavesa[K_DOWN]:
                menu_obchod.kurzor_obchod_dole()
                obchod = False

            if stlacena_klavesa[K_LEFT] and cas > oneskorenie_sipky:
                
                if obchod:
                    oneskorenie_sipky = cas + 200
                    menu_obchod.kurzor_obchod_lavo()
                    if index_obchod != 0:
                        index_obchod -= 1
                else:
                    menu_obchod.kurzor_dolava()
                

            if stlacena_klavesa[K_RIGHT] and cas > oneskorenie_sipky:
                
                if obchod:
                     oneskorenie_sipky = cas + 200
                     menu_obchod.kurzor_obchod_pravo()
                     if index_obchod != 4:
                         index_obchod += 1
                else:
                    menu_obchod.kurzor_doprava()               

            # Nakupovanie rôznych položiek podľa indexov
            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_obchod.polozka_zisti() == 0:
                    if skore_peniaze >= cena:
                        if index_obchod == 0:
                            skore_zivoty += 1
                            skore_peniaze -= cena
                        elif index_obchod == 1 and ob_tablet_rychlost_lvl < 5:
                            ob_tablet_rychlost += 0.5
                            skore_peniaze -= cena
                            ob_tablet_rychlost_lvl += 1
                        elif index_obchod == 2:
                            skore_zivoty_zakladne += 1
                            skore_peniaze -= cena
                        elif index_obchod == 3 and ob_strelba_rychlost_lvl < 10:
                            ob_strelba_rychlost -= 7
                            skore_peniaze -= cena
                            ob_strelba_rychlost_lvl += 1
                        elif index_obchod == 4 and ob_strela_pocet < 3:
                            ob_strela_pocet += 1
                            skore_peniaze -= cena
                elif menu_obchod.polozka_zisti() == 1:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    zvuk.boj_pokrik_p()
                oneskorenie_enter = cas + 200
            if stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
                oneskorenie_enter = cas + 200
                stav = STAV_MENU_HLAVNE
            if stlacena_klavesa[K_m]:
                skore_peniaze += 100
                skore_zivoty_zakladne += 1
                skore_zivoty += 1
                
            skore.update(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore)

        # Hlavné menu hry, spúštané pri spustení hry    
        elif stav == STAV_MENU_HLAVNE:
            obrazovka.blit(Menu.vykresli_menu(menu_hlavne),(0,0))
            
            if stlacena_klavesa[K_UP] and cas > oneskorenie_sipky:
                menu_hlavne.kurzor_hore()
                oneskorenie_sipky = cas + 250
               
            if stlacena_klavesa[K_DOWN] and cas > oneskorenie_sipky:
                menu_hlavne.kurzor_dole()
                oneskorenie_sipky= cas + 250
                
            # Pri spúštaní novej hry, sú všetké dôležité premenné resetované
            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_hlavne.polozka_zisti() == 0:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False

                    skore_zivoty = 5
                    skore_peniaze = 0
                    skore_zivoty_zakladne = 15
                    skore_uroven = 1
                    skore_pod_uroven = 1
                    skore_skore = 0
                    uroven_1 = True

                    ob_tablet_rychlost = 9.0
                    ob_tablet_rychlost_lvl = 1
                    ob_strelba_rychlost = 300
                    ob_strelba_rychlost_lvl = 1
                    ob_strela_pocet = 1
                    
                    noviny = pygame.sprite.RenderUpdates()
                    noviny_ozbrojene = pygame.sprite.RenderUpdates()
                    noviny_boss = pygame.sprite.RenderUpdates()
                    noviny_bonus = pygame.sprite.RenderUpdates()
                    skore = pygame.sprite.RenderUpdates()
                    skore.add(Skore(skore_zivoty, skore_uroven, skore_pod_uroven, skore_zivoty_zakladne, skore_peniaze, skore_skore))
                    tablet = pygame.sprite.RenderUpdates()
                    tablet.add(Tablet())
                    strely = pygame.sprite.RenderUpdates()
                    explozie = pygame.sprite.RenderUpdates()                    
                    strely_noviny = pygame.sprite.RenderUpdates()
                    
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                    zvuk.boj_pokrik_p()                    
                elif menu_hlavne.polozka_zisti() == 1:
                    if obchod_pokracuj:
                        stav = STAV_MENU_OBCHOD
                    else:
                        stav = STAV_V_HRE
                        obrazovka.blit(pozadie, (0, 0))
                        pygame.display.update()
                elif menu_hlavne.polozka_zisti() == 2:
                    stav = STAV_MENU_AKO
                elif menu_hlavne.polozka_zisti() == 3:
                    pygame.quit()
                    sys.exit()
                oneskorenie_enter = cas + 200
            
                
        # Rôzne menšie stavy hry ako je menu ako hrat, pozitívny alebo negatívny koniec hry a pauza        
        elif stav == STAV_MENU_AKO:
            if stlacena_klavesa[K_RETURN]  and cas > oneskorenie_enter:
              stav = STAV_MENU_HLAVNE
              oneskorenie_enter = cas + 200

            obrazovka.blit(Menu.vykresli_menu(menu_ako),(0,0))

        elif stav == STAV_MENU_PAUSE:

            obrazovka.blit(Menu.vykresli_popup_menu(menu_pause, obrazovka),(0,0))

            if stlacena_klavesa[K_LEFT]:
                menu_pause.kurzor_dolava()

            if stlacena_klavesa[K_RIGHT]:
                menu_pause.kurzor_doprava()

            if stlacena_klavesa[K_RETURN] and cas > oneskorenie_enter:
                if menu_pause.polozka_zisti() == 0:
                    stav = STAV_V_HRE
                    obchod_pokracuj = False
                    obrazovka.blit(pozadie, (0, 0))
                    pygame.display.update()
                elif menu_pause.polozka_zisti() == 1:
                    stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200

            elif stlacena_klavesa[K_ESCAPE] and cas > oneskorenie_enter:
              stav = STAV_V_HRE
              obchod_pokracuj = False
              obrazovka.blit(pozadie, (0, 0))
              pygame.display.update()
              oneskorenie_enter = cas + 250
              
        elif stav == STAV_VYHRA:
            obrazovka.blit(Menu.vykresli_koniec(menu_vyhra, obrazovka),(0,0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
              stav = STAV_MENU_HLAVNE
              oneskorenie_enter = cas + 200

        elif stav == STAV_PREHRA:            
            obrazovka.blit(Menu.vykresli_koniec(menu_prehra, obrazovka),(0,0))
            pygame.display.update()

            if stlacena_klavesa[K_ESCAPE]  and cas > oneskorenie_enter:
                stav = STAV_MENU_HLAVNE
                oneskorenie_enter = cas + 200              


# Zavolanie hlavnej funkcie ak je spustený tento skript
if __name__ == '__main__':
    main()
