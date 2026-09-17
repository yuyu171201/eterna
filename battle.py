from enum import Enum

ACTION_COST = 10000

class Camp(Enum):
    PLAYER = 1
    ENEMY = 2

class BattleEltena:
    def __init__(self, master, camp=None):
        self.master = master
        self.camp = camp

        self.current_hp = master.max_hp

        self.action_gauge = 0
        self.threshold = ACTION_COST

        self.normal_attack = BattleSkill(master.normal_attack)

        self.skills = [BattleSkill(skill) for skill in master.skills]

    def take_damage(self, damage):
        self.current_hp = max(self.current_hp - damage, 0)

    def on_acted(self):
        self.action_gauge -= self.threshold
        for action in self.actions:
            action.on_acted()

    def overheat(self):
        self.threshold += ACTION_COST

    def cooldown(self):
        self.threshold = ACTION_COST


    @property
    def is_alive(self):
        return self.current_hp > 0

    @property
    def atk(self):
        return self.master.atk

    @property
    def spd(self):
        return self.master.spd

    @property
    def name(self):
        return self.master.name

    @property
    def actions(self):
        return [self.normal_attack, *self.skills]
    
    def __repr__(self):
        return f'{self.__class__.__name__}(master={self.master.name}, camp={self.camp})'

class BattleSkill:
    def __init__(self, skill):
        self.skill = skill
        self.current_ct = skill.max_ct

    @property
    def name(self):
        return self.skill.name

    @property
    def is_ready(self):
        return self.current_ct >= self.skill.max_ct

    def on_acted(self):
        if self.current_ct < self.skill.max_ct:
            self.current_ct += 1

    def on_used(self):
        self.current_ct = 0

    def execute(self, attacker, target):
        self.on_used()
        return self.skill.execute(attacker, target) 

class ActionOrderManager:
    def __init__(self, combatants : list[BattleEltena]):
        self.combatants = combatants

    def tick(self):
        alive_actors = get_alive_combatants(self.combatants)

        for actor in alive_actors:
            actor.action_gauge += actor.spd

        max_action_gauge = 0
        maxed_actor = None

        for actor in alive_actors:
            if actor.action_gauge >= actor.threshold and actor.action_gauge > max_action_gauge:
                max_action_gauge = actor.action_gauge
                maxed_actor = actor

        if maxed_actor is not None:
            for actor in alive_actors:
                if actor == maxed_actor:
                    actor.on_acted()
                    actor.overheat()
                else:
                    actor.cooldown()
            return maxed_actor

        return None

    def next_actor(self):
        while True:
            actor = self.tick()
            if actor is not None:
                return actor


def get_alive_combatants(
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    alives = [combatant for combatant in combatants if combatant.is_alive]
    return alives

def get_enemies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    enemies = [combatant for combatant in combatants if combatant.camp != attacker.camp]
    return enemies

def get_alive_enemies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    alive_enemies = get_enemies_of(attacker, get_alive_combatants(combatants))
    return alive_enemies

def get_allies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    allies = [combatant for combatant in combatants if combatant.camp == attacker.camp]
    return allies

def get_count_in_camp(
    camp : Camp ,
    combatants : list[BattleEltena]  
) -> int:
    in_camps = [battle_eltena for battle_eltena in combatants if battle_eltena.camp == camp]
    return len(in_camps)

def is_action_usable(
        action_idx : int ,
        actions : list[BattleSkill]
) -> bool:
    return action_idx >= 0 and action_idx < len(actions) and actions[action_idx].is_ready

def is_target_selectable(
        target_idx : int ,
        targets : list[BattleEltena]
) -> bool:
    return target_idx >= 0 and target_idx < len(targets)