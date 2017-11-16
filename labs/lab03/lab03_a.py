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
            
            opening = cv2.morphologyEx(self.images_g[i], cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, kernel)
            opening = closing
            
            bilater = cv2.bilateralFilter(opening, -1, (1.0 - 0.3) * np.std(self.images[i]), 10)#cv2.bilateralFilter(opening, 95, 75, 75)
            img_g = cv2.GaussianBlur(bilater, (3, 3), 0)
            
            v = np.median(img_g)
            lower = int(max(0, (1.0 - 0.3) * v))
            upper = int(min(255, (1.0 + 0.3) * v))
                        
            edges = cv2.Canny(img_g, lower, upper)
            
            for k in range(10):
                #final_img = cv2.dilate(edges, kernel, iterations = 1)
                final_img = cv2.erode(cv2.dilate(edges, kernel, iterations = 1), kernel, iterations = 1)
            
            imgMod = cv2.morphologyEx(final_img, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))
            x, contours, z = cv2.findContours(imgMod, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            resul = cv2.drawContours(self.images[i], contours, -1, (244, 255, 0), cv2.FILLED)
            
            self.images_g[i] = resul

    def generate_images(self):
        #plt.subplot(2,2,1), plt.imshow(img, cmap = 'gray'), plt.title('Orginal')
        #plt.subplot(2,2,2), plt.imshow(final_img, cmap = 'gray'), plt.title('Processed')
        
        num = len(self.files)
        cols = min(num, 3)
        rows = num // cols
        if(num % cols != 0):
            rows += 1
        
        cv2.imshow("Edges",self.images_g[0])
        cv2.waitKey(0)
        cv2.imshow("Edges",self.images_g[1])
        cv2.waitKey(0)
        return
        
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
