from peewee import *
import csv
import datetime
import os

db = SqliteDatabase('inventory.db')

class Product(Model):
    product_id = IntegerField(primary_key=True, unique=True)
    product_name = TextField(unique=True)
    product_quantity = IntegerField()
    product_price = IntegerField()
    date_updated = DateTimeField()

    class Meta:
        database = db
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def csv_products():
    with open('inventory.csv', newline='') as inventory_file:
        inventory_data = csv.DictReader(inventory_file, delimiter=',')
        rows = list(inventory_data)
        product_list = []
        for row in rows:
            money = row['product_price'].replace('.', '')
            money = money.replace('$', '')
            dic = {
            'product_name': row['product_name'],
            'product_quantity': row['product_quantity'],
            'product_price': money,
            'date_updated': row['date_updated']}
            product_list.append(dic)
        return product_list

def add_list_database(list):
    for product in list:
        try:
            Product.create(
            product_name=product['product_name'],
            product_quantity=product['product_quantity'],
            product_price=product['product_price'],
            date_updated=product['date_updated'])
        except:
            old_date = Product.select().where(Product.product_name == product['product_name']).get()
            if old_date.date_updated >= product['date_updated']:
                pass
            else:
                Product.update(
                product_quantity=product['product_quantity'],
                product_price=product['product_price'],
                date_updated=product['date_updated']
                ).where(Product.product_name == product['product_name']).execute()

def menu():
    while True:
        print('\n\nv) Use ID to search for a product')
        print('a) Add a NEW product to the database')
        print('b) Make a backup of the database')
        print('q) Quit')
        while True:
            choice = input('Action [V/A/B/Q]: ').lower()
            if choice not in 'vabq' or len(choice) != 1:
                print('Please input a single letter corresponding to the option you like.')
                continue
            break
        if choice == 'v':
            clear()
            view_products()
        elif choice == 'a':
            clear()
            new_product()
        elif choice == 'b':
            backup()
        else:
            break

def view_products():
    while True:
        search_query = input("Whats the Pruduct's ID: ")
        try:
            search_query = int(search_query)
        except:
            print('\nPlease enter only a numeric value for the id.\n')
            continue
        if search_query > len(Product.select()) or search_query < 1:
            print('\nThat product id doesnt exit. There are {} existing IDs.\n'.format(len(Product.select())))
            continue
        searched_product = Product.select().where(Product.product_id == (search_query)).get()
        coin = str(searched_product.product_price)
        point = len(coin) - 2
        cash ='$' + coin[0:point] + '.' + coin[point:]
        clear()
        print('Product ID:{},  {},  Qty:{},  {},  {}'.format(
        searched_product.product_id,
        searched_product.product_name,
        searched_product.product_quantity,
        cash,
        searched_product.date_updated))
        break

def new_product():
    name = input('Enter the name of the product: ')
    while True:
        quantity = input('Enter the quantity of the product: ')
        try:
            int(quantity)
            break
        except:
            print('\nPlease only enter a numeric value.\n')
    while True:
        price = input('Enter the price of the product: ')
        try:
            int(price)
            break
        except:
            print('\nPlease only enter a numeric value.\n')
    money = price.replace('.', '')
    money = money.replace('$', '')
    try:
        Product.create(
        product_name=name,
        product_quantity=quantity,
        product_price=money,
        date_updated=datetime.datetime.now().strftime('%m/%d/%Y'))
        clear()
        print('New Product added')
    except:
        old_date = Product.select().where(Product.product_name == name).get()
        new  = datetime.datetime.now().strftime('%m/%d/%Y')
        if old_date.date_updated > new:
            clear()
            print("Sorry a more recent entry of that product was found.")
        else:
            Product.update(
            product_quantity=quantity,
            product_price=money,
            date_updated=datetime.datetime.now().strftime('%m/%d/%Y')
            ).where(Product.product_name == name).execute()
            clear()
            print('Updated old entry')

def backup():
    if os.path.isfile('./backup.csv'):
        clear()
        while True:
            ans = input('A backup already exits. Would you like to overwrite it? [Y/N] ').lower()
            if ans == 'y' or ans == 'n':
                break
            else:
                print('\nPlease enter "y" or "n"\n')
        if ans == 'y':
            with open('backup.csv', 'w') as csv_backup:
                fieldnames = ['product_id', 'product_name', 'product_price', 'product_quantity', 'date_updated']
                Backup = csv.DictWriter(csv_backup, fieldnames=fieldnames)
                Backup.writeheader()
                products = Product.select().order_by(Product.product_id)
                for entry in products:
                    coin = str(entry.product_price)
                    point = len(coin) - 2
                    cash ='$' + coin[0:point] + '.' + coin[point:]
                    Backup.writerow({
                    'product_id': entry.product_id,
                    'product_name': entry.product_name,
                    'product_price': cash,
                    'product_quantity': entry.product_quantity,
                    'date_updated': entry.date_updated})
            clear()
            print('Backup Successful!')
        if ans == 'n':
            clear()
            print('Backup aborted')


if __name__ == '__main__':
    db.connect()
    db.create_tables([Product], safe=True)
    add_list_database(csv_products())
    clear()
    menu()
    db.close()
