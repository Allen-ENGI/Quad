import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

GPIO.setup(37, GPIO.OUT)

pwm = GPIO.PWM(37, 50)
#initialize the duty cycle
pwm.start(0)

def wait(angle):
    #5V
    time = angle/60 * 0.16
    #6V
    time = angle/60 * 0.14
    return time
    
def SetAngle(angle):

    #range from 2.5% to 12.5%
    duty = angle/18 + 2.5
    time = duty * 2
    print(duty)
    GPIO.output(37, True)
    pwm.ChangeDutyCycle(duty)
    #sleep time to reach the angle
    sleep(0.52)
    #reduce oscillation
    pwm.ChangeDutyCycle(0)
    sleep(0.1)
    #GPIO.output(37, False)

SetAngle(0)

for i in range (0, 180, 10):

    SetAngle(i)

pwm.stop()
GPIO.cleanup()