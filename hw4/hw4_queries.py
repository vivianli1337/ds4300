import pandas as pd
import mysql.connector
import getpass

# Ask user for sensitive credentials for database configuration
username = input("Enter your username: ")
password = getpass.getpass("Enter your password: ")
database = input("Enter your graph database: ")

# Store credentials
db_config = {
    'host': 'localhost',
    'user': username,
    'password': password,
    'database': database
}

conn = mysql.connector.connect(**db_config)

cursor = conn.cursor()


def sql_q(query):
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    conn.commit()

def main():
    total_prices = """SELECT SUM(COALESCE(num_value, 0)) AS total_book_prices 
            FROM node_props
            WHERE propkey = 'price';"""
    sql_q(total_prices)

    acquaintance =  """SELECT np1.string_value AS person1, np2.string_value AS person2
        FROM edge e1
        JOIN edge e2 ON e1.out_node = e2.in_node AND e1.in_node = e2.out_node
        JOIN node_props np1 ON e1.out_node = np1.node_id
        JOIN node_props np2 ON e1.in_node = np2.node_id
        WHERE e1.type = 'knows' AND e2.type = 'knows' AND np1.node_id < np2.node_id;"""
    sql_q(acquaintance)

    s_book = """SELECT np_title.string_value AS title, np_price.num_value AS price
        FROM edge AS e
        JOIN node_props AS np_title ON e.out_node = np_title.node_id
        JOIN node_props AS np_price ON e.out_node = np_price.node_id
        WHERE e.type = 'bought'
        AND e.in_node = 2
        AND np_title.propkey = 'title'
        AND np_price.propkey = 'price';"""
    
    sql_q(s_book)

    know = """SELECT np1.string_value AS person1, np2.string_value AS person2
FROM edge e1
JOIN edge e2 ON e1.out_node = e2.in_node AND e1.in_node = e2.out_node
JOIN node_props np1 ON e1.out_node = np1.node_id
JOIN node_props np2 ON e1.in_node = np2.node_id
WHERE e1.type = 'knows' AND e2.type = 'knows' AND np1.node_id < np2.node_id;"""

    conn.close()

if __name__ == "__main__":
    main()  

