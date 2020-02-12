import re
typeTable = [
        "TEXT",
        "INT",
        "FLOAT",
        "DATETIME",
        "DATE"
]

defaultValues = {
    "TEXT"  : "",
    "INT"   : 0,
    "FLOAT" : 0.0
}

class TypeCaster:
    def __init__(self):
        # Regex for:

        self.re_float = re.compile(r"[0-9\.]+") # Float
        self.re_integ = re.compile(r"[0-9]+") # Int
        self.re_dateT = re.compile(r"[0-9][0-9]\:[0-9][0-9]\:[0-9][0-9]") # TODO: Datetime

        self.defaults = defaultValues

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

    def __getitem__(self, key):
        """ Get the default value
        """
        self.defaults[key]
