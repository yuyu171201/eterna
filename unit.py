class Unit:
    id_counter = 0

    # 初期化
    def __init__(self, name, hp, atk, spd, id=None):
        self.name = name
        self.max_hp = hp
        self.atk = atk
        self.spd = spd
        if id is None:
            Unit.id_counter += 1
            self.id = Unit.id_counter
        else:
            self.id = id

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"SPD: {self.spd}")
        print()