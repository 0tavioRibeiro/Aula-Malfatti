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

class Camera(Dispositovo):
    def __init__(self):
