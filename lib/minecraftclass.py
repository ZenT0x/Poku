import json as js
import os

class jsonclass:
    def __init__(self, file_path): # file_path = chemin du fichier json
        self.file_path = file_path # chemin du fichier json
        self.data = None # dict des données du fichier json
        self.list_keys = [] # liste des clés du fichier json    

    def read_config(self): # lit le fichier json
        with open(self.file_path, 'r') as f: # ouvre le fichier json
            self.data = js.load(f) # lit le fichier json et le stocke dans self.data

    def write_config(self,data,add=0): # écrit dans le fichier json
        if add == 1: # si add = 1, on ajoute les données à celles déjà présentes
            self.read_config() # on lit le fichier json
            self.data.update(data) # on ajoute les données à celles déjà présentes
        with open(self.file_path, "w") as file: # on ouvre le fichier json
            js.dump(self.data,file,sort_keys=False,indent=4) # on écrit les données dans le fichier json

    def del_value_from_key_list(self,key,value): # supprime une valeur d'une liste
        self.read_config() # on lit le fichier json
        self.data[key].remove(value) # on supprime la valeur de la liste
        self.write_config(self.data) # on écrit les données dans le fichier json

    def add_value_from_key_list(self,key,value): # ajoute une valeur à une liste
        self.read_config() # on lit le fichier json
        self.data[key].append(value) # on ajoute la valeur à la liste
        self.write_config(self.data) # on écrit les données dans le fichier json
        
    def append_list_keys(self,): # ajoute les clés du fichier json à la liste self.list_keys
        self.list_keys = list(self.data.keys()) # ajoute les clés du fichier json à la liste self.list_keys
    

config = jsonclass("/home/zentox/suhome/Discord/Poku/old/config.json") # on crée un objet jsonclass pour le fichier config.json
config.read_config() # on lit le fichier config.json

minecraft = jsonclass("/home/zentox/suhome/Discord/Poku/old/minecraft_servers.json") # on crée un objet jsonclass pour le fichier minecraft_servers.json
minecraft.read_config() # on lit le fichier minecraft_servers.json

class serverclass: # classe pour les serveurs minecraft
    def __init__(self, server_id): # server_id = id du serveur
        self.data = minecraft.data["servers"][server_id] # dict des données du serveur
        self.id = self.data["id"] # id du serveur
        self.name = self.data["name"] # nom du serveur
        self.description = self.data["description"] # description du serveur
        self.running = self.data["running"] # booléen si le serveur est en cours de fonctionnement
        
    def start(self):
        if minecraft.data["running"] == 0 and self.data["running"] == 0:
            os.system('bash '+self.data["path_script"]) # commande pour démarrer le serveur    
            data = {"activity": str("Serveur open")}
            config.write_config(data,1) 
            data = {"running": 1}
            minecraft.write_config(data,1)
            return 1
        else:
            return 2
        
    def stop(self):
        os.system('bash mcstop.sh')
        data = {"activity": str("Serveur fermé")}
        config.write_config(data,1)
        data = {"running": 0}
        minecraft.write_config(data,1)

    def restart(self):
        os.system('bash mcrestart.sh')
            

token = config.data["token"]
liste_op = config.data["liste_op"]
liste_op_minecraft = minecraft.data["op_minecraft"]
prefix = config.data["prefix"]
ratio = config.data["ratio"]

serveur_vanilla = serverclass(1)
serveur_mode = serverclass(2)
