import mysql.connector
from mysql.connector import errorcode

# Configuration for connecting to MySQL
config = {
    'user': 'root',             # replace with your MySQL username
    'password': '',    # replace with your MySQL password
    'host': 'localhost',           # or the IP address of your MySQL server
    'database': 'sanjay'       # name of the database
}

def create_table(cursor):
    # SQL command to create the table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS customer (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        products VARCHAR(100),  -- Increased to handle more products
        item_price DECIMAL(10, 2)
    )
    """
    # Execute the SQL command
    cursor.execute(create_table_query)
    print("Table 'customer' created successfully")

def add_customer(cursor, name, products, item_price):
    # SQL command to insert the data
    insert_data_query = """
    INSERT INTO customer (name, products, item_price)
    VALUES (%s, %s, %s)
    """
    # Execute the SQL command
    cursor.execute(insert_data_query, (name, products, item_price))
    print("Data inserted successfully")

def display_customer_details(cursor, customer_name):
    # Retrieve and display the data for a specific customer
    select_query = "SELECT name, products, item_price FROM customer WHERE name = %s"
    cursor.execute(select_query, (customer_name,))
    
    total_price = 0
    print(f"\nCustomer '{customer_name}' Purchase Details:")
    for (name, products, item_price) in cursor:
        print(f"Products: {products}, Price: {item_price}")
        total_price += item_price
    print(f"Total Purchase Price: {total_price}\n")
    
    # Fetch all remaining results to avoid 'Unread result found' error
    cursor.fetchall()

def get_customer_details(cursor, customer_name):
    # Fetch customer details for validation or additional processing
    select_query = "SELECT name FROM customer WHERE name = %s"
    cursor.execute(select_query, (customer_name,))
    
    # Fetch all remaining results to avoid 'Unread result found' error
    result = cursor.fetchone()
    cursor.fetchall()
    
    return result

try:
    # Connect to the MySQL server
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("Successfully connected to the database")

    # Create table if not exists
    create_table(cursor)

    while True:
        # Ask user for options
        print("Choose an option:")
        print("1. Add customer details")
        print("2. Display customer details")
        print("3. Exit")
        option = int(input("Enter your choice (1, 2, 3): "))
        
        if option == 1:
            # Ask for customer details
            name = input("Enter customer name: ")
            products = input("Enter products: ")
            item_price = float(input("Enter item price: "))
            
            # Add customer details to the database
            add_customer(cursor, name, products, item_price)
            cnx.commit()
        
        elif option == 2:
            # Display customer details
            customer_name = input("Enter customer name to display details: ")
            if get_customer_details(cursor, customer_name):
                display_customer_details(cursor, customer_name)
            else:
                print(f"No customer found with name '{customer_name}'")
        
        elif option == 3:
            # Exit the program
            print("Exiting the program.")
            break
        
        else:
            print("Invalid option. Please try again.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
finally:
    # Close the cursor and connection
    if 'cursor' in locals():
        cursor.close()
    if 'cnx' in locals():
        cnx.close()
