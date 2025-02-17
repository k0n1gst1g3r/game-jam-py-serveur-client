import socket
import threading

MAX_CONNECTIONS = 5

HOST = 'http://localhost'
PORT = 3033

class server:
    def __init__(self, max_co, host, port):
        """
        Création de l'instance du serveur.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#ipv4, tcp
        self.server_socket.bind((host, port))
        self.server_socket.listen(max_co)

        self.clients = []

        #Mutex pour éviter les erreurs d'accès concurrents
        self.lock = threading.lock()

        #lancement de la boucle d'écoute des nouveaux clients:
        self.listen()
    
    def handle_client(self, client_socket, client_address):
        """
        Boucle de gestion d'un client, invoquée quand une nouvelle connection est établie.
        """
        print(f"Nouvelle connection: {client_address}")

        try:
            while True:
                message = client_socket.recv(1024)
                if len(message) == 0:
                    print(f"Le client {client_address} s'est déconnecté")
                    break
                
                #broadcast du message
                self.broadcast(message, client_socket)

        except:
            print(f"Erreur lors de la récepition en provenance du client {client_address}")

        #fermeture de la connection
        self.disconnect(client_socket)

    def broadcast(self, message, sender_socket):
        """
        Envoi du message à tous les clients
        """
        with self.lock:
            for client in self.clients.copy():
                if client != sender_socket:
                    try:
                        self.server_socket.send(message)
                        pass
                    except:
                        print(f"Erreur lors du broadcast vers le client {client}")
                        self.disconnect(client)

    def disconnect(self, client_socket):
        """
        Déconnecte un client
        """
        with self.lock:
            print(f"Déconnexion du client {client_socket}")
            self.clients.remove(client_socket)
            client_socket.close()

    def listen(self):
        """
        Boucle pour accepter les nouveaux clients.
        """
        while True:
            client_socket, client_address = self.server_socket.accept()
            with self.lock: 
                self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
        
if __name__ == "__main__":
    serveur = server(max_co=MAX_CONNECTIONS, host=HOST, port=PORT)