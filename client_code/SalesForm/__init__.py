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
    
    self.sales_grid.items = app_tables.sales.search()
    #self.refresh_sales_grid()
    #self.orders_grid.add_event_handler("x-edit-order", self.edit_order)

  ########## Sales Details : date, type, products, order value, discount, commission, notes

  def add_sales_details_click(self, **event_args):
    item = {}
    editing_form = SalesEdit(item=item)
    if alert(content=editing_form, large=True):  # matlab jab OK button jabaunga
      # add the movie to the Data Table with the filled in information
      if isinstance(item.get('order_value'), str):
        item['order_value'] = float(item['order_value'].replace('£', '').strip())
      print("Item data:", item)
      new_sale = anvil.server.call(
        "add_sales", item
      )  # item is dict{} and new_sale is row in db
      self.calculate_and_update_commission(new_sale)
      # refresh the Data Grid
      self.refresh_sales_grid()
    customer_ref_number = item['customer_ref_number'].strip('-')
    if len(customer_ref_number) > 12:
      alert("Customer Reference Number must be 12 characters or fewer.")

  def edit_sale(self, sale, **event_args):
    # movie is the row from the Data Table
    item = dict(sale)
    editing_form = SalesEdit(item=item)  # item is name,place, email, phone, add

    # if the user clicks OK on the alert
    if alert(content=editing_form, large=True):
      # pass in the Data Table row and the updated info
      if isinstance(item.get('order_value'), str):
            item['order_value'] = float(item['order_value'].replace('£', '').strip())
      anvil.server.call("update_sale", sale, item)
      existing_row = app_tables.orders.get(order_id=sale['order_id'])
      
      if existing_row:
        existing_row.update(customer_ref_number=sale['customer_ref_number'])
      self.calculate_and_update_commission(sale)
      existing_row_commission = app_tables.commission.get(order_id=sale['order_id'])
      if existing_row_commission:
        existing_row_commission.update(customer_ref_number=sale['customer_ref_number'])
      self.refresh_sales_grid()
      # refresh the Data Grid
    customer_ref_number = item['customer_ref_number'].strip('-')
    if len(customer_ref_number) > 12:
      alert("Customer Reference Number must be 12 characters or fewer.")
      


  def delete_sale(self, sale, **event_args):
    if confirm(f"Do you really want to delete the customer row {sale['type']}?"):
      anvil.server.call("delete_sale", sale)
      print(sale)
      # refresh the Data Grid
      self.sales_grid.items = app_tables.sales.search()

  def calculate_and_update_commission(self, sale):
    # Calculate commission for the given sale row
    item = dict(sale)
    customer_ref_number = item['customer_ref_number']
    commission_percentage = item["commission"]
    if isinstance(item.get('order_value'), str):
      item['order_value'] = float(item['order_value'].replace('£', '').strip())

    if commission_percentage > 0:
      commission = item["order_value"] * (commission_percentage / 100)
      print(f"Calculated commission: {commission}")
    else:
      commission = 0

    # Update only the 'calculated_commission' for this specific sale
    sale.update(calculated_commission=commission)
    existing_row = app_tables.commission.get(order_id=sale['order_id'])
    if existing_row:
      print(f"Item in cal_commision is : {item}")
      existing_row.update(due_commission=commission, customer_ref_number=customer_ref_number)
    else:
      commission_data = {
          'order_id': sale['order_id'],
          'status': 'Not Paid',
          'customer_ref_number': customer_ref_number,
          'due_commission': commission,
          'commission_received': 0,
          'commission_pending': 0
        }
      app_tables.commission.add_row(**commission_data)
      self.refresh_sales_grid()
    #Optionally update the grid to reflect the new commission
      # Refresh the grid to show updated commission

  def refresh_sales_grid(self):
    sales_data = app_tables.sales.search()
    # Prepare a list to hold the formatted data
    formatted_sales_data = []

    for item in sales_data:
        # Check if necessary fields exist and format them if required
        formatted_item = dict(item)
        
        # Handle 'None' values early before adding to the formatted data
        formatted_item['order_value'] = f"£{formatted_item['order_value'] if formatted_item['order_value'] is not None else 0.00}"
        #formatted_item['commission'] = f"£{formatted_item['commission'] if formatted_item['commission'] is not None else 0.00:.2f}"
        formatted_item['calculated_commission'] = f"£{formatted_item['calculated_commission'] if formatted_item['calculated_commission'] is not None else 0.00:.2f}"

        # Add the formatted item to the list
        formatted_sales_data.append(formatted_item)

    # Now update the grid with the fully prepared data
    self.sales_grid.items = formatted_sales_data

  #############Order Processing status table#############

  def go_to_home_click(self, **event_args):
    open_form('Form1')

  def go_to_orders_click(self, **event_args):
    open_form('OrdersForm')

  def go_to_commission_click(self, **event_args):
    open_form('CommissionForm')
