import cv2
import pygame
import picamera
from picamera.array import PiRGBArray
import numpy as np
import time

pygame.init()
dispx=640
dispy=480
disp=pygame.display.set_mode((dispx,dispy))

face_cas=cv2.CascadeClassifier("./haarcascade_frontalface_alt_tree.xml")
running = True
image_no=0
bitchnumber=0
stay=False
camera = picamera.PiCamera()
camera.resolution = (400, 200)
camera.framerate = 60
raw = PiRGBArray(camera, size = (400, 200))
time.sleep(0.1)
while running:

    for i in camera.capture_continuous(raw, format = "bgr", use_video_port = True):
        if running:
            fram = i.array
            raw.truncate(0)
            fram=cv2.flip(fram,1)
            color_frame=fram
            fram=cv2.cvtColor(fram,cv2.COLOR_BGR2GRAY)
            faces=face_cas.detectMultiScale(fram)
            temp_disp=pygame.Surface(disp.get_size())

            for (x,y,z,a) in faces:
                detect=True
                cv2.rectangle(color_frame,(x,y+10),(x+w,z+a+20),(255,0,0))
                test=fram[y+30:y+h-15,x+10:x+z-10]
                dim = (300 , 300)
                try:
                    test = cv2.resize(test, dim, interpolation = cv2.INTER_AREA)
                except:
                    test=[]
            try:
                test_frame=cv2.cvtColor(test,cv2.COLOR_GRAY2RGB)
                test_frame=cv2.flip(test_frame,1)
                face_img=pygame.surfarray.make_surface(test_frame)
                face_img=pygame.transform.rotate(face_img,-90)
            except:
                print "error"
            finally:
                frame=cv2.cvtColor(color_frame,cv2.COLOR_BGR2RGB)
                frame=cv2.flip(frame,1)
                img=pygame.surfarray.make_surface(frame)
                img=pygame.transform.rotate(img,-90)
                temp_disp.blit(img,(0,0))
            for events in pygame.event.get():
                if events.type==pygame.QUIT:
                    running=False
                if events.type==pygame.KEYDOWN:
                    if (events.key==pygame.K_SPACE):
                        stay=not stay
                    if events.key==pygame.K_ESCAPE:
                        running=False
                    if events.key==pygame.K_TAB:
                        new_number+=1
                        image_no=0
                        print "hey number changed to "+str(bitchnumber)
                    if events.key==pygame.K_a:
                        new_number-=1
                        image_no=0
                        print "hey number changed to "+str(bitchnumber)


            if(stay==True and detect==True):
                image_no+=1
                if(image_no>=100):
                    stay= not stay
                print "Saved "+str(new_number)+str(image_no)
                cv2.imwrite("./pics/s"+str(new_number)+"/"+str(image_no)+".pgm",test)
            disp.blit(temp_disp,(0,0))
            disp.blit(face_img,(0,0))
            pygame.display.update()
        else:
            break
pygame.quit()
cv2.destroyAllWindows()
