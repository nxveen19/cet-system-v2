import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

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
  
