## @package Parcour
#
# @brief Fichier qui sert a représenter un parcours
#
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 1 classe :
# - la classe Parcour qui permet de représenter un parcours

from classes.Parser import Parser
from classes.Gift import Gift
from classes.Acceleration import Acceleration
import math

## Classe qui permet de représenter un parcours
#
# @param parser : Le parser qui permet de récupérer les données du fichier
#
# @section description Description
#
# Cette classe va permettre de représenter un parcours.
# Chaque parcours a un parser, une liste de cadeaux, un index de traîneau, un traîneau courant, un poids maximum, une accélération maximum, un temps limite, un poids, une position et une accélération.
# On peut récupérer le parser, la liste de cadeaux, l'index de traîneau, le traîneau courant, le poids maximum, l'accélération maximum, le temps limite, le poids, la position et l'accélération.
# On peut aussi vérifier si un cadeau peut être chargé et charger un cadeau.
# On peut terminer un parcours.
#
# @section parcours Parcours
# 
# Le parcours va commencer à [0, 0] et va se terminer à [0, 0].
# Il ne gere pas les déplacements de cadeaux.
class Parcour():

    ## Constructeur de la classe Parcour
    # 
    # @param parser : Le parser qui permet de récupérer les données du fichier    
    def __init__(self, parser : Parser):
        self.parser     : Parser = parser        
        
        self.gifts      : list[Gift] = []
        
        self.sleighIndex = 0
        self.currentSleigh = parser.getSleigh()[self.sleighIndex]
        
        self.maxWeight = self.currentSleigh.maxWeight
        self.maxAcc = self.currentSleigh.maxAcceleration
        self.timeLimit = parser.getTimeLimit()
        
        self.weight     : int = 0
        self.pos        : tuple[int, int] = (0, 0)
        self.time       : int = 0
        self.actions    : list[Acceleration | Gift] = []
        self.carrots    : int = 0
        
    ## Fonction qui permet de regarder si le cadeau peut être chargé
    #
    # @param gift : Le cadeau à charger
    def canLoad(self, gift : Gift) -> bool:
        """Check if the gift is reachable and if the gift can be loaded
        """
        
        # go to gift
        acc = Acceleration(self.pos, gift.position, self.maxAcc)
        acc2 = Acceleration(gift.position, (0, 0), self.maxAcc)
        
        if self.weight + gift.weight + self.carrots + acc.getCarrots() + acc2.getCarrots() >= self.maxWeight: return False
        
        if acc.getTime() + self.time > self.timeLimit: return False
        
        return True
            
    ## Fonction qui permet de charger un cadeau
    #
    # @param gift : Le cadeau à charger
    def loadGift(self, gift : Gift):
        self.gifts.append(gift)
        
        if math.sqrt((self.pos[0] - gift.position[0])**2 + (self.pos[1] - gift.position[1])**2) > self.parser.getReach():
            acc = Acceleration(self.pos, gift.position, self.maxAcc)
            self.pos = gift.position
            self.time += acc.getTime()
            self.carrots += acc.getCarrots()
            self.actions.append(acc)
        
        self.actions.append(gift)
        self.weight += gift.weight
          
    ## Fonction qui permet de terminer un parcours  
    def end(self) -> None:
        
        acc = Acceleration(self.pos, (0, 0), self.maxAcc)
        
        self.actions.append(acc)
        self.pos = [0, 0]
        self.time += acc.getTime()
        self.carrots += acc.getCarrots()
            
    def __str__(self) -> str:
        return f"Parcour({len(self.actions)})"   
    
    def __repr__(self) -> str:
        return self.__str__()     
        