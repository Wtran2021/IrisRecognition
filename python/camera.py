# Camera Code

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

def capture(enrOrver):
    # Init
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(17, GPIO.OUT)
    
    camera = PiCamera()
    camera.rotation = 180
    
    # Exec
    camera.start_preview()
    sleep(3)

    if not enrOrver:
        for i in range(2):
            if i == 1:
                GPIO.output(17, GPIO.HIGH)
                sleep(.1)
                GPIO.output(17, GPIO.LOW)
                # LED FLASHES before we capture
            camera.capture('../tempImgs/image%s.jpg' % i)
            if i == 0:
                sleep(3)
    else:
        camera.capture('../tempImgs/tempEnrimage.jpg')
        
    camera.stop_preview()
    
if __name__ == '__main__':
    capture(False) #default to verification
