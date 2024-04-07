import mysql.connector
import pickle
import sys
import datetime 

# Establishing the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="haris",
    database="used_cars_db"
)

# Creating a cursor to interact with the database
cursor = db.cursor()


# Creating the car table (execute this only once)
create_table_query = """
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    make VARCHAR(255),
    model VARCHAR(255),
    year INT,
    price DECIMAL(10, 2)
)
"""
cursor.execute(create_table_query)
db.commit()


d={}
def signup():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    user_data = load_user_data()
    
    if username in user_data:
        print("Username already exists. Please choose a different username.")
        signup()
    else:
        user_data[username] = password
        save_user_data(user_data)
        print("Signed up successfully.")

def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    user_data = load_user_data()
    
    if username in user_data and user_data[username] == password:
        print("Login successful. Welcome, " + username + "!")
    else:
        print("Wrong username or password. Please exit and try again.")
        sys.exit()

def load_user_data():
    try:
        with open("user_data.pkl", "rb") as file:
            return pickle.load(file)
    except (FileNotFoundError, EOFError):
        return {}
def save_user_data(user_data):
    with open("user_data.pkl", "wb") as file:
        pickle.dump(user_data, file)



    

def seller_interface():
    sch=int(input("Sell a new car or delete a existing lisiting? 1 for Selling and 2 for deleting and 3 for editing"))
    if sch==1:
        
        
        print("Seller Interface")
        make = input("Enter car make: ")
        model = input("Enter car model: ")
        year = int(input("Enter car year: "))
        price = float(input("Enter car price: "))

    # Inserting car details into the database
        insert_query = "INSERT INTO cars (make, model, year, price) VALUES (%s, %s, %s, %s)"
        values = (make, model, year, price)
        cursor.execute(insert_query, values)

    #Getting contact information of the seller
        sname=input("Enter your name; ")
        ph=int(input("Enter your contact number"))
        insert_query = "INSERT INTO sellers (sname,ph) VALUES (%s, %s, %s, %s)"       
    
 
    
        db.commit()

    

        print("Car details added successfully!")
    elif sch==2:
        delete_car_listing()
    elif sch==3:
        edit_car_listing()

def buyer_interface():
    print("Buyer Interface")
    
    # Fetching and displaying car details from the database
    fetch_query = "SELECT id, make, model, year, price FROM cars"
    cursor.execute(fetch_query)
    cars = cursor.fetchall()
    
    print("Available Cars:")
    if cars:
        print("{:<5} {:<10} {:<10} {:<10} {:<10}".format("ID", "Make", "Model", "Year", "Price"))
        for car in cars:
            print("{:<5} {:<10} {:<10} {:<10} {:<10}".format(car[0], car[1], car[2], car[3], car[4]))
    else:
        print("No cars available.")
    
    qw = int(input("Enter 1 to access filters or 2 to continue: "))
    if qw == 1:
        sort_car_listings()
    # Option to buy a car
    buy_car_choice = int(input("Enter 1 to buy a car or 2 to continue: "))
    if buy_car_choice == 1:
    # Get the car ID from the user
        car_id = int(input("Enter the ID of the car you want to buy: "))

    # Get the buyer details
        buyer_name = input("Enter your name: ")
        buyer_email = input("Enter your email address: ")
        buyer_phone = input("Enter your phone number: ")
        

    # Calculate the road tax
        road_tax_percent = 10  # This can be varied depending on the state in India
        selected_car = None

    # Find the selected car by its ID
        for car in cars:
            if car[0] == car_id:
                selected_car = car
                break

        if selected_car:
            road_tax = selected_car[4] * road_tax_percent / 100
            

            

    # Calculate the total price
            total_price = selected_car[4] + road_tax
            current_datetime = datetime.datetime.now()

    # Print the final bill
            print("\n" + "=" * 50)
            print("{:^50}".format("Final Bill"))
            print("=" * 50)
            print("{:<20} {:<30}".format("Car details:", f"{selected_car[1]} {selected_car[2]} ({selected_car[3]})"))
            print("{:<20} {:<30}".format("Car price:", f"Rs{selected_car[4]:,.2f}"))
            print("{:<20} {:<30}".format("Road tax:", f"Rs{road_tax:,.2f}"))
            print("\n" + "=" * 50)
            print("{:^50}".format("Final Bill"))
            print("=" * 50)
            print("{:<20} {:<30}".format("Total price:", f"Rs{total_price:,.2f}"))
            print("=" * 50)
            print("{:<20} {:<30}".format("Buyer details:", ""))
            print("{:<20} {:<30}".format("Name:", buyer_name))
            print("{:<20} {:<30}".format("Email:", buyer_email))
            print("{:<20} {:<30}".format("Phone number:", buyer_phone))
            print("{:<20} {:<30}".format("Purchase Date and Time:", current_datetime))
            print(current_datetime)
            
            
            print("=" * 50 + "\n")
            
            sys.exit()

            
            
        else:
            print("Invalid car ID. Purchase canceled.")


  
       
        
    
def search_by_year_range():
    print("Search Cars by Year Range")
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    
    # Fetch and display cars within the specified year range
    fetch_query = "SELECT id, make, model, year, price FROM cars WHERE year BETWEEN %s AND %s"
    cursor.execute(fetch_query, (start_year, end_year))
    cars = cursor.fetchall()
    
    if cars:
        print("Cars within the specified year range:")
        for car in cars:
            print(f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Price: {car[4]}")
    else:
        print("No cars found within the specified year range.")

    
def search_by_price_range():
    print("Search Cars by Price Range")
    min_price = float(input("Enter the minimum price: "))
    max_price = float(input("Enter the maximum price: "))
    
    # Fetch and display cars within the specified price range
    fetch_query = "SELECT id, make, model, year, price FROM cars WHERE price BETWEEN %s AND %s"
    cursor.execute(fetch_query, (min_price, max_price))
    cars = cursor.fetchall()
    
    if cars:
        print("Cars within the specified price range:")
        for car in cars:
            print(f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Price: {car[4]}")
    else:
        print("No cars found within the specified price range.")
def sort_car_listings():
    print("Sort Car Listings")
    print("1. Sort by Price (Low to High)")
    print("2. Sort by Price (High to Low)")
    print("3. Sort by Year (Old to New)")
    print("4. Sort by Year (New to Old)")
    
    sort_option = int(input("Enter your sorting choice: "))
    
    if sort_option == 1:
        fetch_query = "SELECT id, make, model, year, price FROM cars ORDER BY price ASC"
    elif sort_option == 2:
        fetch_query = "SELECT id, make, model, year, price FROM cars ORDER BY price DESC"
    elif sort_option == 3:
        fetch_query = "SELECT id, make, model, year, price FROM cars ORDER BY year ASC"
    elif sort_option == 4:
        fetch_query = "SELECT id, make, model, year, price FROM cars ORDER BY year DESC"
    else:
        print("Invalid sorting choice.")
        return
    
    cursor.execute(fetch_query)
    cars = cursor.fetchall()
    
    if cars:
        print("Sorted Car Listings:")
        for car in cars:
            print(f"ID: {car[0]}, Make: {car[1]}, Model: {car[2]}, Year: {car[3]}, Price: {car[4]}")
    else:
        print("No cars found.")

def delete_car_listing():
    print("Delete Car Listing")
    car_id = int(input("Enter the ID of the car you want to delete: "))
    
    # Delete the car listing by ID
    delete_query = "DELETE FROM cars WHERE id = %s"
    cursor.execute(delete_query, (car_id,))
    db.commit()
    
    if cursor.rowcount > 0:
        print("Car listing deleted successfully.")
    else:
        print("Car not found with the provided ID.")


def edit_car_listing():
    print("Edit Car Listing")
    car_id = int(input("Enter the ID of the car you want to edit: "))

    # Fetch the car details for the provided ID
    fetch_query = "SELECT id, make, model, year, price FROM cars WHERE id = %s"
    cursor.execute(fetch_query, (car_id,))
    car = cursor.fetchone()

    if car:
        print("Current Car Details:")
        print("{:<5} {:<10} {:<10} {:<10} {:<10}".format("ID", "Make", "Model", "Year", "Price"))
        print("{:<5} {:<10} {:<10} {:<10} {:<10}".format(car[0], car[1], car[2], car[3], car[4]))

        # Get the new details from the user
        make = input("Enter new car make (press Enter to keep current value): ") or car[1]
        model = input("Enter new car model (press Enter to keep current value): ") or car[2]
        year = int(input("Enter new car year (press Enter to keep current value): ") or car[3])
        price = float(input("Enter new car price (press Enter to keep current value): ") or car[4])

        # Update the car details in the database
        update_query = "UPDATE cars SET make = %s, model = %s, year = %s, price = %s WHERE id = %s"
        update_values = (make, model, year, price, car_id)
        cursor.execute(update_query, update_values)
        db.commit()

        print("Car listing updated successfully!")

    else:
        print("Car not found with the provided ID.")






# Main program loop
while True:
    print("*" * 70)
    print("*{:^68}*".format("Welcome to Cars24 Kochi"))
    print("*" * 70)
    print("Please select an option to proceed:")
    print("\nMenu:")
    print("1. Buyer Interface")
    print("2. Seller Interface")
    print("3. Exit")
    
    choice = int(input("Enter your choice 1,2 or 3: "))
    
    if choice == 1:
        uch=input("Press 1 for Sign up and press 2 for login")
        
            
            
        
        if uch=='1':
            
            
                
                
            signup()
            buyer_interface()
                
            ych=int(input("Press 1 if you want to search cars based on year range and 2 to continue"))
            if ych==1:
                
                search_by_year_range()
            elif ych==2:
                
                zch=input("Do you want to search cars based on price range? (Yes/No): ")
                if zch.lower() in ["yes", "y"]:
                    
                    search_by_price_range()
                elif zch.lower() in ["no", "n"]:
                    break
                        
                        
                
                       
                        
                
                
                
                
        elif uch=='2':
            login()
            buyer_interface()
            ych=int(input("Press 1 if you want to search cars based on year range and 2 to continue"))
            if ych==1:
                search_by_year_range()
                
                        
                 
                 
        buyer_interface()
    elif choice == 2:
        
        uch=input("Press 1 for Sign up and press 2 for login")
        
            
            
        
        if uch=='1':
            
            signup()
            seller_interface()
            
            
                
                
                
                
                
                
        elif uch=='2':
            login()
        
            seller_interface()
    elif choice == 3:
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please select a valid option.")

# Closing the database connection
db.close()


