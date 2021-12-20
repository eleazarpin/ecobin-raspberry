import smtplib
from email.mime.text import MIMEText

correo_origen = 'ecobinargentina@gmail.com'
password = 'Proyecto2020'
correo_destino = ["eleazarpinetchave@gmail.com"]
#correo_destino = ['alexserrano.unlam@gmail.com', 'leacanella@yahoo.com.ar','braian.fritz@gmail.com','eleazarpinetchave@gmail.com']


msg = MIMEText("Se encuentra el cesto del sistema ecobin lleno")
msg['Subject'] = 'Cesto lleno'
msg['From'] = correo_origen
msg['To'] = ", ".join(correo_destino)
#msg['To'] = correo_destino

server = smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(correo_origen,password)
server.sendmail(correo_origen,correo_destino,msg.as_string())

print("Su Email ha sido enviado.")

server.quit()
