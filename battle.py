import heapq

BASE_SPEED = 80

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


# 素早さ順に並び替える
def build_moveorder(unit1, unit2):
    unit1_amount = max(unit1.spd // BASE_SPEED, 1)
    unit2_amount = max(unit2.spd // BASE_SPEED, 1)

    unit1_spd = []
    unit2_spd = []

    steps = []
    for i in range(unit1_amount):
        unit1_spd.append(unit1.spd // (i + 1))
    for i in range(unit2_amount):
        unit2_spd.append(unit2.spd // (i + 1))

    steps = [
        unit
        for _, unit in heapq.merge(
            [(v, unit1) for v in unit1_spd], 
            [(v, unit2) for v in unit2_spd],
            key = lambda p: -p[0]
        )
    ]

    return steps


# 敗北者の判定
def find_loser(unit):
    if unit.hp <= 0:
        return unit
    else:
        return None


# バトルの実行
def run_battle(unit1, unit2):
    turn = 0
    logs = []

    steps = build_moveorder(unit1, unit2)

    while True:
        turn += 1
        for step in steps:
            enemy = select_target(step, unit1, unit2)
            event = attack(step, enemy)
            event['turn'] = turn
            logs.append(event)

            if find_loser(enemy):
                return enemy, logs


if __name__ == "__main__":
    yusha = Unit("勇者", 20, 10, 100)
    yusha.show_status()
    slime = Unit("スライム", 20, 5, 90)
    slime.show_status()

    print("バトル開始!\n")


    loser, logs = run_battle(yusha, slime)
    for log in logs:
        print(f"turn {log['turn']}: {log['attacker']} は {log['defender']} に {log['damage']} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")