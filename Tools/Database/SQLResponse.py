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

class SQLResponse(Response):
    def __init__(self, type, table = None, fields = None, returnquery = None ):

        self.internal = {
            "type": type,
            "table" : table,
            "fields" : fields,
            "return" : returnquery
        }



SQLNone = SQLResponse("NONE")
