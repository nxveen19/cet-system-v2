import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import uuid

@anvil.server.callable
def add_customer(customer_data):
  customer_id = str(uuid.uuid4())  # Generates a unique string like 'c9b1b3d8-8f93-45ea-a8f7-8e1f6b1d333f'
  customer_data['customer_ref_id'] = customer_id
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
    order_id = str(uuid.uuid4())  # Generate a unique order ID
    sales_data['order_id'] = order_id
    # Validate required fields
    required_fields = ['type', 'customer_ref_number', 'customer_ref', 'products_sold', 'order_value', 'discount', 'commission']
    if not all(sales_data.get(field) for field in required_fields):
        raise ValueError("Missing required sales data.")

    # Validate customer reference number length
    customer_ref_number = sales_data['customer_ref_number']
    customer_ref_number_strip = customer_ref_number.strip('-')
    if len(customer_ref_number_strip) <= 12:
      new_sale = app_tables.sales.add_row(**sales_data)
    else:
      print("Customer Reference Number must be 12 characters or fewer.")

    # Add sales row
    print("Received customer data:", sales_data)


    # Prepare and add order row
    order_data = {
        'order_id': order_id,
        'customer_ref': sales_data['customer_ref'],
        'customer_ref_number': customer_ref_number,
        'order_value': sales_data['order_value'],
        'status': 'Order Placed',  # Default status for new orders
        'deposit_amount': 0,  # Default deposit amount
        'installation_status': 'Pending',  # Default installation status
        'final_amount': 0,  # Default final amount received
        'outstanding_balance': 0
    }
    app_tables.orders.add_row(**order_data)

    return new_sale

  
@anvil.server.callable
# db customer jo ki argument hai, takes customer list as customer_data.it is rep as json file
# server me update fn(it connects directly to db)
def update_sale(sale, sale_data):
  # customer_data = {} items from CustomerEdit are appended into it
  # print(sale)
  # print(sale_data)
  sale_data['date'] = datetime.now().date()
  existing_row_in_order = app_tables.orders.get(order_id=sale_data['order_id'])
  if existing_row_in_order:
    existing_row_in_order.update(order_value=sale_data['order_value'])
  if sale_data['type'] and sale_data['customer_ref_number'] and sale_data['customer_ref'] and sale_data['products_sold'] and sale_data['order_value'] and sale_data['discount'] and sale_data['commission']:
    customer_ref_number = sale_data['customer_ref_number'].strip('-')
    if len(customer_ref_number) <= 12:
      sale.update(**sale_data)

@anvil.server.callable
def delete_sale(sale):
  sale.delete()

#########################Order Details module
@anvil.server.callable
def add_order_details(order, order_data):
  if order_data['order_id'] and order_data['status'] and order_data['installation_status'] and order_data['deposit_amount'] and order_data['final_amount']:
    order.update(**order_data)
  else:
    print("Missing Field in adding order")

@anvil.server.callable
def add_commission_details(commission, commission_data):
  commission_data['commission_pending'] = commission_data['due_commission'] - commission_data['commission_received']
  if commission_data['order_id'] and commission_data['due_commission']:
    commission.update(**commission_data)
  else:
    print("Missing field in adding commission")
  
  
