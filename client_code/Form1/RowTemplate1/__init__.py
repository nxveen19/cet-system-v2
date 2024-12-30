from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import uuid


class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
# customer ko db se nahi data grid me elements se access kr rhe hai by = customer
  def edit_row_click(self, **event_args):
    self.parent.raise_event('x-edit-customer', customer=self.item)

  def delete_row_click(self, **event_args):
    self.parent.raise_event('x-delete-customer', customer=self.item)

  def add_customer_sale_click(self, **event_args):
    # Extract the customer details from the current row
    customer = self.item
    customer_id = customer['customer_ref_id']
    customer_name = customer['name']
    order_id = str(uuid.uuid4())

    # Create a new sale row associated with this customer
    sales_data = {
        'order_id': order_id,  # Unique order ID
        'customer_ref_id': customer_id,
        'customer_ref': customer_name,
        'date': datetime.now().date(),
        'type': 'None',
        'products_sold': 'None',
        'order_value': 0,
        'discount': 0,
        'commission': 0,
        'calculated_commission': 0,
        'notes': 'None'
    }
    order_data = {
            'order_id': sales_data['order_id'],
            'customer_ref': customer_name,
            'customer_ref_id': customer_id,
            'order_value': sales_data['order_value'],
            'status': '',  # Default status for new orders
            'deposit_amount': 0,  # Default deposit amount
            'installation_status': 'Pending',  # Default installation status
            'final_amount': 0,  # Default final amount received
            'outstanding_balance': 0
        }

    app_tables.sales.add_row(**sales_data)
    app_tables.orders.add_row(**order_data)
    self.parent.raise_event('x-go-to-sales')
    
    # Refresh the sales grid (if applicable)
