import os

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'Helpforu@09')
    MYSQL_DB = os.getenv('MYSQL_DB', 'autopods_db')  # Change as per your database name
