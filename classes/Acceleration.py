## @package Acceleration
#
# @brief Fichier qui sert a initialiser les données pour une accélération
#
# @section classes_fonctions Classes & Fonctions
#
# On retrouve dans ce fichier 1 classe :
# - la classe Acceleration qui permet d'initialiser les données pour une accélération

## Classe qui permet d'initialiser les données pour une accélération
#
# @param start : La position de départ
# @param destination : La position d'arrivée
# @param maxAcc : L'accélération maximale
#
# @section description Description
#
# Cette classe va permettre d'initialiser les données pour une accélération.
# Elle va permettre de calculer les actions à effectuer pour atteindre la destination.
# Elle va aussi permettre de calculer le nombre de carottes nécessaires pour atteindre la destination.
# 
# @section exemple Exemple
# 
# @code
# from classes.Acceleration import Acceleration
# 
# a = Acceleration([0,0], [1000, 1000], 1000)
# print(a.actions)
# print(a.carrots)
# @endcode
class Acceleration():
    # The aim is to accelerate in one of four directions (up,down,left or right) and use Carrots.
    def __init__(self, start : list[int]|tuple[int,int], destination : list[int]|tuple[int,int], maxAcc : int) -> None:

        self.actions = [] 
        self.carrots = 0

        self.directions = ["right" if start[0] < destination[0] else "left", "up" if start[1] < destination[1] else "down"]
        self.distances = [abs(destination[0] - start[0]), abs(destination[1] - start[1])]
        self.velocity = [0, 0]
        self.deceleration = [0, 0]
            
        if self.distances[0] <= maxAcc:
            self.actions.append((self.directions[0], self.distances[0], 1))
            self.actions.append((self.directions[0], -self.distances[0], 1))
                
            self.distances[0] = 0
            self.carrots += 2
            
        if self.distances[1] <= maxAcc:
            self.actions.append((self.directions[1], self.distances[1], 1))
            self.actions.append((self.directions[1], -self.distances[1], 1))
            
            self.carrots += 2
            self.distances[1] = 0
            
            
        if self.distances[0] > self.distances[1]:
            self.directions = [self.directions[1], self.directions[0]]
            self.distances = [self.distances[1], self.distances[0]]
            
            
        while self.distances[0] > 0:
            
            if self.distances[0] - (maxAcc + self.velocity[0]) > \
                self.deceleration[0] + self.velocity[0]:
                    
                if self.distances[1] - (maxAcc + self.velocity[1]) * 5 > \
                self.deceleration[1] + self.velocity[1] and \
                    self.velocity[0] >= 300 and self.velocity[0] > self.velocity[1] * 1.5:
                    
                    self.accelerate(1, maxAcc)
                        
                else:
                    self.accelerate(0, maxAcc)
                    
            elif self.distances[0] - self.velocity[0] >= \
                self.deceleration[0] + self.velocity[0]:

                    if self.distances[1] - (maxAcc + self.velocity[1]) * 5 > \
                        self.deceleration[1] + self.velocity[1]:
                    
                        self.accelerate(1, maxAcc)
                        
                    elif self.distances[1] - self.velocity[1] * 3 >= \
                        self.deceleration[1] + self.velocity[1]: 
                        
                        self.float()
                        
                    elif self.distances[1] > maxAcc: self.decelerate(1, maxAcc)
                        
                    else: self.stop(1, maxAcc)
                
            elif self.distances[0] > maxAcc: self.decelerate(0, maxAcc)
                
            else: self.stop(0, maxAcc)
        
        while self.distances[1] > 0:
                    
            if self.distances[1] - (maxAcc + self.velocity[1]) > \
                self.deceleration[1] + self.velocity[1]:
                    
                self.accelerate(1, maxAcc)
                
            elif self.distances[1] - self.velocity[1] >= \
                self.deceleration[1] + self.velocity[1]:

                self.float()
                
            elif self.distances[1] > maxAcc: self.decelerate(1, maxAcc)
                
            else: self.stop(1, maxAcc)

    ## Fonction qui permet d'avancer en accélérant
    #
    # @param index : L'index de la direction
    # @param maxAcc : L'accélération maximale
    def accelerate(self, index: int, maxAcc: int) -> None:
        self.actions.append((self.directions[index], maxAcc, 1))
        self.carrots += 1
        self.velocity[index] += maxAcc
        self.deceleration[index] += self.velocity[index] - maxAcc
        self.distances[0] -= self.velocity[0]
        self.distances[1] -= self.velocity[1]

    ## Fonction qui permet d'avancer en maintenant la vélocité
    def float(self) -> None:
        self.actions.append(("Float", 0, 1))
        self.distances[1] -= self.velocity[1]
        self.distances[0] -= self.velocity[0]
        
    ## Fonction qui permet d'avancer en décélérant
    # 
    # @param index : L'index de la direction
    # @param maxAcc : L'accélération maximale
    def decelerate(self, index : int, maxAcc : int) -> None:
        self.actions.append((self.directions[index], -maxAcc, 1))
        self.carrots += 1
        self.velocity[index] -= maxAcc
        self.deceleration[index] -= self.velocity[index]
        self.distances[1] -= self.velocity[1]
        self.distances[0] -= self.velocity[0]
        
    ## Fonction qui permet d'arrêter le déplacement
    # 
    # @param index : L'index de la direction
    # @param maxAcc : L'accélération maximale
    def stop(self, index : int, maxAcc : int) -> None:
        self.actions.append((self.directions[index], -(maxAcc - self.distances[index]), 1))
        self.actions.append((self.directions[index], -self.distances[index], 1))
        self.carrots += 2
        self.distances[index] = 0
        self.velocity[index] = 0
        
        self.distances[1] -= 2 * self.velocity[1]

    ## Fonction qui permet de récupérer le nombre de carottes nécessaires pour atteindre la destination
    def getCarrots(self) -> int:
        return self.carrots
    
    ## Fonction qui permet de récupérer le temps nécessaire pour atteindre la destination
    def getTime(self) -> int:
        return len(self.actions)
                    
    def __str__(self) -> str:
        return f"Acceleration({self.actions})"
    
    def __repr__(self) -> str:
        return self.__str__()