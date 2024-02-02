from casino.roulette import Outcome, Wheel, Bin


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
