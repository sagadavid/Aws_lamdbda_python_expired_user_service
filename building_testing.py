# import pymysql
# from datetime import datetime, timedelta
#
# # Replace these values with your MySQL server configuration
# host = "localhost"
# user = "root"
# password = "pass0rd."
# database = "moso"
#
# # Define a class to represent an Expiring_User object
# class Expiring_User:
#     def __init__(self, uuid, full_name, last_login, email):
#         self.uuid = uuid
#         self.full_name = full_name
#         self.last_login = last_login
#         self.email = email
#
#
# def main():
#     try:
#         # Connect to the MySQL server
#         conn = pymysql.connect(host=host, user=user, password=password, database=database)
#         cursor = conn.cursor()
#
#         # Define the SQL query to select users with last_login older than 3 months
#         interval_query = '''
#                   SELECT uuid, full_name, last_login, email
#                   FROM users
#                   WHERE last_login < DATE_SUB(NOW(), INTERVAL 11 MONTH);
#                   '''
#
#         # Execute the SQL query
#         cursor.execute(interval_query)
#
#         # Fetch all the rows that meet the condition
#         results = cursor.fetchall()
#         print(f'Result length: {len(results)}')
#
#         # Convert the results into Expiring_User objects
#         expiry_user_objects = []
#         for row in results:
#             uuid, full_name, last_login, email = row
#             expiry_user = Expiring_User(uuid, full_name, last_login, email)
#             expiry_user_objects.append(expiry_user)
#
#         # Now, you have a list of Expiring_User objects
#         for expiry in expiry_user_objects:
#             print(
#                 f"UUID: {expiry.uuid}, Full Name: {expiry.full_name}, "
#                 f"Last Login: {expiry.last_login}, Email: {expiry.email}")
#
#         print(f'type of expiry user objects: {type(expiry_user_objects)}')
#
#         for expiry in expiry_user_objects:
#             check_query = "SELECT uuid from warned_users where uuid=%s"
#             cursor.execute(check_query, (expiry.uuid,))
#             warned_user_fetch = cursor.fetchone()
#             print(f'warned users : {warned_user_fetch}')
#
#             # close conection to database
#         cursor.close()
#         conn.close()
#
#         # see if there is any error
#     except pymysql.Error as e:
#         print(f"An error getting_expiry_users: {e}")
#
#     return expiry_user_objects
#
# # def read_expiry (expiry_objects):
# #     try:
# #         # Connect to the MySQL server
# #         conn = pymysql.connect(host=host, user=user, password=password, database=database)
# #         cursor = conn.cursor()
# #
# #         for expiry in expiry_objects:
# #             # Check if expiry exists in the warned_users table
# #             check_query = "SELECT isMailed,isDeleted, mail_date, delete_date from warned_users where uuid=%s"
# #             cursor.execute(check_query, (expiry.uuid,))
# #             expiry_read = cursor.fetchone()
# #
# #         # Commit changes and close the database connection
# #         conn.commit()
# #         conn.close()
# #
# #         return expiry_read
# #
# #     except pymysql.Error as err:
# #         print(f'an error during cross_check: {err}')
# #
#
#
# # def draft ():
# #     try:
# #         # Connect to the MySQL server
# #         conn = pymysql.connect(host=host, user=user, password=password, database=database)
# #         cursor = conn.cursor()
# #
# #         # Cross-checks between expiry user to warned_user
# #         for expiry in expiry_read:
# #             isMailed, isDeleted, mail_date, delete_date = expiry_read
# #             one_week_ago = datetime.now() - timedelta(days=7)
# #
# #             if isMailed and mail_date < one_week_ago:
# #                 # Delete user from the users table
# #                 delete_user_query = "DELETE FROM users WHERE uuid = %s"
# #                 if cursor.execute(delete_user_query, (expiry.uuid,)):
# #                     print('expiry user deleted')
# #
# #                     # Set isDeleted true in the warned_users table
# #                     update_warned_users_query = "UPDATE warned_users SET isDeleted = 1 WHERE uuid = %s"
# #                     if cursor.execute(update_warned_users_query, (expiry.uuid,)):
# #                         print('isDeleted updated')
# #
# #                 elif not isMailed:
# #                     # Send an email to the user
# #                     # send_email_to_user(expiry.email)
# #                     print('email sent')
# #
# #                     # Set isMailed to true and update mail_date
# #                     update_warned_users_query = "UPDATE warned_users SET isMailed = 1, mail_date = NOW() WHERE uuid = %s"
# #                     if cursor.execute(update_warned_users_query, (expiry.uuid)):
# #                         print('isMailed updated')
# #             else:
# #                 # Expiry does not exist in warned_users, so save it as a new row
# #                 insert_warned_user_query = "INSERT INTO warned_users (uuid, full_name, last_login, email ) VALUES (%s,%s,%s,%s)"
# #                 if cursor.execute(insert_warned_user_query,
# #                                   (expiry.uuid, expiry.full_name, expiry.last_login, expiry.email)):
# #                     print('new record created on warned user')
# #                 # Then, do as in 'If isMailed is false or empty'
# #                 # send_email_to_user(expiry.email)
# #                 print('email sent')
# #
# #         #         # Commit changes and close the database connection
# #         conn.commit()
# #         conn.close()
# #
# #     except pymysql.Error as err:
# #         print(f'an error during cross_check: {err}')
#
#
# def send_email_to_user(email_address):
# Add your email sending logic here
# You can use libraries like smtplib or a third-party service to send emails
# Include the email content as described in your requirements
#
# if expiry_on_warned == None:
#     return True
#     # print('no expiry is in the table of warned_users')
#     # # Expiry does not exist in warned_users, so save it as a new row
#     # insert_warned_user_query = "INSERT INTO warned_users (uuid, full_name, last_login, email ) VALUES (%s,%s,%s,%s)"
#     # if cursor.execute(insert_warned_user_query,
#     #                       (expiry.uuid, expiry.full_name, expiry.last_login, expiry.email)):
#     #         print('new epiry record created on warned_users table')
# else:
#     return False
#     print(f'expirees allready in the table: {expiry_on_warned}')

# if __name__=='__main__':
#     main()
#
#
#
