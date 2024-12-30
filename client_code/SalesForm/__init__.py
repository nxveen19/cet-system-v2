from ._anvil_designer import SalesFormTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CustomerEdit import CustomerEdit
from ..SalesEdit import SalesEdit
from ..OrdersEdit import OrdersEdit


class SalesForm(SalesFormTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.sales_grid.add_event_handler("x-edit-sale", self.edit_sale)
    self.sales_grid.add_event_handler("x-delete-sale", self.delete_sale)
    self.refresh_sales_grid()

    #self.orders_grid.add_event_handler("x-edit-order", self.edit_order)

  ########## Sales Details : date, type, products, order value, discount, commission, notes

  def add_sales_details_click(self, **event_args):
    item = {}
    editing_form = SalesEdit(item=item)
    if alert(content=editing_form, large=True):  # matlab jab OK button jabaunga
      # add the movie to the Data Table with the filled in information
      print("Item data:", item)
      # print("hello world")
      new_sale = anvil.server.call(
        "add_sales", item
      )  # item is dict{} and new_sale is row in db
      self.calculate_and_update_commission(new_sale)
      # refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()

  def edit_sale(self, sale, **event_args):
    # movie is the row from the Data Table
    item = dict(sale)
    editing_form = SalesEdit(item=item)  # item is name,place, email, phone, add

    # if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      # pass in the Data Table row and the updated info
      anvil.server.call("update_sale", sale, item)

      # refresh the Data Grid
      self.calculate_and_update_commission(sale)
      self.sales_grid.items = app_tables.sales.search()

  def delete_sale(self, sale, **event_args):
    if confirm(f"Do you really want to delete the customer row {sale['type']}?"):
      anvil.server.call("delete_sale", sale)
      self.refresh_sales_grid()
      print(sale)
      # refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()

  def calculate_and_update_commission(self, sale):
    # Calculate commission for the given sale row
    item = dict(sale)
    commission_percentage = item["commission"]

    if commission_percentage > 0:
      commission = round(
        (item["order_value"]) * (commission_percentage / 100)
      )
      print(f"Calculated commission: {commission}")
    else:
      commission = 0

    # Update only the 'calculated_commission' for this specific sale
    sale.update(calculated_commission=commission)
    existing_row = app_tables.commission.get(order_id=sale['order_id'])
    if existing_row:
      existing_row.update(due_commission=commission)
    else:
      commission_data = {
          'order_id': sale['order_id'],
          'status': 'Not Paid',
          'due_commission': commission,
          'commission_received': 0,
          'commission_pending': 0
        }
      app_tables.commission.add_row(**commission_data)
    #Optionally update the grid to reflect the new commission
    self.refresh_sales_grid()  # Refresh the grid to show updated commission

  def refresh_sales_grid(self):
    # Refresh only the grid's items based on the updated sales data
    self.sales_grid.items = app_tables.sales.search()
    #self.orders_grid.items = app_tables.orders.search()

  #############Order Processing status table#############

  def go_to_home_click(self, **event_args):
    open_form('Form1')

  def go_to_orders_click(self, **event_args):
    open_form('OrdersForm')
