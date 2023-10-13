import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))

from classes.Santa import Santa, SantaException
from classes.Parser import Parser
from classes.Gift import Gift
from classes.Sleigh import SleighCategorie

def test_load() -> None:
    p = Parser("data/a_an_example.in.txt")
    s = Santa(p.getSleigh(), p.getGifts(), p.getReach(), p.getTimeLimit())

    game_gifts = s.GAME_GIFTS

    keys = list(game_gifts.keys())
    
    s.LoadGift(keys[0])

    assert s.gifts == {
        keys[0]: game_gifts[keys[0]]
    }

    s.LoadGift(keys[1])

    assert s.gifts == {
        keys[0]: game_gifts[keys[0]],
        keys[1]: game_gifts[keys[1]]
    }

    #s.LoadGift(game_gifts[keys[0]])
    # insert test for double gift of same person

if __name__ == '__main__':
    test_load()

