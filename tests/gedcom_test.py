import sys
sys.path.insert(0, '../src')

import main
from helpers import dates
from modules import birth_date_check
from modules import marriage_date_check, list_upcoming_dates, list_deceased, unique_id, list_recent
import pytest
from _pytest.compat import CaptureAndPassthroughIO
from _pytest.compat import CaptureIO
from _pytest.compat import TYPE_CHECKING
from _pytest.config import Config
from _pytest.fixtures import FixtureRequest

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
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1998","18 NOV 2019") is True
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 2000","18 NOV 2019") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1997","18 NOV 1998") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1997","18 OCT 1999") is True
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","18 NOV 1998","N/A") is True
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","19 NOV 2000","N/A") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","N/A","N/A") is False
    assert birth_date_check.birth_before_marriage_of_parents("18 NOV 1999","N/A","18 NOV 2019") is False

def test_us09():
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 2000","18 NOV 2019") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1999","18 NOV 2019") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1998","18 NOV 2019") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 2000","18 NOV 1998") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1999","18 OCT 1999") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","N/A","18 NOV 2019") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","N/A","18 NOV 1998") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 2019","N/A") is True
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","18 NOV 1998","N/A") is False
    assert birth_date_check.birth_before_death_of_parents("18 NOV 1999","N/A","N/A") is True
def test_us06():
    assert marriage_date_check.divorce_date_before_death("10 OCT 2010", "N/A", "N/A") is True
    assert marriage_date_check.divorce_date_before_death("N/A", "10 OCT 2000", "2 JAN 2011") is False
    assert marriage_date_check.divorce_date_before_death("10 OCT 2013", "9 OCT 2013", "1 JAN 2014") is False
    assert marriage_date_check.divorce_date_before_death("10 OCT 2005", "11 OCT 2005", "11 OCT 2005") is True
    assert marriage_date_check.divorce_date_before_death("10 OCT 2005", "N/A", "11 OCT 2005") is True
    assert marriage_date_check.divorce_date_before_death("10 OCT 2005", "11 OCT 2005", "N/A") is True

def test_us07():
    assert birth_date_check.less_than_150_years("10 OCT 2000", "N/A") is True
    assert birth_date_check.less_than_150_years("10 OCT 1850", "N/A") is False
    assert birth_date_check.less_than_150_years("10 OCT 1000", "3 FEB 1009") is True
    assert birth_date_check.less_than_150_years("10 OCT 1000", "11 OCT 1150") is False

def test_us42():
    assert dates.us42ValidDate("21 AUG 2019") is True
    assert dates.us42ValidDate("33 JUL 2011") is False
    assert dates.us42ValidDate("garbageText") is False
    assert dates.us42ValidDate("April 21st 2020") is False
    assert dates.us42ValidDate("20 FEB 2000") is True

def test_30dayhelp():
    assert dates.dateChecker("7 JUL 2020", 30, True) is True
    assert dates.dateChecker("7 JUL 1000", 30, True) is True
    assert dates.dateChecker("10 DEC 2020", 30, True) is False

def test_us39():
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "Y", "N/A", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is True
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "N", "19 FEB 2000", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is True
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2000", "N/A", "01"]],[["001", "30 JUN 2019", "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is True
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "Y", "N/A", "N/A", "01"]],[["001", "30 JUN 2019", "31 JUN 2019", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
    
def test_us29(capsys):
    #normal date
    list_deceased.us29ListDeceased(
        [["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2000", "N/A", "01"]]
    )
    expected = "US29: DEAD: 02 Hannah Montana died on 19 FEB 2000.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    #future date
    list_deceased.us29ListDeceased(
        [["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2025", "N/A", "01"]]
    )
    expected2 = ""
    captured2 = capsys.readouterr()
    assert captured2.out == expected2
    # bad date
    list_deceased.us29ListDeceased(
        [["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "FakeDeathString" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2025", "N/A", "01"]]
    )
    expected3 = ""
    captured3 = capsys.readouterr()
    assert captured3.out == expected3
    
def test_us22(capsys):
    #normal duplicates case
    unique_id.us22UniqueIds([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["01", "Hannah Montana", "F", "18 FEB 2000", "20",  "Y", "N/A", "N/A", "01"]],[['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}'], ['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']])
    
    expected = "US22: ERROR: DUPID: Bob Thornton has a duplicate individual ID of 01.\n" + "US22: ERROR: DUPID: Hannah Montana has a duplicate individual ID of 01.\n" + "US22: ERROR: DUPID: Family ID @F5@.\n" + "US22: ERROR: DUPID: Family ID @F5@.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    #no duplicates case
    unique_id.us22UniqueIds([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "Y", "N/A", "N/A", "01"]],[['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}'], ['@F3@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']])
    
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected


def test_us36():
    assert dates.dateChecker("7 JUN 2020", -30, False) is True
    assert dates.dateChecker("7 JUN 1000", -30, False) is False
    assert dates.dateChecker("10 DEC 2020", -30, False) is False
    assert dates.dateChecker("10 JUL 2020", -30, False) is False

def test_us35(capsys):
    list_recent.list_recent([["01", "Bob Thornton", "M", "18 FEB 2000", "20","N", "25 JUN 2020", "N/A", "02"],["01", "Hannah Montana", "F", "18 JUN 2020", "0",  "Y", "N/A", "N/A", "01"]])
    
    expected = "US36: RECENT DEATH: Bob Thornton died on JUN 25.\n" + "US35: RECENT BIRTH: Hannah Montana was born on JUN 18!\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    list_recent.list_recent([["01", "Bob Thornton", "M", "18 JUN 2020", "20","N", "25 JUN 2020", "N/A", "02"]])
    
    expected =  "US36: RECENT DEATH: Bob Thornton died on JUN 25.\n" + "US35: RECENT BIRTH: Bob Thornton was born on JUN 18!\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    list_recent.list_recent([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 JUN 2000", "20",  "Y", "N/A", "N/A", "01"]])
    
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected
