import mysql.connector as mysql
from datetime import timedelta, datetime

# prepared statements
host='localhost'
user='root'
password='pass0rd.'
database='moso'


def main():
    conn=mysql.connect(host=host, user=user, password=password, database=database)
    cursor=conn.cursor(prepared=True)

    reading = cursor.execute("select full_name, uuid, email, last_login from users where last_login is not null")

    for execution in cursor:
        # returns tuple
        print(f'execution {type(execution)} {execution}')

    print(type(reading))
    # <class 'NoneType'> The type of reading here is a database query.


    cursor.close()
    conn.close()


if __name__=="__main__":
    main()


