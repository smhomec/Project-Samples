
#========The beginning of the class==========
class Shoe:
    '''
    This class will be used to represent a shoe.
    '''
    def __init__(self, country, code, product, cost, quantity):
        # Initialise the country, code, product, cost and quantity attributes.
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
    
    def get_cost(self):
        '''
        Return the cost of the shoe.
        '''
        print(self.cost)

    def get_quantity(self):
        '''
        Return the quantity of the shoes.
        '''
        print(self.quantity)

    def __str__(self):
        # Return a string representation of a class.
        return f"{self.country},{self.code},{self.product},{self.cost},{self.quantity}"

#=============Shoe list===========
# The list will be used to store a list of objects of shoes.
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list.
    '''
    try:
        with open("inventory.txt", "r", encoding="utf-8") as f:
            for line in f.readlines()[1:]:
                country, code, product, cost, quantity = line.strip().split(",")
                shoe = Shoe(country, code, product, float(cost), int(quantity))
                shoe_list.append(shoe)
            # Create a shoes object from this data
            # Append the shoes object into the shoe list
        print("Data loaded successfully.")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    # Remove the overly broad exception handler to avoid masking unexpected errors.
    except OSError as e:
        print(f"File error: {e}")

def capture_shoes():
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''
    # Allow a user to capture data about a shoe
    country = input("Enter the country: ").strip()
    code = input("Enter the shoe code: ").strip()
    product = input("Enter the product name: ").strip()
    # Create a shoe object and append this object inside the shoe list
    try:
        cost = float(input("Enter the cost: ").strip())
        quantity = int(input("Enter the quantity: ").strip())
        if cost < 0 or quantity < 0:
            print("Cost and quantity must be non-negative.")
            return
        shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(shoe)
        print(f"Shoe added: {shoe}")
        # Optionally, write the new shoe to the inventory file
        with open("inventory.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{country},{code},{product},{cost},{quantity}")
        print("Inventory updated successfully.")
    except ValueError:
        print("Invalid input. Please enter valid numbers for cost and quantity.")

def view_all():
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function.
    '''
    # Iterate over shoes list and print the details of the shoes returned from the _str_ function
    for shoe in shoe_list:
        print(shoe)

def re_stock():
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''
    # Find the shoe object with the lowest quantity
    if not shoe_list:
        print("Shoe list is empty.")
        return
    lowest_quantity_shoe = min(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"Shoe with the lowest quantity: {lowest_quantity_shoe}")
    # Ask the user if they want to add this quantity of shoes and then update it
    print(input("Do you want to add more stock for this shoe? (yes/no): ").strip().lower())
    try:
        add_quantity = int(input("Enter the quantity to add: "))
        if add_quantity < 0:
            print("Quantity cannot be negative.")
            return
        lowest_quantity_shoe.quantity += add_quantity
        print(f"Updated shoe: {lowest_quantity_shoe}")
        # Update the file for this shoe
        with open("inventory.txt", "w", encoding="utf-8") as f:
            f.write("Country,Code,Product,Cost,Quantity\n")
            for shoe in shoe_list:
                f.write(f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n")
        print("Inventory updated successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except OSError as e:
        print(f"File error: {e}")

def search_shoe():
    '''
     This function will search for a shoe from the list
     using the shoe code and return this object so that it will be printed.
    '''
    # Search for a shoe from the list using the shoe code
    search_code = input("Enter the shoe code to search: ").strip()
    # Return this object so that it will be printed
    for shoe in shoe_list:
        if shoe.code == search_code:
            print(shoe)
            return

def value_per_item():
    '''
    This function will calculate the total value for each item and
    then print this information on the console for all the shoes.
    '''
    # Calculate the total value for each item and print this information 
    # on the console for all the shoes
    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        print(f"Total value for {shoe.product} (Code: {shoe.code}): ${value:.2f}")

def highest_qty():
    '''
    This function will determine the product with the highest quantity
    and print this shoe as being for sale.
    '''
    # Determine the product with the highest quantity and print this shoe as being for sale
    if not shoe_list:
        print("Shoe list is empty.")
        return
    highest_quantity_shoe = max(shoe_list, key=lambda shoe: shoe.quantity)
    print(f"Shoe with the highest quantity (for sale): {highest_quantity_shoe}")


#==========Main Menu=============
# Create a menu that executes each function above
def main():
    # Read the data from the file inventory.txt
    read_shoes_data()
    while True:
        print("\nShoe Inventory Management System")
        print("1. View All Shoes")
        print("2. Capture New Shoe")
        print("3. Re-stock Shoe")
        print("4. Search Shoe")
        print("5. Calculate Value per Item")
        print("6. Show Highest Quantity Shoe")
        print("7. Exit")
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            view_all()
        elif choice == '2':
            capture_shoes()
        elif choice == '3':
            re_stock()
        elif choice == '4':
            search_shoe()
        elif choice == '5':
            value_per_item()
        elif choice == '6':
            highest_qty()
        elif choice == '7':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()