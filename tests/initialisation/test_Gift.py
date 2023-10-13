import sys, os, pytest
def par(x) : return os.path.dirname(x)
sys.path.append(par(par(par(os.path.realpath(__file__)))))
from classes.Gift import Gift

def getGift() -> Gift:
    return Gift("Olivia", 1, 10, 5, 1)

def test_create() -> None:
    g = Gift("Olivia", 1, 10, 5, 1)

    assert g.score.__class__ == int
    assert g.weight.__class__ == int
    assert g.position.__class__ == tuple
    assert g.name.__class__ == str
    assert g.position[0].__class__ == int
    assert len(g.position) == 2

def test_getters() -> None:
    g = getGift()

    assert g.getName() == 'Olivia'
    assert g.getPosition() == (5, 1)
    assert g.getScore() == 1
    assert g.getWeight() == 10
    
if __name__ == '__main__':
    test_create()
    test_getters()
