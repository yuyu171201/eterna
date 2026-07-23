class Unit:

    # 初期化
    def __init__(self,name , hp, atk):
        self.name = name
        self.hp = hp
        self.atk = atk

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


def battle(unit1, unit2):
    logs = []

    step = 0
    while unit1.hp > 0 and unit2.hp > 0:
        step += 1
        if step % 2 == 1:
            logs.append([attack(unit1, unit2), step])
        else:
            logs.append([attack(unit2, unit1), step])


    # 勝敗判定 ： 倒された側を返す
    if unit1.hp <= 0:
        return unit1, logs
    if unit2.hp <= 0:
        return unit2, logs


if __name__ == "__main__":
    yusha = Unit("勇者", 20, 10)
    yusha.show_status()
    slime = Unit("スライム", 20, 5)
    slime.show_status()

    print("バトル開始!\n")

    loser, logs = battle(yusha, slime)
    for log in logs:
        print(f"step {log[1]}: {log[0][0]} は {log[0][1]} に {log[0][2]} のダメージを与えた!\n")
    print(f"{loser.name} は倒れた!")