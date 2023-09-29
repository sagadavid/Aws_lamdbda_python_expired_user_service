import pymysql

def main():
    # Connect to your MySQL database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='pass0rd.',
        database='moso'
    )

    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Define the SQL query to create the table with boolean columns
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS warned_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            uuid VARCHAR(255),
            full_name VARCHAR(255),
            last_login DATETIME,
            email VARCHAR(255),
            isMailed TINYINT(0),
            isDeleted TINYINT(0),
            mail_date DATE,
            delete_date DATE
        )
    '''

    # Execute the query to create the table
    cursor.execute(create_table_query)

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__=="__main__":
    main()