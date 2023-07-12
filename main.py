import tkinter as tk
from tkinter import ttk
import subprocess
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

class MyoInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configurar la ventana principal
        self.title("Interfaz Myo Armband")
        self.geometry("900x600")
        self.resizable(False, False)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular las coordenadas para centrar la ventana
        x = int((screen_width / 2) - (900 / 2))
        y = int((screen_height / 2) - (600 / 2))
        self.geometry(f"900x600+{x}+{y}")

        # Crear variables para los valores de las barras de progreso
        self.progress_x = tk.DoubleVar()
        self.progress_y = tk.DoubleVar()
        self.progress_z = tk.DoubleVar()


        self.positions = [
            ("Contracción de los dedos", "images/image_pose_fist.png"),
            ("Extensión de los dedos", "images/image_pose_fingers_spread.png"),
            ("Muñeca hacia adentro", "images/image_pose_wave_in.png"),
            ("Muñeca hacia afuera", "images/image_pose_wave_out.png")
        ]

        # Crear una lista de variables de control para los Checkbutton
        self.check_vars = [tk.BooleanVar() for _ in range(len(self.positions))]


        # Variable para realizar el seguimiento del nombre del paciente anterior
        self.previous_patient_name = ""

        # Crear widgets de la interfaz
        self.create_patient_entry()
        self.create_progress_bars()
        self.create_position_checkboxes()
        self.create_send_button()

        # Iniciar la comunicación con el programa output.py
        self.start_output_process()

    def create_patient_entry(self):
        # Marco que contiene la etiqueta, el campo de entrada y el botón "Iniciar"
        entry_frame = tk.Frame(self)
        entry_frame.pack()

        # Etiqueta para el nombre del paciente
        label = tk.Label(entry_frame, text="Nombre del paciente:")
        label.pack(side="left")

        # Campo de entrada para el nombre del paciente
        self.patient_entry = tk.Entry(entry_frame)
        self.patient_entry.pack(side="left")

        # Botón "Iniciar" para reiniciar las variables
        start_button = ttk.Button(entry_frame, text="Iniciar", command=self.reset_variables)
        start_button.pack(side="left", padx=(10, 0),)
    
    def reset_variables(self):
        global min_x, min_y, min_z, max_x, max_y, max_z

        new_patient_name = self.patient_entry.get()
        if new_patient_name != self.previous_patient_name:
            min_x = 100
            min_y = 100
            min_z = 100
            max_x = 0
            max_y = 0
            max_z = 0
            self.previous_patient_name = new_patient_name

    def create_progress_bars(self):
        # Etiquetas y barras de progreso para los giros en X, Y y Z
        x_label = tk.Label(self, text="Giro de muñeca:")
        x_label.pack()

        x_progressbar = ttk.Progressbar(self, variable=self.progress_x, maximum=100)
        x_progressbar.pack()

        y_label = tk.Label(self, text="Doblez de codo:")
        y_label.pack()

        y_progressbar = ttk.Progressbar(self, variable=self.progress_y, maximum=100)
        y_progressbar.pack()

        z_label = tk.Label(self, text="Giro de hombro:")
        z_label.pack()

        z_progressbar = ttk.Progressbar(self, variable=self.progress_z, maximum=100)
        z_progressbar.pack()

    def start_output_process(self):
        # Iniciar el programa output.py como un subproceso
        self.output_process = subprocess.Popen("hello-myo.exe", stdout=subprocess.PIPE, universal_newlines=True)

        # Iniciar la recepción de datos
        self.receive_data()

    global min_x, min_y, min_z
    min_x, min_y, min_z = 100, 100, 100
    global max_x, max_y, max_z
    max_x, max_y, max_z = 0, 0, 0
    
    def receive_data(self):
        global aux, aux1, aux2, pose, mode, info, cad, roll, pitch, yaw, cad_roll, cad_pitch, cad_yaw
        # Leer datos desde el programa output.py
        output = self.output_process.stdout.readline().strip()
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
                    roll+=10
                if cad_pitch[i]=="*" and pitch<=100 and pitch>=0:
                    pitch+=6
                if cad_yaw[i]=="*" and yaw<=100 and yaw>=0:
                    yaw+=5
            '''
            if yaw>=40:
                yaw=140-yaw
            else:
                yaw=40-yaw
            '''        
            #print("Roll:",roll)
            #print("Pitch:",pitch)
            #print("Yaw:",yaw)

            if mode=="unlocked":
                self.check_vars[0].set(pose == "fist" or self.check_vars[0].get())
                self.check_vars[1].set(pose == "fingersSpread" or self.check_vars[1].get())
                self.check_vars[2].set(pose == "waveIn" or self.check_vars[2].get())
                self.check_vars[3].set(pose == "waveOut" or self.check_vars[3].get())
            
            if mode!=aux2 or pose!=aux1:
                aux2=mode
                aux1=pose
                info = aux2 + "," + aux1
            #print(info)


            #Impresión de datos
            #print(f"{mode},{pose},{roll},{pitch},{yaw}")
            self.progress_x.set(roll)
            self.progress_y.set(pitch)
            self.progress_z.set(yaw)
            
            
            # Obtener los valores mínimos y máximos de las barras de progreso
            aux1 = self.progress_x.get()
            aux2 = self.progress_y.get()
            aux3 = self.progress_z.get()
            global min_x, min_y, min_z
            global max_x, max_y, max_z
            if aux1 < min_x and aux1 >= 0:
                min_x = aux1
            if aux2 < min_y and aux2 >= 0:
                min_y = aux2
            if aux3 < min_z and aux3 >= 0:
                min_z = aux3
            if aux1 > max_x and aux1 <= 100:
                max_x = aux1
            if aux2 > max_y and aux2 <= 100:
                max_y = aux2
            if aux3 > max_z and aux3 <= 100:
                max_z = aux3
        # Actualizar las barras de progreso con los datos recibidos
        self.after(10, self.receive_data)
        
    def create_position_checkboxes(self):
        # Lista de posiciones y sus imágenes correspondientes

        # Crear widgets para cada posición
        for i, (position, image_path) in enumerate(self.positions):
            position_frame = tk.Frame(self)
            position_frame.pack(side="top", pady=10)

            # Cargar imagen de la posición
            position_image = tk.PhotoImage(file=image_path).subsample(5)
            image_label = tk.Label(position_frame, image=position_image)
            image_label.image = position_image
            image_label.pack(side="left")

            # Etiqueta para la posición
            position_label = tk.Label(position_frame, text="Posición: " + position)
            position_label.pack(side="left")

            # Checkbox para marcar si se cumple la condición
            condition_check = tk.Checkbutton(position_frame, variable=self.check_vars[i])
            condition_check.pack(side="left")

    def create_send_button(self):
        # Botón para enviar los resultados
        send_button = ttk.Button(self, text="Enviar resultados", command=self.send_results)
        send_button.pack()

    

    def send_results(self):
        
        # Obtener el estado de las condiciones (Check o equis)
        # y almacenar los resultados en una base de datos
        # (aquí se puede agregar la lógica para enviar los datos a Node-RED o a otro servidor)
        patient_name = self.patient_entry.get()

        print("Resultados enviados para el paciente:", patient_name)
        print("Giro X: minimo =", min_x, "maximo =", max_x)
        print("Giro Y: minimo =", min_y, "maximo =", max_y)
        print("Giro Z: minimo =", min_z, "maximo =", max_z)
        print("Posiciones:")
        print("fist:", self.check_vars[0].get())
        print("fingersSpread:", self.check_vars[1].get())
        print("waveIn:", self.check_vars[2].get())
        print("WaveOut:", self.check_vars[3].get())
        
        aux = []
        for i in range(4):
            if self.check_vars[i].get():
                aux.append("Pudo lograr el gesto")
            else:
                aux.append("No pudo realizar el gesto")

        if max_x - min_x>=50:
            obs_x = "Giro de muñeca normal"
        else:
            obs_x = "Falta movilidad en la muñeca"
        if max_y - min_y>=50:  
            obs_y = "Doblez de codo normal"
        else:  
            obs_y = "Falta movilidad en el codo"
        if max_z - min_z>=50:
            obs_z = "Giro de hombro normal"
        else:
            obs_z = "Falta movilidad en el hombro"


        resultados = tk.Toplevel()
        resultados.title("Resultados")
        resultados.geometry("450x300")
    
        screen_width = resultados.winfo_screenwidth()
        screen_height = resultados.winfo_screenheight()
        
        # Calcular las coordenadas para centrar la ventana
        x = int((screen_width / 2) - (450 / 2))
        y = int((screen_height / 2) - (300 / 2))
        resultados.geometry(f"450x300+{x}+{y}")

        texto = ("Resultados enviados para el paciente: " + patient_name + "\n"
        + "Giros: " + "\n"
        + "Giro de muñeca: mínimo =" + str(min_x) + " máximo ="+ str(max_x) + "\n"
        + "Doblez de codo: mínimo =" +  str(min_y) + " máximo =" + str(max_y) + "\n"
        + "Giro de hombro: mínimo =" + str(min_z) + " máximo =" +  str(max_z) + "\n"
        + "Posiciones:" + "\n"
        + "Puño cerrado: " + aux[0] + "\n"
        + "Palma abierta: "+ aux[1] + "\n"
        + "Muñeca hacia adentro: "+ aux[2] + "\n"
        + "Muñeca hacia afuera: "+ aux[3] + "\n"
        + "Observaciones:" + "\n"
        + obs_x + "\n"
        + obs_y + "\n"
        + obs_z + "\n")

        label_resultados = tk.Label(resultados, text=texto)
        label_resultados.pack(side="top", pady=10)
        
if __name__ == "__main__":
    myo_interface = MyoInterface()
    myo_interface.mainloop()
