import RPi.GPIO as GPIO
import time
import smtplib
import requests
from email.mime.text import MIMEText
from picamera import PiCamera
from time import sleep
from datetime import datetime
import threading
import multiprocessing
from multiprocessing import Process, Lock, Array
import sys
import os
from PIL import Image


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#------manejo de Sensores ultrasonicos de cestos llenos

GPIO_TRIGGER1 = 11
GPIO_ECHO1 = 12
GPIO_TRIGGER2 = 33
GPIO_ECHO2 = 8
GPIO_TRIGGER3 = 31
GPIO_ECHO3 = 10

GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_TRIGGER3, GPIO.OUT)

GPIO.setup(GPIO_ECHO1, GPIO.IN)
GPIO.setup(GPIO_ECHO2, GPIO.IN)
GPIO.setup(GPIO_ECHO3, GPIO.IN)

# distancia a la que se consideran los cesto como llenos

cotaCesto1 = 31
cotaCesto2 = 31
cotaCesto3 = 29


bloquearCesto1 = 0
bloquearCesto2 = 0
bloquearCesto3 = 0



#------manejo de Sensor ultrasonico de objeto frente a la camara

GPIO_TRIGGER4 = 36
GPIO_ECHO4 = 38

GPIO.setup(GPIO_TRIGGER4, GPIO.OUT)
GPIO.setup(GPIO_ECHO4, GPIO.IN)
COTACamara = 30#DISTANCIA AL SENSOR 

#--------manejo de camara

#url = 'http://httpbin.org/post'
url = 'http://ec2-52-14-106-209.us-east-2.compute.amazonaws.com:3000/identificador'
#url = 'http://dev.ecobin.com.ar:3000/identificador'

NombreFoto = "/home/pi/Desktop/foto.jpg"

#---------LEDS

GPIO.setup(35, GPIO.OUT)#LED ROJO - OBJETO FRENTE A SENSOR
GPIO.setup(26, GPIO.OUT)#LED VERDE - OBJETO RECONOCIDO
GPIO.setup(32, GPIO.OUT)##LED ROJO - OBJETO NO RECONOCIDO

#-------Variables para manejo de servo

anguloServoApertura = 120
anguloServoCierre = 0
tiempoDeApertura = 5
pinServo1 = 37
pinServo2 = 3
pinServo3 = 40

#--------FUNCIONES---------------------------------------------

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
            
        # tiempo transcurrido
        TimeElapsed = endTime - startTime
        
        #multiplico por velocidad del sonido (34300 cm/s)
        #y divido por dos
        distance = (TimeElapsed * 34300) / 2
        
        #medicion = medicion + distance
        #contMedicion = contMedicion + 1
    
        #distance = medicion / 5
        return distance

def distancePromedio(pinTrig, pinEcho):
    lecturas=float(0.00)
    for cont in range(0,10,1):
        dist = distance(pinTrig, pinEcho)
        lecturas=lecturas+float(dist)
        time.sleep(0.2) 
        promedio=lecturas/10
        #print ("distancia de sensor de camara = %.1f cm" % dist)
    return promedio
    #print("PROMEDIO DE 10 LECTURAS: %.1f cm" % promedio)

def controlCestoLLeno(lock, cadEstado, trigger,ech,cota):
    try:

        nombreProceso = multiprocessing.current_process().name
        print ("Iniciando proceso de: %s" % nombreProceso)
        #print ("Inicio de proceso de control de cesto lleno PID: ", os.getppid())
        nombreCesto = ""
        if nombreProceso == "cesto1":
            nombreCesto = "Cesto de metal"
        if nombreProceso == "cesto2":
            nombreCesto = "Cesto de plastico"
        if nombreProceso == "cesto3":
            nombreCesto = "Cesto de papel y carton"
        
        mensaje= "El " + nombreCesto + " se encuentra lleno."

        banderaCesto = 0

        while (True):
            #print ("Inicio de proceso de control de cesto lleno PID: ", os.getppid())

            time.sleep(4) 

            dist = distancePromedio(trigger,ech)

            lock.acquire()

            print ("distancia a sensor de %s = %.1f cm" % (nombreProceso , dist))

            if(dist<cota and banderaCesto == 0):
                
                EnvioMail(mensaje) 
                print "Mail enviado....."
                banderaCesto = 1

                if (nombreProceso == 'cesto1'):
                    print ("BLOQUEO Cesto 1 \n")
                    cadEstado.value = "Lleno"
                                
                    
                if (nombreProceso == 'cesto2'):
                    print ("BLOQUEO Cesto 2 \n")
                    cadEstado.value = "Lleno"
                    
                    
                if (nombreProceso == 'cesto3'):
                    print ("BLOQUEO Cesto 3 \n")
                    cadEstado.value = "Lleno"
                    

            lock.release()

    except KeyboardInterrupt:
        print ("Interrupcion por teclado en proceso de %s " % nombreProceso)
        #sys.exit()
            
def EnvioMail(texto):

    try:
        
        with open('/home/pi/Desktop/ecobin-raspberry/direcMails.txt', 'r') as f:
            correo_destino = f.read().splitlines()
            print(correo_destino)

        correo_origen = 'ecobinargentina@gmail.com'
        password = 'Proyecto2020'
        msg = MIMEText(texto, _charset='UTF-8')
        msg['Subject'] = 'Estado de Ecobin'
        
        try:
            server = smtplib.SMTP('smtp.gmail.com',587)
            server.starttls()
            server.login(correo_origen,password)           
            server.sendmail(correo_origen,correo_destino,msg.as_string())
            print("Su Email ha sido enviado...")
            server.quit()

        except smtplib.SMTPException:
            print str(e)

    except (IOError,NameError,EOFError) as e:
        print str(e)
  
def moverServo(angulo,pin):
    #recibe un angulo entre 0 y 180 , ademas del pin GPIO donde esta
    #conectado el servo

    GPIO.setup(pin,GPIO.OUT)
    servo = GPIO.PWM(pin,50) # pin 11 con pulso 50Hz
    servo.start(0)# inicio PWM con valor 0 (pulso off)

    servo.ChangeDutyCycle(2+(angulo/18))
    time.sleep(0.5)
    servo.ChangeDutyCycle(0)
           
def sacarFoto():

    print("Sacando foto...") 

    try:

        try:
            
            P=PiCamera()
            P.resolution= (1280,720)
            P.ISO = 800 # ISO de 100 a 800
            P.brightness= 55 #brillo de 0 a 100
            #P.shutter_speed= 300000    #velocidad de obturacion 
            P.start_preview()
                
            #time.sleep(1) 
            P.capture(NombreFoto) 

            # Crop
            imagen = Image.open('/home/pi/Desktop/foto.jpg')
            region = (0,0,850,720)
            imagen_crop = imagen.crop(region)

            imagen_crop.save('/home/pi/Desktop/foto.jpg')
            
            #time.sleep(1)
            
            try:

                files = {'image': open ('/home/pi/Desktop/foto.jpg', 'rb')}            

                try:

                    dateTimeObj = datetime.now()
                    print(dateTimeObj)

                    response = requests.post(url, files=files)

                    dateTimeObj = datetime.now()
                    print(dateTimeObj)

                    try:
                
                        if response.status_code == 200:
                            print("Foto enviada...") 
                            #print response.content   
                            diccionarioJson = response.json() #crea un diccionario   
                            idMaterial = diccionarioJson['id']
                            nomMaterial = diccionarioJson['nombre']

                            print("idMaterial: %d " % idMaterial)
                            print("nomMaterial: %s " % nomMaterial)

                            abrirCestoPorCamara(idMaterial)

                        else:
                            print "Error!! Status Code: ",response.status_code  

                    except (KeyError) as e: 
                        print str(e)

                except requests.exceptions.RequestException as e: 
                    print e    
            
            except (IOError) as e:
                print str(e)   

        except picamera.exc.PiCameraError:
            print('Problemas con la camara')
            EnvioMail("Problemas con la camara..")

    except KeyboardInterrupt:
        print ("Interrupcion por teclado en sacarFoto ")
        sys.exit()

    finally:
        P.stop_preview()
        P.close()

def fotografiar(lock):
    try:


        print ("Proceso Fotografiar PID: ", os.getppid())

        while True:

            
            
            dist = distancePromedio(GPIO_TRIGGER4,GPIO_ECHO4)
            print ("distancia a sensor de CAMARA = %.1f cm" % dist)
            

            if(dist<COTACamara):
                GPIO.output(35, True)    #prendo led de aviso de camara 
                print("OBJETO DETECTADO FRENTE A CAMARA...") 

                sacarFoto()
                
                # este es el tiempo que tiene para iniciar el proximo reconocimiento
                # una vez que se apague el led
                time.sleep(2)
                GPIO.output(35,False)    #apago led de aviso de camara

    except KeyboardInterrupt:
        print ("Interrupcion por teclado en proceso de control camara..")
        sys.exit()

def abrirCestoPorCamara(id):

    if (id == 0 or id == 1 or id == 7 or id == 6):
        print "OBJETO NO ADMITIDO"
        GPIO.output(32, True)
        time.sleep(5)
        GPIO.output(32, False)
     
    if (id == 5 ):
        print "Abro cesto 1"
        GPIO.output(26, True)
        moverServo(anguloServoApertura,pinServo1)
        time.sleep(tiempoDeApertura)
        moverServo(anguloServoCierre,pinServo1)
        GPIO.output(26, False)
        
   
    if (id == 4 ):  
        print "Abro cesto 2"    
        GPIO.output(26, True)
        moverServo(anguloServoApertura,pinServo2)
        time.sleep(tiempoDeApertura)
        moverServo(anguloServoCierre,pinServo2)
        GPIO.output(26, False)
        

    if (id == 3 or id == 2 ):
        print "Abro cesto 3"    
        GPIO.output(26, True)
        moverServo(80,pinServo3)  
        time.sleep(tiempoDeApertura)
        moverServo(anguloServoCierre,pinServo3) 
        GPIO.output(26, False)
        
       

#------------MAIN-----------------------------------------------

#while True:
if __name__ == '__main__':
    
    try:
        
        print("******MAIN******") 
        print("Presione ctrl-c para finalizar...") 
        print("PROCESO MAIN PID: %d " % os.getppid())

        lock = Lock() #semaforo


        #MEMORIA COMPARTIDA
        estadoCesto1 = Array("c", 11)
        estadoCesto2 = Array("c", 11)  
        estadoCesto3 = Array("c", 11)  
        estadoCesto1.value = "Libre"
        estadoCesto2.value = "Libre"
        estadoCesto3.value = "Libre"


        #CREACION DE PROCESOS DE CONTROL DE LLENADO
        # procesoCestoLleno1 = multiprocessing.Process( name='cesto1' ,target=controlCestoLLeno , args=(lock, estadoCesto1, GPIO_TRIGGER1,GPIO_ECHO1,cotaCesto1,))
        # procesoCestoLleno2 = multiprocessing.Process( name='cesto2' ,target=controlCestoLLeno , args=(lock, estadoCesto2, GPIO_TRIGGER2,GPIO_ECHO2,cotaCesto2,))
        # procesoCestoLleno3 = multiprocessing.Process( name='cesto3' ,target=controlCestoLLeno , args=(lock, estadoCesto3, GPIO_TRIGGER3,GPIO_ECHO3,cotaCesto3,))

        #CREACION DE PROCESO DE MANEJO DE CAMARA DE LA RASPBERRY
        procesoFotografiar = multiprocessing.Process(target=fotografiar , args=(lock,))
        
        #INICIO PROCESOS
        # procesoCestoLleno1.start()
        # procesoCestoLleno2.start()
        # procesoCestoLleno3.start()
        procesoFotografiar.start()

        
        #FINALIZACION DE PROCESOS
        # procesoCestoLleno1.join()
        # procesoCestoLleno2.join()
        # procesoCestoLleno3.join()
        procesoFotografiar.join()
       
        
    except KeyboardInterrupt:
        print ("Interrupcion por teclado en main..")
        sys.exit()
    finally:
        print ("limpiando todo....")

        #cierro cestos
        moverServo(anguloServoCierre,pinServo1)
        moverServo(anguloServoCierre,pinServo2)
        moverServo(anguloServoCierre,pinServo3)
        GPIO.output(35, False)
        GPIO.output(32, False)
        GPIO.output(26, False)
        GPIO.cleanup()
        
     
    #time.sleep(1)
 


