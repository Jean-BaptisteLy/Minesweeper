import random
import copy
import time
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
import inspect # affiche la ligne du code, très utile

lineno = lambda: inspect.currentframe().f_back.f_lineno

class Minesweeper:

	def __init__(self, nbre_lignes, nbre_colonnes, nbre_mines):

		self.nbre_lignes = nbre_lignes
		self.nbre_colonnes = nbre_colonnes
		self.superficie = nbre_lignes * nbre_colonnes
		self.nbre_mines = nbre_mines
		self.mines = {}

		# terrain réel
		self.terrain_reel = []
		for i in range(self.nbre_lignes):
			ligne = []
			for j in range(self.nbre_colonnes):
				ligne.append('0')
			self.terrain_reel.append(ligne)
		# terrain du démineur
		self.terrain_demineur = []
		for i in range(self.nbre_lignes):
			ligne = []
			for j in range(self.nbre_colonnes):
				ligne.append('*')
			self.terrain_demineur.append(ligne)

		self.nbre_tentatives = 0
		self.nbre_deminage = 0 # Permet de déterminer la victoire
		self.victoire = False
		self.mort = False

	# Mets des mines à des positions aléatoires
	def put_mines_random(self):
		for i in range(self.nbre_mines):
			while(True):
				ligne = random.randint(0,self.nbre_lignes-1)
				colonne = random.randint(0,self.nbre_colonnes-1)
				if self.terrain_reel[ligne][colonne] == '*':
					continue
				else:
					self.mines[i] = (ligne,colonne)
					self.terrain_reel[ligne][colonne] = '*'
					break

	# Mets des mines aux positions choisies
	def put_mines_myself(self, mines):
		'''
		mines : liste de tuples (x,y) qui sont des coordonnées
		'''
		cpt = 0
		self.mines = mines
		print(self.mines)
		for key, value in self.mines.items():
			print(value)
			self.terrain_reel[value[0]][value[1]] = '*'
			cpt += 1
			if cpt > self.nbre_mines:
				print("Erreur",lineno(),": Nombre limite de mines dépassé")
				break
		if cpt < self.nbre_mines:
			print("Erreur",lineno(),": Pas assez de mines à mettre")

	# Initialise le terrain réel
	def put_indices(self):
		# Amélioration possible avec un dictionnaire
		for key, value in self.mines.items():
			i = value[0]
			j = value[1]
			if self.terrain_reel[i][j] == '*':
				if i-1 >= 0 and self.terrain_reel[i-1][j] != '*':
					self.terrain_reel[i-1][j] = str(int(self.terrain_reel[i-1][j]) + 1)
				if j-1 >= 0 and self.terrain_reel[i][j-1] != '*':
					self.terrain_reel[i][j-1] = str(int(self.terrain_reel[i][j-1]) + 1)
				if i+1 <= self.nbre_lignes-1 and self.terrain_reel[i+1][j] != '*':
					self.terrain_reel[i+1][j] = str(int(self.terrain_reel[i+1][j]) + 1)
				if j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i][j+1] != '*':
					self.terrain_reel[i][j+1] = str(int(self.terrain_reel[i][j+1]) + 1)
				if i-1 >= 0 and j-1 >= 0 and self.terrain_reel[i-1][j-1] != '*':
					self.terrain_reel[i-1][j-1] = str(int(self.terrain_reel[i-1][j-1]) + 1)
				if i+1 <= self.nbre_lignes-1 and j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i+1][j+1] != '*': 
					self.terrain_reel[i+1][j+1] = str(int(self.terrain_reel[i+1][j+1]) + 1)
				if i-1 >= 0 and j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i-1][j+1] != '*':
					self.terrain_reel[i-1][j+1] = str(int(self.terrain_reel[i-1][j+1]) + 1)
				if i+1 <= self.nbre_lignes-1 and j-1 >= 0 and self.terrain_reel[i+1][j-1] != '*':
					self.terrain_reel[i+1][j-1] = str(int(self.terrain_reel[i+1][j-1]) + 1)

	# Une action de déminage
	def deminage(self, x, y):
		if self.terrain_reel[x][y] == '*':
			print("BOUM !!!")
			self.mort = True
		elif self.terrain_demineur[x][y] == '*':
			if self.terrain_reel[x][y] != '0': # mine à proximité
				self.terrain_demineur[x][y] = self.terrain_reel[x][y]
				self.nbre_deminage += 1
			elif self.terrain_reel[x][y] == '0': # aucune mine
				self.terrain_demineur[x][y] = '0'
				self.nbre_deminage += 1
				if x-1 >= 0:
					#print("a")
					self.deminage(x-1, y)
					#return
				if y-1 >= 0:
					#print("b")
					self.deminage(x, y-1)
				if x+1 <= self.nbre_lignes-1:
					#print("c")
					self.deminage(x+1, y)
				if y+1 <= self.nbre_colonnes-1:
					#print("d")
					self.deminage(x, y+1)
				if x-1 >= 0 and y-1 >= 0:
					#print("e")
					self.deminage(x-1, y-1)
				if x+1 <= self.nbre_lignes-1 and y+1 <= self.nbre_colonnes-1:
					#print("f")
					self.deminage(x+1, y+1)
				if x-1 >= 0 and y+1 <= self.nbre_colonnes-1:
					#print("g")
					self.deminage(x-1, y+1)
					#return
				if x+1 <= self.nbre_lignes-1 and y-1 >= 0:
					#print("h")
					self.deminage(x+1, y-1)

	# Vérifie la victoire
	def check_victoire(self):
		if self.nbre_deminage == (self.superficie - self.nbre_mines):
			self.victoire = True
			print("Vous avez réussi à localiser toutes les mines, bravo !")
		return self.victoire

	def check_mort(self):
		self.nbre_tentatives += 1
		print("Tentative",self.nbre_tentatives,":")
		if self.mort == True:
			print("***** Vous êtes mort *****")
		return self.mort

	# Affichage du terrain réel (réponse)
	def affichage_terrain_reel(self):
		for i in range(self.nbre_lignes):
			print(self.terrain_reel[i])

	# Affichage du terrain du démineur
	def affichage_terrain_demineur(self):
		for i in range(self.nbre_lignes):
			print(self.terrain_demineur[i])

	def get_nbre_deminage(self):
		return self.nbre_deminage

	def get_terrain(self):
		return self.terrain_reel

	def get_mort(self):
		return self.mort

	def get_nbre_tentatives(self):
		return self.nbre_tentatives

def run(nbre_lignes,nbre_colonnes,nbre_mines,mines):
	Demineur = Minesweeper(nbre_lignes,nbre_colonnes,nbre_mines)
	if len(mines) == 0:
		Demineur.put_mines_random()
	else:
		Demineur.put_mines_myself(mines)
	Demineur.put_indices()
	Demineur.affichage_terrain_reel()
	while(True):
		print("############################")
		Demineur.affichage_terrain_demineur()
		print("x =")
		x = int(input())
		print("x =",x)
		print("y =")
		y = int(input())
		print("y =",y)
		Demineur.deminage(x,y)
		if Demineur.check_mort() == True:
			print("***** PERDU *****")
			break
		elif Demineur.check_victoire() == True:
			print("**** GAGNE *****")
			break
	print("Nombre de tentatives jouées :",Demineur.get_nbre_tentatives())


nbre_lignes = 3
nbre_colonnes = 7
nbre_mines = 2
liste_mines = [(2,0),(1,6)]
dico_mines = {}
for i in range(len(liste_mines)):
	dico_mines[i] = (liste_mines[i][0],liste_mines[i][1])
run(nbre_lignes,nbre_colonnes,nbre_mines,dico_mines)