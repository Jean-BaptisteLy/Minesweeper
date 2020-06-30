import random
import copy
import time
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt

class Minesweeper:

	def __init__(self, nbre_lignes, nbre_colonnes, nbre_mines):
		self.nbre_lignes = nbre_lignes
		self.nbre_colonnes = nbre_colonnes
		self.superficie = nbre_lignes * nbre_colonnes
		self.nbre_mines = nbre_mines
		self.mines = []
		#self.terrain_reel = np.zeros((nbre_lignes, nbre_colonnes), dtype = String)
		self.terrain_reel = []
		for i in range(self.nbre_lignes):
			ligne = []
			for j in range(self.nbre_colonnes):
				ligne.append(0)
			self.terrain_reel.append(ligne)
		self.terrain_demineur = []
		for i in range(self.nbre_lignes):
			ligne = []
			for j in range(self.nbre_colonnes):
				ligne.append(9)
			self.terrain_demineur.append(ligne)
		self.nbre_deminage = 0
		self.victoire = False
		self.mort = False

	def put_mines_random(self):
		for i in range(self.nbre_mines):
			while(True):
				ligne = random.randint(0,self.nbre_lignes-1)
				colonne = random.randint(0,self.nbre_colonnes-1)
				if self.terrain_reel[ligne][colonne] == 9:
					continue
				else:
					self.terrain_reel[ligne][colonne] = 9
					break

	'''
	mines : liste de tuples (x,y) qui sont des coordonnées
	'''
	def put_mines_myself(self, mines):
		self.mines = mines.copy() # deepcopy() ?
		cpt = 0
		for m in mines:
			self.terrain_reel[m[0]][m[1]] = 9
			cpt += 1
			if cpt > self.nbre_mines:
				print("Erreur : Nombre limite de mines dépassé")
				break
		if cpt < self.nbre_mines:
			print("Erreur : Pas assez de mines à mettre")

	def put_indices(self):
		for i in range(self.nbre_lignes):
			for j in range(self.nbre_colonnes):
				if self.terrain_reel[i][j] == 9:
					if i-1 >= 0 and self.terrain_reel[i-1][j] != 9:
						self.terrain_reel[i-1][j] += 1
					if j-1 >= 0 and self.terrain_reel[i][j-1] != 9:
						self.terrain_reel[i][j-1] += 1
					if i+1 <= self.nbre_lignes-1 and self.terrain_reel[i+1][j] != 9:
						self.terrain_reel[i+1][j] += 1
					if j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i][j+1] != 9:
						self.terrain_reel[i][j+1] += 1
					if i-1 >= 0 and j-1 >= 0 and self.terrain_reel[i-1][j-1] != 9:
						self.terrain_reel[i-1][j-1] += 1
					if i+1 <= self.nbre_lignes-1 and j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i+1][j+1] != 9: 
						self.terrain_reel[i+1][j+1] += 1
					if i-1 >= 0 and j+1 <= self.nbre_colonnes-1 and self.terrain_reel[i-1][j+1] != 9:
						self.terrain_reel[i-1][j+1] += 1
					if i+1 <= self.nbre_lignes-1 and j-1 >= 0 and self.terrain_reel[i+1][j-1] != 9:
						self.terrain_reel[i+1][j-1] += 1

	def get_terrain(self):
		return self.terrain_reel

	def deminage(self, x, y):
		if self.terrain_reel[x][y] == 9:
			print("BOUM !!!")
			self.mort = True
			return nbre_deminage
		elif self.terrain_demineur[x][y] == 9:
			if self.terrain_reel[x][y] != 0: # mine à proximité
				self.terrain_demineur[x][y] = self.terrain_reel[x][y]
				self.nbre_deminage += 1
			elif self.terrain_reel[x][y] == 0: # mine à 
				self.terrain_demineur[x][y] = 0
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

	def check_victoire(self):
		if self.nbre_deminage == (self.superficie - self.nbre_mines):
			self.victoire = True
		return self.victoire

	def affichage_terrain_reel(self):
		for i in range(self.nbre_lignes):
			print(self.terrain_reel[i])

	def affichage_terrain_demineur(self):
		for i in range(self.nbre_lignes):
			print(self.terrain_demineur[i])

	def get_nbre_deminage(self):
		return self.nbre_deminage

	def get_mort(self):
		return self.mort

def run(nbre_lignes,nbre_colonnes,nbre_mines,mines):
	Demineur = Minesweeper(nbre_lignes,nbre_colonnes,nbre_mines)
	Demineur.put_mines_random()
	#Demineur.put_mines_myself(mines)
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
		if Demineur.get_mort() == True:
			print("***** PERDU *****")
			break
		elif Demineur.check_victoire() == True:
			print("**** GAGNE *****")
			break

run(3,7,2,[(2,0),(1,6)])