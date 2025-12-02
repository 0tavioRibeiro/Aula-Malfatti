# Smart Home System
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Callable, List
from tqdm import tqdm
import time


# HERANÇA – Classe base para todos os dispositivos

class Device(ABC):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass
 
    @abstractmethod
    def status(self) -> str:
        pass



# FACTORY – Criação de dispositivos de forma padronizada

class Light(Device):
    def __init__(self):
        self._on = False

    def turn_on(self):
        self._on = True

    def turn_off(self):
        self._on = False

    def status(self) -> str:
        return "Luz: LIGADA" if self._on else "Luz: DESLIGADA"


class Camera(Device):
    def __init__(self):
        self._recording = False

    def turn_on(self):
        self._recording = True

    def turn_off(self):
        self._recording = False

    def status(self) -> str:
        return "Câmera: Gravação" if self._recording else "Câmera: DESLIGADA"


class MotionSensor(Device):
    def __init__(self):
        self._active = False

    def turn_on(self):
        self._active = True

    def turn_off(self):
        self._active = False

    def status(self) -> str:
        return "Sensor de Movimento: Ativo" if self._active else "Sensor de movimento: DESLIGADO"


# Factory que cria objetos automaticamente
class DeviceFactory:
    @staticmethod
    def create(device_type: str) -> Device:
        mapping = {
            "light": Light,
            "camera": Camera,
            "sensor": MotionSensor
        }

        if device_type not in mapping:
            raise ValueError(f"Tipo desconhecido: {device_type}")

        return mapping[device_type]()


# OBSERVER – Notificações enviadas para vários observadores
# Ele permite que vários objetos recebam notificações quando algo acontece no sistema

class Observer(ABC):
    @abstractmethod
    def update(self, event: str):
        pass


class UserApp(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, event: str):
        print(f"{self.name} - APP received notification: {event}")


class Notifier:
    def __init__(self):
        self._observers: List[Observer] = []

    def register(self, observer: Observer):
        self._observers.append(observer)

    def remove(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, event: str):
        for observer in list(self._observers):
            observer.update(event)



# STRATEGY – Modos de operação diferentes

class OperationMode(ABC):
    @abstractmethod
    def apply(self, devices: List[Device]):
        pass


class EcoMode(OperationMode):
    def apply(self, devices: List[Device]):
        for device in devices: 
            try:
                device.turn_off()
            except Exception:
                pass


class ComfortMode(OperationMode):
    def apply(self, devices: List[Device]):
        for device in devices:
            try:
                device.turn_on()
            except Exception:
                pass


class SecurityMode(OperationMode):
    def apply(self, devices: List[Device]):
        for device in devices:
            if isinstance(device, (MotionSensor, Camera)):
                device.turn_on()
            elif isinstance(device, Light):
                device.turn_off()


# Construção de rotinas passo a passo

class Routine:
    def __init__(self, name: str, actions: List[Callable]):
        self.name = name
        self.actions = actions

    def execute(self):
        for action in self.actions:
            action()


class RoutineBuilder:
    def __init__(self):
        self.name = "Routine"
        self.actions = []

    def with_name(self, name: str):
        self.name = name
        return self

    def add_action(self, action: Callable):
        self.actions.append(action)
        return self

    def build(self) -> Routine:
        return Routine(self.name, self.actions)


# FACADE – Interface simples para controlar o sistema

class SmartHomeFacade:
    def __init__(self, controller):
        self._controller = controller

    def activate_security_mode(self):
        self._controller.set_mode(SecurityMode())

    def activate_comfort_mode(self):
        self._controller.set_mode(ComfortMode())

    def execute_routine(self, routine: Routine):
        routine.execute()

    def turn_on_device(self, device: Device):
        self._controller.execute_command(TurnOnCommand(device))

    def turn_off_device(self, device: Device):
        self._controller.execute_command(TurnOffCommand(device))



#  Adiciona funcionalidades sem alterar a classe base

class DeviceDecorator(Device):
    def __init__(self, device: Device):
        self._device = device

    def turn_on(self):
        self._device.turn_on()

    def turn_off(self):
        self._device.turn_off()

    def status(self):
        return self._device.status()


class RemoteMonitoringDecorator(DeviceDecorator):
    def __init__(self, device: Device, notifier: Notifier):
        super().__init__(device)
        self._notifier = notifier

    def turn_on(self):
        super().turn_on()
        self._notifier.notify(
            f"{self._device.__class__.__name__} remotely turned ON"
        )

    def turn_off(self):
        super().turn_off()
        self._notifier.notify(
            f"{self._device.__class__.__name__} remotely turned OFF"
        )



#Executar e desfazer ações

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class TurnOnCommand(Command):
    def __init__(self, device: Device):
        self._device = device

    def execute(self):
        self._device.turn_on()

    def undo(self):
        self._device.turn_off()


class TurnOffCommand(Command):
    def __init__(self, device: Device):
        self._device = device

    def execute(self):
        self._device.turn_off()

    def undo(self):
        self._device.turn_on()


# SINGLETON + DEPENDENCY INJECTION – Controlador central

class CentralController:
    _instance = None

    def __new__(cls, notifier=None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, notifier=None):
        if not hasattr(self, "_initialized"):
            self._devices = []
            self._history = []
            self._mode = None
            self._notifier = notifier or Notifier()
            self._initialized = True

    def add_device(self, device: Device):
        self._devices.append(device)
        self._notifier.notify(f"Device added: {device.__class__.__name__}")

    def execute_command(self, command: Command):
        command.execute()
        self._history.append(command)
        self._notifier.notify(f"Command executed: {command.__class__.__name__} at {datetime.now()}")

    def undo_last(self):
        if not self._history:
            return
        cmd = self._history.pop()
        cmd.undo()
        self._notifier.notify(f"Command undone: {cmd.__class__.__name__} at {datetime.now()}")

    def set_mode(self, mode: OperationMode):
        self._mode = mode
        if mode:
            mode.apply(self._devices)
            self._notifier.notify(f"Mode set: {mode.__class__.__name__}")




if __name__ == "__main__":
    notifier = Notifier()
    app = UserApp("Otavio")
    notifier.register(app)

    controller = CentralController(notifier=notifier)

    l1 = DeviceFactory.create("light")
    c1 = DeviceFactory.create("camera")
    s1 = DeviceFactory.create("sensor")




    for device in [l1, c1, s1,]:
        controller.add_device(device)

    facade = SmartHomeFacade(controller)

    facade.activate_security_mode()


    for device in controller._devices:
        print(device.status())

    for tempo in tqdm(range(5)):
        time.sleep(0.5)

    routine = (
        RoutineBuilder()
        .with_name("Boa noite")
        .add_action(lambda: facade.turn_off_device(l1))
        .add_action(lambda: facade.activate_comfort_mode())
        .build()
    )

    facade.execute_routine(routine)

    for device in controller._devices:
        print(device.status())

    for tempo in tqdm(range(5)):
        time.sleep(0.5)

    controller.undo_last()


    print("Fim")
