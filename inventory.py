# This program allows the user to choose a few options from a menu to handle the global inventory of shoes.
# It contains a Shoe class, and various functions outside the class that executes upon the user's choice. 


from tabulate import tabulate

#========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):

        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    def __str__(self):
        string = f'''
        Country:    {self.country}
        Code:       {self.code}
        Product:    {self.product}
        Unit Cost:  {self.cost}
        Stock Qty:  {self.quantity}
        '''
        return string
        

#=============Shoe list===========
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():  # this function will be called in the other functions below to ensure that shoe_list contains the latest data.
    try:
        with open('inventory.txt', 'r+') as f:
            count = 0
            for line in f:
                line_list = line.strip("\n").split(",")
                count += 1
                if not line_list[0] == "Country":
                    shoe_list.append(Shoe(line_list[0],line_list[1],line_list[2],line_list[3],line_list[4]))

    except FileNotFoundError:
        print("File not found. Check filename and directory location. Try again.")

    except IndexError:
        print(f"Line {count} of the file does not contain all the necessary stock information. Amend and try again.")

    return shoe_list
    
def capture_shoes():

    country = input("Country: ").strip().capitalize()
    code = input("Code: ").strip().upper()
    product = input("Product: ").strip()
    cost = input("Cost: ").strip()
    quantity = input("Quantity: ").strip()

    new_shoe = Shoe(country, code, product, cost, quantity)
    shoe_list.append(new_shoe)
    
    try:
        with open('inventory.txt', 'a+') as f:
            f.write(f"\n{country},{code},{product},{cost},{quantity}")
            print("New shoe added to shoe list and inventory file.")
    except FileNotFoundError:
        print("File not found. Check filename and directory location. Try again.")

    return

def view_all():

    read_shoes_data()
    table = [[shoe.country, shoe.code, shoe.product, shoe.cost, shoe.quantity] for shoe in shoe_list]
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table, headers))
    return

def re_stock():
    
    read_shoes_data()
    try:
        qty_list = [int(shoe.quantity) for shoe in shoe_list]
        shoe = shoe_list[qty_list.index(min(qty_list))]
        print(f'''
        --- Lowest Quantity ---{shoe.__str__()}
        ''')

        add = input(f"Re-stock {int(shoe.quantity)} units? Y/N ").strip().lower()
        if add == "y":
            new_qty = int(shoe.quantity) * 2
            shoe.quantity = str(new_qty)

            file_text = "Country,Code,Product,Cost,Quantity\n"
            text_list = [f"{shoe.country},{shoe.code},{shoe.product},{shoe.cost},{shoe.quantity}\n" for shoe in shoe_list]
            file_text = file_text + "".join(text_list)

            with open('inventory.txt', 'w+') as f:
                f.write(file_text)
                print("Re-stocked!")

    except ValueError:
        print("At least one shoe quantity is not numerical. Amend and try again.")
    except FileNotFoundError:
        print("File not found. Check filename and directry location. Try again.")

    return

def search_shoe():

    read_shoes_data()
    shoe_code = input("Enter the shoe code: ").strip().upper()
    code_list = [shoe.code for shoe in shoe_list]

    if shoe_code in code_list:
        shoe_print = shoe_list[code_list.index(shoe_code)].__str__()
    else:
        shoe_print = "Shoe code not found."
    
    return print(shoe_print)

def value_per_item():
    
    read_shoes_data()
    table = [[shoe.product, shoe.code, int(shoe.cost) * int(shoe.quantity)] for shoe in shoe_list]
    headers = ["Product", "Code", "Value"]
    print(tabulate(table, headers))
    return

def highest_qty():
    try:
        read_shoes_data()
        qty_list = [int(shoe.quantity) for shoe in shoe_list]

        shoe_print = f'''
        --- SALE ---
        {shoe_list[qty_list.index(max(qty_list))].__str__()}
        '''

    except ValueError:
        print("At least one shoe quantity is not numerical. Amend and try again.")

    return print(shoe_print)

#==========Main Menu=============

choice = ""

while choice != "qq":
    choice = input(f'''
    What would you like to do:
        rd - Read Shoes Data
        cs - Capture New Shoe Data
        va - View All
        rs - Re-stock
        ss - Search for Shoe
        vi - Value per Item
        hq - Highest Quantity
        qq - Quit
    ''').strip().lower()

    if choice == "rd":
        read_shoes_data()
        print("Data read!")
    
    elif choice == "cs":
        capture_shoes()

    elif choice == "va":
        view_all()

    elif choice == "rs":
        re_stock()
    
    elif choice == "ss":
        search_shoe()

    elif choice == "vi":
        value_per_item()

    elif choice == "hq":
        highest_qty()

    elif choice == "qq":
        print("Goodbye!")
        exit()

    else:
        print("Invalid entry. Try again.")


