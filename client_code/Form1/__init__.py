from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .CustomerEdit import CustomerEdit


class Form1(Form1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.customer_grid.items = app_tables.customers.search()
  def add_customer_info_click(self, **event_args):
    item = {}
    editing_form = CustomerEdit(item=item)
    if alert(content=editing_form, large=True):
    #add the movie to the Data Table with the filled in information
      print("Item data:", item)
      print("hello world")
      anvil.server.call('add_customer', item)
    #refresh the Data Grid
      self.customer_grid.items = app_tables.customers.search()

  def button_1_click(self, **event_args):
    item = {}
    editing_form = CustomerEdit(item=item)
    if alert(content=editing_form, large=True):
    #add the movie to the Data Table with the filled in information
      anvil.server.call('add_customer', item)
    #refresh the Data Grid
      self.customer_grid.items = app_tables.customers.search()



 
