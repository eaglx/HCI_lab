#!/usr/bin/python3

import cv2
import numpy as np
import random as rand
from matplotlib import pyplot as plt

def gen_random_color():
    color = []
    for i in range(3):
        color.append(rand.randint(0, 255))
    return color

class imageProcessing:
    def __init__(self, fileList):
        self.files = fileList
        self.images = []
        self.images_g = []
        self.images_m = []
        
        for img in self.files:
           self.images.append(cv2.imread(img))

    def processing_images(self):
        kernel = np.ones((5,5), np.uint8)
        for i in range(len(self.files)):
            self.images_g.append(cv2.cvtColor(self.images[i], cv2.COLOR_BGR2GRAY))
            
            opening = cv2.morphologyEx(self.images_g[i], cv2.MORPH_OPEN, kernel)
            #closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
            #opening = closing
            
            bilater = cv2.bilateralFilter(opening, -1, (1.0 - 0.3) * np.std(self.images_g[i]), 10)
            #bilater = cv2.bilateralFilter(opening, 9, 75, 75)
            img_g = cv2.GaussianBlur(bilater, (3, 3), 0)
            
            v = np.median(img_g)
            lower = int(max(0, (1.0 - 0.3) * v))
            upper = int(min(255, (1.0 + 0.2) * v))
                        
            edges = cv2.Canny(img_g, lower, upper)
            
            final_img = cv2.erode(cv2.dilate(edges, kernel, iterations = 2), kernel, iterations = 1)    
            
            self.images_m.append(final_img)
            
            imgMod = cv2.morphologyEx(final_img, cv2.MORPH_CLOSE, kernel)
            x, contours, z = cv2.findContours(imgMod, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for lp in range(len(contours)):
                moments = cv2.moments(contours[lp])
                self.images_g[i] = cv2.drawContours(self.images[i], contours, lp, gen_random_color(), thickness=2)
                self.images_g[i] = cv2.circle(self.images_g[i], (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])), 5, (255, 255, 255), -1)

    def generate_images(self):
        #plt.subplot(2,2,1), plt.imshow(img, cmap = 'gray'), plt.title('Orginal')
        #plt.subplot(2,2,2), plt.imshow(final_img, cmap = 'gray'), plt.title('Processed')
        
        num = len(self.files)
        cols = min(num, 3)
        rows = num // cols
        if(num % cols != 0):
            rows += 1
        
        
        for ims in range(num):
            cv2.imshow("Edges",self.images_g[ims])
            cv2.waitKey(0)
        
        fig, plots = plt.subplots(rows, cols, facecolor='black')
        for r in range(rows):
            for c in range(cols):
                if(r * cols + c < num):
                    plots[r,c].imshow(self.images_m[r * cols + c], cmap = 'gray')
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
