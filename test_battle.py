# import pytest

import skills
from battle import (
    ActionOrderManager,
    BattleEltena,
    Camp,
    get_alive_actors,
    get_allies_amount,
    get_enemies_of,
)
from driver import auto_battle
from eltena_master import EltenaMaster


def test_take_damage():
    actor = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    actor.take_damage(5)
    assert actor.current_hp == 15

def test_not_minus_hp():
    actor = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    actor.take_damage(100)
    assert actor.current_hp == 0

def test_fastest_eltena_acts_first():
    fast = EltenaMaster("勇者", 20, 10, 100)
    late = EltenaMaster("スライム", 20, 5, 90)
    entries = [[fast, Camp.PLAYER], [late, Camp.ENEMY]]
    _, logs = auto_battle(entries)
    assert logs[0]['attacker'] == "勇者"

def test_winner_camp():
    win  = EltenaMaster("勇者", 20, 10, 100)
    lose = EltenaMaster("スライム", 20, 5, 90)
    entries = [[win, Camp.PLAYER], [lose, Camp.ENEMY]]
    winner, _ = auto_battle(entries)
    assert winner == Camp.PLAYER

def test_speed_order():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 100), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 90), Camp.ENEMY)
    action = ActionOrderManager([actor1, actor2])
    assert actor1.action_gauge == 0
    assert actor2.action_gauge == 0
    action.tick()
    assert actor1.action_gauge == 100
    assert actor2.action_gauge == 90
    for i in range(99):
        action.tick()
    assert actor1.action_gauge == 0
    assert actor2.action_gauge == 9000

def test_speed_order_same_tick_to_threshold():
    actor1 = BattleEltena(EltenaMaster("勇者", 20, 10, 150), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("スライム", 20, 5, 151), Camp.ENEMY)
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.action_gauge == 10050 # 150 * 67
    assert actor2.action_gauge == 117   # 151 * 67 - 10000
    action.next_actor()
    assert actor1.action_gauge == 200   # 150 * 68 - 10000
    assert actor2.action_gauge == 268   # 151 * 68 - 10000

def test_overheat_allows_double_at_3x():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 150), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50), Camp.ENEMY)
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.action_gauge == 50    # 150 * 67  - 10000
    assert actor1.threshold == 20000
    assert actor2.action_gauge == 3350  # 50  * 67
    assert actor2.threshold == 10000 
    action.next_actor()
    assert actor1.action_gauge == 0     # 150 * 200 - 10000 - 20000
    assert actor1.threshold == 30000
    assert actor2.action_gauge == 10000 # 50  * 200
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.action_gauge == 150   # 150 * 201 - 30000
    assert actor1.threshold == 10000
    assert actor2.action_gauge == 50    # 50  * 201 - 10000
    assert actor2.threshold == 20000

def test_overheat_allows_double_at_4x():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 200), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50), Camp.ENEMY)
    action = ActionOrderManager([actor1, actor2])
    action.next_actor()
    assert actor1.action_gauge == 0     # 200 * 50  - 10000
    assert actor1.threshold == 20000
    assert actor2.action_gauge == 2500  # 50  * 50 
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.action_gauge == 0     # 200 * 150 - 10000 - 20000
    assert actor1.threshold == 30000
    assert actor2.action_gauge == 7500  # 50  * 150
    assert actor2.threshold == 10000
    action.next_actor()
    assert actor1.action_gauge == 10000  # 200 * 200 - 30000
    assert actor1.threshold == 10000
    assert actor2.action_gauge == 0      # 50  * 200
    assert actor2.threshold == 20000
    action.next_actor()
    assert actor1.action_gauge == 200    # 200 * 201 - 30000 - 10000
    assert actor1.threshold == 20000
    assert actor2.action_gauge == 50     # 50  * 201 - 20000
    assert actor2.threshold == 10000

def test_overheat_action_order():
    actor1 = BattleEltena(EltenaMaster("勇者", 200, 10, 60), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("スライム", 200, 5, 50), Camp.ENEMY)
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

def test_overheat_action_order_3player():
    actor1 = BattleEltena(EltenaMaster("勇者1", 10000, 1, 150), Camp.PLAYER)
    actor2 = BattleEltena(EltenaMaster("勇者2", 10000, 1, 100), Camp.PLAYER)
    actor3 = BattleEltena(EltenaMaster("勇者3", 10000, 1, 50), Camp.PLAYER)
    sandbag = BattleEltena(EltenaMaster("相手", 100000, 0, 1), Camp.ENEMY)

    combatants = [actor1, actor2, actor3, sandbag]
    action = ActionOrderManager(combatants)

    assert action.next_actor() == actor1
    assert action.next_actor() == actor2
    assert action.next_actor() == actor1
    assert action.next_actor() == actor2
    assert action.next_actor() == actor1
    assert action.next_actor() == actor3

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

def test_get_allies_amounts():
    p1 = BattleEltena(EltenaMaster('p1', 1, 1, 1), Camp.PLAYER)
    p2 = BattleEltena(EltenaMaster('p2', 1, 1, 1), Camp.PLAYER)
    p3 = BattleEltena(EltenaMaster('p3', 1, 1, 1), Camp.PLAYER)
    p4 = BattleEltena(EltenaMaster('p4', 1, 1, 1), Camp.PLAYER)
    e1 = BattleEltena(EltenaMaster('p1', 1, 1, 1), Camp.ENEMY)

    combatants = [p1, p2, p3, p4, e1]
    allies_amount = get_allies_amount(Camp.PLAYER, combatants)
    assert allies_amount == 4

def test_dead_actor_action_order():
    alive1_player = BattleEltena(EltenaMaster('player1', 10, 1, 1 ), Camp.PLAYER)
    alive2_enemy  = BattleEltena(EltenaMaster('enemy1',  10, 1, 1 ), Camp.ENEMY)
    death1_enemy  = BattleEltena(EltenaMaster('enemy2',  0 , 1, 10), Camp.ENEMY)

    combatants = [alive1_player, alive2_enemy, death1_enemy]
    action = ActionOrderManager(combatants)
    for _ in range(10):
        attacker = action.next_actor()
        assert attacker != death1_enemy

def test_over_max_amount_per_camp():
    actor1 = EltenaMaster('p1', 1, 1, 1)
    actor2 = EltenaMaster('p2', 1, 1, 1)
    actor3 = EltenaMaster('p3', 1, 1, 1)
    actor4 = EltenaMaster('p4', 1, 1, 1)
    actor5 = EltenaMaster('p5', 1, 1, 1)
    actor6 = EltenaMaster('e1', 1, 1, 1)

    entries = [
        [actor1, Camp.PLAYER] ,
        [actor2, Camp.PLAYER] ,
        [actor3, Camp.PLAYER] ,
        [actor4, Camp.PLAYER] ,
        [actor5, Camp.PLAYER] ,
        [actor6, Camp.ENEMY]
    ]
    try:
        auto_battle(entries)
    except ValueError as e:
        assert str(e) == "Too many actors in one camp"

def test_default_skill_execution():
    skill = skills.Skill("Attack", 100)
    attacker = BattleEltena(EltenaMaster("勇者", 20, 10, 100))
    target = BattleEltena(EltenaMaster("スライム", 20, 5, 90))
    event = skill.execute(attacker, target)
    assert event['attacker'] == "勇者"
    assert event['defender'] == "スライム"
    assert event['using_skill'] == "Attack"
    assert event['damage'] == 10

def test_ne_BattleSkill_and_BattleEltena_skill():
    owner_master = EltenaMaster("owner", 1, 1, 1)
    skill_owner0 = BattleEltena(owner_master)
    skill_owner1 = BattleEltena(owner_master)

    assert skill_owner0.normal_attack is not skill_owner1.normal_attack
    assert skill_owner0.normal_attack.skill is skill_owner1.normal_attack.skill

def test_no_op_battle_return(capsys):
    player = EltenaMaster('player', 100, 100, 100)
    enemy  = EltenaMaster('enemy', 1, 1, 1)
    entries = [[player, Camp.PLAYER], [enemy, Camp.ENEMY]]

    auto_battle(entries)
    captured = capsys.readouterr()

    assert captured.out == ''
    assert captured.err == ''