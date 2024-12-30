from ._anvil_designer import OrdersEditTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class OrdersEdit(OrdersEditTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.deposit_amount.type = 'number'
    self.final_amount.type = 'number'
    self.status.items = ['Order Placed', 'Deposit Received', 'Installed']
    self.installation_status.items = ['Pending', 'Processing', 'Installed']
    self.status.change = self.update_status
    self.installation_status.change = self.update_status

  def update_status(self, **event_args):
    # Get the selected value from the dropdown
    new_status = self.status.selected_value
    new_installation_status = self.installation_status.selected_value
    # Update the database row
    if self.item:
      row = app_tables.orders.get(order_id=self.item['order_id'])
      if row:
        row.update(status=new_status, installation_status=new_installation_status)
        print(f"Order ID {self.item['order_id']} status updated to {new_status}")

