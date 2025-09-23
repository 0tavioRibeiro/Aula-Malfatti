from tqdm import tqdm
import time

class Login:
    def __init__(self, titular: str, agencia: str = '5936-5', conta: str = '25692-0', senha: str = 'Otavio25@'):
        self.titular = titular
        self._agencia_correto = '5936-5'
        self._conta_correto = '25692-0'
        self._senha_correto = 'Otavio25@'
        # Verifica os dados
        if agencia != self._agencia_correto:
            raise ValueError('Dados incorreto')
        if conta != self._conta_correto:
            raise ValueError("Dados incorreto")
        if senha != self._senha_correto:
            raise ValueError('Dados incorreto')
        # Se passou por todas verificaçoes, salva os atributos
        self.agencia = agencia
        self.conta = conta
        self.senha = senha

# Tentativas
tentativas = 3
while tentativas > 0:
    age = input('Digite a sua agencia: ')
    co = input('Digite a sua conta: ')
    se = input('Digite a sua senha: ')
    try:
        login1 = Login(titular='Otávio Ribeiro Dos Santos', agencia=age, conta=co, senha=se)
        print('Logando...')
        for i in tqdm(range(10)):
                time.sleep(0.10)
        print('Login realizado com sucesso!')
        break  # encerra o loop se der certo.
    except ValueError as e:
        tentativas -= 1
        print('Erro {}'.format(e))
        if tentativas > 0:
            print(f"Você tem {tentativas} tentativa(s) restante(s).\n")
        else:
            print("Acesso bloqueado! Número máximo de tentativas atingido.")

# Texto que vai dentro do quadrado
texto = f"Nome: {login1.titular} | Agência: {login1.agencia} | Conta: {login1.conta} | Senha: {login1.senha}"
largura = len(texto) + 4  
print("*" * largura)
print(f"* {texto} *")
print("*" * largura)

# Class Conta Bancaria  
class contaBancaria:
    def __init__(self, chave_Pix: str, limiteCartão: float, saldo: float = 0):
        self.chave_Pix = chave_Pix
        self.limiteCartão = limiteCartão  # trata-se do limite disponível do cartão
        self.saldo = saldo
        self.extrato = []

    # Funcionalidade de depositar
    def deposito(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: R${valor:.2f} | Saldo: R${self.saldo:.2f}")
            print('Depósito \033[31mR${:.2f}\033[m. Saldo Atual\033[32m R${:.2f}\033[m'.format(valor, self.saldo))
        else:
            print('Valor de depósito deve ser positivo.')

    # Transferência PIX normal (usa apenas saldo)
    def pix(self, chave_destino, valor):
        if chave_destino == self.chave_Pix:
            print('\033[31mErro\033[m: \033[4mNão é permitido fazer transferência para a própria chave PIX!\033[m')
            return
        if valor <= 0:
            print('Valor do PIX deverá ser positivo.')
            return
        if self.saldo >= valor:
            self.saldo -= valor
            self.extrato.append(f"PIX: R${valor:.2f} | Saldo: R${self.saldo:.2f}")
            print('Transferência \033[31mR${:.2f}\033[m. Saldo Atual \033[32mR${:.2f}\033[m'.format(valor, self.saldo))
            print('PIX realizado com sucesso!')
        else:
            # Saldo insuficiente — informa o deficit e pede decisão no menu
            print("\033[31mSaldo insuficiente\033[m. Saldo Atual \033[32mR${:.2f}\033[m".format(self.saldo))

    # PIX usando o cartão de crédito (quando saldo for insuficiente ou negativo)
    def pix_com_cartao(self, chave_destino, valor):
        if chave_destino == self.chave_Pix:
            print('\033[31mErro\033[m:\033[4mNão é permitido fazer transferência para a própria chave PIX!\033[m')
            return
        if valor <= 0:
            print('Valor do PIX deverá ser positivo.')
            return

        # Disponível em conta só considera saldo positivo
        disponivel_em_dinheiro = max(self.saldo, 0)
        credito_necessario = valor - disponivel_em_dinheiro  # quanto precisa do cartão

        if credito_necessario <= 0:
            # tendo saldo suficiente  executar como PIX normal
            self.saldo -= valor
            self.extrato.append(f"PIX (saldo): R${valor:.2f} | Saldo: R${self.saldo:.2f}")
            print('Transferência \033[31mR${:.2f}\033[m usando saldo. Saldo Atual \033[32mR${:.2f}\033[m'.format(valor, self.saldo))
            print('PIX realizado com sucesso!')
            return

        # Verifica limite do cartão
        if self.limiteCartão >= credito_necessario:
            # usa todo o saldo disponível (se houver) e o resto no cartão
            self.limiteCartão -= credito_necessario
            # saldo fica reduzido pelo valor total (poderá ficar negativo)
            self.saldo -= valor
            self.extrato.append(f"PIX (cartão): R${valor:.2f} | Usou R${credito_necessario:.2f} do cartão | Saldo: R${self.saldo:.2f}")
            print('PIX \033[31mR${:.2f}\033[m realizado: \033[33mR${:.2f}\033[m usado do cartão de crédito.'.format(valor, credito_necessario))
            print('Saldo atual: \033[32mR${:.2f}\033[m | Limite disponível no cartão: \033[33mR${:.2f}\033[m'.format(self.saldo, self.limiteCartão))
            print('PIX via cartão de crédito realizado com sucesso!')
        else:
            print('\033[31mErro\033[m: \033[4mlimite do cartão insuficiente\033[m. Limite disponível: \033[32mR${:.2f}\033[m'.format(self.limiteCartão))

    def altera_Chave_Pix(self, nova_Chave):
        self.chave_Pix = nova_Chave
        print('Chave de pix atual: {}'.format(self.chave_Pix))
        print('Chave Pix alterada com sucesso!')

    def altera_limite_Cartão(self, novo_Limite):
        if novo_Limite <= 2000:
            self.limiteCartão = novo_Limite
            print('Limite alterado para \033[32mR${:.2f}\033[m'.format(self.limiteCartão))
        else:
            print('\033[31mErro\033[31m:\033[4m O limite não pode ultrapassar \033[31mR$2000,00\033[m')

    # Funcionalidade de Verificar saldo
    def varificãodeSaldo(self):
        print('Saldo Atual\033[32m R${:.2f}\033[m'.format(self.saldo))
    #Funcionalidade Extarto
    def ver_extrato(self):
        print("\n--- EXTRATO ---")
        if not self.extrato:
            print("Nenhuma movimentação realizada.")
        else:
            for mov in self.extrato:
                print(mov)
        print("----------------\n")
#Menu
def menu():
    conta = contaBancaria(chave_Pix="otavio07@gmail.com", limiteCartão=1000.0, saldo=0)  # exemplo com limite disponível
    while True:
        # Menu funções
        print('---Funções do Sistema---')
        print('1. Depósito')
        print('2. PIX')
        print('3. Altera chave pix')
        print('4. Saldo')
        print('5. Altera limite de crédito')
        print('6. Extarto')
        print('7. Sair')
        opeção = (input('Escolha qual opção deseja: '))
        if opeção == '1':
            valor = float(input('Qual o valor que deseja depositar R$: '))
            # DEPOSITAR FUNDOS
            conta.deposito(valor)
            print('Valor depositado!')
        elif opeção == '2':
            # TRANSFERÊNCIA\PIX
            chave = str(input('Informe a chave Pix: '))
            valor = float(input('Qual valor deseja transferir R$: '))
            # Primeiro tenta PIX normal
            if conta.saldo >= valor:
                conta.pix(chave, valor)
            else:
                print('Saldo insuficiente para o valor solicitado.')
                usar_cartao = input('Deseja fazer o PIX usando o cartão de crédito? (Sim/Não): ').strip().lower()
                if usar_cartao == 'sim':
                    conta.pix_com_cartao(chave, valor)
                else:
                    print('Operação cancelada.')
        #Verificar a Chave Pix atual/Altera a Chave Pix
        elif opeção == '3':
            print('Chave Pix atual: {}'.format(conta.chave_Pix))
            altera = input('Deseja alterar a chave pix? (Digite Sim/Não): ').strip().lower()
            if altera == 'sim':
                nova = str(input('Digite a nova chave pix: '))
                conta.altera_Chave_Pix(nova)
            else:
                print('Chave Pix mantida: {}'.format(conta.chave_Pix))
        #Verifica o saldo.
        elif opeção == '4':
            conta.varificãodeSaldo()
            print('Limite disponível no cartão: R${:.2f}'.format(conta.limiteCartão))
        #Altera o limite do cartão
        elif opeção == '5':
            print('Limite atual: R${:.2f}'.format(conta.limiteCartão))
            limite = float(input('Digite o valor do limite que deseja alterar: '))
            conta.altera_limite_Cartão(limite)
        elif opeção == '6':
            conta.ver_extrato()
        #Fecha o sistema.
        elif opeção == '7':
            print('Saindo da conta, Tenha um bom dia!')
            break
        else:
            print('Opção inválida!')

menu()
