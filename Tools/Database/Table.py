import DBErrors as err
import DBResponse as res

# TODO: REMOVE THIS IMPORT. The types are 100% certainly a SQL only thing!!!
from Types import typeTable, TypeCaster



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
    def __init__(self):
        self.name = "None"

    def TryCreateTable(self, name, fields):
        """
        """
        # Check if all types exist, if one doesn't raise an error
        for field in fields.keys():
            if not fields[field] in typeTable:
                return err.TYPENOTFOUNDERROR(fields[field])

        self.name   = name
        self.fields = fields
        self.rows   = []
        self.caster = TypeCaster()

        return res.DBResponse(
            type      = "SUCCESS",
            operation = "CREATE TABLE",
            table     = name
        )

    def Insert(self, kvpairs):
        """ Check whether if the items in the row are of the correct type and insert them
        """

        row = {}
        # Check whether the table has the key and ifso insert into row
        for key, value in kvpairs:
            if not self.fields.has_key(key):    # Check if key exists
                return err.KEYNOTFOUNDERROR(key, self.name)

            # Check typing and add to row
            if not self.fields[key] == "TEXT":
                type, cast = self.caster.TypeCast(value)
                if type == self.fields[key]:
                    row[key] = cast
                else:
                    return err.TYPEERROR(key, self.fields[key], type)
            else: # Ignore typing if field type is text
                row[key] = value

        self.rows.append(row)
        return res.DBResponse("SUCCESS", operation = "INSERT", table = self.name)

        # Raise acc?
