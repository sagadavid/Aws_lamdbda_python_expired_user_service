import json
import pymysql

def lambda_handler(event, context):

    # TODO implement
    # connect aws passive dbS
    conn = pymysql.connect(
        host="moso-praksis-source-db.cna5r0k4nskc.eu-north-1.rds.amazonaws.com",
        user="admin",
        password="moso123.",
        database="moso-aws-praksis",
        port=3306
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to select users with last_login older than 11 months
    interval_query = '''
                   SELECT uuid, full_name, last_login, email
                   FROM users
                   WHERE last_login < DATE_SUB(NOW(), INTERVAL 11 MONTH);
                   '''

    # Execute the SQL query
    cursor.execute(interval_query)
    fetchy_results = cursor.fetchall()

    # close connection to database
    cursor.close()
    conn.close()

    return {
        'statusCode': 200,
        'body': fetchy_results
    }

testa=lambda_handler('a','b')
print(testa)