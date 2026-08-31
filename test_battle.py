# import pytest

from battle import (
    ActionOrderManager,
    BattleEltena,
    Camp,
    auto_battle,
    get_alive_actors,
    get_enemies_of,
)
from eltena_master import EltenaMaster


def test_take_damage():
    actor = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    actor.take_damage(5)
    assert actor.current_hp == 15

def test_not_minus_hp():
    actor = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    actor.take_damage(100)
    assert actor.current_hp == 0

def test_fastest_unit():
    unit1 = EltenaMaster("勇者", 20, 10, 100)
    unit2 = EltenaMaster("スライム", 20, 5, 90)
    entries = [[unit1, Camp.PLAYER], [unit2, Camp.ENEMY]]
    _, logs = auto_battle(entries)
    assert logs[0]['attacker'] == "勇者"

def test_winner_camp():
    unit1 = EltenaMaster("勇者", 20, 10, 100)
    unit2 = EltenaMaster("スライム", 20, 5, 90)
    entries = [[unit1, Camp.PLAYER], [unit2, Camp.ENEMY]]
    winner, _ = auto_battle(entries)
    assert winner == Camp.PLAYER

def test_speed_order():
    actor1 = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    actor2 = BattleEltena(EltenaMaster("スライム", 20, 5, 90))
    action = ActionOrderManager([actor1, actor2])
    assert actor1.ct == 0
    assert actor2.ct == 0
    action.tick()
    assert actor1.ct == 100
    assert actor2.ct == 90
    for i in range(99):
        action.tick()
    assert actor1.ct == 0
    assert actor2.ct == 9000

def test_speed_order_same_tick_to_threshold():
    actor1 = BattleEltena(EltenaMaster("勇者", 20, 10, 150))
    actor2 = BattleEltena(EltenaMaster("スライム", 20, 5, 151))
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.ct == 10050 # 150 * 67
    assert actor2.ct == 117   # 151 * 67 - 10000
    action.next_actor()
    assert actor1.ct == 200   # 150 * 68 - 10000
    assert actor2.ct == 268   # 151 * 68 - 10000

def test_overheat_allows_double_at_3x():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 150))
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50))
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.ct == 50    # 150 * 67  - 10000
    assert actor1.threshold == 20000
    assert actor2.ct == 3350  # 50  * 67
    assert actor2.threshold == 10000 
    action.next_actor()
    assert actor1.ct == 0     # 150 * 200 - 10000 - 20000
    assert actor1.threshold == 30000
    assert actor2.ct == 10000 # 50  * 200
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.ct == 150   # 150 * 201 - 30000
    assert actor1.threshold == 10000
    assert actor2.ct == 50    # 50  * 201 - 10000
    assert actor2.threshold == 20000

def test_overheat_allows_double_at_4x():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 200))
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50))
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.ct == 0     # 200 * 50  - 10000
    assert actor1.threshold == 20000
    assert actor2.ct == 2500  # 50  * 50 
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.ct == 0     # 200 * 150 - 10000 - 20000
    assert actor1.threshold == 30000
    assert actor2.ct == 7500  # 50  * 150
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.ct == 10000  # 200 * 200 - 30000
    assert actor1.threshold == 10000
    assert actor2.ct == 0      # 50  * 200
    assert actor2.threshold == 20000
    action.next_actor()
    assert actor1.ct == 200    # 200 * 201 - 30000 - 10000
    assert actor1.threshold == 20000
    assert actor2.ct == 50     # 50  * 201 - 20000
    assert actor2.threshold == 10000

def test_overheat_action_order():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 60))
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50))
    action = ActionOrderManager([actor1, actor2])
    actor = action.next_actor()
    assert actor == actor1
    actor = action.next_actor()
    assert actor == actor2
    actor = action.next_actor()
    assert actor == actor1
    actor = action.next_actor()
    assert actor == actor2
    actor = action.next_actor()
    assert actor == actor1
    actor = action.next_actor()
    assert actor == actor2

def test_get_enemies_player_to_enemy():
    player1 = BattleEltena(EltenaMaster('player1', 1, 1, 1), Camp.PLAYER)
    enemy1  = BattleEltena(EltenaMaster('enemy1', 1, 1, 1),  Camp.ENEMY)
    enemy2  = BattleEltena(EltenaMaster('enemy2', 1, 1, 1),  Camp.ENEMY)

    combatants = [player1, enemy1, enemy2]
    enemies = get_enemies_of(player1, combatants)
    assert len(enemies) == 2

def test_get_enemies_enemy_to_player():
    player1 = BattleEltena(EltenaMaster('player1', 1, 1, 1), Camp.PLAYER)
    enemy1  = BattleEltena(EltenaMaster('enemy1', 1, 1, 1),  Camp.ENEMY)
    enemy2  = BattleEltena(EltenaMaster('enemy2', 1, 1, 1),  Camp.ENEMY)

    combatants = [player1, enemy1, enemy2]
    enemies = get_enemies_of(enemy1, combatants)
    assert len(enemies) == 1

def test_get_alives():
    alive1 = BattleEltena(EltenaMaster('alive1', 1, 1, 1))
    alive2 = BattleEltena(EltenaMaster('alive2', 1, 1, 1))
    death1 = BattleEltena(EltenaMaster('death1', 0, 1, 1))

    combatants = [alive1, alive2, death1]
    alives = get_alive_actors(combatants)
    assert len(alives) == 2

def test_dead_actor_action_order():
    alive1_player = BattleEltena(EltenaMaster('player1', 10, 1, 1 ), Camp.PLAYER)
    alive2_enemy  = BattleEltena(EltenaMaster('enemy1',  10, 1, 1 ), Camp.ENEMY)
    death1_enemy  = BattleEltena(EltenaMaster('enemy2',  0 , 1, 10), Camp.ENEMY)

    combatants = [alive1_player, alive2_enemy, death1_enemy]
    action = ActionOrderManager(combatants)
    for _ in range(10):
        attacker = action.next_actor()
        assert attacker != death1_enemy