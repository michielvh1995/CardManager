from Database import DataBase

db = DataBase()
print db.create_table("test", fields = ["id", "value"])
