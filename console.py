from battle import (
    BattleEltena,
    Camp,
    get_alive_actors,
    get_living_enemies_of,
    is_action_usable,
    is_target_selectable,
)


def show_attacker(attacker : BattleEltena):
    print(f'{attacker.name} の攻撃')
    print()

def input_select_action(attacker : BattleEltena):
    print("行動を選択してください")

    actions = attacker.actions

    for i, action in enumerate(actions):
        ready_status = 'is ready!' if action.is_ready else 'is not ready'
        print(f"{i}. {action.name} ({ready_status})")

    while True:
        try:
            action_idx = int(input('行動を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if is_action_usable(action_idx, actions):
            selected_action = actions[action_idx]
            return selected_action
        else:
            print('範囲外の数値です')

# 攻撃対象の入力での選択
def input_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    enemies = get_living_enemies_of(attacker, combatants)

    while True:
        try:
            target_idx = int(input('対象を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if is_target_selectable(target_idx, targets=enemies):
            target = enemies[target_idx]
            print()
            return target
        else:
            print('不適切な入力です')
            print()

def show_alive_combatants_status(combatants):
    alives = get_alive_actors(combatants)
    idx = 0
    for actor in alives:
        hp_rate = actor.current_hp / actor.master.max_hp * 100
        print(f"{actor.name} のステータス")
        print(f"▶︎ hp  => {hp_rate:.2f}%")
        if actor.camp == Camp.PLAYER:
            print(f"▶︎ atk => {actor.atk}")
            print(f"▶︎ spd => {actor.spd}")
        else:
            print("▶︎ atk => ???")
            print("▶︎ spd => ???")
            print(f"to attack --> {idx}")
            idx += 1

        print()

def show_event(event):
    print(f"{event['attacker']} は {event['using_skill']} を使用。 {event['defender']} に {event['damage']} のダメージを与えた!\n")
