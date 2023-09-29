import pymysql
from datetime import datetime, timedelta, date

# Replace these values with your MySQL server configuration
host = "localhost"
user = "root"
password = "pass0rd."
database = "moso"

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
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
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
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # Check if the user exists in warned_users
        check_query = "SELECT uuid from warned_users where uuid=%s"
        cursor.execute(check_query, expiry.uuid)
        uuid_in_table = cursor.fetchone()

        # Close the database connection
        conn.close()

    except pymysql.Error as err:
        raise Exception(f'An error during cross_check: {err}')

    # Return True if the user matched, False otherwise
    return uuid_in_table is not None


def check_mail_date(matching_uuid):
    try:
        # Replace 'your_uuid_here' with the UUID you want to check
        # Connect to the MySQL server
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # mail_date older than 7 or not
        check_query = '''
               SELECT CASE 
               WHEN MAX(mail_date) 
               <= DATE_ADD(CURDATE(), INTERVAL -7 DAY) 
               THEN 'TRUE' 
               ELSE 'FALSE' 
               END AS is_mail_date_older_than_7_days
               FROM warned_users
               WHERE uuid = %s;
               '''

        cursor.execute(check_query, matching_uuid)
        mail_date_older = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Return True if the mailing date is older than 7 days,
        # False otherwise
        return mail_date_older is not None

    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')


def insert_mail_mark_date(matched_object):
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # Expiry does not exist in warned_users, so save it as a new row
        insertion_query = '''
        INSERT INTO warned_users 
        (uuid, full_name, last_login, email ) 
        VALUES (%s,%s,%s,%s)
        '''

        inserted = cursor.execute(insertion_query,
                                  (matched_object.uuid,
                                   matched_object.full_name,
                                   matched_object.last_login,
                                   matched_object.email))
        print(f'inserted one: {inserted}')

        # mail_the_inserted = inserted
        print(f'will be mailed to: {inserted}')

        # got_mark_and_date = mail_inserted
        mark_and_date_query = """
            UPDATE warned_users
            SET isMailed = True, mail_date = NOW()
            WHERE uuid=%s;
            """

        mark_and_date = cursor.execute(mark_and_date_query, matched_object.uuid)
        print(f'marked and dated one: {mark_and_date}')

        # Commit changes and close the database connection
        conn.commit()
        conn.close()

    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')


def delete_user_from_aws_and_warned(older_mail):
    # Replace 'your_uuid_here' with the UUID you want to use for deletion
    uuid_to_delete = older_mail.uuid

    # Establish a connection to the MySQL server
    connection = pymysql.connect(host=host, user=user, password=password, database=database)

    try:
        # Create a new cursor to interact with the database
        cursor = connection.cursor()

        # Define the SQL query to delete the row with the specified UUID
        sql_query = f"DELETE FROM warned_users WHERE uuid = '{uuid_to_delete}'"

        # Execute the SQL query to delete the row
        cursor.execute(sql_query)

        # Commit the changes to the database
        connection.commit()

        # Check if any rows were affected by the delete operation
        if cursor.rowcount > 0:
            print(f"Row with UUID {uuid_to_delete} deleted successfully.")

            # got_mark_and_date = mail_inserted
            mark_and_date_query = """
                        UPDATE warned_users
                        SET isDeleted = True, delete_date = NOW()
                        WHERE uuid=%s;
                        """

            # set deletion date
            cursor.execute(mark_and_date_query, uuid_to_delete)
            print(f'delete_date is set to {date.today()}')

        else:
            print(f"No rows found with UUID {uuid_to_delete} for deletion.")
        print('user should be deleted from aws servers as well !')

    finally:
        # Close the cursor and the database connection
        cursor.close()
        connection.close()
    print(f'user {object} will be deleted form aws and local, later.. so pass now ')


def main():
    # get tuple of last logger in 11 months
    fetch_results = fetch()
    print(fetch_results)

    # iterate results from db
    for result in fetch_results:

        # convert query results to objects
        expiry = convert(result)
        print(f'{expiry.full_name} is an object now')

        # check object uuid in warned table
        in_table_uuid = check_uuid_in_table(expiry)
        print(f'{expiry.full_name} in_table_uuid? {in_table_uuid}')

        # if uuid is in warned_user table
        if in_table_uuid is False or None:

            # insert row, mail it, and note the mail date object to table
            insert_mail_mark_date(expiry)

        elif in_table_uuid is not False or None:

            # check if it is mailed 7 days ago
            seven_days_older = check_mail_date(expiry.uuid)
            print(f'mail_date older than 7 days?????? {seven_days_older}')

            # we conclude that:
            # the user is syk-passive og mailed more than 7 days ago
            if seven_days_older:
                # then delete user from both aws and warned table
                # delete_user_from_aws_and_warned(expiry)
                print('deleted.. but has an issue to calculate 7 days')


if __name__ == "__main__":
    main()

# fix:
# 7 days ?
# needless connections
# set date witout time?
# mail sending on aws
# delete user on aws