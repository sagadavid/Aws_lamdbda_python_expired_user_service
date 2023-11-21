import pymysql
from datetime import datetime, timedelta, date

# # Replace these values with your MySQL server configuration
# host = "localhost"
# user = "root"
# password = "pass0rd."
# database = "moso"
# port = 3306

# connection to aws Servers and theirs databases...
#                       !!!!!!! CALL HOST NAMES AND DATABASES RESPECTIVELY IN EACH FUNCTION !!!!!!
host_passive = 'moso-praksis-passive-users-db.cna5r0k4nskc.eu-north-1.rds.amazonaws.com'
host_source = 'moso-praksis-source-db.cna5r0k4nskc.eu-north-1.rds.amazonaws.com'

database_passive = 'moso_passive_users_db'
database_source = 'moso-aws-praksis'

user = '***'
password = '***'
port = 3306


global fetched_results


# Define a class to represent an Expiring_User object
class ExpiringUser:
    def __init__(self, uuid, full_name, last_login, email):
        self.uuid = uuid
        self.full_name = full_name
        self.last_login = last_login
        self.email = email


# want to reach database and get users depending on my query which is a last log-in interval
def fetch():
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host_source, user=user,
                               password=password, database=database_source, port=port)
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

    # see if there is any error
    except pymysql.Error as e:
        print(f"An error getting_expiry_users: {e}")

    # returns a tuple
    return fetchy_results


def convert(result):
    uuid, full_name, last_login, email = result
    expiry = ExpiringUser(uuid, full_name, last_login, email)
    return expiry


def check_uuid_in_table(expiry):
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host_passive, user=user,
                               password=password, database=database_passive, port=port)
        cursor = conn.cursor()

        # Check if the user exists in warned_users
        check_query = "SELECT uuid from passive_users where uuid=%s"
        cursor.execute(check_query, expiry.uuid)
        uuid_in_table = cursor.fetchone()

        # Close the database connection
        conn.close()

    except pymysql.Error as err:
        raise Exception(f'An error during cross_check: {err}')

    # Return True if the user matched, False otherwise
    return uuid_in_table is not None


def insert_mail_mark_date(matched_object):
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host_passive, user=user,
                               password=password, database=database_passive, port=port)
        cursor = conn.cursor()

        # Expiry does not exist in warned_users, so save it as a new row
        insertion_query = '''
        INSERT INTO passive_users 
        (uuid, full_name, last_login, email ) 
        VALUES (%s,%s,%s,%s)
        '''

        inserted = cursor.execute(insertion_query,
                                  (matched_object.uuid,
                                   matched_object.full_name,
                                   matched_object.last_login,
                                   matched_object.email))
        print(
            f'*** {matched_object.full_name} inserted into passive users table \n')

        # mail_the_inserted = inserted
        # MAILING LOGIC HERE !!!!!
        print(f'run mail service here ! ')
        print(
            f'*** {matched_object.full_name} will be mailed by {matched_object.email}\n')

        # got_mark_and_date = mail_inserted
        mail_and_date_query = """
            UPDATE passive_users
            SET isMailed = True, mail_date = NOW()
            WHERE uuid=%s;
            """

        mail_and_date = cursor.execute(
            mail_and_date_query, matched_object.uuid)

        print(
            f'*** user {matched_object.full_name} was mailed and dated {mail_and_date}\n')

        get_mail_date = '''
            SELECT mail_date FROM passive_users
            WHERE uuid=%s;
            '''

        cursor.execute(get_mail_date, matched_object.uuid)
        maildate = cursor.fetchone()

        if maildate:
            print(
                f'### user {matched_object.full_name} was mailed at date: {maildate[0]}\n')
        else:
            print('no maildate available')

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')


def check_mail_date(matching_uuid):
    try:
        # Replace 'your_uuid_here' with the UUID you want to check
        # Connect to the MySQL server
        conn = pymysql.connect(host=host_passive, user=user,
                               password=password, database=database_passive, port=port)
        cursor = conn.cursor()

        # mail_date older than 7 or not
        check_query = '''
               SELECT 
               CASE 
               WHEN mail_date < DATE_SUB(NOW(), INTERVAL 7 DAY) 
               THEN 'TRUE'
               ELSE 'FALSE'
               END AS is_mail_date_older_than_7_days
               FROM passive_users
               WHERE uuid = %s;
               '''

        cursor.execute(check_query, matching_uuid)
        mail_date_older = cursor.fetchone()

        print(f'*** mail date older ???  {type(mail_date_older[0])}')
        # Return True if the mailing date is older than 7 days,
        # False otherwise
        result = mail_date_older[0]
        if result == 'TRUE':
            return True
        return False

        # return mail_date_older[0] is not None

    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')

 # Close the database connection
        cursor.close()
        conn.close()


def delete_user_from_aws_and_warned(older_mail):
    # Replace 'your_uuid_here' with the UUID you want to use for deletion
    uuid_to_delete = older_mail.uuid

    # Establish a connection to the MySQL server
    connection = pymysql.connect(
        host=host_passive, user=user, password=password, database=database_passive, port=port)

    try:
        # Create a new cursor to interact with the database
        cursor = connection.cursor()

        # Define the SQL query to delete the row with the specified UUID
        sql_query = f"DELETE FROM passive_users WHERE uuid = '{uuid_to_delete}'"

        # Execute the SQL query to delete the row
        cursor.execute(sql_query)

        # Commit the changes to the database
        connection.commit()

        # Check if any rows were affected by the delete operation
        if cursor.rowcount > 0:
            print(
                f"*** Row by UUID {uuid_to_delete} deleted successfully.\n")

            # got_mark_and_date = mail_inserted
            delete_and_date_query = """
                        UPDATE passive_users
                        SET isDeleted = True, delete_date = NOW()
                        WHERE uuid=%s;
                        """

            # set deletion date
            cursor.execute(delete_and_date_query, uuid_to_delete)
            print(f'*** delete_date is set to {date.today()}\n')

        else:
            print(
                f"*** No rows found with UUID {uuid_to_delete} to delete.\n")
        print('*** user should be deleted from aws servers as well !***')

    finally:
        # Close the cursor and the database connection
        cursor.close()
        connection.close()
    print(
        f'*** user {uuid_to_delete} will be deleted form aws and local, later.. so pass now \n')


def main():
    # get tuple of last logger in 11 months
    fetch_results = fetch()
    print(f'*************** fetch resulst: \n {fetch_results}\n')

    # iterate results from db
    for result in fetch_results:

        # convert query results to objects
        expiry = convert(result)
        print(f'*** {expiry.full_name} is an object now\n')

        # check object uuid in warned table
        in_table_uuid = check_uuid_in_table(expiry)
        print(
            f'*** {expiry.full_name} exists in the passive users table? {in_table_uuid}\n')

        # if uuid is in warned_user table
        if in_table_uuid is False or None:

            print(f'** {expiry.full_name} is not in the passive user table\n')
            # insert row, mail it, and note the mail date object to table
            insert_mail_mark_date(expiry)

        elif in_table_uuid is not False or None:
            # elif in_table_uuid is True and not None:

            # check if it is mailed 7 days ago
            seven_days_older = check_mail_date(expiry.uuid)
            # print(f'seven days results: {seven_days_older}')

            # we conclude that:
            # the user is syk-passive og mailed more than 7 days ago
            if seven_days_older is True:
                # NOTE THAT then delete user from both aws and warned table
                print(
                    f'*** is mailing date older than 7 days? {seven_days_older}\n')
                # delete_user_from_aws_and_warned(expiry)
                print('*** deletion skipped for testing purposes \n')
                # print(f'*** {expiry.full_name} is deleted from where? \n')


if __name__ == "__main__":
    main()

# fix:
# 7 days ?
# needless connections
# set date without time?
# mail sending on aws
# delete user on aws
# forbedring: oop based yapilabilir... klasslara donusturulebilir..
