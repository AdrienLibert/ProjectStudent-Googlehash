#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Santa
#
# @brief Fichier qui sert a gérer le Santa
#
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 1 classe et 1 fonction :
# - la classe Santa qui permet de gérer le Santa
# - la fonction formatGifts qui permet de formater la liste des cadeaux

from typing import List 
from classes.Gift import Gift
from classes.Sleigh import SleighCategorie
from classes.Scorer import increase_score, get_score, reset_score
import re, os
import math

## Les directions possibles pour se déplacer
DIRECTIONS = "up|down|left|right"

## Exception qui est levée quand un des tests échoue
class SantaException(Exception):
    pass

## Exception qui est levée quand le temps maximum est dépassé
class TimeLimitException(SantaException):
    pass

## Fonction qui permet de formater la liste des cadeaux
#
# @param gifts : La liste des cadeaux
def formatGifts(gifts : List[Gift]) -> dict[str, Gift]:
    """Formatte la liste des cadeaux en un dictionnaire identifié par le nom de la personne qui recevra le cadeau.
    """
    return {gift.name : gift for gift in gifts}

## Classe qui permet de gérer le Santa
#
# @param Sleigh : La liste des catégories de poids de la traîneau
# @param gameGifts : La liste des cadeaux
# @param reach : La portée du Santa
# @param timeLimit : Le temps limite
# 
# @section description Description
# 
# Cette classe va permettre de gérer le Santa.
# Elle va gérer les actions suivantes :
# - se déplacer
# - prendre/déposer un cadeau
# - charger/décharger une carotte
#
# Elle va également sauvegarder les actions dans un fichier.

class Santa:
    
    ## Constructeur de la classe
    #
    # @param Sleigh : La liste des catégories de poids de la traîneau
    # @param gameGifts : La liste des cadeaux
    # @param reach : La portée du Santa
    # @param timeLimit : Le temps limite
    def __init__(self, Sleigh : List[SleighCategorie] = [], gameGifts : List[Gift] = [], reach : int = 0, timeLimit : int = 0) -> None:
        # This are variables that are given by the game
        # They should never be edited
        self.REACH = reach
        self.SLEIGH = Sleigh
        self.GAME_GIFTS = formatGifts(gameGifts)
        self.TIME_LIMIT = timeLimit
    
        self.actions     = 0
        self.position    = [0, 0]
        self.velocity    = [0, 0]
        self.time        = 0
        
        self.carrots     = 0
        self.gifts       = {}
        self.weightGifts = 0
        
        self.lastIsFloat = True
        self.maxWeight : int = 0 if len(Sleigh) == 0 else int(max([sleigh.maxWeight for sleigh in Sleigh])) 

        if not os.path.exists("output/"):
            os.makedirs("output/")

        with open("output/actions.txt", "w") as f:
            f.write("0\n")

    def __str__(self) -> str: return f"Santa({self.position}, {self.velocity}, {self.time})"
    
    def __repr__(self) -> str: return f"Santa({self.position}, {self.velocity}, {self.time})"

    ## Fonction qui va écrire l'action dans le fichier
    # 
    # @param action : L'action à écrire
    def writeFileAction(self, action : str = "") -> None:
        self.actions += 1
        # replace first line by self.actions

        with open("output/actions.txt", "r+") as f:
            lines = f.readlines()
            lines[0] = str(self.actions) + "\n"

        with open("output/actions.txt", "w") as f:
            f.writelines(lines)
            f.write(action + "\n")

    def distanceFromPoint(self, point : List[int]) -> int:
        if len(point) != 2:
            raise SantaException("Point must be a list of 2 elements")
        
        p = [point[0] - self.position[0], point[1] - self.position[1]]
        
        return math.sqrt(p[0]**2 + p[1]**2)

    ## Fonction qui permet de récupérer le poids du Santa
    def getWeight(self) -> int: return self.carrots + self.weightGifts

    ## Fonction qui permet de changer la vélocité du Santa
    #
    # @param direction : La direction dans laquelle le Santa doit se déplacer
    # @param acc : L'accélération du Santa
    #
    # @section description Description
    #
    # Cette fonction va permettre de changer la vélocité du Santa.
    # la direction doit être une des directions suivantes :
    # - up
    # - down
    # - left
    # - right
    #
    # L'accélération ne doit pas être supérieure à la vitesse maximale du Santa qui est définie par la catégorie de poids du Santa.
    def Accelerate(self, direction : str, acc : int) -> None:
        if not self.lastIsFloat:
            raise SantaException("Last action was not a float")
        
        if not re.match(DIRECTIONS, direction):
            raise SantaException("Wrong direction : " + direction)

        if self.carrots <= 0:
            raise SantaException("No carrots left")

        if self.getWeight() > self.maxWeight:
            raise SantaException("Too heavy")
        
        sleigh = None
        for s in self.SLEIGH:
            if s.minWeight <= self.getWeight() <= s.maxWeight:
                sleigh = s
                break
        
        if sleigh is None:
            raise SantaException("No sleigh found")
        
        if acc > sleigh.maxAcceleration:
            raise SantaException("Acceleration too high")

        self.lastIsFloat = False

        match direction:
            case "up":      self.velocity[1] += acc
            case "down":    self.velocity[1] -= acc
            case "left":    self.velocity[0] -= acc
            case "right":   self.velocity[0] += acc

        self.carrots -= 1
        direction = direction[0].upper() + direction[1:] #make first letter uppercase
        self.writeFileAction(f"Acc{direction} {acc}")

    ## Fonction qui permet de déplacer le Santa
    #
    # @param t : Le temps pendant lequel le Santa doit se déplacer
    #
    # @section description Description
    #
    # Cette fonction va permettre de déplacer le Santa pendant un certain temps.
    # Le Santa ne peut pas se déplacer si le temps est supérieur au temps limite.
    def Float(self, t : int) -> None:
        self.time += t

        if self.time > self.TIME_LIMIT:
            raise TimeLimitException("Time limit reached")
        
        self.lastIsFloat = True

        self.position[0] += self.velocity[0] * t
        self.position[1] += self.velocity[1] * t

        self.writeFileAction(f"Float {t}")

    ## Fonction qui permet de charger des carottes
    # 
    # @param n : Le nombre de carottes à charger
    #
    # @section description Description
    #
    # Cette fonction va permettre de charger des carottes.
    # Le Santa ne peut pas charger de carottes s'il n'est pas dans la range de (0, 0).
    def LoadCarrots(self, n : int) -> None:
        if n < 0:
            raise SantaException("Can't load negative carrots")
        
        if self.distanceFromPoint([0,0]) > self.REACH:
            raise SantaException("Not at the right position")

        self.carrots += n
        self.writeFileAction(f"LoadCarrots {n}")

    ## Fonction qui permet de charger un cadeau
    #
    # @param childName : Le nom de l'enfant dont le cadeau doit être chargé
    #
    # @section description Description
    #
    # Cette fonction va permettre de charger un cadeau.
    # Le Santa ne peut pas charger de cadeau s'il n'est pas dans la range de (0, 0).
    # Le Santa ne peut pas charger de cadeau s'il a déjà chargé un cadeau de cet enfant.
    def LoadGift(self, childName : str) -> None:
        if self.distanceFromPoint([0,0]) > self.REACH:
            raise SantaException("Not at the right position")

        g = self.GAME_GIFTS[childName]

        if g is None :
            raise SantaException("Gift not found")

        if childName in self.gifts :
            raise SantaException("we already loaded the gift : ", childName)
            
        self.gifts[g.name] = g
        self.weightGifts += g.weight
        self.writeFileAction(f"LoadGift {childName}")

    ## Fonction qui permet de décharger un cadeau
    # 
    # @param childName : Le nom de l'enfant dont le cadeau doit être déchargé
    #
    # @section description Description
    #
    # Cette fonction va permettre de décharger un cadeau.
    # Le Santa ne peut pas décharger de cadeau s'il n'est pas dans la range de la position du cadeau.
    # Le Santa ne peut pas décharger de cadeau s'il n'a pas chargé de cadeau de cet enfant.
    def DeliverGift(self, childName : str) -> None:
        g = self.GAME_GIFTS[childName]

        if g is None:
            raise SantaException("Gift not found")

        if g.name not in self.gifts:
            raise SantaException("Gift not loaded")

        if self.gifts[g.name] is None:
            raise SantaException("Gift already delivered")

        if self.distanceFromPoint(g.position) > self.REACH:
            raise SantaException("Not at the right position")

        self.gifts[g.name] = None
        self.weightGifts -= g.weight
        self.writeFileAction(f"DeliverGift {childName}")
        increase_score(g.score)
