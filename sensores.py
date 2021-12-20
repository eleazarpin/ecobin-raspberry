import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#sensor de proximidad a camara
GPIO_TRIGGER1 = 36
GPIO_ECHO1 = 38


#sensor cesto 1
GPIO_TRIGGER2 = 11
GPIO_ECHO2 = 12

#sensor cesto 2
GPIO_TRIGGER3 = 33
GPIO_ECHO3 = 8

#sensor cesto 3
GPIO_TRIGGER4 = 31
GPIO_ECHO4 = 10


def distance(trig,echo):
    
    # set Trigger High  

    GPIO.output(trig, True)
    
    # set Trigger after 0.1ms low
    time.sleep(0.00001)
    GPIO.output(trig, False)
    
    startTime = time.time()
    endTime = time.time()
        
    while GPIO.input(echo) == 0:
        startTime = time.time()
        
    while GPIO.input(echo) == 1:
        endTime = time.time()
        
    # elapsed time
    TimeElapsed = endTime - startTime
    # multiply with speed of sound (34300 cm/s)
    # and division by two
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
def distancePromedio(pinTrig, pinEcho):
    GPIO.setup(pinTrig, GPIO.OUT)
    GPIO.setup(pinEcho, GPIO.IN)

    lecturas=float(0.00)
    for cont in range(0,10,1):
        dist = distance(pinTrig, pinEcho)
        lecturas=lecturas+float(dist)
        time.sleep(0.2) 
        promedio=lecturas/10
        print ("distancia de sensor= %.1f cm" % dist)
    return promedio
    print("PROMEDIO DE 10 LECTURAS: %.1f cm" % promedio)

def probarSensores():
    print("--- SENSOR ACTIVADOR DE CAMARA ---" )
    distancePromedio(GPIO_TRIGGER1, GPIO_ECHO1)

    print("--- SENSOR DE LLENADO CESTO 1 ---" )
    distancePromedio(GPIO_TRIGGER2, GPIO_ECHO2)
    
    print("--- SENSOR DE LLENADO CESTO 2 ---" )
    distancePromedio(GPIO_TRIGGER3, GPIO_ECHO3)

    print("--- SENSOR DE LLENADO CESTO 3 ---" )
    distancePromedio(GPIO_TRIGGER4, GPIO_ECHO4)

    next = raw_input("CONTINUAR PROBANDO ? [Y/N]").lower()
    if next == 'y':
        probarSensores()


if __name__ == '__main__':
    
    try:
        
        print("******PRUEBA DE SENSORES******")        
        probarSensores()
        
        
    except KeyboardInterrupt:
        print ("Interrupcion por teclado en main..")
        sys.exit()

 

