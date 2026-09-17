from random import choice

from battle import (
    ActionOrderManager,
    BattleEltena,
    Camp,
    get_alive_combatants,
    get_alive_enemies_of,
    get_count_in_camp,
)
from eltena_master import EltenaMaster

MAX_ELTENA_PER_CAMP = 4

class NullView:
    def show_attacker(self,attacker):
        pass

    def show_alive_combatants_status(self,combatants):
        pass

    def show_event(self,event):
        pass

null_view = NullView()

# 攻撃対象の選択
def select_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    alive_targets = get_alive_enemies_of(attacker, combatants)

    target = choice(alive_targets)
    return target

def normal_action(attacker : BattleEltena):
    return attacker.normal_attack


# バトルの実行
def auto_battle(
    entries : list[list[EltenaMaster, Camp]],
    choose_target = select_target,
    choose_action = normal_action,
    view = null_view
):  
    logs = []

    combatants = []

    for master, camp in entries:
        combatants.append(BattleEltena(master, camp=camp))

    for camp in Camp:
        count_in_camp = get_count_in_camp(camp, combatants)
        if count_in_camp > MAX_ELTENA_PER_CAMP:
            raise ValueError("Too many actors in one camp")

    action_order = ActionOrderManager(combatants)

    while True:
        survivors = get_alive_combatants(combatants)
        remain_camps = [actor.camp for actor in survivors]
        num_camps = len(set(remain_camps))

        if num_camps == 1:
            return remain_camps[0], logs
        elif num_camps == 0:
            return None, logs
            
        attacker = action_order.next_actor()
        view.show_attacker(attacker)
        view.show_alive_combatants_status(combatants)

        if attacker.camp == Camp.PLAYER:
            action_choice = choose_action(attacker)
            target = choose_target(attacker, combatants)
        else:
            action_choice = normal_action(attacker)
            target = select_target(attacker, combatants)

        event = action_choice.execute(attacker, target)
        view.show_event(event)

        logs.append(event)
