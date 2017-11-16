#!/usr/bin/python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

class imageProcessing:
    def __init__(self, fileList):
        self.files = fileList
        self.images = []
        self.images_g = []
        
        for img in self.files:
           self.images.append(cv2.imread(img))

    def processing_images(self):
        kernel = np.ones((5,5), np.uint8)
        for i in range(len(self.files)):
            self.images_g.append(cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY))
            v = np.median(self.images_g[i])
            lower = int(max(0, (1.0 - 0.33) * v))
            upper = int(min(255, (1.0 + 0.33) * v))
                        
            img_g = cv2.GaussianBlur(self.images_g[i], (3, 3), 0)
            #img_g = cv2.bilateralFilter(self.images[i], 11, 17, 17)
            edges = cv2.Canny(img_g, lower, upper)
            final_img = cv2.dilate(edges, kernel, iterations = 1)  #cv2.morphologyEx(edges, cv2.MORPH_GRADIENT, kernel)
            
            self.images_g[i] = final_img

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
                    plots[r,c].imshow(self.images_g[r * cols + c], cmap = 'gray')
                    plots[r,c].tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off', labelleft='off', labelbottom='off')
        
        plt.tight_layout()
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
