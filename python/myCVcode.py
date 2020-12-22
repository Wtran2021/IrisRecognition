#Adapted OpenCV Example Code
#Joshua Teixeira
#ECE597SD Iris Dilation Detection on CASIA1 DB Images
#    with custom image code and verification tie-in

#Imports
import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import camera, enroll_single, verify

# Flags
attack = False # true means we have no dilated eye image
cap = False # True means we take photos using camera.py

#Code
def areaCalc(fileName): 
    img = cv2.imread(fileName,0)
    
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                                param1=50,param2=50,minRadius=30,maxRadius=100)

    circles = np.uint16(np.around(circles))

    for i in circles[0,:]:
        area = 3.14159265 * i[2] * i[2]
        #print(area)
        
    return area

def enroll():
    #enroll code
    if cap:
        camera.capture(True)
    # This is where the photo would be saved if it worked:
    # fileName = '../tempImgs/tempEnrimage.jpg'
    # Hard code the image to enroll since our photos dont work... ;(
    fileName = '../tempImgs/10/debugEnroll.jpg'
    enroll_single.execfun(fileName)
    
def verification():
    #verify code
    # Capture Photos
    if cap:
        camera.capture(False)

    # Presentation Attack Detection/Mitigation
    # These params used for debug since camera set up is inadequate
    if not attack:
        normEye = '../CASIA1/2/002_1_2.jpg'
        dillEye = '../CASIA1/D/002_1_1D.jpg'
    else:
        normEye = '../CASIA1/2/002_1_2.jpg'
        dillEye = '../CASIA1/2/002_1_2.jpg'

    # Pupil Dilation measurment and calculations
    area1 = areaCalc(normEye)
    area2Dil = areaCalc(dillEye)

    diff = ((area2Dil - area1)/area1)
    print(area1, area2Dil, diff)

    # Semi-arbitrary 25% threshold, depends on person but dilation could be 20-50%
    if (abs(diff))>.25:
        print('This is likely a human eye, dilation factor of %.2f%%\n' %(100*abs(diff)))
        
        # Attempt to verify if this human is a registered user
        verify.execfun(normEye, './templates/temp/')
        
    else:
        print('This is potentially an attack, insignificant/no dilation detected \n')
        print('Dilation factor of %.2f%%' %(100*abs(diff)))
        print('Verification process stopped. Please try again/contact your administrator\n')

##---------------------------------------------------------------------
# Execution here. Basically we take two photos with camera code, then
# we compare their size, and if they are not different enough then we
# know the pupil has not dilated, thus this could be a presentation atk
##---------------------------------------------------------------------
# -----------Init--------------
# Input switches for enrollment/verification selection
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # enroll, green, default low
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # verify, blue, default low

#-------------Exec-----------------
print('Entering loop')
while True:
    if GPIO.input(27):
        # enrollment code
        sleep(.1)
        print('Enrollment underway\n')
        enroll()
        print('Enrollment complete\n')
    elif GPIO.input(22):
        #verification code
        sleep(.1)
        print('Verification underway\n')
        verification()
        print('Verification complete\n')

    