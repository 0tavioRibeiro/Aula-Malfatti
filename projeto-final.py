# ==============================================
# PROJETO: Sistema de Casa Inteligente 
# Implementa os 10 padrões solicitados:
# 1 Singleton, 2 Factory, 3 Observer, 4 Strategy, 5 Builder,
# 6 Facade, 7 Adapter, 8 Decorator, 9 Command, 10 Dependency Injection
# ==============================================

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


# Abstract  base : Dispositivo DeviceFactor
class  Dispositovo (ABC):
    @abstractmethod
    def ligar (self):
        pass

    @abstractmethod
    def desligar (self): 
        pass

    @abstractmethod
    def status (self) -> str:
        pass

# Factory:  DeviceFactor (Fator de dispositivo)
class Luz(Dispositovo):
    def __init__(self):
        self._ligada = False
    
    def ligar(self): self._ligada = True

    def desligar(self): self._ligada = False
    
    def status(self) -> str: 
        return 'Luz: Ligada' if self._ligada else 'Luz: Desligada'

class Camera(Dispositivo):
    def __init__(self):
        self._gravando = False
    
    def ligar(self): self._gravando = True

    def desligar(self): self._gravando = False

    def status (self) -> str:
        return 'Câmera: Gravando' if self._gravando else 'Câmera:Desligada'

class SensorMovimento(Dispositivo):
    def __init__(self):
        self._ativo = False

    def ligar(self): self._ativo = True

    def desligar(self): self._ativo = False

    def status(self) -> str:
        return 'Sensor: Ativo' if self._ativo else 'Sensor: Desligado'
# A classe DispositvosFactory recebe uma string dizendo qual dispositivo criar e retorna um objeto desse tipo. Ela funciona como uma fábrica de dispositivos
# Essa classe será usada como uma fábrica para criar objetos de tipos diferentes (Luz, Camera, SensorMovimento).
class DispositvosFactory:
    @staticmethod #indica que o método não usa self ou informações internas da classe.
    def criar (tipo:str) -> Dispositivo:
        # Cria um dicionário que mapeia uma string (chave) para uma classe (valor):
        m = {
            'luz':Luz,
            'camera':Camera,
            'sensor':SensorMovimento
            }
        if tipo not in m:
            raise ValueError('Tipo desconhecido:{}'.format(tipo))
        return m [tipo]()
    
# OBSERVADOR / NOTIFICAÇÃO
class Observador(ABC):
    @abstractmethod
    def atualizar(self, evento:str):pass

class AppUsuario(Observador):
    def __init__(self,nome):
        self.nome = nome
    
    def atualizar(self, evento: str):
        print('{} -APP'.format(evento))

class Notificacao:
    def __init__(self):
        self._observadores: List[Observador]=[]
    
    def registra(self,obs:Observador):
        self._observadores.append(obs)

    def remover (self,obs:Observador): 
        self._observadores.remove(obs)

    def notificar(self, evento: str):
        for o in list(self._observadores): o.atualizar(evento)
        
# STRATEGY: Modos de operação

class ModoOperacao(ABC):
    @abstractmethod
    def aplicar(self, dispositivos: List[Dispositivo]): pass

class ModoEconomia(ModoOperacao):
    def aplicar(self, dispositivos: List[Dispositivo]):
        for d in dispositivos:
            try:
                d.desligar()
            except Exception:
                pass

class ModoConforto(ModoOperacao):
    def aplicar(self, dispositivos: List[Dispositivo]):
        for d in dispositivos:
            try:
                d.ligar()
            except Exception:
                pass

class ModoSeguranca(ModoOperacao):
    def aplicar(self, dispositivos: List[Dispositivo]):
        # Sensores ligados, cameras ligadas, luzes desligadas
        for d in dispositivos:
            if isinstance(d, SensorMovimento) or isinstance(d, Camera):
                d.ligar()
            elif isinstance(d, Luz):
                d.desligar()
        
#  BUILDER PATTERN
#  Construção gradual de rotinas automatizadas

class Rotina:
    def __init__(self, nome: str, acoes: List[Callable]):
        self.nome = nome
        self.acoes = acoes

    def executar(self):
        for acao in self.acoes:
            acao()


class RotinaBuilder:
    def __init__(self):
        self.nome = "Rotina"
        self.acoes = []

    def com_nome(self, nome: str):
        self.nome = nome
        return self

    def adicionar_acao(self, acao: Callable):
        self.acoes.append(acao)
        return self

    def construir(self) -> Rotina:
        return Rotina(self.nome, self.acoes)



#  FACADE PATTERN
#   Interface  para controlar todo o sistema

class SmartHomeFacade:
    def __init__(self, controller):
        self._controller = controller

    def ativar_modo_seguranca(self):
        self._controller.set_modo(ModoSeguranca())

    def ativar_modo_conforto(self):
        self._controller.set_modo(ModoConforto())

    def executar_rotina(self, rotina: Rotina):
        rotina.executar()

    def ligar_dispositivo(self, dispositivo: Dispositivo):
        self._controller.executar_comando(LigarCommand(dispositivo))

    def desligar_dispositivo(self, dispositivo: Dispositivo):
        self._controller.executar_comando(DesligarCommand(dispositivo))



#  ADAPTER PATTERN
#  Adapta APIs de terceiros para o formato do sistema

class PhilipsHueAPI:
    def __init__(self):
        self.on = False

    def turn_on(self):
        self.on = True

    def turn_off(self):
        self.on = False

    def get_state(self):
        return self.on


class PhilipsHueAdapter(Dispositivo):
    def __init__(self, api: PhilipsHueAPI):
        self._api = api

    def ligar(self):
        self._api.turn_on()

    def desligar(self):
        self._api.turn_off()

    def status(self) -> str:
        return "Luz Hue: Ligada" if self._api.get_state() else "Luz Hue: Desligada"

#  DECORATOR PATTERN
#  Acrescenta funcionalidades extras sem alterar a classe base

class DispositivoDecorator(Dispositivo):
    def __init__(self, dispositivo: Dispositivo):
        self._dispositivo = dispositivo

    def ligar(self):
        self._dispositivo.ligar()

    def desligar(self):
        self._dispositivo.desligar()

    def status(self) -> str:
        return self._dispositivo.status()


class MonitoramentoRemotoDecorator(DispositivoDecorator):
    def __init__(self, dispositivo: Dispositivo, notificador: Notificador):
        super().__init__(dispositivo)
        self._notificador = notificador

    def ligar(self):
        super().ligar()
        self._notificador.notificar(
            f"{self._dispositivo.__class__.__name__} ligado remotamente"
        )

    def desligar(self):
        super().desligar()
        self._notificador.notificar(
            f"{self._dispositivo.__class__.__name__} desligado remotamente"
        )



#  COMMAND PATTERN
#   Permite desfazer ações e registrar histórico

class Command(ABC):
    @abstractmethod
    def executar(self):
        pass

    @abstractmethod
    def desfazer(self):
        pass


class LigarCommand(Command):
    def __init__(self, dispositivo: Dispositivo):
        self._disp = dispositivo

    def executar(self):
        self._disp.ligar()

    def desfazer(self):
        self._disp.desligar()


class DesligarCommand(Command):
    def __init__(self, dispositivo: Dispositivo):
        self._disp = dispositivo

    def executar(self):
        self._disp.desligar()

    def desfazer(self):
        self._disp.ligar()



#  SINGLETON + DEPENDENCY INJECTION
#  CentralController tem apenas uma instância
#  Recebe o notificador como dependência externa

class CentralController:
    _instancia = None

    def __new__(cls, notifier=None):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def __init__(self, notifier=None):
        if not hasattr(self, "_initialized"):
            self._dispositivos = []
            self._historico = []
            self._modo = None
            self._notificador = notifier or Notificador()
            self._initialized = True


    def adicionar_dispositivo(self, dispositivo: Dispositivo):
        self._dispositivos.append(dispositivo)
        self._notificador.notificar(
            f"Dispositivo adicionado: {dispositivo.__class__.__name__}"
        )

    def executar_comando(self, cmd: Command):
        cmd.executar()
        self._historico.append(cmd)
        self._notificador.notificar(
            f"Comando executado: {cmd.__class__.__name__} às {datetime.now()}"
        )

    def desfazer_ultimo(self):
        if not self._historico:
            return
        cmd = self._historico.pop()
        cmd.desfazer()
        self._notificador.notificar(
            f"Comando desfeito:' {cmd.__class__.__name__}' às {datetime.now()}"
        )

    def set_modo(self, modo: ModoOperacao):
        self._modo = modo
        if modo:
            modo.aplicar(self._dispositivos)
            self._notificador.notificar(
                f"Modo definido: {modo.__class__.__name__}"
            )


if __name__ == "__main__":
    # OBSERVER
    notificador = Notificador()
    app = AppUsuario("Otavio")
    notificador.registrar(app)

   
    controle = CentralController(notifier=notificador)

    l1 = DispositivosFactory.criar("luz")
    c1 = DispositivosFactory.criar("camera")
    s1 = DispositivosFactory.criar("sensor")

    hue_api = PhilipsHueAPI()
    hue_lamp = PhilipsHueAdapter(hue_api)

 
    hue_lamp_monitorada = MonitoramentoRemotoDecorator(hue_lamp, notificador)


    for d in [l1, c1, s1, hue_lamp_monitorada]:
        controle.adicionar_dispositivo(d)

    facade = SmartHomeFacade(controle)


    facade.ativar_modo_seguranca()

    facade.ligar_dispositivo(l1)
    for d in controle._dispositivos:
        print(d.status())


    for i in tqdm(range(10)):
        time.sleep(1.0)

    rotina = (RotinaBuilder()
              .com_nome("Boa Noite")
              .adicionar_acao(lambda: facade.desligar_dispositivo(l1))
              .adicionar_acao(lambda: facade.ativar_modo_conforto())
              .construir())

    facade.executar_rotina(rotina)
    for d in controle._dispositivos:
        print(d.status())

    for i in tqdm(range(10)):
        time.sleep(1.0)

    controle.desfazer_ultimo()

    print("Fim da simulação")



