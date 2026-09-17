import console
from battle import Camp
from console import input_select_action, input_target
from driver import auto_battle
from eltena_master import (
    archer_master,
    asashin_master,
    goblin_master,
    slime_master,
    souryo_master,
    yusha_master,
)

if __name__ == "__main__":

    entries = [
        [yusha_master, Camp.PLAYER] ,
        [souryo_master, Camp.PLAYER] ,
        [asashin_master, Camp.PLAYER] ,
        [archer_master, Camp.PLAYER] ,
        [slime_master, Camp.ENEMY] ,
        [goblin_master, Camp.ENEMY]
    ]

    print("バトル開始!\n")

    win_camp, logs = auto_battle(entries, input_target, input_select_action, view = console)
    for i, log in enumerate(logs):
        print(f"turn {i + 1}: {log['attacker']} は {log['using_skill']} を使用 。 {log['defender']} に {log['damage']} のダメージを与えた!\n")

    match win_camp:
        case Camp.PLAYER:
            winner_label = '自'
        case Camp.ENEMY:
            winner_label = '敵'
        case _:
            winner_label = None

    if winner_label:
        print(f"{winner_label}陣営が勝利しました。")