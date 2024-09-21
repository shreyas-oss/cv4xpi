import cv2

class Sticker:
    
    areaArray=[]
    Count=1
    
    def __init__(self,contours,img):
        self.contours=contours
        self.img=img
        
        
    def sticker_for_loop(self):
        
        for i, c in enumerate(self.contours):
            
            #finding the largest area contour
            cnt = max(self.contours, key=cv2.contourArea)
            
            # to find the contour area
            area = cv2.contourArea(c)
            Sticker.areaArray.append(area)
            
            #first sort the array by area
            sorteddata=sorted(self.contours, key=cv2.contourArea, reverse=True)
            
            # finding the second largest Contour
            secondlargestcontour = sorteddata[2]
            
            # finding contour area
            area1=cv2.contourArea(cnt)
            area2=cv2.contourArea(secondlargestcontour)
            
            # extracting edge points of sticker
            x, y, w, h = cv2.boundingRect(secondlargestcontour)
            
            # condition to find second largest contour that is Sticker
            if (area2 >= area1/2.0):
                if ((w <= 2*h)or(h <= 2*w)):
                    secondlargestcontour = sorteddata[2][1]
                    x, y, w, h = cv2.boundingRect(secondlargestcontour)
            
            # Drawing Rectangle around the sticker       
            second_Largest_rect=cv2.rectangle(self.img, (x,y), (x+w, y+h), (0,0,0), -1)
            
        return  second_Largest_rect

