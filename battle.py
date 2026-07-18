class Unit:

    # 初期化
    def __init__(self,name , HP, ATK):
        self.name = name
        self.HP = HP
        self.ATK = ATK

    def take_damage(self, damage):
        self.HP = self.HP - damage
        if self.HP < 0:
            self.HP = 0


def atack(unit1, unit2):
    print(f"{unit1.name} の攻撃!")
    print(f"{unit2.name} に {unit1.ATK} のダメージ!")
    print()

    unit2.take_damage(unit1.ATK)


def battle(unit1, unit2):
    print("バトル開始!\n")

    step = 0
    while unit1.HP > 0 and unit2.HP > 0:
        step += 1
        if step % 2 == 1:
            atack(unit1, unit2)
        else:
            atack(unit2, unit1)

    if unit1.HP <= 0:
        print(f"{unit1.name} は倒れた!")
    if unit2.HP <= 0:
        print(f"{unit2.name} は倒れた!")


if __name__ == "__main__":
    yusha = Unit("勇者", 20, 10)
    slime = Unit("スライム", 20, 5)
    battle(yusha, slime)