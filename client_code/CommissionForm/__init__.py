from ._anvil_designer import CommissionFormTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CommissionEdit import CommissionEdit

class CommissionForm(CommissionFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.commission_grid.add_event_handler('x-edit-commission', self.edit_commission)
    self.commission_grid.items = anvil.server.call('get_commission_for_user')
    # Any code you write here will run before the form opens.
  def edit_commission(self, commission_row, **event_args):
    item = dict(commission_row)
    editing_form = CommissionEdit(item=item)
    if alert(content=editing_form, large=True):
      print("Item Data:", item)
      anvil.server.call("add_commission_details", commission_row, item)
      self.commission_grid.items = anvil.server.call('get_commission_for_user')
      # self.calculate_outstanding_balance(order)

  def go_to_home_click(self, **event_args):
    open_form('Form1')

  def go_to_sales_click(self, **event_args):
    open_form('SalesForm')

  def go_to_orders_click(self, **event_args):
    open_form('OrdersForm')
  
