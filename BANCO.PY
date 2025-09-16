from tqdm import tqdm
import time
class Login:
    def __init__(self,agencia: str = '5936-5', conta:str ='25692-0', senha: str = 'Otavio25@'):
#Valores corretos 
        self._agencia_correto = '5936-5'
        self._conta_correto = '25692-0'
        self._senha_correto = 'Otavio25@'
#Verifica os dados
        if agencia != self._agencia_correto:
            raise ValueError('Dados incorreto')
        if conta != self._conta_correto:
            raise ValueError("Dados incorreto")
        if senha != self._senha_correto:
            raise ValueError ('Dados incorreto')
#Se passou por todas verificação, Salva os atributos
        self.agencia =agencia
        self.conta = conta
        self.senha = senha 

#Tentativas
tentativas = 3
while tentativas > 0:
    age = input('Digite a sua agencia: ')
    co = input('Digite a sua conta: ')
    se = input('Digite a sua senha: ')
    try:
        login1 = Login(agencia=age, conta=co, senha=se)
        print('Login realizado com sucesso!')

        break #encerra o loop se der certo.
    except ValueError as e:
        tentativas -=1
        print ( 'Erro {}'.format(e))
        if tentativas > 0:
            print(f"Você tem {tentativas} tentativa(s) restante(s).\n")
        else:
            print("Acesso bloqueado! Número máximo de tentativas atingido.")
# Texto que vai dentro do quadrado
texto = f"Agência: {login1.agencia} | Conta: {login1.conta} | Senha: {login1.senha}"

# Calcula o tamanho do quadrado baseado no texto
largura = len(texto) + 4  # +4 para margens e bordas

# Desenha o quadrado
print("*" * largura)
print(f"* {texto} *")
print("*" * largura)
#MENU DO BANCO 
class contaBancaria:
    def __init__(self,titular:str,saldo:float = 0):
        self.titular = titular
        self.saldo = saldo
        #Funcionalidade de depositar
    def deposito(self,valor):
        if valor >0:
            self.saldo += valor
            print('Deposito R${:.2f}. Saldo Atual R${:.2f}'.format(valor,self.saldo))
        else:
            print('Valor de deposito deve ser positivo.')
    #Funcionalidade de Retirada
    def Retirada(self,valor):
        if valor > 0:
            if self.saldo >= valor:
                self.saldo -= valor
                print('Retirada R${:.2f}, Saldo Atual R${:.2f}'.format(valor,self.saldo))
            else:
                print("Saldo insuficiente. Saldo Atual R${:.2f}".format(self.saldo)) 
        else:
            print('Valor da retirada devera ser positivo.')
            #Funcionalidade de Verificar saldo
    def varificãodeSaldo(self):
        print('Saldo Atual R${:.2f}'.format(self.saldo))
def menu ():
    conta=contaBancaria('Otávio Ribeiro Dos Santos')
    while True:
        #Menu funções
        print('---Funções do Sistema---')
        print('1.Deposito')
        print('2. PIX')
        print('3.Saldo')
        print('4.Sair')
        opeção=(input('Escolha qual opeção deseja: '))
        if opeção == '1':
            valor=float(input('Qual o valor que deseja depositar R$:')) 
            #DEPOSITAR FUNDOS
            print('Depositando fundo')
            for i in tqdm(range(10)):
                time.sleep(0.5) 
            conta.deposito(valor)
        elif opeção == '2':
            valor=float(input('Qual valor deseja transferir R$:'))
            conta.Retirada(valor)
            #TRASFERENCIA\PIX
            print('Pix realizado com sucesso.  ')
        elif opeção == '3':
            #Ver saldo
            conta.varificãodeSaldo()
        elif opeção == '4':
            print('Saindo da conta, Tenha um bom dia!')
            break
        else:
            print('Opeção invalida!')
menu()