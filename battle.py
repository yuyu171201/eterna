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

    def take_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 0)

    def on_acted(self):
        self.ct -= self.threshold

    def overheat(self):
        self.threshold += ACTION_COST

    def cooldown(self):
        self.threshold = ACTION_COST


    @property
    def is_alive(self):
        return self.current_hp > 0

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

        for actor in self.alived_actors:
            actor.ct += actor.speed

        max_ct = 0
        maxed_actor = None

        for actor in self.alived_actors:
            if actor.ct >= actor.threshold and actor.ct > max_ct:
                max_ct = actor.ct
                maxed_actor = actor

        if maxed_actor is not None:
            for actor in self.alived_actors:
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


def get_alive_actors(
    combatants : list[CombatState]
) -> list[CombatState]:
    alives = [actor for actor in combatants if actor.is_alive]
    return alives

def get_enemies_of(
    attacker : CombatState ,
    combatants : list[CombatState]
) -> list[CombatState]:
    enemies = [actor for actor in combatants if actor.camp != attacker.camp]
    return enemies

def get_valid_enemies(
    attacker : CombatState ,
    combatants : list[CombatState]
) -> list[CombatState]:
    valid_enemies = get_enemies_of(attacker, get_alive_actors(combatants))
    return valid_enemies

def get_allies_of(
    attacker : CombatState ,
    combatants : list[CombatState]
) -> list[CombatState]:
    allies = [actor for actor in combatants if actor.camp == attacker.camp]
    return allies


# 攻撃対象の選択
def select_target(
    attacker : CombatState ,
    combatants : list[CombatState]
) -> CombatState:
    valid_targets = get_enemies_of(attacker, get_alive_actors(combatants))

    target = random.choice(valid_targets)
    return target


# 攻撃対象の入力での選択
def input_target(
    attacker : CombatState ,
    combatants : list[CombatState]
) -> CombatState:
    print(f'{attacker.name} の攻撃')
    enemies = get_valid_enemies(attacker, combatants)
    for i, enemy in enumerate(enemies):
        print(f"{i} --> {enemy.name}")    

    while True:
        try:
            target_idx = int(input('対象を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if target_idx >= 0 and target_idx < len(enemies):
            target = enemies[target_idx]
            print()
            return target
        else:
            print('不適切な入力です')
            print()


# 攻撃処理
def attack(
    attacker : CombatState ,
    defender : CombatState
):
    # 辞書型(攻撃者,　被攻撃者, ダメージ量)
    event = {'attacker':attacker.name, 'defender':defender.name, 'damage':attacker.atk}

    defender.take_damage(attacker.atk)
    return event


# バトルの実行
def auto_battle(
    entries : list[tuple[Unit, Camp]],
    choose_target = select_target
):
    turn = 0
    logs = []

    combatants = []

    for unit, camp in entries:
        combatants.append(CombatState(unit, camp=camp))

    action = ActionOrderManager(combatants)

    while True:
        survivors = get_alive_actors(combatants)
        remain_camps = [actor.camp for actor in survivors]
        num_camps = len(set(remain_camps))

        if num_camps == 1:
            return remain_camps[0], logs
        elif num_camps == 0:
            return None, logs
        
        turn += 1
            
        attacker = action.next_actor()

        if attacker.camp == Camp.PLAYER:
            target = choose_target(attacker, combatants)
        else:
            target = select_target(attacker, combatants)

        event = attack(attacker, target)

        event['turn'] = turn
        logs.append(event)


if __name__ == "__main__":
    yusha = Unit("勇者", 100, 10, 60)
    yusha.show_status()
    slime = Unit("スライム", 100, 5, 50)
    slime.show_status()
    goblin = Unit("ゴブリン", 40, 15, 70)
    goblin.show_status()

    entries = [[yusha, Camp.PLAYER], [slime, Camp.ENEMY], [goblin, Camp.ENEMY]]

    print("バトル開始!\n")

    win_camp, logs = auto_battle(entries, input_target)
    for log in logs:
        print(f"turn {log['turn']}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")

    match win_camp:
        case Camp.PLAYER:
            winner = '自'
        case Camp.ENEMY:
            winner = '敵'

    print(f"{winner}陣営が勝利しました。")