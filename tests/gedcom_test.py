import sys
sys.path.insert(0, '../src')

import main

def test_compile():
    # Can the program compile with no errors
    main.run()


def test_us01():
    assert main.us01DateAfterCurrentDate("22 JUN 2019") is True
    assert main.us01DateAfterCurrentDate("12 APR 2030") is False
    assert main.us01DateAfterCurrentDate("18 DEC 1932") is True
    assert main.us01DateAfterCurrentDate("N/A") is True