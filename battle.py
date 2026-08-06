BASE_SPEED = 80
ACTION_COST = 10000

class Unit:
    id_counter = 0

    # 初期化
    def __init__(self,name , hp, atk, spd, id=None):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd
        if id is None:
            Unit.id_counter += 1
            self.id = Unit.id_counter
        else:
            self.id = id


    def take_damage(self, damage):
        self.hp = max(self.hp - damage, 0)

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.hp}")
        print(f"ATK: {self.atk}")
        print(f"SPD: {self.spd}")
        print()

class ActionOrderManager:
    def __init__(self, units):
        self.units = units
        self.ct = {unit: 0 for unit in units}

    def tick(self):
        for ids in self.units:
            self.ct[ids] += self.units[ids].spd

        for ids in sorted(self.units.keys()):
            if self.ct[ids] >= ACTION_COST:
                self.ct[ids] -= ACTION_COST
                return self.units[ids]

        return None

    def next_actor(self):
        while True:
            actor = self.tick()
            if actor is not None:
                return actor

        

# 攻撃処理
def attack(unit1, unit2):
    # 辞書型(攻撃者,　被攻撃者, ダメージ量)
    event = {'attacker':unit1.name, 'defender':unit2.name, 'damage':unit1.atk}

    unit2.take_damage(unit1.atk)
    return event


# 攻撃対象の選択
def select_target(attacker, unit1, unit2):
    if attacker == unit1:
        return unit2
    else:
        return unit1


def do_attack(attacker, unit1, unit2):
    enemy = select_target(attacker, unit1, unit2)
    event = attack(attacker, enemy)
    return event, enemy


# バトルの実行
def auto_battle(unit1, unit2):
    turn = 0
    logs = []

    units = {unit1.id: unit1, unit2.id: unit2}

    action = ActionOrderManager(units)

    while True:
        attacker = action.next_actor()

        turn += 1
        event, enemy = do_attack(attacker, unit1, unit2)
        event['turn'] = turn
        logs.append(event)

        if enemy.hp <= 0:
            return enemy, logs


if __name__ == "__main__":
    yusha = Unit("勇者", 100, 10, 60)
    yusha.show_status()
    slime = Unit("スライム", 100, 5, 50)
    slime.show_status()

    print("バトル開始!\n")

    loser, logs = auto_battle(yusha, slime)
    for log in logs:
        print(f"turn {log['turn']}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")