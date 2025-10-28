[Simulador.py](https://github.com/user-attachments/files/23197429/Simulador.py)
from abc import ABC, abstractmethod  # importa ferramentas para criar classes abstratas
import random  # importa módulo para números aleatórios (dano, redução)
import time  # importa módulo para pausas temporais (time.sleep)

# ===== FUNÇÃO AUXILIAR =====
def health_bar(current_hp, max_hp, length=20):
    # calcula a proporção da vida atual em relação à vida máxima
    proportion = max(current_hp / max_hp, 0)  # evita proporção negativa
    # converte a proporção em quantidade de 'blocos' cheios na barra
    filled = int(proportion * length)
    # calcula quantos blocos ficam vazios
    empty = length - filled
    # retorna a string que representa a barra visual e os valores numéricos
    return f"[{'█' * filled}{'░' * empty}] {current_hp}/{max_hp}"

# ===== CLASSE BASE =====
class Character(ABC):
    # Classe abstrata que representa um personagem genérico
    def __init__(self, name, health, level):
        # inicializa nome, vida (e vira int), vida_max e nível (int)
        self.name = name
        self.health = int(health)
        self.max_health = int(health)  # guarda a vida inicial como vida máxima
        self.level = int(level)

    @abstractmethod
    def attack(self):
        # método abstrato: deve retornar o dano causado pelo personagem
        pass

    @abstractmethod
    def defend(self, damage):
        # método abstrato: recebe o dano recebido e deve aplicar na vida
        pass

    def is_alive(self):
        # retorna True se o personagem ainda tiver vida positiva
        return self.health > 0

    def __str__(self):
        # representação em string quando usamos print(objeto)
        return f"Name: {self.name}, Health: {self.health}, Level: {self.level}"


# ===== GUERREIRO =====
class Warrior(Character):
    def __init__(self, name, health, level, sword):
        # inicializa o guerreiro chamando o construtor da classe base
        super().__init__(name, health, level)
        # atributo específico: tipo de espada
        self.sword = sword

    def attack(self):
        # dano base aleatório entre 20 e 35, com bônus de nível
        damage = random.randint(20, 35) + self.level // 2
        # print estilizado informando o ataque
        print(f"⚔️ {self.name} attacks with {self.sword}, dealing {damage} damage!")
        # retorna o dano para ser usado pela função que controla a batalha
        return damage

    def defend(self, damage):
        # redução aleatória que simula bloqueio/armadura
        reduction = random.randint(5, 15)
        # dano final não pode ser negativo
        final_damage = max(damage - reduction, 0)
        # aplica o dano na vida do guerreiro
        self.health -= final_damage
        # mostra mensagem explicando a defesa e o dano tomado
        print(f"🛡️ {self.name} blocks with a shield and takes {final_damage} damage (reduced {reduction})!")


# ===== ARQUEIRO =====
class Archer(Character):
    def __init__(self, name, health, level, bow):
        # inicializa atributos comuns via super
        super().__init__(name, health, level)
        # atributo específico: tipo de arco
        self.bow = bow

    def attack(self):
        # dano base aleatório entre 15 e 30, com um bônus de nível menor
        damage = random.randint(15, 30) + self.level // 3
        # print explicativo
        print(f"🏹 {self.name} shoots an arrow with {self.bow}, dealing {damage} damage!")
        return damage

    def defend(self, damage):
        # arqueiro tem probabilidade de esquivar (redução entre 0 e 10)
        reduction = random.randint(0, 10)
        final_damage = max(damage - reduction, 0)
        self.health -= final_damage
        print(f"💨 {self.name} tries to dodge and takes {final_damage} damage (reduced {reduction})!")


# ===== MAGO =====
class Mage(Character):
    def __init__(self, name, health, level, staff):
        # inicializa via classe base
        super().__init__(name, health, level)
        # atributo específico: cajado
        self.staff = staff

    def attack(self):
        # dano muito variável (10 a 40) com bônus pequeno de nível
        damage = random.randint(10, 40) + self.level // 4
        print(f"✨ {self.name} casts a spell with {self.staff}, dealing {damage} damage!")
        return damage

    def defend(self, damage):
        # magia protetora é fraca aqui: redução entre 0 e 5
        reduction = random.randint(0, 5)
        final_damage = max(damage - reduction, 0)
        self.health -= final_damage
        print(f"🔮 {self.name} uses a protection spell and takes {final_damage} damage (reduced {reduction})!")


# ===== INIMIGO =====
class Enemy(Character):
    def __init__(self, name, health, level, kind):
        # inicializa via classe base
        super().__init__(name, health, level)
        # atributo específico: tipo de inimigo (ex: Goblin, Dragão)
        self.kind = kind

    def attack(self):
        # dano do inimigo, balanceado aqui entre 15 e 30 com bônus de nível
        damage = random.randint(15, 30) + self.level // 2
        print(f"👹 {self.name} ({self.kind}) attacks fiercely, dealing {damage} damage!")
        return damage

    def defend(self, damage):
        # inimigo também possui redução, entre 3 e 10
        reduction = random.randint(3, 10)
        final_damage = max(damage - reduction, 0)
        self.health -= final_damage
        print(f"🪓 {self.name} partially blocks and takes {final_damage} damage (reduced {reduction})!")


# ===== CRIAÇÃO DOS PERSONAGENS =====
# instancia um guerreiro com nome, vida, nível e arma
warrior = Warrior('Thorfinn', 100, 20, 'Long Sword')
# instancia um arqueiro
archer = Archer('Green Archer', 80, 18, 'Long Bow')
# instancia um mago
mage = Mage('Wizard of Oz', 70, 15, 'Oak Staff')
# instancia o inimigo (boss) com vida alta
enemy = Enemy('Goblin King', 250, 22, 'Goblin')

# lista que contém os heróis que vão lutar contra o inimigo
characters = [warrior, archer, mage]

print("\n🌟=== BATTLE START ===🌟\n")  # mensagem inicial
time.sleep(1)  # pausa para dar ritmo à exibição

round_number = 1  # contador de rodadas
# loop principal: enquanto o inimigo estiver vivo e existir ao menos um herói vivo
while enemy.is_alive() and any(c.is_alive() for c in characters):
    print(f"\n🔥 --- ROUND {round_number} --- 🔥\n")
    time.sleep(0.8)  # pequena pausa

    # para cada personagem na lista
    for c in characters:
        # apenas personagens vivos participam; e o inimigo precisa ainda estar vivo
        if c.is_alive() and enemy.is_alive():
            print(f"➡️ {c.name} prepares to attack...")
            time.sleep(0.6)

            # personagem realiza ataque; o método ataque retorna o dano
            damage = c.attack()
            time.sleep(0.5)

            # aplica o dano no inimigo usando o método defesa do inimigo
            enemy.defend(damage)
            # exibe a barra de vida do inimigo
            print(f"❤️ {enemy.name}'s Health: {health_bar(enemy.health, enemy.max_health)}\n")
            time.sleep(0.8)

            # se o inimigo morreu com o ataque, sair do laço interno
            if not enemy.is_alive():
                print(f"💥 {enemy.name} has been defeated!")
                break

            print(f"⚠️ {enemy.name} prepares a counterattack!\n")
            time.sleep(0.8)

            # inimigo contra-ataca o personagem atual
            enemy_damage = enemy.attack()
            time.sleep(0.5)

            # personagem aplica sua defesa recebendo o dano do inimigo
            c.defend(enemy_damage)
            # exibe a barra de vida do personagem
            print(f"💚 {c.name}'s Health: {health_bar(c.health, c.max_health)}\n")
            time.sleep(0.8)

            # se o personagem morreu, informa
            if not c.is_alive():
                print(f"💀 {c.name} has fallen in battle!")
                time.sleep(0.8)

    round_number += 1  # incrementa contador de rodadas
    print("⏳ Preparing next round...\n")
    time.sleep(1.2)

print("\n🏁 === END OF BATTLE === 🏁\n")
time.sleep(1)

# resultado final: verifica se o inimigo ainda está vivo
if enemy.is_alive():
    print(f"💀 The enemy {enemy.name} won the battle!")
else:
    print("🏆 The heroes defeated the enemy!")

print("\n--- FINAL RESULTS ---")
# mostra o status final de cada personagem (vivo ou morto)
for c in characters:
    status = "⚰️ DEAD" if not c.is_alive() else "💪 ALIVE"
    print(f"{c} → {status}")
# imprime também o objeto inimigo (usa __str__)
print(enemy)
