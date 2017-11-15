#!/usr/bin/python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

class imageProcessing:
    def __init__(self, fileList):
        self.files = fileList
        self.images = []
        
        for img in self.files:
           self.images.append(cv2.imread(img, 0))

    def processing_images(self):
        kernel = np.ones((5,5), np.uint8)
        for i in range(len(self.files)):            
            img_g = cv2.GaussianBlur(self.images[i], (5,5), 0)
            edges = cv2.Canny(img_g, 100, 200)
            final_img = cv2.dilate(edges, kernel, iterations = 1)  
            self.images[i] = final_img

    def generate_images(self):
        #plt.subplot(2,2,1), plt.imshow(img, cmap = 'gray'), plt.title('Orginal')
        #plt.subplot(2,2,2), plt.imshow(final_img, cmap = 'gray'), plt.title('Processed')
        
        num = len(self.files)
        cols = min(num, 3)
        rows = num // cols
        if(num % cols != 0):
            rows += 1
        
        fig, plots = plt.subplots(rows, cols, facecolor='black')
        for r in range(rows):
            for c in range(cols):
                if(r * cols + c < num):
                    plots[r,c].imshow(self.images[r * cols + c], cmap = 'gray')
                    plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
        
        fig.savefig('ex1.pdf', facecolor='black')
        plt.close()

if __name__ == "__main__":
	pto = input("Name of the data folder: ")
	print("PROCESSING, Please wait.")
	
	objects = ["samolot11.jpg", "samolot10.jpg", 
				"samolot02.jpg","samolot17.jpg", 
				"samolot07.jpg", "samolot08.jpg"]

	pto = pto + str('/')
	objects = [pto + obj for obj in objects]
	
	planes = imageProcessing(objects)
	planes.processing_images()
	planes.generate_images()
