# Database response:
# [str, table. fields, (other)]

class Response:
    def __init__(self, type):
        self.internal = { "type" : type }

    def __getitem__(self, key):
        return self.internal[key]

    def __setitem__(self, key, value):
        self.internal[key] = value

    def __len__(self):
        return len(self.internal)

    def __str__(self):
        return str(self.internal)

class DBResponse(Response):
    def __init__(self, type, database = None, table = None, operation = None):
        self.internal = {
            "type"      : type,
            "database"  : database,
            "table"     : table,
            "operation" : operation
        }


class SQLResponse(Response):
    def __init__(self, type, table = None, fields = None, returnquery = None):
        self.internal = {
            "type": type,
            "table" : table,
            "fields" : fields,
            "return" : returnquery
        }

class SQLIncomplete(SQLResponse):
    def __init__(self, query, table = None, fields = None, returnquery = None):
        self.internal = {
            "type": "INCOMPLETE",
            "table" : table,
            "fields" : fields,
            "return" : returnquery,
            "query"  : query
        }

class SQLComplete(SQLResponse):
    def __init__(self, query, table = None, fields = None, returnquery = None):
        self.internal = {
            "type": "COMPLETE",
            "table" : table,
            "fields" : fields,
            "return" : returnquery,
            "query"  : query
        }


class FILESysAcknowledge(Response):
    def __init__(self, file = None, operation = None, position = None):
        self.internal = {
            "type" : "ACKNOWLEDGE",
            "file" : file,
            "operation" : operation,
            "position"  : position
        }

# ---------------------------------------------------------------------------
# Standard responses
# ---------------------------------------------------------------------------

SQLNone = SQLResponse("NONE")
