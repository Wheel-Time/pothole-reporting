import mysql.connector
from mysql.connector import errorcode
from wheel_time_potholes import database_settings as db_settings

connection = None

try:
  connection = mysql.connector.connect(
    user=db_settings.username,
    password=db_settings.password,
    host=db_settings.host,
    database=db_settings.database)
  print('Database connection successful')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password. Please make sure your database configuration file is properly set up")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database '" + db_settings.database + "' does not exist. Please make sure your database configuration file is properly set up")
  else:
    print(err)
