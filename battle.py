class Unit:

    # 初期化
    def __init__(self,name , hp, atk, spd):
        self.name = name
        self.hp = hp
        self.atk = atk
        self.spd = spd

    def take_damage(self, damage):
        self.hp = self.hp - damage
        if self.hp < 0:
            self.hp = 0

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.hp}")
        print(f"ATK: {self.atk}")
        print()


def attack(unit1, unit2):
    # ダメージメッセージ
    # タプル(攻撃者,　被攻撃者, ダメージ量)
    event = (unit1.name, unit2.name, unit1.atk)

    unit2.take_damage(unit1.atk)
    return event


def select_target(attacker, unit1, unit2):
    if attacker == unit1:
        return unit2
    else:
        return unit1


def battle(unit1, unit2):
    turn = 0
    logs = []

    if unit1.spd > unit2.spd:
        steps = [unit1, unit2]
    else:
        steps = [unit2, unit1]

    while True:
        turn += 1
        for step in steps:
            enemy = select_target(step, steps[0], steps[1])
            logs.append([attack(step, enemy), turn])
            if enemy.hp <= 0:
                return enemy, logs


if __name__ == "__main__":
    yusha = Unit("勇者", 20, 10, 100)
    yusha.show_status()
    slime = Unit("スライム", 20, 5, 90)
    slime.show_status()

    print("バトル開始!\n")

    loser, logs = battle(yusha, slime)
    for log in logs:
        print(f"turn {log[1]}: {log[0][0]} は {log[0][1]} に {log[0][2]} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")