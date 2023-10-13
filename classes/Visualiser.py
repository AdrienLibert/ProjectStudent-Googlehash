## @package Visualiser
# 
# @brief Fichier qui sert a afficher le parcours en temps réel
# 
# @section classes_fonctions Classes & Fonctions
# 
# On retrouve dans ce fichier 1 classe :
# - la classe Visualiser qui permet d'afficher le parcours

import tkinter as tk
from classes.Parser import Parser
from classes.Gift import Gift
from classes.Santa import Santa
from PIL import Image
import io, threading, imageio, os

## Classe qui permet d'afficher le parcours
#
# @param parser : Le parser qui permet de récupérer les données
# @param background_task : La fonction qui permet de lancer le solver
#
# @section description Description
# 
# Cette classe va afficher le parcours en temps réel.
# Pour cela, elle va créer une fenêtre tkinter et afficher les éléments.
# 
# Le zoom est géré automatiquement pour que tout les éléments soient affichés.
class Visualiser:
    
    ## Constructeur
    #
    # @param parser : Le parser qui permet de récupérer les données
    # @param background_task : La fonction qui permet de lancer le solver
    # 
    # @section description Description
    # 
    # Cette fonction va créer la fenêtre tkinter et afficher les éléments.
    # Elle va aussi géré le zoom automatiquement.
    # La fonction va aussi créer un thread qui va permettre de lancer le solver.
    def __init__(self, parser : Parser, background_task) -> None:
        self.parser = parser
        self.gifts = {}

        # Create the main window
        self.root = tk.Tk()

        self.width = 950
        self.height = self.width

        # Create a canvas widget
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        self.x, self.y = self.canvas.canvasx(self.width/2), self.canvas.canvasy(self.height/2)

        self.minX = Gift("None", 0, 0, 0, 0)
        self.maxX = Gift("None", 0, 0, 0, 0)
        self.minY = Gift("None", 0, 0, 0, 0)
        self.maxY = Gift("None", 0, 0, 0, 0)

        for gift in self.parser.getGifts():
            
            if gift.position[0] not in self.gifts:
                self.gifts[gift.position[0]] = {}
                
            if gift.position[1] not in self.gifts[gift.position[0]]:
                self.gifts[gift.position[0]][gift.position[1]] = []
                
            if gift.position[0] < self.minX.position[0]:
                self.minX = gift
                
            elif gift.position[0] > self.maxX.position[0]:
                self.maxX = gift
                
            if gift.position[1] < self.minY.position[1]:
                self.minY = gift
                
            elif gift.position[1] > self.maxY.position[1]:
                self.maxY = gift
                
            self.gifts[gift.position[0]][gift.position[1]] = self.canvas.create_oval(
                self.x + gift.position[0],self.y + gift.position[1], 
                self.x + gift.position[0],self.y + gift.position[1], fill='red', outline='red')

        self.reach = self.canvas.create_oval(self.x - parser.getReach(),self.y - parser.getReach()
                                             ,self.x + parser.getReach(),self.y + parser.getReach(), fill='')
        self.velocity = self.canvas.create_line(self.x + 0,self.y + 0,self.x +  10,self.y + 0, fill='black', width=1)
        self.santa = self.canvas.create_oval(self.x - 1,self.y - 1,self.x + 1,self.y + 1, fill='blue', outline='blue')
        
        self.canvas.scale('all', self.x, self.y, 10, 10)
        self.scale = 10
        
        p = self.gifts[self.minX.position[0]][self.minX.position[1]]
        while self.canvas.bbox(p)[0] < 0:
            self.canvas.scale('all', self.x, self.y, 0.9, 0.9)
            self.scale *= 0.9
            
        p = self.gifts[self.maxX.position[0]][self.maxX.position[1]]
        while self.canvas.bbox(p)[2] > self.width:
            self.canvas.scale('all', self.x, self.y, 0.9, 0.9)
            self.scale *= 0.9
            
        p = self.gifts[self.minY.position[0]][self.minY.position[1]]
        while self.canvas.bbox(p)[1] < 0:
            self.canvas.scale('all', self.x, self.y, 0.9, 0.9)
            self.scale *= 0.9
            
        p = self.gifts[self.maxY.position[0]][self.maxY.position[1]]
        while self.canvas.bbox(p)[3] > self.height:
            self.canvas.scale('all', self.x, self.y, 0.9, 0.9)
            self.scale *= 0.9
            
        thread = threading.Thread(target=background_task, args=(parser, self))
        thread.start()
            
        self.root.mainloop()

        thread.join(timeout=1)
    
    ## Fonction qui permet de déplacer le père noël
    #
    # @param time : Le temps à partir duquel on veut déplacer le père noël
    # @param santa : Le père noël
    # 
    # @section description Description
    # 
    # Cette fonction va déplacer le père noël à partir du temps donné en paramètre.
    # Elle va aussi prendre une capture d'écran à chaque déplacement.
    def Float(self, time : int, santa : Santa) -> None:
        for i in range(time): 
            pos = santa.position
            pos[0] += santa.velocity[0] * i
            pos[1] += santa.velocity[1] * i
            self.move(pos, santa.velocity)
            self.takeScreenshot(santa.time + i)
    
    ## Fonction qui permet de délivrer un cadeau
    #
    # @param gift : Le cadeau à délivrer
    # 
    # @section description Description
    # 
    # Cette fonction va délivrer le cadeau donné en paramètre en le coloriant en vert.
    def deliverGift(self, gift : Gift):
        p = self.gifts[gift.position[0]][gift.position[1]]
        
        self.canvas.itemconfig(p, fill='green', outline='green')
        
    ## Fonction qui permet de réellement de déplacer le père noël
    #
    # @param pos : La position du père noël
    # @param velocity : La vitesse du père noël
    #
    # @section description Description
    #
    # Cette fonction va déplacer le père noël à la position donnée en paramètre.
    # Elle va aussi déplacer la zone de portée et la flèche de vitesse.
    # 
    # Cette fonction est appelée par la fonction Float afin de déplacer le père noël.
    def move(self, pos, velocity):
        self.canvas.coords(self.reach, self.x + (pos[0] - self.parser.getReach()) * self.scale,
                            self.y + (pos[1] - self.parser.getReach()) * self.scale,
                            self.x + (pos[0] + self.parser.getReach()) * self.scale,
                            self.y + (pos[1] + self.parser.getReach()) * self.scale)
        
        self.canvas.coords(self.velocity, self.x + pos[0] * self.scale,
                            self.y + pos[1] * self.scale,
                            self.x + ( pos[0] + velocity[0] ) * self.scale,
                            self.y + ( pos[1] + velocity[1] ) * self.scale)
        self.canvas.coords(self.santa, self.x + (pos[0] - 1) * self.scale,
                            self.y + (pos[1] - 1) * self.scale,
                            self.x + (pos[0] + 1) * self.scale,
                            self.y + (pos[1] + 1) * self.scale)
        
        self.canvas.update()

    ## Fonction qui permet de prendre une capture d'écran
    #
    # @param name : Le nom de la capture d'écran
    # 
    # @section description Description
    # 
    # Cette fonction va prendre une capture d'écran et la sauvegarder dans le dossier output.
    # Le nom de la capture d'écran est donné en paramètre.
    def takeScreenshot(self, name):
        screenshot = self.canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(screenshot.encode('utf-8')))
        img.save("output/" + str(name) + '.png')

    ## Fonction qui permet de créer une animation gif
    # 
    # @param max : Le nombre de captures d'écran
    # 
    # @section description Description
    # 
    # Cette fonction va créer une animation gif à partir des captures d'écran.
    # Elle va aussi supprimer les captures d'écran.
    def createGif(self, max : int):
        self.gif = imageio.get_writer('output/animation.gif', mode='I')
        photos = ["output/" + str(i) + '.png' for i in range(max)]
        
        for filename in photos:
            image = imageio.imread(filename)
            self.gif.append_data(image)
            os.remove(filename)
        
        self.gif.close()
        self.root.quit()
        


