# import pytest

from battle import (
    Unit,
    auto_battle,
    build_moveorder,
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
    unit1 = Unit("勇者", 20, 10, 170)
    unit2 = Unit("スライム", 20, 5, 90)
    steps = build_moveorder(unit1, unit2)
    assert steps[0].name == "勇者"
    assert steps[1].name == "スライム"
    assert steps[2].name == "勇者"