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

        self.normal_attack = BattleSkill(master.normal_attack)

        self.skills = [BattleSkill(skill) for skill in master.skills]

    def take_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 0)

    def on_acted(self):
        self.action_gauge -= self.threshold
        for action in self.actions:
            action.on_acted()

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

    @property
    def actions(self):
        return [self.normal_attack, *self.skills]
    
    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master.name}, camp={self.camp})'

class BattleSkill:
    def __init__(self, skill):
        self.skill = skill
        self.current_ct = skill.max_ct

    @property
    def name(self):
        return self.skill.name

    @property
    def is_ready(self):
        return self.current_ct == self.skill.max_ct

    def on_acted(self):
        if self.current_ct < self.skill.max_ct:
            self.current_ct += 1

    def on_used(self):
        self.current_ct = 0

    def execute(self, attacker, target):
        return self.skill.execute(attacker, target) 

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

def input_select_action(attacker : BattleEltena):
    print("行動を選択してください")
    actions = list(enumerate([attacker.normal_attack, *attacker.skills]))

    for i, action in actions:
        print(f"{i}. {action.name}")

    while True:
        try:
            action = int(input('行動を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if action >= 0 and action < len(actions):
            selected_action = actions[action][1]
            return selected_action.execute
        else:
            print('範囲外の数値です')

def normal_action(attacker : BattleEltena):
    return attacker.normal_attack.execute

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
            action_choice = choose_action(attacker)
            target = choose_target(attacker, combatants)
        else:
            action_choice = normal_action(attacker)
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