import sys
sys.path.insert(0, '../src')

import main

def test_compile():
    # Can the program compile with no errors
    main.run()
    
def test_us42():
    assert main.us42ValidDate("21 AUG 2019") is True
    assert main.us42ValidDate("33 JUL 2011") is False
    assert main.us42ValidDate("garbageText") is False
    assert main.us42ValidDate("April 21st 2020") is False
    assert main.us42ValidDate("20 FEB 2000") is True
