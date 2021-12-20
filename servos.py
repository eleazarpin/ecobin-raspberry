import RPi.GPIO as GPIO
import time
import smtplib
import requests
from time import sleep
from datetime import datetime
import sys

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#-------Variables para manejo de servo

pinServo1 = 37
pinServo2 = 3
pinServo3 = 40

#--------FUNCIONES---------------------------------------------
       
def moverServo(angulo,pin):
    #recibe un angulo entre 0 y 180 , ademas del pin GPIO donde esta
    #conectado el servo

    GPIO.setup(pin,GPIO.OUT)
    servo = GPIO.PWM(pin,50) # pin 37 con pulso 50Hz
    servo.start(0)# inicio PWM con valor 0 (pulso off)

    servo.ChangeDutyCycle(2+(angulo/18))
    time.sleep(0.5)
    #time.sleep(4)
    servo.ChangeDutyCycle(0)


def abrirTapaservo(pin):

    moverServo(120,pin) 
    time.sleep(10)
    moverServo(0,pin)

def abrirTapaservo3(pin):
    moverServo(80,pin) 
    time.sleep(10)
    moverServo(0,pin)


def probarServo():

    abrirTapaservo(pinServo1)
    abrirTapaservo(pinServo2)
    abrirTapaservo3(pinServo3)

    
    next = raw_input("CONTINUAR PROBANDO ? [Y/N]").lower()
    if next == 'y':
        probarServo()
       

#------------MAIN-----------------------------------------------

if __name__ == '__main__':
    
    try:
        
        print("******PRUEBA DE SERVOS******")        
        probarServo()
        
        
    except KeyboardInterrupt:
        print ("Interrupcion por teclado en main..")
        sys.exit()
    finally:
        print ("limpiando..")
        
        
 


