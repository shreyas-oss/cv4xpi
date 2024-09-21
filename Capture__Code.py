import cv2
import os
import time
start_time = time.time()

def show_webcam(mirror=False):
                scale=10

                cam = cv2.VideoCapture(0)

                cv2.namedWindow("Captured")

                img_counter = 1

                while True:
                  ret_val,image = cam.read()
                  if mirror:
                    image = cv2.flip(image, 1)
                                
                 #get the camera size
                  height, width, channels = image.shape
                
                 #prepare the crop
                  centerX,centerY = int(height/2), int(width/2)
                  radiusX,radiusY = int(scale*height/100), int(scale*width/100)
                
                  minX,maxX = centerX-radiusX, centerX+radiusX
                  minY,maxY = centerY-radiusY, centerY+radiusY
                
                  cropped = image[minX:maxX, minY:maxY]
                  resized_cropped = cv2.resize(cropped, (width, height))
                
                  cv2.imshow('Press SPACE to Capture', resized_cropped)
                
                

                  k = cv2.waitKey(1)
    
                  if k%256 == 27:
                  # ESC pressed
                    print("Escape hit, closing...")
                    break
      
                  curr_time = int(time.time())
                  time_elasped = curr_time-int(start_time)
                  if(time_elasped==80):
                    break
                                
                 #add + or - 5 to zoom
                 
                 #Zoom in 
                  if k%256 == 82:
                   scale +=5
                 
                 #Zoom out  
                  if k%256 == 84:
                   scale = 5
                
                  elif k%256 == 32:
                  # SPACE pressed
                    img_name = "Test_{}.png".format(img_counter)
                    path = '/home/ubuntu/Pictures'
                    cv2.imwrite(os.path.join(path , img_name), image)
                    print("{} Captured!".format(img_name))
                    img_counter += 1
                    time.sleep(0.005)

                cam.release()

                cv2.destroyAllWindows()

def main():
                show_webcam(mirror=True)
                
if __name__ == '__main__':
                main()
