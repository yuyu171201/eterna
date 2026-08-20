import random
from enum import Enum

from unit import Unit

BASE_SPEED = 80
ACTION_COST = 10000

class Camp(Enum):
    PLAYER = 1
    ENEMY = 2

class CombatState:
    def __init__(self, unit, camp=None):
        self.unit = unit
        self.camp = camp

        self.current_hp = unit.max_hp

        self.ct = 0
        self.threshold = ACTION_COST

        self.is_alive = True

    def take_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 0)

    def on_acted(self):
        self.ct -= self.threshold

    def overheat(self):
        self.threshold += ACTION_COST

    def cooldown(self):
        self.threshold = ACTION_COST

    @property
    def atk(self):
        return self.unit.atk

    @property
    def speed(self):
        return self.unit.spd

    @property
    def name(self):
        return self.unit.name
    
    def __repr__(self):
        return f'{self.__class__.__name__}(unit={self.unit.name}, camp={self.camp})'

class ActionOrderManager:
    def __init__(self, actors):
        self.actors = actors

    def tick(self):
        self.alived_actors = get_alive_actors(self.actors)

        for actor in self.actors:
            actor.ct += actor.speed

        max_ct = 0
        maxed_actor = None

        for actor in self.actors:
            if actor.ct >= actor.threshold and actor.ct > max_ct:
                max_ct = actor.ct
                maxed_actor = actor

        if maxed_actor is not None:
            for actor in self.actors:
                if actor == maxed_actor:
                    actor.on_acted()
                    actor.overheat()
                else:
                    actor.cooldown()
            return maxed_actor

        return None

    def next_actor(self):
        while True:
            actor = self.tick()
            if actor is not None:
                return actor


def get_alive_actors(combatants):
    alives = [actor for actor in combatants if actor.is_alive]
    return alives

def get_enemies_of(attacker, combatants):
    enemies = [actor for actor in combatants if actor.camp != attacker.camp]
    return enemies

def get_allies_of(attacker, combatants):
    allies = [actor for actor in combatants if actor.camp == attacker.camp]
    return allies
        

# 攻撃処理
def attack(actor1, actor2):
    # 辞書型(攻撃者,　被攻撃者, ダメージ量)
    event = {'attacker':actor1.name, 'defender':actor2.name, 'damage':actor1.atk}

    actor2.take_damage(actor1.atk)
    return event


# 攻撃対象の選択
def select_target(attacker, combatants):
    valid_targets = get_enemies_of(attacker, get_alive_actors(combatants))

    target = random.choice(valid_targets)
    return target


def do_attack(attacker, combatants):
    target = select_target(attacker, combatants)
    event = attack(attacker, target)
    return event, target


# バトルの実行
def auto_battle(units):
    turn = 0
    logs = []

    combatants = []

    for unit, camp in units.items():
        combatants.append(CombatState(unit, camp=camp))

    action = ActionOrderManager(combatants)

    while True:
        attacker = action.next_actor()

        turn += 1
        event, enemy = do_attack(attacker, combatants)
        event['turn'] = turn
        logs.append(event)

        if enemy.current_hp <= 0:
            return enemy, logs


if __name__ == "__main__":
    yusha = Unit("勇者", 100, 10, 60)
    yusha.show_status()
    slime = Unit("スライム", 100, 5, 50)
    slime.show_status()
    goblin = Unit("ゴブリン", 40, 15, 70)
    goblin.show_status()

    units = {yusha: Camp.PLAYER, slime: Camp.ENEMY, goblin: Camp.ENEMY}

    print("バトル開始!\n")

    loser, logs = auto_battle(units)
    for log in logs:
        print(f"turn {log['turn']}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")