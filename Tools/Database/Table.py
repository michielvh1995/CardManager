import DBErrors as err
import DBResponse as res

from Types import typeTable, TypeCaster

class TypedTable:
    def __init__(self):
        self.name = "None"

        # For setting default values per field
        self.defaults = {}
        self.defaultsSet = []

    def TryCreateTable(self, name, fields):
        """ TODO: Description
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

    # TODO: Refactor for speed
    # TODO: Add support for other type of conditions than WHERE
    def Select(self, fields, conditions = []):
        """ Select the fields for the rows for which the conditions are true.
        """
        out = []

        exec_cond = []

        # Turn the conditions into something useful
        for cond_field, action, value in conditions:
            # Typecheck conditions
            cond_type, cond_val = self.caster.TypeCast(value)
            if not self.fields[cond_field] == cond_type:
                return err.TYPEERROR(cond_field, self.fields[cond_field], cond_type)

            fun = False
            # Unpack the condition into a function
            if action == "=":           # WHERE A = B
                fun = lambda f : f[cond_field] == cond_val
            elif action == ">=":        # WHERE A >= B
                fun = lambda f : f[cond_field] >= cond_val
            elif action == "<=":        # WHERE A <= B
                fun = lambda f : f[cond_field] <= cond_val

            if not fun:
                # TODO: define an error for this
                return err.ERROR("INVALID CONDITIONING OPERATOR")

            exec_cond.append(fun)

        # Do the actual searching
        for row in self.rows:
            r = []
            use = True

            # Execute the conditions
            for cond in exec_cond:
                use = cond(row)

            # If all conditions hold, subset the row
            if use:
                for f in fields:
                    r.append(row[f])

                # If the row is usable
                out.append(r)
        return out

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
                    row[key]    = cast
                else:
                    return err.TYPEERROR(key, self.fields[key], type)
            else: # Ignore typing if field type is text
                row[key]    = value

        for key in self.fields.keys():               # Fill in the default values for all empty keys
            if not row.has_key(key):
                row[key] = self.Defaults(key)

        self.rows.append(row)
        return res.DBResponse("SUCCESS", operation = "INSERT", table = self.name)

    def Defaults(self, field):
        """ Returns the default value for a given field
        """
        if field in self.defaultsSet:
            return self.defaults[field]

        return self.caster[self.fields[field]]
