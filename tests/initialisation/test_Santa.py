import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))
from classes.Santa import Santa, SantaException
from classes.Parser import Parser
from classes.Gift import Gift

def test_create() -> None:
    p = Parser("data/a_an_example.in.txt")
    s = Santa(p.getSleigh(), p.getGifts(), p.getReach(), p.getTimeLimit())

    assert s.REACH.__class__ == int
    assert s.TIME_LIMIT.__class__ == int
    assert s.GAME_GIFTS.__class__ == dict
    for k in s.GAME_GIFTS:
        assert s.GAME_GIFTS[k].__class__ == Gift

    assert s.SLEIGH.__class__ == list

    assert s.position.__class__ == list
    assert len(s.position) == 2
    assert s.time.__class__ == int
    assert s.gifts.__class__ == dict
    assert len(s.gifts) == 0
    assert s.velocity.__class__ == list
    assert len(s.velocity) == 2
    assert s.weightGifts.__class__ == int

    assert s.maxWeight.__class__ == int

def test_values() -> None:
    p = Parser("data/a_an_example.in.txt")
    s = Santa(p.getSleigh(), p.getGifts(), p.getReach(), p.getTimeLimit())
    
    assert s.REACH == p.getReach()
    assert s.TIME_LIMIT == p.getTimeLimit()
    for k in s.GAME_GIFTS:
        assert s.GAME_GIFTS[k] in p.getGifts()
    assert len(s.GAME_GIFTS) == len(p.getGifts())

    assert s.SLEIGH == p.getSleigh()

    assert s.position == [0, 0]
    assert s.time == 0
    assert s.gifts == {}
    assert s.velocity == [0, 0]
    assert s.weightGifts == 0

    maxW = 0
    for sleigh in p.getSleigh():
        if sleigh.maxWeight > maxW:
            maxW = sleigh.maxWeight

    assert s.maxWeight == maxW

if __name__ == '__main__':
    test_create()
    test_values()
