from casino.roulette import Outcome, Wheel, Bin, BinBuilder, Game


def test_outcome():
    o1 = Outcome("Red", 1)
    o2 = Outcome("Red", 1)
    o3 = Outcome("Black", 2)
    assert str(o1) == "Red 1:1"
    assert repr(o2) == "Outcome(name='Red', odds=1)"
    assert o1 == o2
    assert o1.odds == 1
    assert o1.name == "Red"
    assert o1 != o3
    assert o2 != o3


def test_bin():
    one = Outcome("1", 1)
    odd = Outcome("Odd", 19)
    low = Outcome("Low", 12)
    two = Outcome("2", 1)
    even = Outcome("Even", 19)

    b1 = Bin({one, odd, low})
    b2 = Bin({two, even, low})

    assert isinstance(b1, Bin)
    assert isinstance(b2, Bin)

    for outcome in b1.outcomes:
        assert isinstance(outcome, Outcome)

    for outcome in b2.outcomes:
        assert isinstance(outcome, Outcome)


def test_wheel_sequence():
    wheel = Wheel()
    wheel.add_outcome(8, Outcome("test", 1))
    wheel.rng.seed(1)
    assert Outcome("test", 1) in wheel.choose()

def test_bin_builder(): 
    wheel = Wheel()
    builder = BinBuilder(wheel)
    
    builder.build_straight_bets()
    assert Outcome(f"Bin no. 0", Game.STRAIGHT_BET) in wheel.bins[0].outcomes
    assert Outcome(f"Bin no. 00", Game.STRAIGHT_BET) in wheel.bins[37].outcomes
    assert Outcome(f"Bin no. 1", Game.STRAIGHT_BET) in wheel.bins[1].outcomes
    assert Outcome(f"Bin no. 36", Game.STRAIGHT_BET) in wheel.bins[36].outcomes
    
    builder.build_split_bets()
    assert Outcome("Split 1-2", Game.SPLIT_BET) in wheel.bins[1].outcomes
    assert Outcome("Split 1-4", Game.SPLIT_BET) in wheel.bins[1].outcomes
    assert Outcome("Split 33-36", Game.SPLIT_BET) in wheel.bins[36].outcomes
    assert Outcome("Split 35-36", Game.SPLIT_BET) in wheel.bins[36].outcomes
    
    builder.build_street_bets()
    assert Outcome("Street 1-2-3", Game.STREET_BET) in wheel.bins[1].outcomes
    assert Outcome("Street 34-35-36", Game.STREET_BET) in wheel.bins[36].outcomes

    builder.build_corner_bets()
    assert Outcome("Corner 1-2-4-5", Game.CORNER_BET) in wheel.bins[1].outcomes

    assert Outcome("Corner 1-2-4-5", Game.CORNER_BET) in wheel.bins[4].outcomes
    assert Outcome("Corner 4-5-7-8", Game.CORNER_BET) in wheel.bins[4].outcomes

    assert Outcome("Corner 1-2-4-5", Game.CORNER_BET) in wheel.bins[5].outcomes
    assert Outcome("Corner 4-5-7-8", Game.CORNER_BET) in wheel.bins[5].outcomes
    assert Outcome("Corner 2-3-5-6", Game.CORNER_BET) in wheel.bins[5].outcomes
    assert Outcome("Corner 5-6-8-9", Game.CORNER_BET) in wheel.bins[5].outcomes

    # builder.build_line_bets()
    # builder.build_dozen_bets()
    # builder.build_column_bets()
    # builder.build_outside_bets()
    # builder.build_five_bet()


