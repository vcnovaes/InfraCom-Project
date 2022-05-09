from utility.RDT3 import RDTConnection
import os, ast
from random import randint

port = randint(3000, 3050)
byebye = "Agradecemos a sua visita\n"
def prepare_msg(msg):
    if len(msg) % 2 == 1:
        msg += '\0'
    return msg    


def main():
    os.system(f"kill -9 $(lsof -t -i:{port})")
    os.system("clear")
    client_connection = RDTConnection("client", "0.0.0.0", port)

    try: 
        while True: 
            msg = input()
            # msg = input()
            msg = prepare_msg(msg)
            client_connection.send(msg,"0.0.0.0", 1200)
            data, _ = client_connection.receive()
            data = ast.literal_eval(data.decode())
            print(data["data"])
            if byebye in data["data"]: 
                client_connection.close() 
                break
            # print(f"[FROM client.py] {data}")

            
    except KeyboardInterrupt:
        client_connection.close()        



if __name__ == "__main__":
    main() 