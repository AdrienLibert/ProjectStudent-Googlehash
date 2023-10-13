import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))

from classes.Santa import Santa, SantaException
from classes.Parser import Parser

def test_DoubleAcc() -> None:
    p = Parser("data/a_an_example.in.txt")
    s = Santa(p.getSleigh(), p.getGifts(), p.getReach(), p.getTimeLimit())
    
    game_gifts = s.GAME_GIFTS

    keys = list(game_gifts.keys())

    s.LoadCarrots(2)
    s.LoadGift(keys[0])
    s.LoadGift(keys[1])
    
    s.Accelerate("up", 1)
    with pytest.raises(SantaException):
        s.Accelerate("up", 1)
    
    s.Float(1)
    s.Accelerate("up", 1)


if __name__ == '__main__':
    test_DoubleAcc()
