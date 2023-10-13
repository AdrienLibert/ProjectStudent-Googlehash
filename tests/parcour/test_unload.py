import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))

from classes.Santa import Santa, SantaException
from classes.Parser import Parser
from classes.Gift import Gift
from classes.Sleigh import SleighCategorie

def test_unload() -> None:
    p = Parser("data/a_an_example.in.txt")
    s = Santa(p.getSleigh(), p.getGifts(), p.getReach(), p.getTimeLimit())

    game_gifts = s.GAME_GIFTS

    keys = list(game_gifts.keys())
    
    assert len(s.gifts) == 0
    
    assert keys[0] not in s.gifts
    assert keys[1] not in s.gifts

    s.LoadGift(keys[0])
    s.LoadGift(keys[1])

    assert s.gifts == {
        keys[0]: game_gifts[keys[0]],
        keys[1]: game_gifts[keys[1]]
    }

    s.REACH = 0
    if game_gifts[keys[0]].getPosition() != [0, 0]:
        with pytest.raises(SantaException):
            s.DeliverGift(keys[0])

    s.position = game_gifts[keys[0]].position
    s.DeliverGift(keys[0])

    assert s.gifts == {
        keys[0]: None,
        keys[1]: game_gifts[keys[1]]
    }

    s.position = game_gifts[keys[1]].position
    s.DeliverGift(keys[1])

    assert s.gifts == {
        keys[0]: None,
        keys[1]: None
    }

    #s.UnloadGift(game_gifts[keys[0]])
    # insert test for double gift of same person
    
if __name__ == '__main__':
    test_unload()
