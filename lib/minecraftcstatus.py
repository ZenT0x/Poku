from mcstatus import JavaServer

def get_minecraft_status(server_address):
    server_port = 25565  # Port par défaut du serveur Minecraft
    try:
        server = JavaServer.lookup(f'{server_address}:{server_port}')
        num_players = server.status().players.online
        ping = server.ping()
        #players = server.query().players.names[:5]
        players = ""
        return num_players, players, int(ping)
    except:
        return -1,-1,-1