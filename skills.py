class Skill:
    def __init__(self, name : str, multiplier : int, max_ct : int = 0
    ):
        self.name = name
        self.multiplier = multiplier
        self.max_ct = max_ct

    def execute(self, attacker, target):
        damage = int(attacker.atk * self.multiplier / 100)
        target.take_damage(damage)
        event = {
            'attacker': attacker.name,
            'defender': target.name,
            'using_skill': self.name,
            'damage': damage
        }
        return event

class NormalAttack(Skill):
    def __init__(self):
        super().__init__('通常攻撃', 100)

class NormalSlash(Skill):
    def __init__(self):
        super().__init__('スラッシュ', 200)