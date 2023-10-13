#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Sleigh
#
# @brief Fichier qui sert a représenter les catégories de traîneaux
# 
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 1 classe :
# - la classe SleighCategorie qui permet de représenter les catégories de traîneaux

## Classe qui permet de représenter les catégories de traîneaux
# 
# @param minweight : Le poids minimum du traîneau
# @param maxweight : Le poids maximum du traîneau
# @param maxAcceleration : L'accélération maximum du traîneau
# 
# @section description Description
# 
# Cette classe va permettre de représenter les catégories de traîneaux.
class SleighCategorie:
    def __init__(self, minweight, maxweight, maxAcceleration) -> None:
        self.minWeight = int(minweight)
        self.maxWeight = int(maxweight)
        self.maxAcceleration = int(maxAcceleration)
    
    def __str__(self) -> str:
        return f"SleighCategorie({self.minWeight}, {self.maxWeight}, {self.maxAcceleration})"

    def __repr__(self) -> str:
        return f"SleighCategorie({self.minWeight}, {self.maxWeight}, {self.maxAcceleration})"
    
    def __eq__(self, __o: object) -> bool:
        return self.minWeight == __o.minWeight \
            and self.maxWeight == __o.maxWeight \
            and self.maxAcceleration == __o.maxAcceleration
    
    def __lt__(self, __o: "SleighCategorie") -> bool:
        return self.maxWeight > __o.maxWeight