import sqlite3
import os

class MinecraftDB:
    def __init__(self):
        self.conn = sqlite3.connect('minecraftservers.db')
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS servers
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, running INTEGER, launchscript TEXT)''')
        self.conn.commit()

    def add_server(self, name, description, running, launchscript):
        self.c.execute('''INSERT INTO servers(name, description, running, launchscript) VALUES(?,?,?,?)''', (name, description, running, launchscript))
        self.conn.commit()

    def get_server(self, id):
        self.c.execute('''SELECT * FROM servers WHERE id=?''', (id,))
        return self.c.fetchone()
    
    def del_server(self, id):
        self.c.execute('''DELETE FROM servers WHERE id=?''', (id,))
        self.conn.commit()
    
    def get_all_servers(self):
        self.c.execute('''SELECT * FROM servers''')
        return self.c.fetchall()
    
    def get_all_servers_names(self):
        self.c.execute('''SELECT name FROM servers''')
        return [name[0] for name in self.c.fetchall()]
    
    def get_all_servers_ids(self):
        self.c.execute('''SELECT id FROM servers''')
        return self.c.fetchall()
    
    def is_server_running(self, id):
        self.c.execute('''SELECT running FROM servers WHERE id=?''', (id,))
        return self.c.fetchone()[0]
    
    def set_server_running(self, id, running):
        self.c.execute('''UPDATE servers SET running=? WHERE id=?''', (running, id))
        self.conn.commit()
        
    def get_server_launch_script(self, id):
        self.c.execute('''SELECT launchscript FROM servers WHERE id=?''', (id,))
        return self.c.fetchone()[0]
    
    
db = MinecraftDB()
print("Initialazing database")
minecraftLaunchScripts = os.listdir('scripts/minecraft_boot')
minecraftLaunchScriptsNames = [file.replace(".sh", "") for file in minecraftLaunchScripts]
for i in range(len(minecraftLaunchScripts)):
    serverLaunchScript = minecraftLaunchScripts[i]
    serverName = minecraftLaunchScriptsNames[i]
    if serverName not in db.get_all_servers_names():
        print(f"Adding {serverName} to database")
        db.add_server(serverName, "Serveur basé sur "+serverName, 0, serverLaunchScript)

for i in range(len(db.get_all_servers())):
    server = db.get_all_servers()[i]
    if server[1] not in minecraftLaunchScriptsNames:
        print(f"Removing {server[1]} from database")
        db.del_server(server[0])
            
    
            
                


