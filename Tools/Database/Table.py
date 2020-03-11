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
        fbuild = {}
        for field in fields.keys():
            if not fields[field][0] in typeTable:
                return err.TYPENOTFOUNDERROR(fields[field][0])
            fbuild[field] = fields[field][0]


        self.name   = name
        self.fields = fbuild    # Fields & types
        self.rows   = []
        self.caster = TypeCaster()

        # Set constraints
        self.primary = "ID"
        self.setConstraints(fields)

        self.primaryIndex = {}  # Elke insert krijgt de primary key hier + de index ervan in de rows

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
        """ Check for uniqueness in the primary key and types, then finally add the type-cast value to the db
        """

        row = {}

        # Check whether the table has the key and ifso insert into row
        for key, value in kvpairs:
            if not self.fields.has_key(key):    # Check if key exists
                return err.KEYNOTFOUNDERROR(key, self.name)

                # Check for primary uniqueness
                if key == self.primary:
                    if value in self.self.primaryIndex.keys():
                        # TODO: Raise proper error
                        return err.ERROR(text = "Tried to insert not-unique primary key!")

                # Check types and typecast
                if not self.fields[key] == "TEXT":
                    type, cast = self.caster.TypeCast(value)
                    if type == self.fields[key]:    # Check for correct type
                        row[key] = cast
                    else:
                        return err.TYPEERROR(key, self.fields[key], type)
                else:
                    row[key]     = value

        # Now fill up the missed keys in the row
        for key in self.fields.keys():
            if not row.has_key(key):
                row[key] = self.Defaults(key)

        # Finally add the row to the database
        self.rows.append(row)
        return res.DBResponse("SUCCESS", operation = "INSERT", table = self.name)

    def setConstraints(self, constraints):
        """ Fills in a list of lambda functions for each of the fields
        input:
            TODO
        returns:
            DBResponse  :   The response of filling in the constraints; can be a type error
        """
        self.consts = {}

        for field in constraints.keys():
            funcs = []

            # Check the type consrtaint
            if not constraints[field][0] in typeTable:
                return err.TYPENOTFOUNDERROR(constraints[field][0])

            # Set the type constraint
            # type, cast = self.caster.TypeCast(value)
            print constraints[field][0]
            f = None
            if constraints[field][0] == "TEXT":
                f = lambda x: True
            else:
                f = lambda x: self.caster.TypeCast(x)[0] == constraints[field][0]

            funcs.append(f)

            # The other constraitns
            for c in constraints[field][1:]:
                # primary:
                funcs.append(lambda x: not x in self.primaryIndex.keys())

                continue

            self.consts[field] = funcs

        return res.Response("ACC")




    def Defaults(self, field):
        """ Returns the default value for a given field
        """
        if field in self.defaultsSet:
            return self.defaults[field]

        return self.caster[self.fields[field]]
