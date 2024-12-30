import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import uuid

@anvil.server.callable
def add_customer(customer_data):
  if customer_data.get('name') and customer_data.get('post_code') and customer_data.get('phone') and customer_data.get('email') and customer_data.get('address'):
    print("Received customer data:", customer_data)
    app_tables.customers.add_row(**customer_data)
  else:
    print("missing")
@anvil.server.callable
# db customer jo ki argument hai, takes customer list as customer_data.it is rep as json file
# server me update fn(it connects directly to db)
def update_customer(customer, customer_data):
  # customer_data = {} items from CustomerEdit are appended into it
  if customer_data['name'] and customer_data['post_code'] and customer_data['phone'] and customer_data['phone'] and customer_data['address']:
    customer.update(**customer_data)
@anvil.server.callable
def delete_customer(customer):
    customer.delete()

##############################SALES DETAILS MODULE
@anvil.server.callable
def add_sales(sales_data):
  today = datetime.now().date()
  sales_data['date'] = today
  order_id = str(uuid.uuid4())  # Generates a unique string like 'c9b1b3d8-8f93-45ea-a8f7-8e1f6b1d333f'
  sales_data['order_id'] = order_id
  if sales_data.get('type') and sales_data.get('products_sold') and sales_data.get('order_value') and sales_data.get('discount') and sales_data.get('commission') or sales_data.get('notes'):
    print("Received customer data:", sales_data)
    new_sale = app_tables.sales.add_row(**sales_data)
    order_data = {
            'order_id': order_id,
            'order_value': sales_data['order_value'],
            'status': 'Order Placed',  # Default status for new orders
            'deposit_amount': 0,  # Default deposit amount
            'installation_status': 'Pending',  # Default installation status
            'final_amount': 0,  # Default final amount received
            'outstanding_balance': 0
        }
        # Add row to orders table
    app_tables.orders.add_row(**order_data)
  else:
    print("missing")
  return new_sale
@anvil.server.callable
# db customer jo ki argument hai, takes customer list as customer_data.it is rep as json file
# server me update fn(it connects directly to db)
def update_sale(sale, sale_data):
  # customer_data = {} items from CustomerEdit are appended into it
  print(sale)
  print(sale_data)
  if sale_data['type'] and sale_data['products_sold'] and sale_data['order_value'] and sale_data['discount'] and sale_data['commission'] or sale_data['notes']:
    sale.update(**sale_data)

@anvil.server.callable
def delete_sale(sale):
  sale.delete()

#########################Order Details module
@anvil.server.callable
def add_order(order_data):
  order_data['order_id'] = '123abc'
  if order_data.get('status') and order_data.get('installation_status') and and order_data.get('depposit_amount') and order_data.get('final_amount'):
    app_tables.orders.add_row(**order_data)
  else:
    print("Missing Field")
  
