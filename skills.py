class Skill:
    def __init__(self, name, multiplier):
        self.name = name
        self.multiplier = multiplier

    def execute(self, attacker, target):
        damage = attacker.atk * self.multiplier
        target.take_damage(damage)
