import socket
import pyautogui#pip install pyautogui
import threading
import time
import pickle

HOST = 'http://localhost'
PORT = 3033
UPDATE_COODOWN = 0.05

class client:
    def __init__(self, host, port, update_cooldown):
        """
        Connexion au serveur
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))
        
        self.update_cooldown = update_cooldown
        self.recieved_positions = {}

        self.listen_thread = threading.Thread(target=self.listen_loop)
        self.send_thread = threading.Thread(target=self.send_loop)
        self.listen_thread.start()
        self.send_thread.start()

    def get_mouse_coordinates(self):
        """
        Renvoie un couple (x, y) avec les positions de la souris.

        A moduler en fonction de ce qu'on veut partager commme données
        """
        return pyautogui.position()

    def listen_loop(self):
        """
        Boucle qui reçoit les positions et les met dans self.positions
        """
        while True:
            decoded_message = pickle.loads(self.client_socket.recv(1024))
            #voir ce qu'on reçoit

    def send_loop(self):
        """
        Boucle qui envoie
        """
        while True:
            encoded_message = pickle.dumps(self.get_mouse_coordinates())
            self.client_socket.send(encoded_message)
            time.sleep(self.update_cooldown)


