import skills


class EltenaMaster:

    # 初期化
    def __init__(self, name, hp, atk, spd, normal_attack = skills.NormalSlash):
        self.name = name
        self.max_hp = hp
        self.atk = atk
        self.spd = spd

        self.normal_attack = normal_attack()

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"SPD: {self.spd}")
        print()

yusha_master   = EltenaMaster("勇者", 100, 10, 60)
souryo_master  = EltenaMaster("僧侶", 100, 5, 100)
asashin_master = EltenaMaster("アサシン", 30, 30, 130)
archer_master  = EltenaMaster("アーチャー", 120, 10, 40)

slime_master   = EltenaMaster("スライム", 100, 5, 50)
goblin_master  = EltenaMaster("ゴブリン", 40, 15, 70)