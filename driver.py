from random import choice

from battle import (
    ActionOrderManager,
    BattleEltena,
    Camp,
    get_alive_actors,
    get_allies_amount_of,
    get_enemies_of,
)
from console import (
    show_alive_combatants_status,
    show_attacker,
    show_event,
)
from eltena_master import EltenaMaster

MAX_ELTENA_PER_CAMP = 4

# 攻撃対象の選択
def select_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    valid_targets = get_enemies_of(attacker, get_alive_actors(combatants))

    target = choice(valid_targets)
    return target

def normal_action(attacker : BattleEltena):
    return attacker.normal_attack


# バトルの実行
def auto_battle(
    entries : list[list[EltenaMaster, Camp]],
    choose_target = select_target,
    choose_action = normal_action
):  
    logs = []

    combatants = []

    for master, camp in entries:
        combatants.append(BattleEltena(master, camp=camp))

    for camp in Camp:
        num_of_party_eltenas = get_allies_amount_of(camp, combatants)
        if num_of_party_eltenas > MAX_ELTENA_PER_CAMP:
            raise ValueError("Too many actors in one camp")

    action = ActionOrderManager(combatants)

    while True:
        survivors = get_alive_actors(combatants)
        remain_camps = [actor.camp for actor in survivors]
        num_camps = len(set(remain_camps))

        if num_camps == 1:
            return remain_camps[0], logs
        elif num_camps == 0:
            return None, logs
            
        attacker = action.next_actor()
        show_attacker(attacker)
        show_alive_combatants_status(combatants)

        if attacker.camp == Camp.PLAYER:
            action_choice = choose_action(attacker)
            target = choose_target(attacker, combatants)
        else:
            action_choice = normal_action(attacker)
            target = select_target(attacker, combatants)

        event = action_choice.execute(attacker, target)
        show_event(event)

        logs.append(event)
