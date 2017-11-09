#!/usr/bin/python3

from skimage import data, io, filter, feature, morphology
from skimage.color import rgb2gray
from matplotlib import pyplot as plt

class imageProcessing:
	def __init__(self, file_list):
		self.files = file_list

if __name__ == "__main__":
	pto = input("Name of the data folder: ")
	print("PROCESSING, Please wait.")
	
	objects = ["samolot14.jpg", "samolot01.jpg", 
				"samolot02.jpg","samolot17.jpg", 
				"samolot07.jpg", "samolot08.jpg",
				"samolot09.jpg","samolot10.jpg", 
				"samolot11.jpg"]

	pto = pto + str('/')
	objects = [pto + obj for obj in objects]
