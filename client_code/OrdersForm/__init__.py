from ._anvil_designer import OrdersFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CustomerEdit import CustomerEdit
from ..SalesEdit import SalesEdit
from ..OrdersEdit import OrdersEdit


class OrdersForm(OrdersFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.orders_grid.items = app_tables.orders.search()
    self.orders_grid.add_event_handler("x-edit-order", self.edit_order)
    self.refresh_orders_grid()
  ########## Sales Details : date, type, products, order value, discount, commission, notes

  #############Order Processing status table#############

  def edit_order(self, order, **event_args):
    item = dict(order)
    editing_form = OrdersEdit(item=item)
    if alert(content=editing_form, large=True):
      print("Item Data:", item)
      anvil.server.call("add_order_details", order, item)
      self.calculate_outstanding_balance(order)
      self.refresh_orders_grid()

  def calculate_outstanding_balance(self, order):
    item = dict(order)
    deposit_amount = item["deposit_amount"]
    if deposit_amount > 0:
      outstanding_balance = item["order_value"] - (
        item["deposit_amount"] + item["final_amount"]
      )
      print(f"Calculated outsatanding balance: {outstanding_balance}")
    else:
      outstanding_balance = 0
      # Update only the 'calculated_commission' for this specific sale
    order.update(outstanding_balance=outstanding_balance)
    self.orders_grid.items = app_tables.orders.search()
    # self.refresh_sales_grid()  # Refresh the grid to show updated commission

  def refresh_orders_grid(self):
    self.orders_grid.items = app_tables.orders.search()
    

  def back_to_customer_click(self, **event_args):
    open_form('Form1')  # Navigate to the SalesForm

  def go_to_sales_click(self, **event_args):
    open_form('SalesForm')

  def go_to_commission_click(self, **event_args):
    open_form('CommissionForm')