#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Gift
#
# @brief Fichier qui sert a représenter les cadeaux
#
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 1 classe :
# - la classe Gift qui permet de représenter les cadeaux

import math

## Classe qui permet de représenter les cadeaux
# 
# @param name : Le nom du cadeau
# @param score : Le score du cadeau
# @param weight : Le poids du cadeau
# @param x : La position x du cadeau
# @param y : La position y du cadeau
# 
# @section description Description
# 
# Cette classe va permettre de représenter les cadeaux.
# Chaque cadeau a un nom, un score, un poids et une position.
# On peut récupérer le nom, le score, le poids et la position d'un cadeau.
# On peut aussi calculer la distance d'un cadeau par rapport à l'origine.
class Gift:
    
    ## Constructeur de la classe Gift
    #
    # @param name : Le nom du cadeau
    # @param score : Le score du cadeau
    # @param weight : Le poids du cadeau
    # @param x : La position x du cadeau
    # @param y : La position y du cadeau
    def __init__(self, name : str, score : str|int, weight : str|int, x : str|int, y : str|int) -> None: #Each gift has a name,score,weight and position
        self.name = name
        self.score = int(score)
        self.weight = int(weight)
        self.position = (int(x), int(y))

    ## Fonction qui permet de calculer la distance d'un cadeau par rapport à l'origine
    def distanceFromOrigin(self) -> int:
        return math.sqrt(self.position[0]**2 + self.position[1]**2)

    ## Fonction qui permet de récupérer le nom du cadeau
    def getName(self) -> str:
        return self.name
    
    ## Fonction qui permet de récupérer le score du cadeau
    def getScore(self) -> int:
        return self.score
    
    ## Fonction qui permet de récupérer le poids du cadeau
    def getWeight(self) -> int:
        return self.weight
    
    ## Fonction qui permet de récupérer la position du cadeau
    def getPosition(self) -> list[int]:
        return self.position

    def __str__(self) -> str:
        return f"Gift({self.name}, {self.score}, {self.weight}kg, x{self.position[0]}, y{self.position[1]})" 

    def __repr__(self) -> str:
        return f"Gift({self.name}, {self.score}, {self.weight}kg, x{self.position[0]}, y{self.position[1]})"

    def __eq__(self, __o : "Gift") -> bool:
        return self.name == __o.name \
            and self.score == __o.score \
            and self.weight == __o.weight \
            and self.position == __o.position

    def __lt__(self, __o : "Gift") -> bool:
        return self.score **2 / self.weight < __o.score **2 / __o.weight
    
    def __hash__(self) -> int:
        return hash(self.name)
