from battle import (
    BattleEltena,
    Camp,
    get_alive_actors,
    get_valid_enemies,
)


def show_attacker(attacker : BattleEltena):
    print(f'{attacker.name} の攻撃')
    print()

def input_select_action(attacker : BattleEltena):
    print("行動を選択してください")

    for i, action in enumerate(attacker.actions):
        ready_status = 'is ready!' if action.is_ready else 'is not ready'
        print(f"{i}. {action.name} ({ready_status})")

    while True:
        try:
            action = int(input('行動を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if action >= 0 and action < len(attacker.actions) and attacker.actions[action].is_ready:
            selected_action = attacker.actions[action]
            return selected_action.execute
        else:
            print('範囲外の数値です')

# 攻撃対象の入力での選択
def input_target(
    attacker : BattleEltena ,
    combatants : list[BattleEltena]
) -> BattleEltena:
    enemies = get_valid_enemies(attacker, combatants)

    while True:
        try:
            target_idx = int(input('対象を選択して : '))
        except ValueError:
            print('数値で入力してください')
            continue

        if target_idx >= 0 and target_idx < len(enemies):
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
            print(f"▶︎ spd => {actor.speed}")
        else:
            print("▶︎ atk => ???")
            print("▶︎ spd => ???")
            print(f"to attack --> {idx}")
            idx += 1

        print()

def show_event(event):
    print(f"{event['attacker']} は {event['defender']} に {event['damage']} のダメージを与えた!\n")
