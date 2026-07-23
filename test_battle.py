# import pytest

from battle import Unit, run_battle

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
    loser, logs = run_battle(unit1, unit2)
    assert logs[0]['attacker'] == "勇者"

def test_loser():
    unit1 = Unit("勇者", 20, 10, 100)
    unit2 = Unit("スライム", 20, 5, 90)
    loser, logs = run_battle(unit1, unit2)
    assert loser.name == "スライム"