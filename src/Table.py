# File for Table object
# Table object will simply hold the row and column data in accessible data members
# Utilizes prettytable to print the data

from prettytable import PrettyTable


class Table:
    def __init__(self, fieldNames=[]):
        self.Rows = []
        self.Columns = []
        self.Field_Names = fieldNames

        self.Table = PrettyTable(fieldNames)

    def Set_Field_Names(self, filedNames):
        self.Table.field_names = filedNames

    def Add_Row(self, row):
        self.Rows += [row]
        self.Table.add_row(row)

    def Display_Table(self):
        print(self.Table)
