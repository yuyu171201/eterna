class Skill:
    def __init__(self, name, multiplier):
        self.name = name
        self.multiplier = multiplier

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

