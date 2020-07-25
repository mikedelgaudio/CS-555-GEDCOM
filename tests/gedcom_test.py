import sys
sys.path.insert(0, '../src')

import sqlite3
import main
import datetime
from helpers import dates, sorting, fam, database as db
from modules import birth_date_check
from modules import marriage_date_check, marriage_check, list_upcoming_dates, list_deceased, unique_id, list_recent, list_living, gender_check, multiple_births
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

def test_us12():
    assert birth_date_check.parents_too_old("18 NOV 1999","18 NOV 1998","18 NOV 1998") is True
    assert birth_date_check.parents_too_old("18 NOV 1999","18 NOV 1938","18 NOV 1998") is False
    assert birth_date_check.parents_too_old("18 NOV 1999","18 NOV 1998","18 NOV 1918") is False
    assert birth_date_check.parents_too_old("18 NOV 1999","18 NOV 1938","18 NOV 1918") is False

def test_us21():
    assert gender_check.husb_wife_gender("M","F") is True
    assert gender_check.husb_wife_gender("F","F") is False
    assert gender_check.husb_wife_gender("M","M") is False
    assert gender_check.husb_wife_gender("F","M") is False
    assert gender_check.husb_wife_gender("Text","Text") is False

def test_us10():
    assert marriage_date_check.older_than_14("10 OCT 2000", "11 OCT 1000", "1 JAN 1015") is False
    assert marriage_date_check.older_than_14("10 OCT 2000", "11 OCT 1000", "1 JAN 2001") is False
    assert marriage_date_check.older_than_14("10 OCT 2000", "11 OCT 1000", "1 JAN 1001") is False
    assert marriage_date_check.older_than_14("10 OCT 2000", "11 OCT 1000", "1 JAN 2020") is True

def test_us11():
    assert fam.bigomy_checker([["", "", "N/A", "", "", "", "", ""], ["", "", "10 OCT 2000", "", "", "", "", ""], 
    ["", "", "11 OCT 2001", "", "", "", "", ""]]) is True
    assert fam.bigomy_checker([["", "", "N/A", "", "", "", "", ""], ["", "", "10 OCT 2000", "", "", "", "", ""], 
    ["", "", "N/A", "", "", "", "", ""]]) is False
    assert fam.bigomy_checker([["", "", "N/A", "", "", "", "", ""], ["", "", "N/A", "", "", "", "", ""], 
    ["", "", "N/A", "", "", "", "", ""]]) is False
    assert fam.bigomy_checker([["", "", "10 OCT 2020", "", "", "", "", ""], ["", "", "10 OCT 2000", "", "", "", "", ""], 
    ["", "", "11 OCT 2001", "", "", "", "", ""]]) is True
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
    today = datetime.datetime.now()
    assert dates.dateChecker((today + datetime.timedelta(25)).strftime("%d %b %Y").upper(), 30, True) is True
    assert dates.dateChecker((today + datetime.timedelta(368)).strftime("%d %b %Y").upper(), 30, True) is True
    assert dates.dateChecker((today + datetime.timedelta(200)).strftime("%d %b %Y").upper(), 30, True) is False

def test_us39():
    today = datetime.datetime.now()
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "Y", "N/A", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", (today + datetime.timedelta(-361)).strftime("%d %b %Y").upper(), "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is True
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20", "N", "19 FEB 2000", "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20", "Y", "N/A", "N/A", "01"]],[["001", (today + datetime.timedelta(-570)).strftime("%d %b %Y").upper(), "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "N", "19 FEB 2000", "N/A", "01"]],[["001", (today + datetime.timedelta(-67)).strftime("%d %b %Y").upper(), "N/A", "01",
                          "Bob Thornton", "02", "Hannah Montana", "N/A"]]) is False
    assert list_upcoming_dates.anniversary([["01", "Bob Thornton", "M", "18 FEB 2000", "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", "18 FEB 2000", "20",  "Y", "N/A", "N/A", "01"]],[["001", (today + datetime.timedelta(-360)).strftime("%d %b %Y").upper(), (today + datetime.timedelta(-359)).strftime("%d %b %Y").upper(), "01",
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
    today = datetime.datetime.now()
    assert dates.dateChecker((today + datetime.timedelta(-25)).strftime("%d %b %Y").upper(), -30, False) is True
    assert dates.dateChecker((today + datetime.timedelta(-200005)).strftime("%d %b %Y").upper(), -30, False) is False
    assert dates.dateChecker((today +datetime.timedelta(-125)).strftime("%d %b %Y").upper(), -30, False) is False
    assert dates.dateChecker((today +datetime.timedelta(25)).strftime("%d %b %Y").upper(), -30, False) is False

def test_us35(capsys):
    today = datetime.datetime.now()
    list_recent.list_recent([["01", "Bob Thornton", "M", "18 FEB 2000", "20","N", (today + datetime.timedelta(-20)).strftime("%d %b %Y").upper(), "N/A", "02"],["01", "Hannah Montana", "F", (today + datetime.timedelta(-18)).strftime("%d %b %Y").upper(), "0",  "Y", "N/A", "N/A", "01"]])

    expected = "US36: RECENT DEATH: Bob Thornton died on " + (today + datetime.timedelta(-20)).strftime("%b %d").upper() + ".\n" + "US35: RECENT BIRTH: Hannah Montana was born on " + (today + datetime.timedelta(-18)).strftime("%b %d").upper() + "!\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    list_recent.list_recent([["01", "Bob Thornton", "M", (today + datetime.timedelta(-10)).strftime("%d %b %Y").upper(), "20","N", (today + datetime.timedelta(-5)).strftime("%d %b %Y").upper(), "N/A", "02"]])

    expected =  "US36: RECENT DEATH: Bob Thornton died on "+(today + datetime.timedelta(-5)).strftime("%b %d").upper()+".\n" + "US35: RECENT BIRTH: Bob Thornton was born on " + (today + datetime.timedelta(-10)).strftime("%b %d").upper()+ "!\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    list_recent.list_recent([["01", "Bob Thornton", "M", (today + datetime.timedelta(-100)).strftime("%d %b %Y").upper(), "20","Y", "N/A" "N/A", "02"],["02", "Hannah Montana", "F", (today + datetime.timedelta(10)).strftime("%d %b %Y").upper(), "20",  "Y", "N/A", "N/A", "01"]])

    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

def test_us30(capsys):
    ## Happy case
    list_living.us30([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']]) 
    
    expected = "US30: ALIVE & MARRIED: Aerys /Targaryon/ and Rhaella /Targaryon/ are alive and married.\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    ## Husband died
    list_living.us30([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","FALSE", "N/A" "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']]) 
    
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

    ## Wife died
    list_living.us30([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "FALSE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']]) 
    
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

    ## Divorced
    list_living.us30([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']]) 
    
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected


def test_us31(capsys):
    ## Nobody is alive and single!
    list_living.us31([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A", "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']]) 
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

    ## Every single person is under 30
    list_living.us31([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A", "N/A", "N/A"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "N/A"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Father', '@I7@', 'Mother', '{@01@ @02@}']]) 
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected
    ## single person died 
    list_living.us31([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "40","FALSE", "N/A", "N/A", "N/A"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "N/A"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Father', '@I7@', 'Mother', '{@01@ @02@}']]) 
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected
    ## Divorced
    list_living.us31([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "40","TRUE", "N/A", "N/A", "N/A"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "40",  "TRUE", "N/A", "N/A", "N/A"]],
                             [['@F5@', '10 JUL 2001', '11 JUL 2001', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@0112@ @0122@}']])
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

    ## Both Alive and Single over 30 
    list_living.us31([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "40","TRUE", "N/A", "N/A", "N/A"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "40",  "TRUE", "N/A", "N/A", "N/A"]],
                             [['@F5@', '10 JUL 2001', 'N/A', '@I8@', 'Father', '@I7@', 'Mother', '{@01@ @02@}']]) 
    expected = "US31: ALIVE & SINGLE: Aerys /Targaryon/ is over 30 and has never been married.\n" + "US31: ALIVE & SINGLE: Rhaella /Targaryon/ is over 30 and has never been married.\n"

def test_us28(capsys):
    #IDs that don't exist in table
    sorting.us28([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "02"],["01", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']])
    
    expected = "US28: ERROR: Family ID @F5@ has a child ID @I2@ that does not exist in individual table.\nUS28: ERROR: Family ID @F5@ has a child ID @I9@ that does not exist in individual table.\nUS28: ERROR: Family ID @F5@ has a child ID @I10@ that does not exist in individual table.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    #IDs that exist in table
    sorting.us28([["01", "Aerys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "02"],["@I9@", "Rhaella /Targaryon/", "F", "18 FEB 2000", "20",  "TRUE", "N/A", "N/A", "01"]],
                             [['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{@I2@ @I9@ @I10@}']])
    
    expected = "US28: ERROR: Family ID @F5@ has a child ID @I2@ that does not exist in individual table.\nUS28: CHILDREN SORTED: Family ID @F5@ has 1 children sorted AGE 20--> @I9@ Rhaella /Targaryon/; \n"
    captured = capsys.readouterr()
    assert captured.out == expected


def test_us32_us14(capsys):
    ## no multiple births
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2001", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "18 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02}']])

    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected
    #twins
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02}']])

    expected = "US32: Family @F5@ has twins!\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    #triplets
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["03", "Merys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02 03}']])

    expected = "US32: Family @F5@ has triplets!\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    #quadruplets
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["03", "Merys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["04", "Lerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["05", "Ferys /Targaryon/", "M", "20 FEB 2003", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02 03 04 05}']])

    expected = "US32: Family @F5@ has quadruplets!\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    #quintuplets
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["03", "Merys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["04", "Lerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["05", "Ferys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02 03 04 05}']])

    expected = "US32: Family @F5@ has quintuplets!\n"
    captured = capsys.readouterr()
    assert captured.out == expected

    # > 5 kids born at the same time
    multiple_births.us32_us14([["01", "Aerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["06", "OHNO /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["03", "Merys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["04", "Lerys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["05", "Ferys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"],["02", "Berys /Targaryon/", "M", "20 FEB 2000", "20","TRUE", "N/A" "N/A", "N/A"]],[['@F5@', '10 JUL 2001', '21 AUG 2002', '@I8@', 'Aerys /Targaryon/', '@I7@', 'Rhaella /Targaryon/', '{01 02 03 04 05 06}']])

    expected = "US14: ANOMALY: No more than 5 siblings should be born at the same time.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
def test_us17():
    #yes we are marrying children
    assert fam.us17NoMarrriage2Child([['@I2@', 'Rhaegar /Targaryon/', 'F', '15 AUG 1780', 230, 'FALSE', '15 DEC 2010', '@F3@', '@F6@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'], ['@F1@', '10 AUG 2000', '10 AUG 1999', '@I2@', 'Rhaegar /Targaryon/', '@I4@', 'Elia /Martell/', '{@I4@ @I5@}']]) is False
    
    #no marriage
    assert fam.us17NoMarrriage2Child([['@I2@', 'Rhaegar /Targaryon/', 'F', '15 AUG 1780', 230, 'FALSE', '15 DEC 2010', '@F3@', '@F6@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'], ['@F1@', '10 AUG 2000', '10 AUG 1999', '@I2@', 'Rhaegar /Targaryon/', '@I4@', 'Elia /Martell/', '{@I8@ @I5@}']]) is True 
    
    # cause an exception
    assert fam.us17NoMarrriage2Child([['@I2@', 'Rhaegar /Targaryon/', 'F', '15 AUG 1780', 230, 'FALSE', '15 DEC 2010', '@F3@', '@F6@'], ['@F1@', '10 AUG 2000', '10 AUG 1999', '@I2@', 'Rhaegar /Targaryon/', '@I4@', 'Elia /Martell/', '{@I4@ @I5@}']]) is None
    
def test_us34(capsys):
    #husb's older case
    marriage_date_check.us34ListLargeAge([['@I2@', 'Rhaegar /Targaryon/', 'F', '15 AUG 1780', 230, 'FALSE', '15 DEC 2010', '@F3@', '@F6@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'], ['@I5@', 'Aegon /Targaryon/', 'M', '29 JUN 2005', 15, 'TRUE', 'N/A', '@F1@', 'N/A'], ['@F1@', '10 AUG 2000', '10 AUG 1999', '@I2@', 'Rhaegar /Targaryon/', '@I4@', 'Elia /Martell/', '{@I4@ @I5@}']])
    expected = "US34: ANOMALY: Large age difference on family @F1@! @I2@ Rhaegar /Targaryon/ is more than twice as old as spouse @I4@ Elia /Martell/.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    #madam's older
    marriage_date_check.us34ListLargeAge([['@I16@', 'Aegon V /Targaryon/', 'M', '9 JUL 1950', -10, 'FALSE', '5 JUL 1941', 'N/A', '@F4@'], ['@I15@', 'Cersei /Targaryon/', 'F', '5 JUL 2021', -1, 'FALSE', '5 JUL 2020', 'N/A', '@F4@'], ['@I24@', 'Funcan /Targaryon/', 'M', '27 DEC 2003', 16, 'TRUE', 'N/A', '@F4@', 'N/A'], ['@F4@', '30 JUL 1959', 'N/A', '@I16@', 'Aegon V /Targaryon/', '@I15@', 'Cersei /Targaryon/', '{@I20@ @I21@ @I22@ @I23@ @I24@ @I25@}']])
    expected = "US34: ANOMALY: Large age difference on family @F4@! @I15@ Cersei /Targaryon/ is more than twice as old as spouse @I16@ Aegon V /Targaryon/.\n"
    captured = capsys.readouterr()
    assert captured.out == expected
    
    #broken input
    marriage_date_check.us34ListLargeAge([['@I16@', 'Aegon V /Targaryon/', 'M', '9 JUL 1950', -10, 'FALSE', '5 JUL 1941', 'N/A', '@F4@'], ['@I15@', 'Cersei /Targaryon/', 'F', '5 JUL 2021', -1, 'FALSE', '5 JUL 2020', 'N/A', '@F4@']])
    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

def test_us20(capsys):
    # yes i am marrying niece/nephew
    ind = [['@I2@', 'Rhaegar /Targaryon/', 'M', '15 AUG 1780', 230, 'FALSE', '15 DEC 2010', '@F3@', '@F1@'], ['@I4@', 'Elia /Martell/', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F1@'],
            ['@I6@', 'brother dad', 'M', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', '@F1@', '@F5@'],
             ['@I27@', 'sister wife', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', 'N/A', '@F5@'],
             ['@I5@', 'uncle', 'M', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', '@F1@', '@F10@'], 
             ['06', 'niece', 'F', '11 MAY 1980', 18, 'FALSE', '10 OCT 1998', '@F5@', '@F10@']]
    fam = [['@F1@', '10 AUG 2000', '10 AUG 1999', '@I2@', 'Rhaegar /Targaryon/', '@I4@', 'Elia /Martell/', '{@I6@ @I5@}'], 
            ['@F5@', '10 JUL 2001', '21 AUG 2002', '@I6@', 'brother dad', '@I27@', 'sister wife', '{06}'], 
            ['@F10@', '10 JUL 2001', '21 AUG 2002', '@I5@', 'uncle', '06', 'niece', 'N/A']]
    conn = sqlite3.connect("../familytable.db")

    if conn is not None:
        cur = conn.cursor()
        cur.execute(db.create_ind_table())
        cur.execute(db.create_fam_table())
        for i in ind:
            db.populate_ind(i, cur, conn)
        for f in fam:
            db.populate_fam(f, cur, conn)


    marriage_check.us20(ind, fam, cur)

    expected = "US20: ANOMALY: Family @F10@ -> @I5@ should NOT marry their niece/nephew 06.\n"
    captured = capsys.readouterr()
    assert captured.out == expected


    cur.execute("DELETE FROM families WHERE id=?", ("@F10@",))

    marriage_check.us20(ind, fam, cur)

    expected = ""
    captured = capsys.readouterr()
    assert captured.out == expected

     # clear db at the end!
    sql = 'DELETE FROM individuals'
    cur.execute(sql)
    conn.commit()

    sql = 'DELETE FROM families'
    cur.execute(sql)
    conn.commit()