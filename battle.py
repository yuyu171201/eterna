import unit

BASE_SPEED = 80
ACTION_COST = 10000

class CombatState:
    def __init__(self, unit):
        self.unit = unit
        
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
    def atk(self):
        return self.unit.atk

    @property
    def speed(self):
        return self.unit.spd

    @property
    def name(self):
        return self.unit.name

    @property
    def id(self):
        return self.unit.id

class ActionOrderManager:
    def __init__(self, actors):
        self.actors = actors

    def tick(self):
        for actor in self.actors.values():
            actor.ct += actor.speed

        max_ct = 0
        maxed_actor = None

        for actor in self.actors.values():
            if actor.ct >= actor.threshold and actor.ct > max_ct:
                max_ct = actor.ct
                maxed_actor = actor

        if maxed_actor is not None:
            for actor in self.actors.values():
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

        

# 攻撃処理
def attack(actor1, actor2):
    # 辞書型(攻撃者,　被攻撃者, ダメージ量)
    event = {'attacker':actor1.name, 'defender':actor2.name, 'damage':actor1.atk}

    actor2.take_damage(actor1.atk)
    return event


# 攻撃対象の選択
def select_target(attacker, actor1, actor2):
    if attacker == actor1:
        return actor2
    else:
        return actor1


def do_attack(attacker, actor1, actor2):
    enemy = select_target(attacker, actor1, actor2)
    event = attack(attacker, enemy)
    return event, enemy


# バトルの実行
def auto_battle(unit1, unit2):
    turn = 0
    logs = []

    actor1 = CombatState(unit1)
    actor2 = CombatState(unit2)

    actors = {actor1.id: actor1, actor2.id: actor2}

    action = ActionOrderManager(actors)

    while True:
        attacker = action.next_actor()

        turn += 1
        event, enemy = do_attack(attacker, actor1, actor2)
        event['turn'] = turn
        logs.append(event)

        if enemy.current_hp <= 0:
            return enemy, logs


if __name__ == "__main__":
    yusha = unit.Unit("勇者", 100, 10, 60)
    yusha.show_status()
    slime = unit.Unit("スライム", 100, 5, 50)
    slime.show_status()

    print("バトル開始!\n")

    loser, logs = auto_battle(yusha, slime)
    for log in logs:
        print(f"turn {log['turn']}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")