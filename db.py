import mysql.connector as mysql


# Establish a connection
# TODO what if unsuccessfull
db = mysql.connect(
    host="localhost",
    user="user1",
    passwd="sala1",
    database="personal_finance_app"
)