import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import tkinter as tk
import tkinter.ttk as ttk
import cv2
from PIL import Image, ImageTk
import webbrowser
import threading
from queue import Queue

class JSONEventHandler(FileSystemEventHandler):
    def __init__(self, path_to_watch, app_instance):
        self.path_to_watch = path_to_watch
        self.app_instance = app_instance

    def erro_para_points(self, erro_percentual):
        if erro_percentual >= 0 and erro_percentual <= 5:
            return int(91 + (erro_percentual - 0) * 2)
        elif erro_percentual >= 6 and erro_percentual <= 10:
            return int(71 + (erro_percentual - 6) * 2)
        elif erro_percentual >= 11 and erro_percentual <= 20:
            return int(51 + (erro_percentual - 11) * 2)
        elif erro_percentual >= 21 and erro_percentual <= 40:
            return int(11 + (erro_percentual - 21) * 2)
        elif erro_percentual >= 41 and erro_percentual <= 60:
            return int(1 + (erro_percentual - 41) * 1)
        elif erro_percentual >= 61 and erro_percentual <= 100:
            return int(0)
        else:
            return int(999)  
          
    def on_created(self, event):
        print("c")
        if event.is_directory:
            return None
        elif event.event_type == 'created' and event.src_path.endswith('.json'):
            json_to_compare_path = event.src_path

            # Verifique se um JSON de referência foi selecionado
            if self.app_instance.reference_json_path:
                print("a")
                # Execute a comparação apenas quando um arquivo JSON for criado
                
                
                self.compare_json(self.app_instance.reference_json_path, json_to_compare_path)

    def compare_json(self, reference_path, compare_path):

        with open(reference_path) as f1, open(compare_path) as f2:
            data1 = json.load(f1)
            data2 = json.load(f2)

            error = {}

            for i, person1 in enumerate(data1["people"]):
                if i >= len(data2["people"]):
                    break
                person2 = data2["people"][i]
                error[i] = []
                for j in range(len(person1["hand_right_keypoints_2d"])):
                    error[i].append((abs(person1["hand_right_keypoints_2d"][j] - person2["hand_right_keypoints_2d"][j])) / (
                                person1["hand_right_keypoints_2d"][j]) * 100)
                    error_media = sum(error[i]) / len(error[i])
                    

            pontuacao = self.erro_para_points(error_media)
            print(pontuacao)
            self.app_instance.update_number(pontuacao)

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player")
        self.root.configure(bg="#292929")  # Set background color of the root window

        # Variáveis para controle
        self.photo_image = None  # Initialize the instance variable
        self.current_video = 0
        self.video_playing = False
        self.videos = ["video1.mp4", "video2.mp4", "video3.mp4", "video4.mp4"]
        self.json_paths = ["keypoints1.json", "keypoints2.json", "keypoints3.json", "keypoints4.json"]

        # Frame para os botões superiores (Avaliação, Ajuda, Dúvidas)
        self.top_button_frame = tk.Frame(self.root, bg="#292929")  # Use tk.Frame instead of ttk.Frame
        self.top_button_frame.pack(pady=10)

        self.avaliacao_button = ttk.Button(self.top_button_frame, text="Avaliação", command=self.open_avaliacao)
        self.avaliacao_button.pack(side=tk.LEFT, padx=10)

        self.ajuda_button = ttk.Button(self.top_button_frame, text="Ajuda", command=self.open_ajuda)
        self.ajuda_button.pack(side=tk.LEFT, padx=10)

        self.duvidas_button = ttk.Button(self.top_button_frame, text="Dúvidas", command=self.open_duvidas)
        self.duvidas_button.pack(side=tk.LEFT, padx=10)

        # Frame para exibir o número em um retângulo
        self.number_frame = tk.Frame(self.root, bg="#292929")  # Use tk.Frame
        self.number_frame.pack()

        self.number_canvas = tk.Canvas(self.number_frame, width=200, height=50, borderwidth=2, relief=tk.RIDGE, bg="#292929")
        self.number_canvas.pack()

        self.number_rectangle = self.number_canvas.create_text(100, 25, text="Pontuação: 0", font=("Helvetica", 12), fill="white")

        # Frame para os botões de vídeo
        self.button_frame = tk.Frame(self.root, bg="#292929")  # Use tk.Frame
        self.button_frame.pack(side=tk.LEFT, padx=20, pady=10)

        self.buttons = []
        for i in range(4):
            button = ttk.Button(self.button_frame, text=f"Exercício {i+1}", command=lambda idx=i: self.play_video_and_compare_json(idx))
            button.pack(anchor=tk.W, pady=5)
            self.buttons.append(button)

        # Canvas para exibir o vídeo (aumentado)
        self.video_canvas = tk.Canvas(self.root, width=800, height=600, borderwidth=2, relief=tk.RIDGE)
        self.video_canvas.pack(side=tk.RIGHT, padx=20, pady=10)

        self.video_rectangle = self.video_canvas.create_text(300, 200, text="Área de Vídeo", font=("Helvetica", 14))

    def play_video_and_compare_json(self, idx):
        if not self.video_playing:  # Verifique se não há vídeo em reprodução
            print("v")
            self.video_playing = True
            self.video_playing_idx = idx
            
            diretorio_base = os.path.dirname(os.path.abspath(__file__))
            self.reference_json_path = os.path.join(diretorio_base, 'keypoints', f'keypoints{idx+1}.json')

            # Abrir o vídeo correspondente ao exercício
            self.play_video(idx)


    def play_video(self, idx):
        diretorio_base = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(diretorio_base, 'videos')
        self.current_video = idx
        video_filename = self.videos[idx]
        video_path = 'videos'  # Path to the folder containing videos
        full_video_path = os.path.join(video_path, video_filename)

        # Remove the existing text from the video rectangle
        self.video_canvas.itemconfig(self.video_rectangle, text="")

        # Open the video using OpenCV
        cap = cv2.VideoCapture(full_video_path)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convert the frame from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.photo_image = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

            # Clear the canvas and draw the new image
            canvas_width = self.video_canvas.winfo_width()
            canvas_height = self.video_canvas.winfo_height()
            image_width = self.photo_image.width()
            image_height = self.photo_image.height()

            # Calculate the position to center the image within the canvas
            x_position = (canvas_width - image_width) // 2
            y_position = (canvas_height - image_height) // 2

            # Clear the canvas and draw the new image
            self.video_canvas.delete("all")
            self.video_canvas.create_image(x_position, y_position, anchor=tk.NW, image=self.photo_image)


            # Update the GUI
            self.root.update()

        # Release the video capture and destroy any OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        self.video_playing = False
        print("end")
        self.video_playing_idx = -1



    def open_avaliacao(self):
        avaliacao = "pontos.txt"
        os.system(f"start {avaliacao}")
    
    def open_ajuda(self):
        arquivo = "TUTORIAL.txt"
        os.system(f"start {arquivo}")
    
    def open_duvidas(self):
        url = "https://github.com/Neuroproteses/TerapiaRemotaOP/tree/main"  # Substitua com a URL desejada

        # Abrir a página no navegador padrão
        webbrowser.open(url)

    def update_number(self, new_number):
        self.number_canvas.itemconfig(self.number_rectangle, text=f"Pontuação: {new_number}")
        if self.video_playing_idx >= 0 and new_number<101:
            with open("pontos.txt", "a") as arquivo:  # Usando "a" para anexar ao arquivo
                arquivo.write(f"Pontuação: {new_number} - Exercício: {self.video_playing_idx+1}\n")
        

def start_observer(observer_queue):
    print("ex")
    direct_base = os.path.dirname(os.path.abspath(__file__))
    path_to_watch = os.path.join(direct_base, "output_json_folder")

    event_handler = JSONEventHandler(path_to_watch, app)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()

    try:
        while True:
            print("loop")
            observer_queue.put(True)
            time.sleep(1)
            if observer_queue.get() is None:
                for file_name in os.listdir(path_to_watch):
                    os.remove(os.path.join(path_to_watch, file_name))
                observer.stop()
                break
    except KeyboardInterrupt:
        for file_name in os.listdir(path_to_watch):
            os.remove(os.path.join(path_to_watch, file_name))
        observer.stop()
    observer.join()

def check_observer():
    print("ob")
    while True:
        # Verifique periodicamente a fila para eventos do Observer
        if not observer_queue.empty():
            # Execute a lógica para tratar os eventos do Observer aqui
            print("Evento do Observer detectado")
            observer_queue.get()
        time.sleep(1)                

def on_closing():
    # Função a ser chamada quando a janela for fechada pelo usuário
    print("close")
    observer_queue.put(None)  # Sinalize o encerramento do observador
    root.destroy()  # Feche a janela do Tkinter

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    observer_queue = Queue()
    observer_thread = threading.Thread(target=start_observer, args=(observer_queue,))
    observer_thread.start()

    root.mainloop()
    print("root")
    
