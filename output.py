import subprocess
import time
from io import open

#variables
aux=""
aux1=""
aux2=""
pose=""
mode=""
info=""
cad=""
roll=0
pitch=0
yaw=0
cad_roll=""
cad_pitch=""
cad_yaw=""


# Ejecutar el archivo .exe (hello-myo.exe en este caso)
process = subprocess.Popen("hello-myo.exe", stdout=subprocess.PIPE, universal_newlines=True)
#print("Se ejecutó el archivo .exe")
#time.sleep(3)        

# Leer y mostrar la salida
while process.poll() is None:

    output = process.stdout.readline().rstrip()
    if output != aux and output != "Attempting to find a Myo..." and output != "Connected to a Myo armband!":
        archivo = open("data_temp.txt", "w")
        archivo.write(output)

        aux=output
        archivo.close()
        cad_roll=output[1:19]
        cad_pitch=output[21:39]
        cad_yaw=output[41:59]

        mode=output[61:69].replace(" ","")
        pose=output[74:88].replace(" ","")
        
        roll, pitch, yaw = 0, 0, 0

        for i in range(0,17):
            if cad_roll[i]=="*" and roll<=100 and roll>=0:
                roll+=5
            if cad_pitch[i]=="*" and pitch<=100 and pitch>=0:
                pitch+=5
            if cad_yaw[i]=="*" and yaw<=100 and yaw>=0:
                yaw+=5
        #print("Roll:",roll)
        #print("Pitch:",pitch)
        #print("Yaw:",yaw)

        if mode!=aux2 or pose!=aux1:
            aux2=mode
            aux1=pose
            info = aux2 + "," + aux1
        #print(info)
        
        #Impresión de datos
        print(f"{roll},{pitch},{yaw}")

'''
print("Salimos del bucle")
exit_code = process.returncode
print("El programa ha finalizado con código de salida:", exit_code)
'''