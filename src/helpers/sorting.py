# All helpers used for sorting, whether it be dates individuals families etc

import re
# Resource cited:https://intellipaat.com/community/33368/does-python-have-a-built-in-function-for-string-natural-sort
# This is known as natural sorting, almost like char sorts we did in 392


def sortById(gedcomList):
    def convert(text): return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key): return [convert(c)
                                   for c in re.split('([0-9]+)', key)]
    # returns a copy of the sorted list by index 0 which is the unique ID field
    return sorted(gedcomList, key=lambda x: alphanum_key(x[0]))
