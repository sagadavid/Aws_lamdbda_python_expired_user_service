import mysql.connector as mysql
from datetime import timedelta, datetime

# prepared statements
host='localhost'
user='root'
password='pass0rd.'
database='moso'


def main():
    db=mysql.connect(host=host, user=user, password=password, database=database)
    cur=db.cursor(prepared=True)

    cur.execute("select full_name, uuid, email, last_login from users where last_login is not null")

    for execution in cur:
        print(execution)

    cur.close()
    db.close()


if __name__=="__main__":
    main()


