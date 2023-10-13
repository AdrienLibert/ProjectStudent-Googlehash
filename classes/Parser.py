#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Parser
#
# @brief Fichier qui sert a parser les données du challenge
#
# @section classes_fonctions Classes & Fonctions
#
# On retrouve dans ce fichier 1 classe et 1 fonction :
# - la classe Parser qui permet de parser les données du challenge
# - la fonction readFile qui permet de lire le fichier

from typing import List
from classes.Sleigh import SleighCategorie
from classes.Gift import Gift

## Classe qui permet de parser les données du challenge
#
# @param fileName : Le nom du fichier à parser 
#
# @section description Description
# 
# Cette classe va permettre de parser les données du challenge.
# Elle va permettre de récupérer les données suivantes :
# - le temps limite
# - les cadeaux
# - les catégories de traîneaux
# - la portée du Santa
class Parser:
    
    ## Constructeur de la classe
    #
    # @param fileName : Le nom du fichier à parser
    def __init__(self, fileName : str = "data/a_an_example.in.txt") -> None: #Definit les deux paramêtres de la classe le fichier et data pour lire le fichier
        self.fileName = fileName
        self.data = readFile(fileName)

    ## Fonction qui permet de récupérer le temps limite
    def getTimeLimit(self) -> int:
        return int(self.data['timeLimit'])

    ## Fonction qui permet de récupérer les cadeaux
    def getGifts(self) -> List[Gift]:
        return self.data['gifts']
    
    ## Fonction qui permet de récupérer les catégories de traîneaux
    def getSleigh(self) -> List[SleighCategorie]:
        return self.data['sleigh']

    ## Fonction qui permet de récupérer la portée du Santa
    def getReach(self) -> int:
        return int(self.data['reach'])
    
## Fonction qui permet de lire le fichier
#
# @param fileName : Le nom du fichier à parser
# 
# @section description Description
#
# Cette fonction va permettre de lire le fichier et de récupérer les données suivantes :
# - le temps limite
# - les cadeaux
# - les catégories de traîneaux
# - la portée du Santa
#
# Elle va retourner un dictionnaire contenant les données précédentes
def readFile(fileName : str = "data/a_an_example.in.txt"):
    
    file = open(fileName, "r") #Ouvrir le fichier en lecture pour pouvoir récupérer les informations
    timeLimit, reachRange, numberOfSleigh, numberOfGifts = file.readline().split(" ")

    sleigh = []
    minWeight = 0
    for i in range(int(numberOfSleigh)):
        line = file.readline()
        line = line.replace("\n", "")
        w = SleighCategorie(minWeight , *line.split(" "))
        sleigh.append(w)
        minWeight = w.maxWeight

    gifts = []
    for i in range(int(numberOfGifts)):
        line = file.readline()
        line = line.replace("\n", "")
        g = Gift(*line.split(" "))
        gifts.append(g)
        
    return { 
        "timeLimit" : timeLimit, 
        "reach" : reachRange, 
        "sleigh" : sleigh, 
        "gifts" : gifts,
    }