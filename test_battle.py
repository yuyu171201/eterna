# import pytest

from battle import (
    ActionOrderManager,
    Unit,
    auto_battle,
)


def test_set_id():
    unit1 = Unit("勇者", 20, 10, 100)
    unit2 = Unit("スライム", 20, 5, 90)
    unit3 = Unit("魔王", 30, 15, 120, id=99)
    assert unit1.id == 1
    assert unit2.id == 2
    assert unit3.id == 99

def test_take_damage():
    unit = Unit("勇者", 20, 10, 100)
    unit.take_damage(5)
    assert unit.hp == 15

def test_not_minus_hp():
    unit = Unit("勇者", 20, 10, 100)
    unit.take_damage(100)
    assert unit.hp == 0

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
    unit1 = Unit("勇者", 20, 10, 100)
    unit1_id = 1
    unit2 = Unit("スライム", 20, 5, 90)
    unit2_id = 2
    action = ActionOrderManager({unit1_id: unit1, unit2_id: unit2})
    assert action.ct[unit1_id] == 0
    assert action.ct[unit2_id] == 0
    action.tick()
    assert action.ct[unit1_id] == 100
    assert action.ct[unit2_id] == 90
    for i in range(99):
        action.tick()
    assert action.ct[unit1_id] == 0
    assert action.ct[unit2_id] == 9000

def test_speed_order2():
    unit1 = Unit("勇者", 20, 10, 150)
    unit1_id = 1
    unit2 = Unit("スライム", 20, 5, 151)
    unit2_id = 2
    action = ActionOrderManager({unit1_id: unit1, unit2_id: unit2})
    action.next_actor()
    assert action.ct[unit1_id] == 10050 # 150 * 67
    assert action.ct[unit2_id] == 117   # 151 * 67 - 10000
    action.next_actor()
    assert action.ct[unit1_id] == 200   # 150 * 68 - 10000
    assert action.ct[unit2_id] == 268   # 151 * 68 - 10000


