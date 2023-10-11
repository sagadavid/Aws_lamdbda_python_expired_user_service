import json
import pymysql

def lambda_handler(event, context):

    # TODO implement
    # connect aws passive dbS
    conn = pymysql.connect(
        host="moso-praksis-passive-users-db.cna5r0k4nskc.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="moso123.",
        database="moso_passive_users_db",
        port=3306
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to select users with last_login older than 11 months
    query = '''
                   SELECT uuid, full_name, last_login, email
                   FROM passive_users;
                   '''

    # Execute the SQL query
    cursor.execute(query)
    results = cursor.fetchall()

    # close connection to database
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': results
    }

testa = lambda_handler('a','b')
print(testa)