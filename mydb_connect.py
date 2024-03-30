import mysql.connector

mydb = mysql.connector.connect(
                        host='gin040.mysql.pythonanywhere-services.com',
                        user='gin040',
                        password='mydb%pw>3!',
                        database='gin040$mydb',
                        auth_plugin='mysql_native_password'
                        )

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE users")
mycursor.execute()
#
# mycursor.execute("ALTER TABLE name")
# mycursor.execute("SHOW DATABASES")
# mycursor.execute("SHOW DATABASES")
# mycursor.execute("SHOW DATABASES")
# mycursor.execute("SHOW DATABASES")

