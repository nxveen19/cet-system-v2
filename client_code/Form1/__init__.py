from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CustomerEdit import CustomerEdit
from ..SalesEdit import SalesEdit


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
    if alert(content=editing_form, large=True): # matlab kab OK button jabaunga
    #add the movie to the Data Table with the filled in information
      print("Item data:", item)
      # print("hello world")
      anvil.server.call('add_sales', item) # item is dict{}
      # self.refresh_sales_grid()
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
      # self.refresh_sales_grid()
    #refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()
  def delete_sale(self, sale, **event_args):
    if confirm(f"Do you really want to delete the customer row {sale['type']}?"):
      anvil.server.call('delete_sale', sale)
      self.refresh_sales_grid()
      print(sale)
    #refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()

  # def calculate_commission_click(self, sale, **event_args):
  #   item = dict(sale)
  def get_sales_with_commission(self):
    # Calculate and include commission for each sale
    sales_with_commission = []
    for sale in app_tables.sales.search():
      item = dict(sale)
      print(f'item is {item}')
      print(f"sale is {sale}")
      commission_percentage = item['commission']
          
      if commission_percentage > 0:
          commission = (item['order_value'] - item['discount']) / commission_percentage
          print(commission)
      else:
          commission = 0
      sale.update(calculated_commission=commission)
      sales_with_commission.append({
        **item,
        'calculated_commission': commission})

    # Return the list of sales with commission included
      print(sales_with_commission)
      return sales_with_commission

  def refresh_sales_grid(self):
    self.sales_grid.items = self.get_sales_with_commission()
    
    



 
