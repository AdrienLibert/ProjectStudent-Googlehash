#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Solver
# 
# @brief Fichier qui sert a initialisation les données pour le parcours, générer les parcours et ensuite les éxécuter
#
# @section classes_fonctions Classes & Fonctions
#
# On retrouve dans ce fichier 2 classes et 1 fonctions :
# - la classe Organizer qui permet de générer les données pour le parcours
# - la fonction solve qui permet de générer les parcours
# - la classe Resolver qui permet d'éxécuter le parcours

from classes.Parser import Parser
from classes.Santa import Santa, TimeLimitException
from classes.Gift import Gift
from classes.Acceleration import Acceleration
from classes.Parcour import Parcour
from classes.Visualiser import Visualiser
import math
from datetime import datetime

## Classe qui permet d'éxécuter un parcours 
#
# @param parcour : Le parcours à éxécuter
# @param santa : Le père noël
# @param v : Le visualiser qui permet d'afficher le parcours
# 
# @section description Description
#
# Cette classe va éxéctuer un parcour en plusieurs étapes :
# 1. On charge les carottes
# 2. On charge les cadeaux
# 3. On itère sur les actions du parcours :
#  - Si c'est une accélération, on accélère et on flotte
#  - Si c'est un cadeau, on le livre
#
# Cette classe va aussi etre charger de dire au Visualiser de se déplacer et de livrer les cadeaux.
class Resolver():
    
    def __init__(self, parcour : Parcour, santa : Santa, v : Visualiser):
        self.parcour = parcour
        self.santa = santa
        self.visualiser = v
        
    def execute(self):
        self.santa.LoadCarrots(self.parcour.carrots)
        
        for gift in self.parcour.gifts:
            self.santa.LoadGift(gift.name)
        
        for action in self.parcour.actions:
            if isinstance(action, Acceleration):
                for dir, force, time in action.actions:
                    
                    if dir == "Float":
                        if self.visualiser is not None : self.visualiser.Float(time, self.santa)
                        
                        self.santa.Float(time)
                        
                    else:
                        self.santa.Accelerate(dir, force)
                        
                        if self.visualiser is not None : self.visualiser.Float(time, self.santa)
                        self.santa.Float(time)
                        
            elif isinstance(action, Gift):
                self.santa.DeliverGift(action.name)
                if self.visualiser is not None : self.visualiser.deliverGift(action)

            else:
                raise Exception("Unknown action")

## Fonction qui permet de générer les données pour l'algorithme 
#
# @param parser : Le parser qui permet de récupérer les données
# 
# @section description Description
# 
# Cette fonction va générer les données suivantes afin d'etre utilisés par l'algorithme :
# - nameToGift : Un dictionnaire qui permet de retrouver un cadeau à partir de son nom
# - posToGift : Un dictionnaire qui permet de retrouver un cadeau à partir de sa position
# - giftsNearStart : Une liste des cadeaux qui sont dans la zone de départ
# - giftsInRange : Un dictionnaire qui permet de retrouver les cadeaux qui sont dans la zone de dépot d'un cadeau
class Organizer():
    
    def __init__(self, parser : Parser):
        self.parser = parser
        
        self.nameToGift : dict[str, Gift] = {}
        self.posToGift : dict[int, dict[int, Gift]] = {}
        self.giftsNearStart : list[Gift] = []
        self.giftsInRange : dict[str, set[str]]= {}
        
        for gift in parser.getGifts():
            
            if abs(gift.position[0]) <= parser.getReach() \
                and abs(gift.position[1]) <= parser.getReach() \
                and math.sqrt(gift.position[0]**2 + gift.position[1]**2) <= parser.getReach():
                    
                    self.giftsNearStart.append(gift)
            
            self.nameToGift[gift.name] = gift
            if gift.position[0] not in self.posToGift:
                self.posToGift[gift.position[0]] = {}
                
            self.posToGift[gift.position[0]][gift.position[1]] = gift 
            self.giftsInRange[gift.name] = set()            
            xs = range(gift.position[0] - parser.getReach(), gift.position[0] + parser.getReach() + 1) & self.posToGift.keys()
            for lookupX in xs:
                
                ys = range(gift.position[1] - parser.getReach(), gift.position[1] + parser.getReach() + 1) & self.posToGift[lookupX].keys()
                for lookupY in ys:
                    if math.sqrt((lookupX - gift.position[0])**2 + (lookupY - gift.position[1])**2) > parser.getReach(): continue
                    
                    g = self.posToGift[lookupX][lookupY]
                    
                    if g.name in self.giftsInRange[gift.name]: continue
                    
                    self.giftsInRange[gift.name].add(g.name)
                    self.giftsInRange[g.name].add(gift.name)
                    
        for key in self.giftsInRange:
            self.giftsInRange[key] = sorted(self.giftsInRange[key], key = lambda x : self.nameToGift[x] < self.nameToGift[key])
                     
## Fonction qui permet de résoudre le problème
# 
# @param parser : Le parser qui permet de récupérer les données
# @param v : Le visualiser qui permet de visualiser le parcours ou None si on ne veut pas visualiser
#
# @section description Description
# 
# Cette fonction va résoudre le problème en utilisant l'algorithme suivant :
# - On dépose les cadeaux qui sont dans la zone de départ
# - tant que le temps n'est pas écoulé :
#  - On récupère un cadeau proche de la position actuelle
#  - Si le cadeau peut etre chargé :
#   - On charge le cadeau
#   - On charge le plus de cadeaux proches que possible
#  - Sinon :
#   - On Termine le parcour
#   - On ajoute le parcour a la liste des parcours
# - On éxécute les parcours
# 
def solve(parser : Parser, v : Visualiser|None) -> None:
    timer = datetime.now()
    start = timer
    
    santa = Santa(parser.getSleigh(), parser.getGifts(), parser.getReach(), parser.getTimeLimit())
    organizer = Organizer(parser)

    parcour = Parcour(parser)
    parcours : list[Parcour] = []
    delivered = set()
    
    print("Organisation : ", datetime.now() - timer)
    timer = datetime.now()
    
    # We deliver the gifts that are in the starting zone
    for g in organizer.giftsNearStart:
        santa.LoadGift(g.name)
        santa.DeliverGift(g.name)
        delivered.add(g.name)
        if v: v.deliverGift(g)
    
    gift = None
    totalTime = 0
    while totalTime < santa.TIME_LIMIT:

        reach = parser.getReach() * 2
        while gift is None:
            # look for the closest gift to the current position of the parcour
            
            xs = range(-reach + parcour.pos[0], reach + 1 + parcour.pos[0]) & organizer.posToGift.keys()
            for x in xs:
                ys = range(-reach + parcour.pos[1], reach + 1 + parcour.pos[1]) & organizer.posToGift[x].keys()
                for y in ys:
                    if not math.sqrt((x - parcour.pos[0])**2 + (y - parcour.pos[1])**2) <= reach: continue
                    gift = organizer.posToGift[x][y]
                    break

                
                if gift is not None: 
                    if gift.name in delivered: gift = None
                    else : break
                
            if reach == 0: reach = 1
            reach *= 2
            
        # we load the gift and every gift in the range of the gift
        
        if parcour.canLoad(gift):
            if gift.name in delivered: 
                gift = None
                continue
                
            parcour.loadGift(gift)
            delivered.add(gift.name)
            
            for g in organizer.giftsInRange[gift.name]:
                if g in delivered: continue
                if not parcour.canLoad(organizer.nameToGift[g]): continue
                
                parcour.loadGift(organizer.nameToGift[g])
                delivered.add(g)
                
        else:
            parcour.end()
            totalTime += parcour.time
            parcours.append(parcour)
            parcour = Parcour(parser)

    print("Parcours : ", datetime.now() - start)
    timer = datetime.now()

    for parcour in parcours:
        resolver = Resolver(parcour, santa, v)
        try : resolver.execute()
    
        except TimeLimitException as e:
            
            if v: v.createGif(santa.time)
            
            print("Finished with time limit exceeded", datetime.now() - timer)
            print("Total time :", datetime.now() - start)
            return
        
        #print("Parcour : ", datetime.now() - timer)
        timer = datetime.now()
        
    if v: v.createGif(santa.time)
    
    print("Finished", datetime.now() - timer)
    print("Total time :", datetime.now() - start)