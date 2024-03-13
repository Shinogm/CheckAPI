from mysqlclientpy import DB
from app.utils.env import Env

check_db = DB(
    database=Env.get_secure('NAME_DB'),
    host=Env.get_secure('HOST_DB'),
    password=Env.get_secure('PASS_DB'),
    user=Env.get_secure('USER_DB')
)