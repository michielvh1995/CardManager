import re
typeTable = [
        "TEXT",
        "INT",
        "FLOAT",
        "DATETIME",
        "DATE"
]

class TypeCaster:
    def __init__(self):
        # Regex for:

        self.re_float = re.compile(r"[0-9\.]+") # Float
        self.re_integ = re.compile(r"[0-9]+") # Int
        self.re_dateT = re.compile(r"[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]") # TODO: Datetime

    def TypeCast(self, string):
        type = "TEXT"
        cast = string

        if self.re_integ.match(string):
            type = "INT"
            cast = int(string)
        elif self.re_float.match(string):
            type = "FLOAT"
            cast = float(string)
        elif self.re_dateT.match(string):   # TODO: fix datetime casting
            type = "DATETIME"
            cast = string

        return (type, cast)
