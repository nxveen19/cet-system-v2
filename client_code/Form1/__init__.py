from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CustomerEdit import CustomerEdit
from ..SalesForm import SalesForm
from ..SalesEdit import SalesEdit
from ..OrdersEdit import OrdersEdit


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.customer_grid.items = app_tables.customers.search()
    self.sales_grid.items = app_tables.sales.search()
    self.customer_grid.add_event_handler('x-edit-customer', self.edit_customer)
    self.customer_grid.add_event_handler('x-delete-customer', self.delete_customer)

    self.sales_grid.add_event_handler('x-edit-sale', self.edit_sale)
    self.sales_grid.add_event_handler('x-delete-sale', self.delete_sale)
    self.refresh_sales_grid()

    self.orders_grid.add_event_handler('x-edit-order', self.edit_order)

  def add_customer_info_click(self, **event_args):
    item = {}
    editing_form = CustomerEdit(item=item)
    if alert(content=editing_form, large=True): # matlab kab OK button jabaunga
    #add the movie to the Data Table with the filled in information
      print("Item data:", item)
      # print("hello world")
      anvil.server.call('add_customer', item) # item is dict{}
    #refresh the Data Grid
      self.customer_grid.items = app_tables.customers.search()
  def edit_customer(self, customer, **event_args):
  #movie is the row from the Data Table
    item = dict(customer)
    editing_form = CustomerEdit(item=item) # item is name,place, email, phone, add

  #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
    #pass in the Data Table row and the updated info
      anvil.server.call('update_customer', customer, item)
    #refresh the Data Grid
      self.customer_grid.items = app_tables.customers.search()
  def delete_customer(self, customer, **event_args):
    if confirm(f"Do you really want to delete the customer row {customer['name']}?"):
      anvil.server.call('delete_customer', customer)
    #refresh the Data Grid
      self.customer_grid.items = app_tables.customers.search()

########## Sales Details : date, type, products, order value, discount, commission, notes

  def add_sales_details_click(self, **event_args):
    item = {}
    editing_form = SalesEdit(item=item)
    if alert(content=editing_form, large=True): # matlab jab OK button jabaunga
    #add the movie to the Data Table with the filled in information
      print("Item data:", item)
      # print("hello world")
      new_sale = anvil.server.call('add_sales', item) # item is dict{} and new_sale is row in db
      self.calculate_and_update_commission(new_sale)
      
    #refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()
      
  def edit_sale(self, sale, **event_args):
  #movie is the row from the Data Table
    item = dict(sale)
    editing_form = SalesEdit(item=item) # item is name,place, email, phone, add

  #if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
    #pass in the Data Table row and the updated info
      anvil.server.call('update_sale', sale, item)
      
    #refresh the Data Grid
      self.calculate_and_update_commission(sale)
      self.sales_grid.items = app_tables.sales.search()
  def delete_sale(self, sale, **event_args):
    if confirm(f"Do you really want to delete the customer row {sale['type']}?"):
      anvil.server.call('delete_sale', sale)
      self.refresh_sales_grid()
      print(sale)
    #refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()

  def calculate_and_update_commission(self, sale):
        # Calculate commission for the given sale row
        item = dict(sale)
        commission_percentage = item['commission']

        if commission_percentage > 0:
            commission = round((item['order_value'] - item['discount']) * (commission_percentage / 100))
            print(f"Calculated commission: {commission}")
        else:
            commission = 0

        # Update only the 'calculated_commission' for this specific sale
        sale.update(calculated_commission=commission)

        # Optionally update the grid to reflect the new commission
        self.refresh_sales_grid()  # Refresh the grid to show updated commission

  def refresh_sales_grid(self):
        # Refresh only the grid's items based on the updated sales data
    self.sales_grid.items = app_tables.sales.search()
    self.orders_grid.items = app_tables.orders.search()

  #############Order Processing status table#############

  def edit_order(self, order, **event_args):
    item = dict(order)
    editing_form = OrdersEdit(item=item)
    if alert(content=editing_form, large=True):
      print("Item Data:", item)
      anvil.server.call('add_order_details', order, item)
      self.calculate_outstanding_balance(order)

  def calculate_outstanding_balance(self, order):
    item = dict(order)
    deposit_amount = item['deposit_amount']
    if deposit_amount > 0:
      outstanding_balance = item['order_value'] - (item['deposit_amount'] + item['final_amount']) 
      print(f"Calculated outsatanding balance: {outstanding_balance}")
    else:
      outstanding_balance = 0
        # Update only the 'calculated_commission' for this specific sale
    order.update(outstanding_balance=outstanding_balance)
    self.orders_grid.items = app_tables.orders.search()
    #self.refresh_sales_grid()  # Refresh the grid to show updated commission

  def go_to_sales_click(self, **event_args):
     open_form(SalesForm())  # Navigate to the SalesForm
    
    


    
    



 
