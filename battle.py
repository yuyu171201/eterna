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

    @property
    def ready_actions(self):
        return [action for action in self.actions if action.is_ready]
    
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
        return self.current_ct == self.skill.max_ct

    def on_acted(self):
        if self.current_ct < self.skill.max_ct:
            self.current_ct += 1

    def on_used(self):
        self.current_ct = 0

    def execute(self, attacker, target):
        self.on_used()
        return self.skill.execute(attacker, target) 

class ActionOrderManager:
    def __init__(self, actors):
        self.actors = actors

    def tick(self):
        self.alived_actors = get_alive_actors(self.actors)

        for actor in self.alived_actors:
            actor.action_gauge += actor.spd

        max_action_gauge = 0
        maxed_actor = None

        for actor in self.alived_actors:
            if actor.action_gauge >= actor.threshold and actor.action_gauge > max_action_gauge:
                max_action_gauge = actor.action_gauge
                maxed_actor = actor

        if maxed_actor is not None:
            for actor in self.alived_actors:
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


def get_alive_actors(
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    alives = [actor for actor in combatants if actor.is_alive]
    return alives

def get_enemies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    enemies = [actor for actor in combatants if actor.camp != attacker.camp]
    return enemies

def get_living_enemies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    valid_enemies = get_enemies_of(attacker, get_alive_actors(combatants))
    return valid_enemies

def get_allies_of(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> list[BattleEltena]:
    allies = [actor for actor in combatants if actor.camp == attacker.camp]
    return allies

def get_allies_amount(
    camp : Camp ,
    combatants : list[BattleEltena]  
) -> int:
    allies = [eltena for eltena in combatants if eltena.camp == camp]
    return len(allies)

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