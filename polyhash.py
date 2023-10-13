#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## @package polyhash 
#
# @brief Fichier de lancement du projet
#
# @section lunch_options Options de lancement
#
# Afin de lancer le programme, il faut utiliser la commande suivante :
# @code
# python3 polyhash.py data/a_an_example.in.txt
# @endcode
#
# Le program peut être lancé avec les options suivantes :
#
# @arg --seed : seed pour la randomisation des dictionnaires
# @arg --display : affichage de la solution avec sauvegarde sous gif


from classes.Parser import Parser
from classes.Solver import solve
from classes.Scorer import get_score, reset_score
from classes.Visualiser import Visualiser
import argparse, os, sys

## Fonction de lancement du programme
#
# Cette fonction permet de lancer le programme et cela permet aussi de lancer cela en thread si on choisis d'utiliser l'affichage
def lunch_task(challenge : Parser, v : Visualiser):
        solve(challenge, v)
        print(f"Score: {get_score()}")

        reset_score()
        return 1

## Lanceur du programme
#
# Cette fonction permet de lancer le programme et de gérer les options de lancement
# @arg --seed : seed pour la randomisation des dictionnaires
# @arg --display : affichage de la solution avec sauvegarde sous gif
def lunch_program():
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="data/a_an_example.in.txt")
    
    parser.add_argument('--seed', type=int, default=-1, help='seed for random number generator must be within [0, 2^32-1]')
    parser.add_argument('--display', action='store_true', help='display the solution')
    
    args = parser.parse_args()

    seed = args.seed
    hashseed = os.getenv('PYTHONHASHSEED')
    
    if not hashseed and seed >= 0:
        # this lunch the programm again with the hashseed
        
        os.environ['PYTHONHASHSEED'] = str(seed)
        os.execv(sys.executable, [sys.executable] + sys.argv)
        
    else:

        challenge = Parser(args.challenge)
        
        if args.display:
            v = Visualiser(challenge, lunch_task)
            
        else:
            lunch_task(challenge, None)

if __name__ == "__main__":    
    lunch_program()
