class Unit:

    # 初期化
    def __init__(self, name, hp, atk, spd):
        self.name = name
        self.max_hp = hp
        self.atk = atk
        self.spd = spd

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"SPD: {self.spd}")
        print()