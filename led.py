import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

#LED VERDE OBJETO RECONOCIDO
GPIO.setup(26, GPIO.OUT)

#LED ROJO OBJETO NO RECONOCIDO
GPIO.setup(32, GPIO.OUT)

#LED ROJO OBJETO FRENTE A CAMARA
GPIO.setup(35, GPIO.OUT)

def probarLEDS():
    print("LED VERDE OBJ. RECONOCIDO") 
    GPIO.output(26, True)
    time.sleep(5)
    print("LED ROJO OBJ. NO RECONOCIDO") 
    GPIO.output(32, True)
    time.sleep(5)
    print("LED ROJO OBJ. FRENTE A CAMARA") 
    GPIO.output(35,True)
    time.sleep(5)
    GPIO.output(26,False)
    GPIO.output(32,False)
    GPIO.output(35,False)

    next = raw_input("CONTINUAR PROBANDO ? [Y/N]").lower()
    if next == 'y':
        probarLEDS()


if __name__ == '__main__':
    
    try:
        
        print("******PRUEBA DE LEDS******")        
        probarLEDS()
        
        
    except KeyboardInterrupt:
        print ("Interrupcion por teclado en main..")
        sys.exit()
    finally:
        print ("limpiando..")
        GPIO.cleanup()



