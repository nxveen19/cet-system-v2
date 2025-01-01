from ._anvil_designer import Form1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CustomerEdit import CustomerEdit
from ..SalesEdit import SalesEdit
from ..OrdersEdit import OrdersEdit


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    anvil.users.login_with_form()
    anvil.server.call('get_secret_data')
    
    self.customer_grid.items = app_tables.customers.search()
    #self.sales_grid.items = app_tables.sales.search()
    self.customer_grid.add_event_handler('x-go-to-sales', self.go_to_sales_click)
    
    self.customer_grid.add_event_handler('x-edit-customer', self.edit_customer)
    self.customer_grid.add_event_handler('x-delete-customer', self.delete_customer)

    # self.sales_grid.add_event_handler('x-edit-sale', self.edit_sale)
    # self.sales_grid.add_event_handler('x-delete-sale', self.delete_sale)

    # self.orders_grid.add_event_handler('x-edit-order', self.edit_order)

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
  def go_to_sales_click(self, **event_args):
    open_form('SalesForm')  # Navigate to the SalesForm

  def go_to_orders_click(self, **event_args):
    open_form('OrdersForm')

########## Sales Details : date, type, products, order value, discount, commission, notes

  def go_to_commission_click(self, **event_args):
    open_form('CommissionForm')

  def logout_click(self, **event_args):
    current_user = anvil.users.get_user()
    if current_user is not None:
      anvil.users.logout()
      anvil.users.login_with_form()
      




    
    


    
    



 
