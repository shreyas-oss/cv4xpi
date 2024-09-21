# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:50:21 2022

@author: mayur
"""

import cv2

class Contoursa:
    areaArray=[]
    Count=1
    def __init__(self,contours):
        self.contours=contours
        
    def for_loop(self):
        
        for i, c in enumerate(self.contours):
            
            # to find the contour area
            area = cv2.contourArea(c)
            Contoursa.areaArray.append(area)
            
            #sorting the area by size from large to small
            sorteddata=sorted(self.contours, key=cv2.contourArea, reverse=True)
            
        return  sorteddata
