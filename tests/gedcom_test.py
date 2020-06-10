import sys
sys.path.insert(0, '../src')

import main
from helpers import dates

def test_compile():
    # Can the program compile with no errors
    main.run()


def test_us01():
    assert dates.us01DateAfterCurrentDate("22 JUN 2019") is True
    assert dates.us01DateAfterCurrentDate("12 APR 2030") is False
    assert dates.us01DateAfterCurrentDate("18 DEC 1932") is True
    assert dates.us01DateAfterCurrentDate("N/A") is True

def test_us03():
    assert dates.us03BirthBeforeDeath("18 NOV 1999","18 NOV 2019") is True
    assert dates.us03BirthBeforeDeath("18 NOV 1999","18 NOV 1999") is True
    assert dates.us03BirthBeforeDeath("18 NOV 2000","18 NOV 1999") is False
    assert dates.us03BirthBeforeDeath("18 DEC 1999","18 NOV 1999") is False
    assert dates.us03BirthBeforeDeath("25 NOV 1999","18 NOV 1999") is False
    assert dates.us03BirthBeforeDeath("12 APR 2030","N/A") is True
