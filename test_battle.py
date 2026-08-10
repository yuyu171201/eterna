# import pytest

from battle import (
    ActionOrderManager,
    CombatState,
    auto_battle,
)
from unit import Unit


def test_set_id():
    unit1 = Unit("勇者", 20, 10, 100)
    unit2 = Unit("スライム", 20, 5, 90)
    unit3 = Unit("魔王", 30, 15, 120, id=99)
    assert unit1.id == 1
    assert unit2.id == 2
    assert unit3.id == 99

def test_take_damage():
    actor = CombatState(Unit("勇者", 20, 10, 100))
    actor.take_damage(5)
    assert actor.current_hp == 15

def test_not_minus_hp():
    actor = CombatState(Unit("勇者", 20, 10, 100))
    actor.take_damage(100)
    assert actor.current_hp == 0

def test_fastest_unit():
    unit1 = Unit("勇者", 20, 10, 100)
    unit2 = Unit("スライム", 20, 5, 90)
    _, logs = auto_battle(unit1, unit2)
    assert logs[0]['attacker'] == "勇者"

def test_loser():
    unit1 = Unit("勇者", 20, 10, 100)
    unit2 = Unit("スライム", 20, 5, 90)
    loser, _ = auto_battle(unit1, unit2)
    assert loser.name == "スライム"

def test_speed_order():
    actor1 = CombatState(Unit("勇者", 20, 10, 100))
    unit1_id = 1
    actor2 = CombatState(Unit("スライム", 20, 5, 90))
    unit2_id = 2
    action = ActionOrderManager({unit1_id: actor1, unit2_id: actor2})
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
    actor1 = CombatState(Unit("勇者", 20, 10, 150))
    unit1_id = 1
    actor2 = CombatState(Unit("スライム", 20, 5, 151))
    unit2_id = 2
    action = ActionOrderManager({unit1_id: actor1, unit2_id: actor2})
    action.next_actor()
    assert actor1.ct == 10050 # 150 * 67
    assert actor2.ct == 117   # 151 * 67 - 10000
    action.next_actor()
    assert actor1.ct == 200   # 150 * 68 - 10000
    assert actor2.ct == 268   # 151 * 68 - 10000

def test_overheat_allows_double_at_3x():
    actor1 = CombatState(Unit("勇者", 200, 10, 150))
    unit1_id = 1
    actor2 = CombatState(Unit("スライム", 200, 5, 50))
    unit2_id = 2
    action = ActionOrderManager({unit1_id: actor1, unit2_id: actor2})
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
    actor1 = CombatState(Unit("勇者", 200, 10, 200))
    unit1_id = 1
    actor2 = CombatState(Unit("スライム", 200, 5, 50))
    unit2_id = 2
    action = ActionOrderManager({unit1_id: actor1, unit2_id: actor2})
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