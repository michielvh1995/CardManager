class ERROR:
    def __init__(self):
        self.e = "ERROR"
        self.internal = ["ERROR"]

    def __str__(self):
        return self.e

    def __getitem__(self, key):
        return self.internal[key]

class KEYNOTFOUNDERROR(ERROR):
    def __init__(self, key, table = None):
        self.e = "KEY ERROR: key " + str(key) + " not found in table" + ((" in table " + table) if table else "!")
        self.internal = ["ERROR", table, key]


class COMMANDNOTFOUNDERROR(ERROR):
    def __init__(self, SQL):
        self.internal = ["ERROR"]
        self.e = "SQL ERROR: Unknown SQL command \" " + str(SQL) + "\" "
