# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:48:46 2022

@author: mayur
"""

import cv2
#contourza gives zip area array values
class Contourszip:
    areaArray=[]
    Count=1
    
    def __init__(self,contours):
        self.contours=contours
        
    def for_loop(self):
        for i, c in enumerate(self.contours):
            
            # to find the contour area
            area = cv2.contourArea(c)
            Contourszip.areaArray.append(area)
            
            #sorting the area by size from large to small
        sorteddata=sorted(zip(Contourszip.areaArray, self.contours), key=lambda x: x[0], reverse=True)
        
        return sorteddata 
    
    def for_loop1(self,contours):
        
        areaArray1=[]
        Count=1
        
        for i, c in enumerate(contours):
            
            # to find the contour area
            area = cv2.contourArea(c)
            areaArray1.append(area)
            
            #sorting the area by size from large to small
        sorteddata1= sorted(zip(areaArray1, contours), key=lambda x: x[0], reverse=True)
            
        return sorteddata1 