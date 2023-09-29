import pymysql
from datetime import datetime, timedelta

# Replace these values with your MySQL server configuration
host = "localhost"
user = "root"
password = "pass0rd."
database = "moso"


# Define a class to represent an Expiring_User object
class ExpiringUser:
    def __init__(self, uuid, full_name, last_login, email):
        self.uuid = uuid
        self.full_name = full_name
        self.last_login = last_login
        self.email = email

# def connect_db():
#
#     # Connect to the MySQL server
#     conn = pymysql.connect(host=host, user=user, password=password, database=database)
#     cursor = conn.cursor()
#     return conn, cursor
#
#
# def disconnect_db(conn, cursor):
#     # close connection to database
#     cursor.close()
#     conn.close()

def fetch():
    # global results
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

        # Fetch all the rows that meet the condition
        results = cursor.fetchall()
        # close connection to database
        cursor.close()
        conn.close()
    # see if there is any error
    except pymysql.Error as e:
        print(f"An error getting_expiry_users: {e}")
    return results


def converted1(results):
    # global objects
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()
        # Convert the results into Expiring_User objects
        objects = []
        if results is not None:
            for row in results:
                uuid, full_name, last_login, email = row
                expiry = ExpiringUser(uuid, full_name, last_login, email)
                objects.append(expiry)
        # Now, you have a list of Expiring_User objects
        # for expiry in objects:
        #     print(
        #         f"UUID: {expiry.uuid}, Full Name: {expiry.full_name}, "
        #         f"Last Login: {expiry.last_login}, Email: {expiry.email}")

        # print(type(objects))
        # close connection to database
        cursor.close()
        conn.close()
    # see if there is any error
    except pymysql.Error as e:
        print(f"An error getting_expiry_users: {e}")
    return objects

def convert_short(result):
    uuid, full_name, last_login, email = result
    expiry = ExpiringUser(uuid, full_name, last_login, email)
    return expiry

# def match(user_obj, moso_con):
def match(obj):
    # global match
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        # cursor = moso_con.cursor()
        cursor = conn.cursor()

        # Check if the user exists in warned_users
        check_query = "SELECT uuid from warned_users where uuid=%s"
        cursor.execute(check_query, (obj.uuid,))
        match = cursor.fetchone()

        # Close the database connection
        conn.close()

        # Return True if the user is registered, False otherwise
        return match is not None

    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')

    return match


def insert(matching):
    # global inserted
    try:
        # Connect to the MySQL server
        conn = pymysql.connect(host=host, user=user, password=password, database=database)
        cursor = conn.cursor()

        # Expiry does not exist in warned_users, so save it as a new row
        insert_warned_user_query = "INSERT INTO warned_users (uuid, full_name, last_login, email ) VALUES (%s,%s,%s,%s)"
        inserted = cursor.execute(insert_warned_user_query,
                                  (matching.uuid, matching.full_name,
                                   matching.last_login, matching.email))

        # print(inserted)
        # Commit changes and close the database connection
        conn.commit()
        conn.close()
    except pymysql.Error as err:
        print(f'an error during cross_check: {err}')

    # return inserted

def warn_by_email(email):
    print(f'warning email sent to ..... ')
    warned = email
    # be sure that email sent?
    # if email sent med sukses, return true else false
    return True

def set_mail_and_date(warned):
    # Connect to the MySQL server
    conn = pymysql.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    # Construct the SQL query
    sql = """
    UPDATE warned_users
    SET isMailed = True, mail_date = NOW()
    WHERE isMailed IS NULL OR isMailed = False;
    """

    # Execute the SQL query
    cursor.execute(sql)

    # Commit the changes
    conn.commit()

    # Close the cursor and database connection
    cursor.close()
    conn.close()

    return warned


    
def main():
    # get last_logged users in the interval
    _results = fetch()
    for n in _results:
        print(f'fetch result {n}')

    ## convert1
    _objects = converted1(_results)
    for obj in _objects:
        print(f'converted to object: {obj.full_name}')

    ## convert2
    # _objects = converted2 = [convert_test(d) for d in _results]
    # for obj in _objects:
    #     print(f' convert to object : {obj.full_name}')

    ##convert3
    # for result in _results:
    #     expiry_object = convert_short(result)
    #     match(expiry_object)
    #     print(f'uuid {expiry_object.uuid} is already in the table.')

    # # iterate through each user object and check if they are got_uuid

    for obj in _objects:
        # returns uuid or none
        got_uuid = match(obj)
        if got_uuid:
            # ask mail sent 7 days ago
            # returns true or false
            seven_up = get_seven_up(got_uuid)
            if seven_up:
                # then delete usr from both aws and warned table
                delete_user_from_aws_and_warned(got_uuid)
        else:
            # if the user is not got_uuid, insert them
            insert(obj)
            print(f'****** inserted to table: {obj.full_name}')
            succesfull_warning = warn_by_email(email)
                    # take all in one function
                    #     if succesfull_warning:
                    #         set_mail_and_date(succesfull_warning)
                    #     else:
                    # #         retry mail... logic

        print(f'results: {type(_results)}, _objects: {type(_objects)}')


# TODO
# def match(user_obj, moso_con): fix connections in the main
# oppfolging skjer i main, arbeid er i funksjonene
# bruk simplified listing
# loops in main

if __name__ == "__main__":
    main()
