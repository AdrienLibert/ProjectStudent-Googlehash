Description du projet
============

Ce projet a été réalisé dans le cadre du concours PolyHash 2022. Il a été réalisé par l'équipe F.
Les membres de l'équipe sont :
- Adrien LIBERT
- Yann PHILIPPE
- Pierre PAULMIER

Ce projet est basé sur le Google Hashcode 2022 Santa Tracker qui était le sujet final du concours.
Le but de ce projet est de fournir une solution qui permet de délivrer des cadeaux en terminant avec le plus haut score possible.

Le probleme inclus différents variables qui restreignent la solution :
- une distance pour chaque action
- un temps maximal pour délivrer les cadeaux
- une limite du changement de vélocity en fonction du poids des cadeaux chargés


Répartition des tâches/fonctions du projet au sein de l'équipe  
===============================================================

Afin de faciliement se répartir les taches, nous avions un systeme d'issues sur gitlab avec des labels pour facilement connaitre l'état de chaque tache et avec chacun qui s'assignait les taches qu'il voulait faire.

Cela permetait aussi de facilement discuter sur des problemes rencontrés et de pouvoir facilement faire des pull requests pour les taches terminées.

Une tache était mise Terminé lors que la merge request pour celle ci était ouverte et l'issue était fermée lors que la merge request était acceptée.

Adrien LIBERT a réalisé :
- la gestion du CHANGELOG
- le parser : Parser
- les typages des fonctions et classes : Santa, Gift, Parcour, Solver, Sleigh
- l'algorithme de gestion des déplacements : Acceleration
- l'algorithme de délivrance des cadeaux : Solver
- les tests unitaires
- l'interface graphique avec la sauvegarde des images sous une gif : Visualiser
- de nombreux tests de validation dans le Santa, et autres tel que les ranges, dépassement de temps, etc.
- création d'issues sur gitlab pour la répartition des taches
- rédaction des commentaires pour doxygen et déployement de la documentation sur github pages

Pierre PAULMIER a réalisé :
- la gestion du Scorer
- le remplacement des listes par des tuples pour les positions
- rédaction du README
- création de la vidéo de présentation

Yann PHILIPPE a réalisé :
- la vérification du chargement et déchargement des cadeaux
- création de la vidéo de présentation

Procédure d'installation
========================

`pip install -r requirements.txt` permet d'installer les dépendances nécessaires au projet, afin d'utiliser les cas des test ainsi que l'interface graphique.

Il est aussi nécessaire d'installer ghostscript afin de pouvoir créer les GIFs sous Windows, il peut être téléchargé ici : https://www.ghostscript.com/download/gsdnld.html

Procédure d'exécution
=====================

`python3 polyhash2022 <path to input>` permet d'exécuter le projet avec le fichier d'entrée donné en paramètre.  
`python3 polyhash2022 data/a_an_example.in.txt` par exemple.

l'option `--seed <seed>` permet de spécifier la graine utilisée pour la randomisation des dictionnaires.

l'option `--display` permet d'afficher l'interface graphique avec la sauvegarde des images sous une gif dans le dossier output.  
**Attention** : cette option est très lente et ne doit pas être utilisée pour les cas de test ou sur des parcours avec un temps inférieur a 1000.

Stratégie mise en oeuvre et résultats obtenus
============================================

## Introduction

Pour cela, nous avons décidé d'utiliser un algorithme glouton qui va chercher un cadeau proche du Santa puis le livrer avec ses voisins.

Pour faciliter notre code, nous avons aussi décider d'utiliser des "parcours" en partant de (0, 0) avec aucune vélocité et en revenant a (0, 0) avec aucune vélocité.  
Cela permet de faciliter grandement la gestion des accélérations et des déplacements mais aussi de pouvoir utiliser les fonctions de vérification de la validité des parcours.

Nous avons aussi décider d'avoir l'algorithme de notre programme dans un Solver et d'utiliser des classes Supplémentaire tel qu'un Santa ou Gift afin de vérifier la validité des parcours.  
Cela a permis de facilement identifier les erreurs mais aussi la source exacte des erreurs.  
Par exemple, Il était particulierement simple de savoir pourquoi on ne pouvais pas délivrer un cadeau, si on était pas dans sa range ou si on avait pas charger le cadeau.

## Principes de l'algorithme

![Algorithme](/images/algo.png)

### Préparation des données

Notre algorithme commence par prendre les donnés qui nous sont fournis par notre parser afin de les rendre plus facilement utilisable :
- un dictionnaire qui prend un nom de cadeau et renvoie le cadeau
- un dictionnaire qui prend les coordonnées des points en clé avec le cadeau pour facilement trouver des cadeaux proches de nous.
- une liste des cadeaux suffisamment proche de nous pour pouvoir les délivrer instantanément.
- un dictionnaire qui prend un nom de cadeau en entré et qui renvoie une list des noms des cadeaux qui sont proche de lui.

### Génération des parcours

Ensuite, nous allons répété jusqu'a ce que nous ayons atteint le temps maximal :
- nous allons chercher un cadeau proche de nous.
- s'il n'est pas délivrer et qu'on peut le charger, nous allons le charger
- nous regardons ensuite les cadeaux autour de lui et nous les chargons si possible
- si nous sommes plein, nous retournons au départ sinon nous recommençons par chercher un cadeau proche de nous.

### Éxécution des parcours

Puis, les parcours qui ont été généré sont éxécutés un par un.

Pour cela, chacun de nos parcours nos donne une liste d'actions avec un nombre de carrottes et une liste de cadeaux à délivrer.

Nous allons donc commencer par charger les cadeaux avec les carrottes nécessaires.

Ensuite, nous allons itérer sur les actions et les éxécuter une par une.  
Une action peut etre de 2 types :
- une `Acceleration` qui représente une série de déplacement entre 2 points.
- un `Gift` qui nous permet de savoir quand délivrer un cadeau.

Cette implémentation permet de faciliter grandement l'éxécution car nous n'avons pas besoin d'effectuer de checks et simplement itérer sur les actions.

## Optimisation

Chercher un cadeau proche de nous s'est prouvé être une opération très couteuse en temps.
Cependant, a l'aide du dictionnaire qui permet a l'aide des coordonnées de trouver un cadeau, nous avons pu récupérer ses clés et en faisant une intersection avec une range de coordonnées, nous avons pu réduire le temps de recherche grandemment.  
`xs = range(-reach + parcour.pos[0], reach + 1 + parcour.pos[0]) & organizer.posToGift.keys()`  
En effet, cette opération est beaucoup plus courte car elle est de O(min(range, keys)) donc dans le pire cas nous serions sur un O(n) ce qui est relativement rapide.  
Nous faisons ensuite une double boucle for sur les X et Y qui sont valides, cependant la complexité reste assez faible car nous avons cherchons le premier cadeau non chargé.  
Cette approche s'est montré particulierement efficace dans le parcours b_better_hurry qui aurait précédemment pris des années pour s'éxécuter.

## Résultats

### Résultats obtenus
Les résultats ont été obtenus a partir de la version 0.4.0 du code avec la seed 0.

Pour faire l'étude de l'utilisation de la mémoire nous avons utilisé le package `memory_profiler` qui nous permet de voir l'utilisation de la mémoire au cours de l'éxécution du programme.

| Fichier | Score | Temps | Utilisation de la mémoire |
|---------|-------|-------|---------------------------|
| a_an_example.in.txt | 0 | 0.015s | 52.378MB |
| b_better_hurry.in.txt | 63418 | 0.268s | 52.503MB |
| c_carousel.in.txt | 412212 | 32.786s | 69.785MB |
| d_decorated_houses.in.txt | 500805 | 68.570s | 45.859MB |
| e_excellent_weather.in.txt | 325835 | 6.777s | 66.695MB |
| f_festive_flyover.in.txt | 467744 | 0.478s | 130.769MB |

La génération des parcours prends environ 10% du temps total d'éxécution des lors que le temps pour effectué les parcours est supérieur a 1000.
On peut bien voir cela sur les graphiques de mémoire.

**a_an_example.in.txt**  
![Graphe Memoire a_an_example.in.txt](/images/memory_a_an_example.gif)  

**b_better_hurry.in.txt**  
![Parcour b_better_hurry.in.txt](/images/b_better_hurry.gif)  
![Graphe Memoire b_better_hurry.in.txt](/images/memory_b_better_hurry.gif)  

**c_carousel.in.txt**  
![Parcour c_carousel.in.txt](/images/c_carousel.gif)  
![Graphe Memoire c_carousel.in.txt](/images/memory_c_carousel.gif)  

**d_decorated_houses.in.txt**  
![Parcour d_decorated_houses.in.txt](/images/d_decorated_houses.gif)  
![Graphe Memoire d_decorated_houses.in.txt](/images/memory_d_decorated_houses.gif)  

**e_excellent_weather.in.txt**  
![Parcour e_excellent_weather.in.txt](/images/e_excellent_weather.gif)  
![Graphe Memoire e_excellent_weather.in.txt](/images/memory_e_excellent_weather.gif)  

**f_festive_flyover.in.txt**  
![Parcour f_festive_flyover.in.txt](/images/f_festive_flyover.gif)  
![Graphe Memoire f_festive_flyover.in.txt](/images/memory_f_festive_flyover.gif)  

Orginasation du code
====================

Un fichier polyhash.py contient le code qui permet de lire les arguments et lancer le programme.

Le code est organisé avec des classes qui sont regroupées dans le dossier classes.  
Ces classes ont pour but de regrouper les différents éléments du problème afin de pouvoir les manipuler plus facilement.  
Mais aussi de facilement pouvoir typer les variables et de pouvoir les utiliser dans les fonctions.  
Cela a été un grand atout pour la lisibilité du code et pour gérer ce problème en groupe.

Le dossier tests contient les différents tests unitaires qui ont été réalisés pour vérifier le bon fonctionnement du code.  
Ces tests sont éxécutés avec pytest avec le CI de gitlab afin d'assurer nos commits.

Certaines classes tel que le Parser sont des classes qui ne servent qu'a utiliser des fonctions statiques, cela permet de faciliter grandemment le travail de groupe en typant les variables de retour.

Bugs et limitations connues
===========================

Aucun points n'est fait sur le parcours a_an_example, cela est surement du a une mauvais optimisation des accélérations ou un cas non géré.

Le programme va souvent décéllérer jusqu'a 0 alors qu'il n'a pas atteint son point d'arrivé et va ensuite se remettre a accélérer, cela est surement du a des valeurs renseignes lorsque l'on regarder si l'on doit accélérer, floter ou décélérer.

Nous ne prenons pas avantage des différentes catégories de traineau, car nous prenons uniquement celui qui va de 0kg a un point déterminer. Cela a permit de simplifier notre algorithm.  
Cependant, il aurait surement été possible de l'utiliser afin de délivrer plus de cadeau et donc d'avoir un meilleur score.

Il est aussi possible de prendre en compte le point suivant, il faudrait aussi construire notre algorithme en pensant a cela en regardant par example les X et Y des points possibles en ne changeant qu'une seule fois de vélocité.

La génération des gifs est tres lente (plus de 30 minutes pour les data qui ont un temps de plus de 5000).  
Il faudrait remplacement la génération d'image par `tk` par une nouvelle génération plus rapide.

Il devrait aussi etre possible de lancer l'éxécution d'un algorithme juste apres sa génération afin de pouvoir accélérer le programme.  
Cette approche n'aurait cependant pas fait gagner plus de score.
