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
