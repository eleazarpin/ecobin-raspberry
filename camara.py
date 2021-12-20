import time
from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image


P=PiCamera()
P.resolution= (1280,720)
P.start_preview()

filePath = "/home/pi/Desktop/FotosPiCamara/"

def probarCamara():
  
	print("Sacando foto...") #camera warm-up time 
	time.sleep(1) 
	currentTime = datetime.now()
	picTime = currentTime.strftime("%Y.%m.%d-%H%M%S")
	picName = picTime + '.jpg'
		
	NombreFoto = filePath + picName 
	P.capture(NombreFoto) 

    # Crop
	imagen = Image.open(NombreFoto)
	# Left Up Right Low
	region = (0,0,850,720)
	imagen_crop = imagen.crop(region)

	imagen_crop.save(NombreFoto)

	time.sleep(2)

	next = raw_input("CONTINUAR PROBANDO ? [Y/N]").lower()
	if next == 'y':
		probarCamara()


if __name__ == '__main__':
    
    try:
        
        print("******PRUEBA DE CAMARA******")        
        probarCamara()
        
        
    except KeyboardInterrupt:
        print ("Interrupcion por teclado en main..")
        sys.exit()

