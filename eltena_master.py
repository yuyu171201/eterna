import skills


class EltenaMaster:

    # 初期化
    def __init__(self, name, hp, atk, spd, normal_attack = skills.NormalAttack, own_skills = None):
        self.name = name
        self.max_hp = hp
        self.atk = atk
        self.spd = spd

        self.normal_attack = normal_attack()

        self.skills = own_skills or []

    def show_status(self):
        print(f"{self.name} のステータス")
        print(f"HP: {self.max_hp}")
        print(f"ATK: {self.atk}")
        print(f"SPD: {self.spd}")
        print()

yusha_master   = EltenaMaster(
    name="勇者", 
    hp=100, 
    atk=10, 
    spd=60,
    own_skills = [
        skills.NormalSlash()
    ]
)
souryo_master  = EltenaMaster(
    name="僧侶", 
    hp=100, 
    atk=5, 
    spd=100
)
asashin_master = EltenaMaster(
    name="アサシン", 
    hp=30, 
    atk=30, 
    spd=130, 
    own_skills = [
        skills.NormalSlash()
    ]
)
archer_master  = EltenaMaster(
    name="アーチャー", 
    hp=120, 
    atk=10, 
    spd=40
)

slime_master   = EltenaMaster(
    name="スライム", 
    hp=100, 
    atk=5, 
    spd=50
)
goblin_master  = EltenaMaster(
    name="ゴブリン", 
    hp=40, 
    atk=15, 
    spd=70
)