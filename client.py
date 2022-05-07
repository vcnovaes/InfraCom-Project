from utility.RDT3 import RDTConnection
import os

port = 3000

def main():
    os.system(f"kill -9 $(lsof -t -i:{port})")
    os.system("clear")


    client_connection = RDTConnection("client", "0.0.0.0", port)
    try: 
        while True: 
            msg = input("Message to send:")
            if len(msg) % 2 == 1:
                msg += '\0'
            client_connection.send(msg,"0.0.0.0", 3001)
            
    except KeyboardInterrupt:
        client_connection.close()        



if __name__ == "__main__":
    main() 