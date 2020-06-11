import sys
sys.path.insert(0, '../src')

import main
from helpers import dates
from modules import marriage_date_check

def test_compile():
    # Can the program compile with no errors
    main.run()


def test_us01():
    assert dates.us01DateAfterCurrentDate("22 JUN 2019") is True
    assert dates.us01DateAfterCurrentDate("12 APR 2030") is False
    assert dates.us01DateAfterCurrentDate("18 DEC 1932") is True
    assert dates.us01DateAfterCurrentDate("N/A") is True
    
def test_us42():
    assert dates.us42ValidDate("21 AUG 2019") is True
    assert dates.us42ValidDate("33 JUL 2011") is False
    assert dates.us42ValidDate("garbageText") is False
    assert dates.us42ValidDate("April 21st 2020") is False
    assert dates.us42ValidDate("20 FEB 2000") is True

def test_us05():
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "7 SEP 2013", "1 JAN 1900") is True
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "7 SEP 2013", "1 JAN 2020") is False
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "10 OCT 2010", "10 OCT 2010") is False