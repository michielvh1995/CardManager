from DBResponse import Response

class ERROR(Response):
    def __init__(self, text = "No extra information given"):
        self.internal = {
            "type"     : "ERROR",
            "errorText": text
        }

    def __str__(self):
        return "Error: " + self.internal["errorText"]

# ---------------------------------------------------------------------------
# Table errors
# ---------------------------------------------------------------------------
class KEYNOTFOUNDERROR(ERROR):
    def __init__(self, key, table = None):
        ERROR.__init__(self, text = "KEY ERROR: key " + str(key) + " not found in table" + ((" in table " + table) if table else "!"))

# ---------------------------------------------------------------------------
# SQL errors
# ---------------------------------------------------------------------------
class COMMANDNOTFOUNDERROR(ERROR):
    def __init__(self, SQL):
        ERROR.__init__(self, text = "SQL ERROR: Unknown SQL command \" " + str(SQL) + "\" ")

class TYPEERROR(ERROR):
    def __init__(self, field, fieldtype, errtype):
        ERROR.__init__(self, text = "Field " + str(field) + " is of type " + str(fieldtype)  + ", not of type " + str(errtype))

class TYPENOTFOUNDERROR(ERROR):
    def __init__(self, errtype):
        ERROR.__init__(self, text = "Type " + str(errtype) + " not recognized!")

class TABLENOTFOUNDERROR(ERROR):
    def __init__(self, table):
        ERROR.__init__(self, text = "Table " + str(table) + " does not exist!")

# ---------------------------------------------------------------------------
# File system errors
# ---------------------------------------------------------------------------
class FileSysError(ERROR):
    def __init__(self, file = None, operation = None, explanation = None):
        ERROR.__init__(self, text = "FILE SYSTEM ERROR: Cannot execute " + str(operation) + " for file " + str(file) + ": " + str(explanation))
