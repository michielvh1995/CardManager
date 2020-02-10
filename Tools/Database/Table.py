import DBErrors as err
import DBResponse as res

# TODO: REMOVE THIS IMPORT. The types are 100% certainly a SQL only thing!!!
from Types import typeTable



class Table:
    def __init__(self, fieldnames, where=None):
        self.fields = fieldnames    #
        self.header = []        # The field names
        self.rows = []          # [{name: field}]

        for f in self.fields:
            self.header.append(f)

    def Insert(self, names, values, ret = None):
        """ Insert a new row to the table
        """
        row = {}
        for i, f in enumerate(names):
            row[f] = values[i]

        self.rows.append(row)

        # TODO: Fix return
        if ret:
            return "asd"

    def Select(self, fields, tableName = None, where = None):
        """ Check if all names are in the fields and return the values of the rows per field
        """
        out = []
        for row in self.rows:
            r = []
            use = True
            if where:
                for pair in where:
                    if row.has_key(pair[0]):
                        if not row[pair[0]] == pair[1]:
                            use = False
                    else:
                        return err.KEYNOTFOUNDERROR(pair[0])

            # Match the WHERE

            # Select fields per row
            if use:
                for n in fields:
                    if row.has_key(n):
                        r.append(row[n])
                    else:
                        return err.KEYNOTFOUNDERROR(n)
                out.append(r)
        return out


class TypedTable(Table):
    def __init__(self, name, fields, contraints = None):
        self.fields = fields    # { name : type }
        self.rows   = []        # [{fieldname : value}]
        self.name = name

        # TODO: Check whether each of the types given are correct

    # TODO: return a proper response
    def Insert(self, names, values):
        """ Check whether if the items in the row are of the correct type and insert them
        """

        # Check whether the table has the key
        for key in names:
            if not self.fields.has_key(key):
                return err.KEYNOTFOUNDERROR(key, self.name)

        # Add the items and see whether they are the correct type
        row = {}
        for i, f in enumerate(names):
            # Check type in the typetable
            if typeTable[type(values[i])] == self.fields[f]:
                row[f] = values[i]  # Add the values
            else:                   # Throw a type error
                return err.TYPEERROR(f, self.fields[f], type(values[i]))

        self.rows.append(row)
        return res.DBResponse("SUCCESS", operation = "INSERT")

        # Raise acc?
