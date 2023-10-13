#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package Scorer
#
# @brief Fichier qui sert a calculer le score d'un parcours
#
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 3 fonctions :
# - la fonction reset_score qui permet de remettre le score à 0
# - la fonction increase_score qui permet d'augmenter le score
# - la fonction get_score qui permet de récupérer le score
#
# @section description Description
# 
# Cette classe va permettre de calculer le score d'un parcours.
# Elle ne permet pas de calculer le score de plusieurs parcours en même temps.

## Variable globale qui permet de stocker le score
score = 0

## Fonction qui permet de remettre le score à 0
def reset_score() -> None:
    global score
    score = 0

## Fonction qui permet d'augmenter le score
#
# @param gift_score : Le score du cadeau
def increase_score(gift_score) -> None:
    global score
    score = score + gift_score

## Fonction qui permet de récupérer le score
def get_score() -> int:
    global score
    return score
