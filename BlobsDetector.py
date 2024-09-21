# -*- coding: utf-8 -*-
"""
Created on Wed Jul 20 20:45:28 2022

@author: mayur
"""
import cv2
import numpy as np

class BlobsDetector(object):
    
    def __init__(self,img):
        self.img=img
        
    def detect_blobs(self):
        
        # Initialize the blob detector using default parameters
        detector=cv2.SimpleBlobDetector_create()
        
        # Detect blobs
        keypoints_default=detector.detect(self.img)
        
        # Draw blobs on our image as red circles
        blank_default=np.zeros((1,1))
        blobs=cv2.drawKeypoints(self.img,keypoints_default,blank_default,(0,0,255),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Print number of blobs
        number_of_blobs=len(keypoints_default)
        text_Blob="total no of Holes--" + str(len(keypoints_default))
        cv2.putText(blobs,text_Blob,(20,640),cv2.FONT_HERSHEY_SIMPLEX,1,(100,0,255),2)
        
        # initialize parameter setting using cv2.SimpleBlobDetector
        params=cv2.SimpleBlobDetector_Params()
        
        # Set area filtering parameters
        params.filterByArea=True
        params.minArea=10
        
        # Set circularity filtering parameters
        params.filterByCircularity=True
        params.minCircularity=0.9 #0.85
        
        # Set convexity filtering parameter
        params.filterByConvexity=False
        params.minConvexity=0.2  #0.25
        
        # Set inertia filtering parameter
        params.filterByInertia=True
        params.minInertiaRatio=0.01  #0.015
        
        # Create detector with parameter
        detector=cv2.SimpleBlobDetector_create(params)
        
        # detect blobs
        Keypoints=detector.detect(self.img)
        
        # Draw perfect circles on the images as green circles
        blank=np.zeros((1,1))
        Circles=cv2.drawKeypoints(self.img,Keypoints,blank,(0,255,0),cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        number_of_blobs=len(Keypoints)
        
        text="total no of holes without defects--" + str(len(Keypoints))
        Circles=cv2.putText(Circles,text,(20,680),cv2.FONT_HERSHEY_SIMPLEX,1,(0,100,255),2)
        Circles=cv2.putText(Circles,text_Blob,(20,650),cv2.FONT_HERSHEY_SIMPLEX,1,(100,0,255),2)
        
        return Circles , Keypoints