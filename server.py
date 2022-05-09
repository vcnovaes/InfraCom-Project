import ast, os, datetime
from utility.RDT3 import RDTConnection
import math

def timestamp():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time
    
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def format_msg(user, msg):
    return f"{bcolors.OKCYAN}{timestamp()} {user}: {msg}"

class Server:
    def __init__(self):

        self.cardapio = [
            {"num": 1, "nome":"File a Parmegiana".lower(), "preco": 10.00 },
            {"num": 2, "nome": "Frango a Parmegiana".lower(), "preco" : 20.00}, 
            {"num": 3, "nome": "Macarrão com alho".lower(), "preco": 40.00}
        ]
        self.prices = {
            "File a Parmegiana".lower() : 10.00,
            "Frango a Parmegiana".lower() : 20.00,
            "Macarrão com alho".lower() : 40.00
        }
        self.user_options =  '''
            Digite uma das opções a seguir (o número ou por extenso):
            1 - cardápio
            2 - pedido
            3 - conta individual 
            4 - levantar da mesa 
            5 - nada não, tava só testando
            6 - não fecho com robô, chame seu gerente
            7 - conta da mesa
            8 - Pagar Conta
            '''

        self.cnt = 0
        self.server_ip = "0.0.0.0"
        self.server_port = 1200
        self.sent = False
        
        os.system(f"kill -9 $(lsof -t -i:{self.server_port})")
        os.system("clear")

        self.rdt_connection = RDTConnection(type="server", address=self.server_ip, port=self.server_port, buffer_size=2048, timeout=2)
        # print(f"The server is online and listening on address {self.server_ip}:{self.server_port}")

        self.state=0
        self.tabela = {}
        self.current_user = None

        self.last_received = None
        self.undone = False
        self.last_data = None

        self.states = [self.pre_chefia, self.final_state]

    def pedido_extenso_to_int(self, pedido_por_extenso: str):
        pedidos_por_extenso = [ pedido["nome"] for pedido in self.cardapio]
        return pedidos_por_extenso.lower.index(pedido_por_extenso) - 1

    def was_ack(self):
        return self.last_received == "ACK"

    def undo_input(self):
        self.undone = True

    def receber(self):
        print(f'last: {self.last_data}')

        #data = None
        #if self.last_received is None:
        if self.undone:
            self.undone = False
            return self.last_data

        data, user = self.rdt_connection.receive()
        self.current_user = user
        self.sent = False
        #else:
        #    data = self.last_received
        #    self.last_received = None

        data = ast.literal_eval(data.decode())

        # print(f'[SERVER receber()] got {data} from {self.current_user}')

        data = data["data"]


        if data[-1] == '\0':
            data = data[:-1]

        self.last_data = data
        return data

    def enviar(self, msg):
        if not self.sent:
            msg_formatted = format_msg("CINtofome", msg)
            self.rdt_connection.send(msg_formatted, self.current_user[0], self.current_user[1])
        self.sent = True

    def add_new_tbl_entry(self, user):
        self.tabela[user] = {"nome": None, "mesa": None, "conta": 0, "pedidos": [], "state": self.pre_chefia}
        return 

    def pre_chefia(self, state):
        if self.receber().lower() == "chefia":
            return self.initial_state
        else:
            self.undo_input()
            print("manda o chefe, mestre")
            return self.mandarOpcoes

    # cada estado recebe o numero do estado atual e retorna o proximo estado
    def initial_state(self, state):
        # print("eae chefia")
        self.enviar("Bem vindos ao CintoFome, digite sua mesa de 0 a 9: ")

        mesa = self.receber()
        mesa = int(mesa)
        self.enviar("Digite seu nome: ")
        nome = self.receber()

        self.add_new_tbl_entry(self.current_user);

        self.tabela[self.current_user]["nome"] = nome
        self.tabela[self.current_user]["mesa"] = int(mesa)
        return self.mandarOpcoes

    def mandarOpcoes(self, state):
        if not self.undone:
            self.enviar(self.user_options)

        msg = self.receber()

        opts = [
            self.ler_cardapio,
            self.pedido,
            self.conta_individual,
            self.levantar_da_mesa,
            self.teste,
            self.gerente,
            self.conta_da_mesa,
            self.pagarConta
        ]
        
        opt = int(msg) if msg.isnumeric() else self.pedido_em_extenso_to_int(msg) 

        return opts[opt-1]
        
    def final_state(self, state):
        
        msg = "Volte sempre"
        self.enviar(msg)
        return state+1
        
    def ler_cardapio(self, state):
        msg = ""
        for item in self.cardapio:
            msg += f"{item['num']} - {item['nome']}, R${item['preco']}\n" 
            
        self.enviar(msg)
        return self.pre_chefia

    def ler_menu(self, state):
        opt = int(self.receber())

        nexts = []
        
    def pedido(self, state):
        self.enviar("Digite qual o primeiro item que gostaria (número ou por extenso)")
        msg = self.receber()

        # adiciona pedido escolhido pelo usuário na lista de pedidos desse usuário dentro da tabela
        number = int(msg) if msg.isnumeric() else self.pedido_extenso_to_int(msg)
        self.tabela[self.current_user]["pedidos"].append(self.cardapio[number-1]["nome"])
        self.tabela[self.current_user]["conta"] += self.cardapio[number-1]["preco"]

        return self.mandarOpcoes

    def teste(self, state):
        msg = "Obrigado por testar!"
        self.enviar(msg)
        return self.mandarOpcoes

    def conta_individual(self, state):
        pedidos = [ (nome,self.prices[nome]) for nome in self.tabela[self.current_user]["pedidos"] ] 
        total = self.tabela[self.current_user]["conta"]
        msg = self.tabela[self.current_user]["nome"] + "gastou:\n"
        
        for (nome, val) in pedidos:
            msg += str(nome) + "   R$"+ str(val) +"\n"
        msg += "Total: " + str(total) + "\n"
        self.enviar(msg)
        return self.pre_chefia

    def gerente(self, state):
        msg = "Irei chamar o Gerente"
        self.enviar(msg)
        return self.mandarOpcoes

    def update_user_state(self, user, state):
        if not (user in self.tabela):
            self.add_new_tbl_entry(user)

        self.tabela[user]["state"] = state

    def execute_state(self, state):
        return state(None)

    def user_state(self, user: tuple):
        '''
            user: (client_ip, client_port)
        '''

        if not user in self.tabela:
            self.add_new_tbl_entry(user)

        return self.tabela[user]["state"]

    
    def conta_da_mesa(self, state): # pronto
        mesa = self.tabela[self.current_user]["mesa"]
        msg = ""
        totalMesa = 0
        for val in self.tabela.values():
            if val["mesa"] == mesa:
                msg += val["nome"] + "\n"
                for comida in val["pedidos"]:
                    msg += comida + " => R$" + str(self.prices[comida]) + "\n"    
                msg += "\nTotal: R$" + str(val["conta"]) + "\n"
                totalMesa+= val["conta"]
            
        msg += "O Total da Mesa é: R$" +  str(totalMesa) + "\n\n"
        self.enviar(msg)
        return self.pre_chefia
    
    def levantar_da_mesa(self, state): #pronto
        #self.tabela[clientAddress]["state"]
        print(f"{self.current_user} esta tentando levantar da mesa")
        if self.tabela[self.current_user]["conta"] > 0:
            msg = "Você ainda não pagou sua conta de " + str(self.tabela[self.current_user]["conta"]) + " reais!\n"
            self.enviar(msg)
            return self.pre_chefia
        else:
            self.tabela.pop(self.current_user)
            msg = "Agradecemos a sua visita\n"
            self.enviar(msg)
            return self.pre_chefia
    def valorContaMesa(self, mesa):
        total =0
        cnt =0;
        for user in self.tabela.values():
            if user["mesa"] == mesa:
                total += user["conta"]
                cnt+=1
        return total, cnt
    
    def pagarConta(self, state):
        '''
         1 - Printar conta individual e conta da  mesa
        '''
        mesa = self.tabela[self.current_user]["mesa"]
        contaMesa, qtdMesa = self.valorContaMesa(mesa)
        contaIndividual = self.tabela[self.current_user]["conta"]

        msg = "Sua Conta foi de R$ " + str(contaIndividual) + " e a da mesa R$ " + str(contaMesa) + ". Digite o valor a ser pago:\n"
        while True:
            self.enviar(msg)
            dinheiro = int(self.receber())
            if dinheiro >= contaIndividual and dinheiro <= contaMesa:
                self.tabela[self.current_user]["conta"]=0
                self.tabela[self.current_user]["pedidos"] = []
                restante = dinheiro - contaIndividual
                # contar qtd de pessoas na mesma mesa 
                # divide igualmente , resultado faz floor
                if restante > 0:
                    divisao = math.floor(restante/(qtdMesa-1))
                    for user in self.tabela.values():
                        if user["mesa"] == mesa and user["conta"] > 0:
                            user["conta"] -= divisao
                            if user["conta"] < 0: 
                                user["conta"] = 0 
                break    
        return self.mandarOpcoes
                

    def main_loop(self):
        skip_receive = False
        while True:

            print(f'[SERVER] tabela: {self.tabela}')

            #if not skip_receive:
            #    message, user = self.rdt_connection.receive()

            #self.current_user = user
            #self.last_received = message

            if self.was_ack():
                continue


            if self.current_user is None:
                next_state = self.execute_state(self.pre_chefia)
                self.update_user_state(self.current_user, next_state)
            else:
                state = self.user_state(self.current_user)
                next_state = self.execute_state(state)
                self.update_user_state(self.current_user, next_state)

        pass


def main():
    server = Server()
    server.main_loop()




if __name__ == "__main__":
    main() 

#modifiedMessage = message.decode().upper()
#serverSocket.sendto(modifiedMessage.encode(), clientAddress)
        