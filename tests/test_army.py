from app.Army import Army


def test_squads():
    army = Army(squads=2, soldiers=4, vehicles=5, name=1)
    assert len(army.get_squads) == 3


def test_health():
    army = Army(squads=2, soldiers=4, vehicles=4, name=1)
    army2 = Army(squads=2, soldiers=4, vehicles=5, name=2)
    i = 0
    while i <= 100:
        army.attack(army2, 'weakest')
        i += 1
    assert type(army2.get_health()) == float
