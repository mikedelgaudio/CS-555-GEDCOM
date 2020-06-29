import sys
sys.path.insert(0, '../src')

import main
from helpers import dates
from modules import birth_date_check
from modules import marriage_date_check, list_upcoming_dates

def test_compile():
    # Can the program compile with no errors
    main.run()


def test_us01():
    assert dates.us01DateAfterCurrentDate("22 JUN 2019") is True
    assert dates.us01DateAfterCurrentDate("12 APR 2030") is False
    assert dates.us01DateAfterCurrentDate("18 DEC 1932") is True
    assert dates.us01DateAfterCurrentDate("N/A") is True

def test_us02():
    assert birth_date_check.birth_before_marriage("18 NOV 1999","18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_marriage("18 NOV 1999","18 NOV 2019","18 NOV 2010") is False
    assert birth_date_check.birth_before_marriage("18 NOV 1999","18 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage("18 NOV 2000","18 NOV 2000","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage("18 DEC 1999","18 DEC 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage("25 NOV 1999","25 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage("12 APR 2030","12 APR 2030","N/A") is True

def test_us03():
    assert birth_date_check.birth_before_death("18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_death("18 NOV 1999","18 NOV 1999") is True
    assert birth_date_check.birth_before_death("18 NOV 2000","18 NOV 1999") is False
    assert birth_date_check.birth_before_death("18 DEC 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_death("25 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_death("12 APR 2030","N/A") is True

def test_us04():
    assert marriage_date_check.marriage_divorce_date_comparison("N/A", "N/A") is False
    assert marriage_date_check.marriage_divorce_date_comparison("10 OCT 2000", "11 OCT 2000") is True
    assert marriage_date_check.marriage_divorce_date_comparison("10 OCT 2000", "10 OCT 2000") is False

def test_us05():
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "7 SEP 2013", "1 JAN 1900") is True
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "7 SEP 2013", "1 JAN 2020") is False
    assert marriage_date_check.marriage_before_death("10 OCT 2010", "10 OCT 2010", "10 OCT 2010") is False

def test_us08():
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 2019","18 NOV 2010") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 2000","18 NOV 2000","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 DEC 1999","18 DEC 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage_of_parents("25 NOV 1999","25 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_marriage_of_parents("12 APR 2030","12 APR 2030","N/A") is True

def test_us09():
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 2019","18 NOV 2010") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 2000","18 NOV 2000","18 NOV 1999") is False
    assert birth_date_check.birth_before_death_of_parents("18 DEC 1999","18 DEC 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_death_of_parents("25 NOV 1999","25 NOV 1999","18 NOV 1999") is False
    assert birth_date_check.birth_before_death_of_parents("12 APR 2030","12 APR 2030","N/A") is True

def test_us42():
    assert dates.us42ValidDate("21 AUG 2019") is True
    assert dates.us42ValidDate("33 JUL 2011") is False
    assert dates.us42ValidDate("garbageText") is False
    assert dates.us42ValidDate("April 21st 2020") is False
    assert dates.us42ValidDate("20 FEB 2000") is True

def test_30dayhelp():
    assert dates.next30days("7 JUL 2020") is True
    assert dates.next30days("7 JUL 1000") is True
    assert dates.next30days("10 DEC 2020") is False

def test_us39():
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "Y", "N/A", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is True
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "N", "19 FEB 2000", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2000", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "31 JUN 2019", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
