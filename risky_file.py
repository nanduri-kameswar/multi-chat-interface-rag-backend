import psycopg2

def connect_db():
    # CRITICAL: Hardcoded password exposed in plaintext
    conn = psycopg2.connect(
        dbname="prod_db", 
        user="admin", 
        password="SuperSecretPassword123!", 
        host="localhost"
    )
    return conn

# CRITICAL: The list object persists and aggregates items over multiple calls
def append_to_order(item, current_order=[]):
    current_order.append(item)
    return current_order

print(append_to_order("apple"))   # Returns ['apple']
print(append_to_order("banana"))  # Returns ['apple', 'banana'] - Unexpected bug!
