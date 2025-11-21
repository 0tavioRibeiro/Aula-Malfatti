# ==============================================
# PROJETO: Sistema de Casa Inteligente 
# Implementar os 10 padrões solicitados:
# 1 Singleton, 2 Factory, 3 Observer, 4 Strategy, 5 Builder,
# 6 Facade, 7 Adapter, 8 Decorator, 9 Command, 10 Dependency Injection
# ==============================================

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


# Abstract  base : Dispositivo DeviceFactor
class  Dispositivo (ABC):
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
class Luz(Dispositivo):
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
        
#Modos de operação

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
        


        






