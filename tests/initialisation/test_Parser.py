import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))

from classes.Parser import Parser
from classes.Gift import Gift
from classes.Sleigh import SleighCategorie

def test_create() -> None:
    pars = Parser("./data/a_an_example.in.txt")

    assert pars.getReach().__class__ == int
    assert pars.getTimeLimit().__class__ == int
    assert pars.getSleigh().__class__ == list
    assert pars.getSleigh()[0].__class__ == SleighCategorie
    assert pars.getGifts().__class__ == list
    assert pars.getGifts()[0].__class__ == Gift

def test_getters():
    pars = Parser("./data/a_an_example.in.txt")

    assert len(pars.getGifts()) == 4
    assert pars.getReach() == 3
    assert len(pars.getSleigh()) == 4
    assert pars.getTimeLimit() == 15
    
if __name__ == '__main__':
    test_create()
    test_getters()
