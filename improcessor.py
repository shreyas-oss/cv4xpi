# Step-1   Importing Required Libraries
import cv2
import numpy as np
import datetime
import copy
from BlobsDetector import BlobsDetector as bd
from BoardDetector import Board 
from Contoursa import Contoursa as ca
from Contoursza import Contourszip as zipcontour
from StickerDetection import Sticker
from logger import logger
from watchdog.observers.polling import PollingObserver
from watchdog.events import FileSystemEventHandler
from time import sleep


class ImageProcessor:
    
    def run(self,new_image_path):
        
        # Step-2 Calculating the start time

        before=datetime.datetime.now()

        # Step-3 Read the original image

        image = cv2.imread(new_image_path)

        # Step-4 Resize the image for further processing

        img_main=image[50:480,0:640]

        # Image copy for next steps

        img=copy.copy(img_main)
        img1=copy.copy(img_main)
        img2=copy.copy(img_main)
        img_x=copy.copy(img_main) 
        Out_img=copy.copy(img_main)

        # Step-5 Convert the image to graycsale image

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Step-6 Detect the edges in Grayscale image using Canny Edge Detection

        edges = cv2.Canny(image=gray, threshold1=30, threshold2=255)

        # Step-7 Perform Morphological operation that is Image Dilation on the Cannyedge image from previous step

        kernel = np.ones((7,7), dtype=np.uint8)
        img_dilation = cv2.dilate(edges, kernel, iterations=1)

        # Step-8 Detect the contours on the binary image obtained from image dilatin

        contours, hierarchy = cv2.findContours(img_dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        # Step-9 Board Detection in the Image using BOARD library
        # Detecting the board and drawing a Rectangle around it

        lr=Board(contours,img)
        Largest_rect=lr.board_contour()

        # Step-10 Finding the Sticker in the Image and drawing Rectangle around it

        Stck=Sticker(contours,img)
        second_Largest_rect=Stck.sticker_for_loop()

        # Step-11 Detecting Drilled holes in the Board
        Cir = bd(img)
        Circle,Key=Cir.detect_blobs()

        # Step-12 Removing sticker from Canny edge image from step-6

        # Draw a rectangular mask with withe backgroung
         
        mask = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255

        #  Draw sticker on the mask using step-10

        Stck=Sticker(contours,mask)
        second_Largest_rect=Stck.sticker_for_loop()

        #removing sticker from Canny edge image from step-6 using bitwise_and function
        Bitw = cv2.bitwise_and(edges, edges, mask=mask)

        # Step-13 Sort out defects in the board and display on the board

        # Condition if number of holes in board are greater than zero

        if len(Key)>0:
            # All the below steps are for Board with drilled holes
            # Extracting Defects inside the Board
            
            # Step-A Remove all the non defective holes from the image
            
            for x in range(0,len(Key)):
                black_blobs=cv2.circle(Bitw, (int(Key[x].pt[0]),int((Key)[x].pt[1])), radius=int((Key)[x].size), color=(-1), thickness=-1)
            
            # Step-B Perform Morphological operation that is Image Dilation on the image from previous step
            
            img_dilation_B = cv2.dilate(black_blobs, kernel, iterations=1)
            
            # Step-C Detect the contours on the binary image obtained from image dilatin
            contours_B, hierarchy = cv2.findContours(img_dilation_B, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            # Step-D Find the Biggest contours from the dilated image
            
            bb = zipcontour(contours_B)
            sorteddata=bb.for_loop()
            
            big_contour_B = sorteddata[0][1],sorteddata[1][1]
                
            # Step-E Removing the Biggest contour from the Binary image obtained from Step-12
            
            cv2.drawContours(image=black_blobs, contours=big_contour_B, contourIdx=-1, color=(0,0,0),thickness=-1,lineType=cv2.LINE_AA)
            
            #Step-F finding contours in image obtained from Step-E to obtain Defects in image 
            
            contours_B, hierarchy = cv2.findContours(black_blobs, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            # Step-G Draw the defects on the main image
            
            cv2.drawContours(image=Out_img, contours=contours_B, contourIdx=-1, color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)

        else :
            # All the below steps are for Board without drilled holes
            
            # Step-A Perform Morphological operation that is Image Dilation on the binary image from step-12
            
            img_dilation_B = cv2.dilate(Bitw, kernel, iterations=1)
            
            # Step-B Detect the contours on the binary image obtained from image dilatin
            
            contours, hierarchy = cv2.findContours(img_dilation_B, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            # Step-C Find the Biggest contours from the dilated image
            
            bb = zipcontour(contours)
            sorteddata=bb.for_loop()
            
            big_contour_B = sorteddata[0][1],sorteddata[1][1]
               
            # Step-D Removing the Biggest contour from the Binary image obtained from Step-12
            
            cv2.drawContours(image=Bitw, contours=big_contour_B, contourIdx=-1, color=(0,0,0),thickness=-1,lineType=cv2.LINE_AA)
         
            #Step-E finding contours in image obtained from Step-E to obtain Defects in image 
            
            contours, hierarchy = cv2.findContours(Bitw, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            # Step-F Draw the defects on the main image
            
            cv2.drawContours(image=Out_img, contours=contours, contourIdx=-1, color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)


        #  Detecting edge defects of the Board

        # Step-14 Perform Morphological operations

        kernel = np.ones((2,2), dtype=np.uint8)
        img_dilation = cv2.dilate(edges, kernel, iterations=1)

        # Step-15 detect the contours on the binary image

        contours,hierarchy = cv2.findContours(img_dilation,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Step-16 Find the Biggest contours that is board from the dilated image

        ec = zipcontour(contours)
        sorteddata=ec.for_loop1(contours)

        big_contour = sorteddata[0][1],sorteddata[1][1]

        cnt = max(contours, key=cv2.contourArea)
        x1,y1,w1,h1 = cv2.boundingRect(cnt)

        Largest_rect=cv2.rectangle(img1, (x1,y1), (x1+w1, y1+h1), (255,255,0), 1)

        # Step-17 Create a rectangular mask with white background

        mask_C = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255

        # draw contours on the image
        cv2.drawContours(image=mask_C, contours=big_contour, contourIdx=-1, color=(0,0,0),thickness=-1,lineType=cv2.LINE_AA)

        # Step-18 finding the outer edge of the board in from the mask image

        contours,hierarchy = cv2.findContours(mask_C,cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

        # Step-19 Create a rectangular mask with white background

        mask = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255

        # Step-20 get the board contour from previous step

        ec = zipcontour(contours)
        sorteddata=ec.for_loop1(contours)

        big_contour = sorteddata[2][1],sorteddata[2][1]

        # draw contours on the  mask image

        cv2.drawContours(image=mask, contours=big_contour, contourIdx=-1, color=(0,0,0),thickness=1,lineType=cv2.LINE_AA)

        # Step-21 finding the number of edges in the contour

        big_contour = sorteddata[2][1]

        accuracy=0.03*cv2.arcLength(big_contour,True)
        approx=cv2.approxPolyDP(big_contour,accuracy,True)

        # Step-22 condition for board with slots and without slots

        if(len(approx)>4):
            
            # Step-A  creating a rectangular mask with white background
            
            mask = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255
            
            # Step-B  Perform Morphological operations
            
            kernel = np.ones((5,5), dtype=np.uint8)
            closing = cv2.morphologyEx(mask_C, cv2.MORPH_CLOSE, kernel)

            # Step-C  finding contours in the closing image
            
            contours,hierarchy = cv2.findContours(closing,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            # Step-D  finding the slot in the contour

            ec = zipcontour(contours)
            sorteddata=ec.for_loop1(contours)

            secondlargestcontour = sorteddata[1][1]
            
            # Step-E  getting the slot end points
            
            x, y, w, h = cv2.boundingRect(secondlargestcontour)
            
            # Step-F  condition for slot position
            
            if((x-x1)>15):
                
                second_Largest_rect=cv2.rectangle(img1, (x,y), (x+w+((x1+w1)-(x+w)), y+h), (255,255,0), 1)
                
            else:
                
                second_Largest_rect=cv2.rectangle(img1, (x-(x-x1),y), (x+w, y+h), (255,255,0), 1)
            
            # Step-G  drawing a rectangle using Board end points
            
            mask_N3 = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255
            
            Largest_rect1=cv2.rectangle(mask_N3, (x1,y1), (x1+w1, y1+h1), (0,0,0), -1)

            # Step-G  drawing a rectangle using slot end points
            
            mask_N4 = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255
            
            if((x-x1)>15):
                
                Slot_rect1=cv2.rectangle(mask_N4, (x,y), (x+w+((x1+w1)-(x+w)), y+h), (0,0,0), -1)
                
            else:
                
                Slot_rect1=cv2.rectangle(mask_N4, (x-(x-x1),y), (x+w, y+h), (0,0,0), -1)

            # Step-H  subtracting slot rectangle from board to get the desired Board cotour

            subtracted=cv2.subtract(mask_N4, mask_N3)

            # Step-I  Get the board outer edges with no edge defects and drawing it on image
            
            contours,hierarchy = cv2.findContours(subtracted,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) 
            
            mask_N6 = np.ones(Largest_rect.shape[:2], dtype="uint8") * 255
            
            BC = zipcontour(contours)
            sorteddata=BC.for_loop()
            
            big_contour_T = sorteddata[0][1],sorteddata[0][1]

            cv2.drawContours(image=mask_N6, contours=big_contour_T, contourIdx=-1, color=(0,0,255),thickness=-1,lineType=cv2.LINE_AA)
            
            # Step-J  get the outer edge of the board
            
            edges_X = cv2.Canny(image=mask_N6, threshold1=50, threshold2=255)
            
            contours,hierarchy = cv2.findContours(edges_X,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            AA=ca(contours)
            sorteddata=AA.for_loop()
            
            big_contour_X = sorteddata[1]
            
            # Step-K  get the outer edge of the original board
            
            cv2.drawContours(image=img2, contours=big_contour_X, contourIdx=-1, color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
         
            contours,hierarchy = cv2.findContours(img_dilation,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            
            aa=ca(contours)
            sorteddata=aa.for_loop()
            
            big_contour_Y = sorteddata[1]
            
            img3=img_main
            
            cv2.drawContours(image=img3, contours=big_contour_Y, contourIdx=-1, color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
            
            # Step-L  Comparing the original board edges with the created edges
            
            match=cv2.matchShapes(big_contour_X,big_contour_Y,1,0.0)
            print(match)
            
            # if (match>0.0055):0.026
            if (match>0.036):
                
                cv2.drawContours(image=Out_img, contours=big_contour_Y, contourIdx=-1, color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
                
            else:
                
                cv2.drawContours(image=Out_img, contours=big_contour_Y, contourIdx=-1, color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)

            cv2.imshow("Defects_in_Image", Out_img)
            cv2.waitKey(0)

        else:
            
            # Edge defects of the boards without slots
            
            # Step-A create a gray scale image

            gray = cv2.cvtColor(img_x, cv2.COLOR_BGR2GRAY)

            #  Step-B Canny Edge Detection
            
            edges = cv2.Canny(image=gray, threshold1=50, threshold2=255)
            
            #  Step-C Perform morphological operation
            
            kernel_D = np.ones((7,7), dtype=np.uint8)
            img_dilation_1 = cv2.dilate(edges, kernel_D, iterations=1)

            # Sort out defects in the board and display on the board

            # Step-D Creating Mask
            
            mask_M = np.ones(Largest_rect.shape[:2], dtype="uint8") * 0
            
            # Step-E drawing a rectangle with board edge points

            Largest_rect_Mask=cv2.rectangle(mask_M, (x1,y1), (x1+w1, y1+h1), (255,255,0), 1)
          
            # Step-F  getting outer contours of the rectangle
            
            contours31, hierarchy = cv2.findContours(mask_M, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            # Step-G  getting outer contours of the Board
            
            contours32, hierarchy = cv2.findContours(img_dilation_1, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
              
            # Step-H  getting outer contours of the rectangle
            
            aa=ca(contours31)
            sorteddata=aa.for_loop()
            
            largestcontourExternal = sorteddata[0]
            
            # Step-I  getting outer contours of the Board
            
            aa=ca(contours32)
            sorteddata=aa.for_loop()
            
            secondlargestcontour = sorteddata[1]
            

            # Step-J Matching Contour Shapes
            
            ret = cv2.matchShapes(largestcontourExternal,secondlargestcontour,1,0.0)
            print(ret)
            
            if (ret>0.0045):
                cv2.drawContours(image=Out_img, contours=secondlargestcontour, contourIdx=-1, color=(0,0,255),thickness=2,lineType=cv2.LINE_AA)
                
            else:
                cv2.drawContours(image=Out_img, contours=secondlargestcontour, contourIdx=-1, color=(0,255,0),thickness=2,lineType=cv2.LINE_AA)
                
            #cv2.imshow("Defects_in_Image", Out_img)
            
            image_write_status = cv2.imwrite('/aci/image_with_defects.png', Out_img)
            print("the image is written", image_write_status)
            

class NewFileWatcher:
    """
    Watch given directory for new files and execute callback when one is seen
    The callback will be called with one argument: the path of the new file.
    """

    def __init__(self, directory, callback, sleep_time=1):
        self.directory = directory
        self.callback = callback
        self.sleep_time = sleep_time

    def watch(self):
        """
        Start watching
        """
        logger.info('Watching directory %s' % self.directory)

        # Set up handler for when we see new files
        callback = self.callback

        class NewFileEventHandler(FileSystemEventHandler):
            def on_created(self, event):
                if not event.is_directory:
                    src = event.src_path
                    #str1, str2, str3 = str(src).split(".")
                    # dst = str1 + str2 + "_mod." + str3
                    # os.rename(src,dst)
                    logger.info('Detected new file: %s' % str(src))
                    process = ImageProcessor()
                    process.run(str(src))
                    callback(event.src_path)

        event_handler = NewFileEventHandler()

       

        # Use polling observer (rather than filesystem-specific observers),
        # because it is more reliable.
        observer = PollingObserver(timeout=self.sleep_time)

        # Start the observer
        observer.schedule(event_handler, self.directory, recursive=False)
        observer.start()

        # Wait while the observer is running
        try:
            while True:
                sleep(self.sleep_time)
        # Exit gracefully
        except KeyboardInterrupt:
            logger.info('Detected interrupt. Stopping observer.')
            observer.stop()
        observer.join()


# Demo functionality: watch the current directory and print any new files
if __name__ == "__main__":
    directory = '/aci/'
    NewFileWatcher(directory, lambda path: print(path)).watch()




