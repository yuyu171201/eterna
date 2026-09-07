import random
from enum import Enum

from eltena_master import (
    EltenaMaster,
    archer_master,
    asashin_master,
    goblin_master,
    slime_master,
    souryo_master,
    yusha_master,
)

MAX_ELTENA_PER_CAMP = 4
ACTION_COST = 10000

class Camp(Enum):
    PLAYER = 1
    ENEMY = 2

class BattleEltena:
    def __init__(self, master, camp=None):
        self.master = master
        self.camp = camp

        self.current_hp = master.max_hp

        self.action_gauge = 0
        self.threshold = ACTION_COST

    def take_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 0)

    def on_acted(self):
        self.action_gauge -= self.threshold

    def overheat(self):
        self.threshold += ACTION_COST

    def cooldown(self):
        self.threshold = ACTION_COST


    @property
    def is_alive(self):
        return self.current_hp > 0

    @property
    def atk(self):
        return self.master.atk

    @property
    def speed(self):
        return self.master.spd

    @property
    def name(self):
        return self.master.name
    
    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master.name}, camp={self.camp})'

class ActionOrderManager:
    def __init__(self, actors):
        self.actors = actors

    def tick(self):
        self.alived_actors = get_alive_actors(self.actors)

        for actor in self.alived_actors:
            actor.action_gauge += actor.speed

        max_action_gauge = 0
        maxed_actor = None

        for actor in self.alived_actors:
            if actor.action_gauge >= actor.threshold and actor.action_gauge > max_action_gauge:
                max_action_gauge = actor.action_gauge
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
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    alives = [actor for actor in combatants if actor.is_alive]
    return alives

def get_enemies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    enemies = [actor for actor in combatants if actor.camp != attacker.camp]
    return enemies

def get_valid_enemies(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    valid_enemies = get_enemies_of(attacker, get_alive_actors(combatants))
    return valid_enemies

def get_allies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    allies = [actor for actor in combatants if actor.camp == attacker.camp]
    return allies

def get_allies_amount_of(
    camp : Camp ,
    combatants : list[BattleEltena]  
) -> int:
    allies = [eltena for eltena in combatants if eltena.camp == camp]
    return len(allies)


# 攻撃対象の選択
def select_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    valid_targets = get_enemies_of(attacker, get_alive_actors(combatants))

    target = random.choice(valid_targets)
    return target

# 攻撃対象の入力での選択
def input_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    enemies = get_valid_enemies(attacker, combatants)

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

def show_attacker(attacker : BattleEltena):
    print(f'{attacker.name} の攻撃')
    print()

# 攻撃処理
def attack(
    attacker : BattleEltena ,
    defender : BattleEltena
):
    # 辞書型(攻撃者,　被攻撃者, ダメージ量)
    event = {'attacker':attacker.name, 'defender':defender.name, 'damage':attacker.atk}

    defender.take_damage(attacker.atk)
    return event

def slash(
    attacker : BattleEltena ,
    defender : BattleEltena
):
    damage = attacker.atk * 2
    event = {'attacker':attacker.name, 'defender':defender.name, 'damage':damage}

    defender.take_damage(damage)
    return event

def input_select_action():
    print("行動を選択してください")
    print("0. 攻撃")
    print("1. スキル１(スラッシュ)")
    while True:
        try:
            action = int(input('行動を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        match action:
            case 0:
                return attack
            case 1:
                return slash
            case _:
                print('不適切な入力です \n')

def normal_action():
    return attack

def show_event(event):
    print(f"{event['attacker']} は {event['defender']} に {event['damage']} のダメージを与えた!\n")

def show_alive_combatants_status(combatants):
    alives = get_alive_actors(combatants)
    idx = 0
    for actor in alives:
        hp_rate = actor.current_hp / actor.master.max_hp * 100
        print(f"{actor.name} のステータス")
        print(f"▶︎ hp  => {hp_rate:.2f}%")
        if actor.camp == Camp.PLAYER:
            print(f"▶︎ atk => {actor.atk}")
            print(f"▶︎ spd => {actor.speed}")
        else:
            print("▶︎ atk => ???")
            print("▶︎ spd => ???")
            print(f"to attack --> {idx}")
            idx += 1

        print()

# バトルの実行
def auto_battle(
    entries : list[list[EltenaMaster, Camp]],
    choose_target = select_target,
    choose_action = normal_action
):  
    turn = 0
    logs = []

    combatants = []

    for master, camp in entries:
        combatants.append(BattleEltena(master, camp=camp))

    for camp in Camp:
        num_of_party_eltenas = get_allies_amount_of(camp, combatants)
        if num_of_party_eltenas > MAX_ELTENA_PER_CAMP:
            raise ValueError("Too many actors in one camp")

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
        show_attacker(attacker)
        show_alive_combatants_status(combatants)

        if attacker.camp == Camp.PLAYER:
            action_choice = choose_action()
            target = choose_target(attacker, combatants)
        else:
            action_choice = normal_action()
            target = select_target(attacker, combatants)

        event = action_choice(attacker, target)
        show_event(event)

        logs.append(event)


if __name__ == "__main__":

    entries = [
        [yusha_master, Camp.PLAYER] ,
        [souryo_master, Camp.PLAYER] ,
        [asashin_master, Camp.PLAYER] ,
        [archer_master, Camp.PLAYER] ,
        [slime_master, Camp.ENEMY] ,
        [goblin_master, Camp.ENEMY]
    ]

    print("バトル開始!\n")

    win_camp, logs = auto_battle(entries, input_target, input_select_action)
    for i, log in enumerate(logs):
        print(f"turn {i + 1}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")

    match win_camp:
        case Camp.PLAYER:
            winner = '自'
        case Camp.ENEMY:
            winner = '敵'
        case _:
            winner = None

    if winner:
        print(f"{winner}陣営が勝利しました。")