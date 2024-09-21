# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:48:03 2022

@author: mayur
"""
import cv2

class Board:
    def __init__(self,contours,img):
        
        self.contours=contours
        self.img=img
    
    def board_contour(self):
        
        # find largest area contour
        cnt = max(self.contours, key=cv2.contourArea)
        
        #Extracting edge points of largest contour
        x1,y1,w1,h1 = cv2.boundingRect(cnt)
        
        #prints board outline based on the edge points
        Largest_rect=cv2.rectangle(self.img, (x1,y1), (x1+w1, y1+h1), (255,255,0), 1)
        return  Largest_rect


